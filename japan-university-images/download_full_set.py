#!/usr/bin/env python3
"""
Downloads logos and campus photos for the 34 Japanese universities that offer
BACHELOR'S degrees taught in English, names every file after its alt text, and
zips the result into two folders: "Japan University Logos" and "Japan
University Pictures".

Every university in the list is there because it runs an English-medium
undergraduate programme (Waseda SILS, UTokyo PEAK, Sophia FLA, Keio PEARL,
TIU E-Track, APU APS/APM, Akita International, and so on). The programme is
recorded next to every image in alt-texts.csv.

Sources: English Wikipedia (logos, from each university's article infobox) and
Wikimedia Commons (photos, from each university's Commons category — campus,
buildings, dorms, classrooms, libraries, gates, festivals).

USAGE
    pip install requests
    python3 download_full_set.py

    # useful options
    python3 download_full_set.py --photos 20         # photos per university
    python3 download_full_set.py --only waseda       # just matching universities
    python3 download_full_set.py --logos-only
    python3 download_full_set.py --width 2400        # bigger images
    python3 download_full_set.py --pace 3            # gentler on Wikimedia

RATE LIMITING: Wikimedia throttles bulk downloads and answers 429 with
Retry-After of up to 600 seconds. This script avoids provoking that by
downloading 1600px thumbnails rather than 6000px originals (a tenth of the
bytes, and the right size for a website), by slowing itself down after every
429, and by skipping a file instead of sitting out a ten-minute block. Rerun
the script to fill in anything it skipped. Set CONTACT below to your email:
Wikimedia throttles unidentified clients harder.

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
# Wikimedia asks bots to identify themselves with a contact address, and
# throttles generic agents harder. Put your own email here.
CONTACT = "your-email@example.com"
HEADERS = {"User-Agent": f"JapanUniversityImageFetcher/3.0 ({CONTACT}) requests"}

LOGO_DIR = "Japan University Logos"
PIC_DIR = "Japan University Pictures"
ZIP_NAME = "Japan University Images.zip"

EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif",
       "image/svg+xml": ".svg", "image/webp": ".webp"}

# Every university here offers at least one BACHELOR'S degree that can be
# completed in English. The fourth field names that programme and is written
# into alt-texts.csv, so the pack documents why each university is included.
# (alt-text name, English Wikipedia article, Commons category or None, programme)
UNIVERSITIES = [
    ("tokyo international university", "Tokyo International University", None,
     "E-Track: BA Business Economics, International Relations, Digital Business & Innovation"),
    ("ritsumeikan asia pacific university", "Ritsumeikan Asia Pacific University",
     "Ritsumeikan Asia Pacific University",
     "College of Asia Pacific Studies (APS) and College of International Management (APM)"),
    ("kyoto university of advanced science", "Kyoto University of Advanced Science", None,
     "Faculty of Engineering, English-taught BEng"),
    ("waseda university", "Waseda University", "Waseda University",
     "School of International Liberal Studies (SILS), EDESSA, English-based Science & Engineering"),
    ("sophia university", "Sophia University (Japan)", "Sophia University",
     "Faculty of Liberal Arts (FLA), Green Science and Green Engineering"),
    ("temple university japan campus", "Temple University, Japan Campus", None,
     "Full US bachelor's degrees taught entirely in English"),
    ("keio university", "Keio University", "Keio University",
     "PEARL (Economics) and GIGA (Environment and Information Studies)"),
    ("university of tokyo", "University of Tokyo", "University of Tokyo",
     "PEAK - Programs in English at Komaba; Global Science Course"),
    ("kyoto university", "Kyoto University", "Kyoto University",
     "Kyoto iUP; Faculty of Engineering international course"),
    ("osaka university", "Osaka University", "Osaka University",
     "International College: Human Sciences (HUS) and International Undergraduate Program in Science"),
    ("tohoku university", "Tohoku University", "Tohoku University",
     "Future Global Leadership: Applied Marine Biology, IMAC-U, Advanced Molecular Chemistry"),
    ("nagoya university", "Nagoya University", "Nagoya University",
     "G30 International Programs: Automotive Engineering, Chemistry, Physics, Biology, Social Sciences"),
    ("kyushu university", "Kyushu University", "Kyushu University",
     "International Undergraduate Programs: Engineering, Bioresource and Bioenvironment"),
    ("hokkaido university", "Hokkaido University", "Hokkaido University",
     "Integrated Science Program (ISP) and Modern Japanese Studies (MJSP)"),
    ("university of tsukuba", "University of Tsukuba", "University of Tsukuba",
     "Bachelor's Program in Global Issues (BPGI); Interdisciplinary Engineering"),
    ("hiroshima university", "Hiroshima University", "Hiroshima University",
     "School of Integrated Global Studies (IGS)"),
    ("okayama university", "Okayama University", "Okayama University",
     "Discovery Program for Global Learners"),
    ("akita international university", "Akita International University", None,
     "All undergraduate courses in English: Global Business, Global Studies, Global Connectivity"),
    ("international christian university", "International Christian University",
     "International Christian University",
     "Bilingual liberal arts college with English-taught majors"),
    ("meiji university", "Meiji University", "Meiji University",
     "School of Global Japanese Studies, English track"),
    ("rikkyo university", "Rikkyo University", "Rikkyo University",
     "Global Liberal Arts Program (GLAP)"),
    ("hosei university", "Hosei University", "Hosei University",
     "Global and Interdisciplinary Studies (GIS); Institute of Integrated Sciences"),
    ("chuo university", "Chuo University", "Chuo University",
     "Global Management (GLOMAC) and International Business Law (GLIB)"),
    ("doshisha university", "Doshisha University", "Doshisha University",
     "Institute for the Liberal Arts (ILA)"),
    ("ritsumeikan university", "Ritsumeikan University", "Ritsumeikan University",
     "Global Studies Major, Community and Regional Policy Studies, American University joint degree"),
    ("kwansei gakuin university", "Kwansei Gakuin University", "Kwansei Gakuin University",
     "School of International Studies (SIS), English-based degree"),
    ("soka university", "Soka University", "Soka University",
     "Faculty of International Liberal Arts (FILA)"),
    ("toyo university", "Toyo University", "Toyo University",
     "Faculty of Global and Regional Studies; Global Innovation Studies (GINOS)"),
    ("nagoya university of commerce and business", "Nagoya University of Commerce & Business", None,
     "Global BBA taught in English"),
    ("yamanashi gakuin university", "Yamanashi Gakuin University", None,
     "International College of Liberal Arts (iCLA), fully English-medium"),
    ("miyazaki international college", "Miyazaki International College", None,
     "All undergraduate classes taught in English"),
    ("shibaura institute of technology", "Shibaura Institute of Technology", None,
     "Innovative Global Program (IGP), English-taught BEng"),
    ("university of aizu", "University of Aizu", "University of Aizu",
     "Advanced ICT Global Program (ICTG), all-English computer science course"),
    ("kansai gaidai university", "Kansai Gaidai University", None,
     "College of Global Engagement, English-taught BA"),
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
    (re.compile(r"clock tower|monument|statue|fountain|memorial", re.I), "landmark"),
    (re.compile(r"snow|winter|autumn|spring|cherry blossom|sakura|ginkgo|"
                r"night|evening|illuminat", re.I), "campus in season"),
    (re.compile(r"student|graduat|class of|club|circle|orientation", re.I), "students"),
    (re.compile(r"building|hall|tower|faculty of|school of|department of|"
                r"institute|center|centre|annex", re.I), "building"),
    (re.compile(r"campus|aerial|panorama|ground|garden|quad", re.I), "campus"),
]


# When a university has more photos than we need, take these subjects first.
PRIORITY = ["campus", "dormitory", "classroom", "event", "students", "building",
            "library", "campus gate", "auditorium", "cafeteria",
            "sports facility", "laboratory", "campus in season", "landmark",
            "museum"]


def subject_of(title):
    for pattern, word in SUBJECTS:
        if pattern.search(title):
            return word
    return "campus"


class RateLimited(Exception):
    """Wikimedia asked us to wait longer than --max-wait."""


class Api:
    """Polite MediaWiki client.

    Wikimedia throttles bulk downloading hard: ask for too many bytes too
    quickly and it answers 429 with Retry-After: 600. Rather than sit out
    ten-minute blocks, this client slows itself down permanently after each
    429 (so it stops provoking them), waits at most --max-wait, and then gives
    up on that one file. Because the script is resumable, a later run picks up
    whatever was skipped.
    """

    def __init__(self, pace, max_wait=180):
        self.base_pace = pace
        self.pace = pace
        self.max_wait = max_wait
        self.last = 0.0
        self.throttles = 0
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _slow_down(self):
        """Each 429 makes every later request more patient, up to 15s apart."""
        self.throttles += 1
        self.pace = min(15.0, max(self.pace * 1.5, self.base_pace + 1))

    def get(self, url, params=None, timeout=90, attempts=5):
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
                asked = int(r.headers.get("retry-after") or 0) or 30 * (attempt + 1)
                self._slow_down()
                if asked > self.max_wait:
                    raise RateLimited(
                        f"Wikimedia asked for {asked}s (over --max-wait "
                        f"{self.max_wait}s)")
                print(f"    rate limited, waiting {asked}s "
                      f"(pacing now {self.pace:.1f}s between requests)")
                time.sleep(asked)
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


def fetch_logo(api, alt_name, article, programme, rows):
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
    rows.append([LOGO_DIR, filename, f"{alt_name} logo", alt_name, programme,
                 ii["descriptionurl"]])
    print(f"    logo: {filename}")
    return True


def commons_candidates(api, article, category, want):
    """File titles from the university's Commons category (plus subcategories),
    falling back to a Commons text search."""
    titles, seen_cats = [], set()
    queue = [f"Category:{category or article}"]
    if category is None and "(" in article:
        queue.append("Category:" + article.split("(")[0].strip())

    while queue and len(titles) < want * 12:
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
                if len(seen_cats) < 30:
                    queue.append(m["title"])
            else:
                titles.append(m["title"])

    # Text search backfills universities with a thin or missing category.
    if len(titles) < want * 2:
        for search in (f'"{article}"', article):
            data = api.query(CO, action="query", generator="search",
                             gsrsearch=search, gsrnamespace=6, gsrlimit=100)
            titles += [p["title"] for p in data.get("query", {}).get("pages", [])]
            if len(titles) >= want * 2:
                break
    return list(dict.fromkeys(titles))


def fetch_photos(api, alt_name, article, category, programme, want, rows,
                 min_width, per_subject, width):
    have = len(existing(PIC_DIR, alt_name + " "))
    if have >= want:
        print(f"    photos: already have {have}")
        return have

    titles = commons_candidates(api, article, category, want)
    titles = [t for t in titles if not JUNK.search(t) and not LOGO_WORDS.search(t)]
    if not titles:
        print("    !! no Commons photos found")
        return have

    info = api.file_info(CO, titles[:400],
                         thumb_width=width if width < 10 ** 6 else None)
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
    # Cap each subject so one well-photographed building cannot fill the quota.
    for subject in by_subject:
        by_subject[subject] = by_subject[subject][:per_subject]
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
        # A 1600px thumbnail is a fraction of a 6000px original: kinder to
        # Wikimedia, and the right size for a website anyway.
        url = ii["thumburl"] if ii.get("thumburl") and ii["width"] > width else ii["url"]
        try:
            api.download(url, os.path.join(PIC_DIR, filename))
        except RateLimited as e:
            print(f"    {e}\n    skipping the rest of this university; "
                  f"rerun later to fill the gap")
            break
        except Exception as e:
            print(f"    photo failed ({e}), trying next")
            continue
        rows.append([PIC_DIR, filename, alt, alt_name, programme,
                     ii["descriptionurl"]])
        shown = min(width, ii["width"])
        print(f"    photo: {filename}  ({shown}px wide, "
              f"source {ii['width']}x{ii['height']})")
        count += 1

    if count == have:
        print("    !! no photo met the quality bar")
    return count


def write_outputs(rows):
    rows.sort(key=lambda r: (r[0], r[1]))
    with open("alt-texts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "filename", "alt_text", "university",
                    "english_bachelor_program", "source_url"])
        w.writerows(rows)

    cards = []
    for category, filename, alt, uni, programme, src in rows:
        path = html.escape(f"{category}/{filename}")
        cards.append(
            f'<figure><img src="{path}" alt="{html.escape(alt)}" loading="lazy">'
            f'<figcaption><b>{html.escape(alt)}</b><br>'
            f'<code>{html.escape(filename)}</code><br>'
            f'<span class=prog>{html.escape(programme)}</span><br>'
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
            "code{color:#666}.prog{color:#0a7;font-size:11px}</style>"
            f"<h1>Japan University Images &mdash; {len(rows)} files</h1>"
            "<p>Every university below offers an English-taught bachelor's "
            "degree, named in green. Check each picture against its alt text.</p>"
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
    ap.add_argument("--photos", type=int, default=12,
                    help="photos per university (default 12)")
    ap.add_argument("--per-subject", type=int, default=3,
                    help="max photos of one subject per university (default 3)")
    ap.add_argument("--min-width", type=int, default=1000,
                    help="ignore source photos narrower than this")
    ap.add_argument("--width", type=int, default=1600,
                    help="download photos at this width (default 1600; use 0 "
                         "for full-size originals, which Wikimedia throttles)")
    ap.add_argument("--max-wait", type=int, default=180,
                    help="longest rate-limit pause to sit out before skipping "
                         "a file (default 180s)")
    ap.add_argument("--only", default="", help="only universities whose name contains this")
    ap.add_argument("--logos-only", action="store_true")
    ap.add_argument("--pace", type=float, default=1.5,
                    help="seconds between requests (raised automatically "
                         "whenever Wikimedia pushes back)")
    args = ap.parse_args()

    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    os.makedirs(LOGO_DIR, exist_ok=True)
    os.makedirs(PIC_DIR, exist_ok=True)

    rows = []
    if os.path.exists("alt-texts.csv"):
        with open("alt-texts.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for r in reader:
                if len(r) == 5:            # CSV written before the programme column
                    r = r[:4] + ["", r[4]]
                if len(r) == 6 and os.path.exists(os.path.join(r[0], r[1])):
                    rows.append(r)

    api = Api(args.pace, args.max_wait)
    width = args.width or 10 ** 6      # 0 means "give me the original"
    todo = [u for u in UNIVERSITIES if args.only.lower() in u[0]]
    logos = photos = 0

    for i, (alt_name, article, category, programme) in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {article}  —  {programme}")
        try:
            if fetch_logo(api, alt_name, article, programme, rows):
                logos += 1
            if not args.logos_only:
                photos += fetch_photos(api, alt_name, article, category,
                                       programme, args.photos, rows,
                                       args.min_width, args.per_subject, width)
        except KeyboardInterrupt:
            print("\nstopped — rerun to resume")
            break
        except RateLimited as e:
            print(f"    !! {e} — skipping {article} for now")
        except Exception as e:
            print(f"    !! {article}: {e}")

    write_outputs(rows)
    print(f"\n{len(os.listdir(LOGO_DIR))} logos, {len(os.listdir(PIC_DIR))} photos")
    if api.throttles:
        print(f"Wikimedia throttled {api.throttles} request(s). Anything "
              f"skipped is filled in by simply running this script again.")
    print(f"Wrote {ZIP_NAME}, alt-texts.csv and preview.html")
    print("Open preview.html in a browser to check the alt text against each image.")


if __name__ == "__main__":
    main()
