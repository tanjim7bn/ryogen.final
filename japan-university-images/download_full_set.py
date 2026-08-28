#!/usr/bin/env python3
"""
Downloads logos and campus photos for Japanese universities with English-taught
programs, names every file after its alt text, and zips the result into two
folders: "Japan University Logos" and "Japan University Pictures".

Sources: English Wikipedia (logos, from each university's article infobox) and
Wikimedia Commons (photos, from each university's Commons category — campus,
buildings, dorms, classrooms, libraries, gates, festivals).

USAGE
    pip install requests
    python3 download_full_set.py

    # useful options
    python3 download_full_set.py --photos 5          # photos per university
    python3 download_full_set.py --only waseda       # just matching universities
    python3 download_full_set.py --logos-only
    python3 download_full_set.py --pace 0.5          # faster (be polite)

It is resumable: files already on disk are skipped, so you can stop it with
Ctrl-C and run it again. When it finishes it writes:

    Japan University Logos/<university> logo.png
    Japan University Pictures/<university> <subject> N.jpg
    alt-texts.csv       every image with its alt text and source URL
    preview.html        open in a browser to eyeball every image + alt text
    Japan University Images.zip

LICENSING: Commons photos are free-licensed but nearly always require
attribution — alt-texts.csv carries each file's description-page URL, which
names the author and licence. University logos are trademarks: fine for
identifying a university in a listing, not for implying endorsement.
"""

import argparse
import csv
import html
import os
import re
import sys
import time
import zipfile

try:
    import requests
except ImportError:
    sys.exit("Please run:  pip install requests")

EN = "https://en.wikipedia.org/w/api.php"
CO = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "JapanUniversityImageFetcher/2.0 (personal study-abroad site asset collection)"}

LOGO_DIR = "Japan University Logos"
PIC_DIR = "Japan University Pictures"
ZIP_NAME = "Japan University Images.zip"

EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
       "image/svg+xml": ".svg", "image/webp": ".webp"}

# (alt-text name, English Wikipedia article, Commons category or None to guess)
UNIVERSITIES = [
    ("tokyo international university", "Tokyo International University", None),
    ("ritsumeikan asia pacific university", "Ritsumeikan Asia Pacific University", None),
    ("kyoto university of advanced science", "Kyoto University of Advanced Science", None),
    ("waseda university", "Waseda University", "Waseda University"),
    ("sophia university", "Sophia University (Japan)", "Sophia University"),
    ("temple university japan campus", "Temple University, Japan Campus", None),
    ("keio university", "Keio University", "Keio University"),
    ("university of tokyo", "University of Tokyo", "University of Tokyo"),
    ("kyoto university", "Kyoto University", "Kyoto University"),
    ("osaka university", "Osaka University", "Osaka University"),
    ("tohoku university", "Tohoku University", "Tohoku University"),
    ("nagoya university", "Nagoya University", "Nagoya University"),
    ("kyushu university", "Kyushu University", "Kyushu University"),
    ("hokkaido university", "Hokkaido University", "Hokkaido University"),
    ("university of tsukuba", "University of Tsukuba", "University of Tsukuba"),
    ("hiroshima university", "Hiroshima University", "Hiroshima University"),
    ("kobe university", "Kobe University", "Kobe University"),
    ("chiba university", "Chiba University", "Chiba University"),
    ("okayama university", "Okayama University", "Okayama University"),
    ("kanazawa university", "Kanazawa University", "Kanazawa University"),
    ("yokohama national university", "Yokohama National University", None),
    ("international christian university", "International Christian University", None),
    ("meiji university", "Meiji University", "Meiji University"),
    ("rikkyo university", "Rikkyo University", "Rikkyo University"),
    ("hosei university", "Hosei University", "Hosei University"),
    ("chuo university", "Chuo University", "Chuo University"),
    ("aoyama gakuin university", "Aoyama Gakuin University", None),
    ("doshisha university", "Doshisha University", "Doshisha University"),
    ("ritsumeikan university", "Ritsumeikan University", "Ritsumeikan University"),
    ("kwansei gakuin university", "Kwansei Gakuin University", None),
    ("kansai university", "Kansai University", "Kansai University"),
    ("akita international university", "Akita International University", None),
    ("soka university", "Soka University", "Soka University"),
    ("toyo university", "Toyo University", "Toyo University"),
    ("tokyo university of science", "Tokyo University of Science", None),
    ("institute of science tokyo", "Institute of Science Tokyo", "Tokyo Institute of Technology"),
    ("nagoya university of commerce and business", "Nagoya University of Commerce & Business", None),
    ("international university of japan", "International University of Japan", None),
    ("tokai university", "Tokai University", "Tokai University"),
    ("gakushuin university", "Gakushuin University", "Gakushuin University"),
    ("ryukoku university", "Ryukoku University", "Ryukoku University"),
    ("kindai university", "Kindai University", "Kindai University"),
]

# Words that mean "this file is a logo/emblem", used to find logos and to keep
# them out of the photo folder.
LOGO_WORDS = re.compile(r"logo|emblem|crest|seal|wordmark|symbol mark|\bmon\b", re.I)

# Wikipedia/Commons furniture and non-photo files we never want.
JUNK = re.compile(
    r"commons-logo|wiki\w*\.(png|svg)|icon|flag of|\bmap\b|location map|arrow|"
    r"question|edit-|padlock|pog\.svg|ambox|crystal|nuvola|folder|open access|"
    r"clock|increase|decrease|steady|symbol (support|oppose)|disambig|barnstar|"
    r"blue check|red x|speaker|coat of arms|diagram|chart|graph|logo of|"
    r"signature|portrait of|\.pdf|\.ogg|\.oga|\.webm|\.ogv", re.I)

# Photo subject → alt-text word. First match wins, so order matters.
SUBJECTS = [
    (re.compile(r"dorm|residence hall|student housing|ryo\b", re.I), "dormitory"),
    (re.compile(r"classroom|lecture (room|hall|theat)|seminar room", re.I), "classroom"),
    (re.compile(r"librar", re.I), "library"),
    (re.compile(r"festival|matsuri|ceremony|graduation|commencement|"
                r"open campus|sports day|event", re.I), "event"),
    (re.compile(r"\bgate\b|entrance|akamon", re.I), "campus gate"),
    (re.compile(r"auditorium|memorial hall|assembly hall|\bhall\b", re.I), "auditorium"),
    (re.compile(r"cafeteria|dining|canteen|food", re.I), "cafeteria"),
    (re.compile(r"gym|stadium|sports|field|pool|court", re.I), "sports facility"),
    (re.compile(r"laborator|\blab\b|research (center|centre|institute)", re.I), "laboratory"),
    (re.compile(r"museum|gallery|archive", re.I), "museum"),
    (re.compile(r"building|hall|tower|faculty of|school of|department of|"
                r"institute|center|centre|annex", re.I), "building"),
    (re.compile(r"campus|aerial|panorama|ground|garden|quad", re.I), "campus"),
]


# When a university has more photos than we need, take these subjects first.
PRIORITY = ["campus", "dormitory", "classroom", "event", "building", "library",
            "campus gate", "auditorium", "cafeteria", "sports facility",
            "laboratory", "museum"]


def subject_of(title):
    for pattern, word in SUBJECTS:
        if pattern.search(title):
            return word
    return "campus"


class Api:
    """Polite MediaWiki client: paces requests and waits out 429s."""

    def __init__(self, pace):
        self.pace = pace
        self.last = 0.0
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get(self, url, params=None, timeout=90, attempts=6):
        for attempt in range(attempts):
            gap = self.pace - (time.time() - self.last)
            if gap > 0:
                time.sleep(gap)
            try:
                r = self.session.get(url, params=params, timeout=timeout)
            except requests.RequestException as e:
                print(f"    network error ({e.__class__.__name__}), retrying")
                time.sleep(5 * (attempt + 1))
                continue
            finally:
                self.last = time.time()
            if r.status_code == 429:
                wait = int(r.headers.get("retry-after") or 0) or 30 * (attempt + 1)
                print(f"    rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            if r.status_code >= 500:
                time.sleep(5 * (attempt + 1))
                continue
            r.raise_for_status()
            return r
        raise RuntimeError(f"gave up after {attempts} attempts: {url}")

    def query(self, site, **params):
        params.update(format="json", formatversion=2)
        return self.get(site, params=params).json()

    def file_info(self, site, titles, thumb_width=None):
        """{title: imageinfo dict} for a list of File: titles."""
        out = {}
        titles = [t for t in titles if t]
        for i in range(0, len(titles), 50):
            params = dict(action="query", titles="|".join(titles[i:i + 50]),
                          prop="imageinfo", iiprop="url|size|mime|sha1|extmetadata")
            if thumb_width:
                params["iiurlwidth"] = thumb_width
            data = self.query(site, **params)
            for page in data.get("query", {}).get("pages", []):
                info = page.get("imageinfo")
                if info:
                    out[page["title"]] = info[0]
        return out

    def download(self, url, path):
        r = self.get(url, timeout=180)
        if not r.content or r.content[:1] == b"{":
            raise RuntimeError("empty or non-image response")
        with open(path + ".part", "wb") as f:
            f.write(r.content)
        os.replace(path + ".part", path)
        return len(r.content)


def existing(directory, prefix):
    return [f for f in os.listdir(directory) if f.lower().startswith(prefix.lower())]


def fetch_logo(api, alt_name, article, rows):
    if existing(LOGO_DIR, alt_name + " logo"):
        print("    logo: already downloaded")
        return True

    data = api.query(EN, action="query", titles=article, prop="images",
                     imlimit=200, redirects=1)
    pages = data.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing"):
        print(f"    !! no Wikipedia article named {article!r}")
        return False
    images = [i["title"] for i in pages[0].get("images", [])]
    candidates = [t for t in images if LOGO_WORDS.search(t) and not JUNK.search(t)][:25]
    if not candidates:
        print("    !! no logo file found in the article")
        return False

    # Logos live either on Wikipedia (non-free uploads) or on Commons.
    info = api.file_info(EN, candidates, thumb_width=1000)
    missing = [t for t in candidates if t not in info]
    if missing:
        info.update(api.file_info(CO, missing, thumb_width=1000))
    if not info:
        print("    !! logo files unreadable")
        return False

    def rank(item):
        title, ii = item
        svg = "svg" in ii.get("mime", "")
        # a file whose name is exactly "<university> logo" beats a generic one
        named = bool(re.search(r"logo|emblem", title, re.I))
        return (svg, named, ii.get("width", 0))

    title, ii = max(info.items(), key=rank)
    # For SVG, Wikimedia renders a clean PNG at the requested width; if that
    # rendering is unavailable, fall back to the SVG itself.
    svg = "svg" in ii.get("mime", "") and ii.get("thumburl")
    url = ii["thumburl"] if svg else ii["url"]
    ext = ".png" if svg else EXT.get(ii.get("mime"), ".png")
    filename = f"{alt_name} logo{ext}"
    api.download(url, os.path.join(LOGO_DIR, filename))
    rows.append([LOGO_DIR, filename, f"{alt_name} logo", alt_name, ii["descriptionurl"]])
    print(f"    logo: {filename}")
    return True


def commons_candidates(api, article, category, want):
    """File titles from the university's Commons category (plus subcategories),
    falling back to a Commons text search."""
    titles, seen_cats = [], set()
    queue = [f"Category:{category or article}"]
    if category is None and "(" in article:
        queue.append("Category:" + article.split("(")[0].strip())

    while queue and len(titles) < want * 8:
        cat = queue.pop(0)
        if cat in seen_cats:
            continue
        seen_cats.add(cat)
        try:
            data = api.query(CO, action="query", list="categorymembers",
                             cmtitle=cat, cmtype="file|subcat", cmlimit=200)
        except Exception:
            continue
        for m in data.get("query", {}).get("categorymembers", []):
            if m["title"].startswith("Category:"):
                if len(seen_cats) < 8:
                    queue.append(m["title"])
            else:
                titles.append(m["title"])

    if len(titles) < want:
        data = api.query(CO, action="query", generator="search",
                         gsrsearch=f'"{article}"', gsrnamespace=6, gsrlimit=50)
        titles += [p["title"] for p in data.get("query", {}).get("pages", [])]
    return list(dict.fromkeys(titles))


def fetch_photos(api, alt_name, article, category, want, rows, min_width):
    have = len(existing(PIC_DIR, alt_name + " "))
    if have >= want:
        print(f"    photos: already have {have}")
        return have

    titles = commons_candidates(api, article, category, want)
    titles = [t for t in titles if not JUNK.search(t) and not LOGO_WORDS.search(t)]
    if not titles:
        print("    !! no Commons photos found")
        return have

    info = api.file_info(CO, titles[:120])
    usable = []
    for title, ii in info.items():
        w, h = ii.get("width", 0), ii.get("height", 0)
        if ii.get("mime") not in ("image/jpeg", "image/png"):
            continue
        if w < min_width or h < 500:
            continue
        if not 0.5 <= w / h <= 2.6:          # drop banners and thin panoramas
            continue
        usable.append((title, ii))

    # Prefer subject variety first, then resolution.
    usable.sort(key=lambda x: -x[1].get("width", 0))
    by_subject, ordered = {}, []
    for title, ii in usable:
        by_subject.setdefault(subject_of(title), []).append((title, ii))
    order = sorted(by_subject, key=lambda s: PRIORITY.index(s) if s in PRIORITY else 99)
    while len(ordered) < len(usable):
        added = False
        for subject in order:
            if by_subject[subject]:
                ordered.append(by_subject[subject].pop(0))
                added = True
        if not added:
            break

    seen_hashes = set()
    count = have
    for title, ii in ordered:
        if count >= want:
            break
        if ii.get("sha1") in seen_hashes:
            continue
        seen_hashes.add(ii.get("sha1"))
        subject = subject_of(title)
        alt = f"{alt_name} {subject}"
        filename = f"{alt} {count + 1}{EXT.get(ii['mime'], '.jpg')}"
        try:
            api.download(ii["url"], os.path.join(PIC_DIR, filename))
        except Exception as e:
            print(f"    photo failed ({e}), trying next")
            continue
        rows.append([PIC_DIR, filename, alt, alt_name, ii["descriptionurl"]])
        print(f"    photo: {filename}  ({ii['width']}x{ii['height']})")
        count += 1

    if count == have:
        print("    !! no photo met the quality bar")
    return count


def write_outputs(rows):
    rows.sort(key=lambda r: (r[0], r[1]))
    with open("alt-texts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "filename", "alt_text", "university", "source_url"])
        w.writerows(rows)

    cards = []
    for category, filename, alt, uni, src in rows:
        path = html.escape(f"{category}/{filename}")
        cards.append(
            f'<figure><img src="{path}" alt="{html.escape(alt)}" loading="lazy">'
            f'<figcaption><b>{html.escape(alt)}</b><br>'
            f'<code>{html.escape(filename)}</code><br>'
            f'<a href="{html.escape(src)}">source</a></figcaption></figure>')
    with open("preview.html", "w", encoding="utf-8") as f:
        f.write(
            "<!doctype html><meta charset='utf-8'><title>Japan University Images</title>"
            "<style>body{font-family:system-ui,sans-serif;margin:24px;background:#fafafa}"
            "h1{font-size:20px}div.grid{display:grid;gap:18px;"
            "grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}"
            "figure{margin:0;background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px}"
            "img{width:100%;height:170px;object-fit:contain;background:#fff}"
            "figcaption{font-size:12px;line-height:1.45;margin-top:8px;word-break:break-word}"
            "code{color:#666}</style>"
            f"<h1>Japan University Images &mdash; {len(rows)} files</h1>"
            "<p>Check that every picture matches the alt text under it.</p>"
            "<div class='grid'>" + "".join(cards) + "</div>")

    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as z:
        for directory in (LOGO_DIR, PIC_DIR):
            for filename in sorted(os.listdir(directory)):
                if not filename.startswith("."):
                    z.write(os.path.join(directory, filename))
        z.write("alt-texts.csv")
        z.write("preview.html")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--photos", type=int, default=4, help="photos per university (default 4)")
    ap.add_argument("--min-width", type=int, default=1000, help="minimum photo width in px")
    ap.add_argument("--only", default="", help="only universities whose name contains this")
    ap.add_argument("--logos-only", action="store_true")
    ap.add_argument("--pace", type=float, default=1.0, help="seconds between requests")
    args = ap.parse_args()

    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    os.makedirs(LOGO_DIR, exist_ok=True)
    os.makedirs(PIC_DIR, exist_ok=True)

    rows = []
    if os.path.exists("alt-texts.csv"):
        with open("alt-texts.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            rows = [r for r in reader if len(r) == 5
                    and os.path.exists(os.path.join(r[0], r[1]))]

    api = Api(args.pace)
    todo = [u for u in UNIVERSITIES if args.only.lower() in u[0]]
    logos = photos = 0

    for i, (alt_name, article, category) in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {article}")
        try:
            if fetch_logo(api, alt_name, article, rows):
                logos += 1
            if not args.logos_only:
                photos += fetch_photos(api, alt_name, article, category,
                                       args.photos, rows, args.min_width)
        except KeyboardInterrupt:
            print("\nstopped — rerun to resume")
            break
        except Exception as e:
            print(f"    !! {article}: {e}")

    write_outputs(rows)
    print(f"\n{len(os.listdir(LOGO_DIR))} logos, {len(os.listdir(PIC_DIR))} photos")
    print(f"Wrote {ZIP_NAME}, alt-texts.csv and preview.html")
    print("Open preview.html in a browser to check the alt text against each image.")


if __name__ == "__main__":
    main()
