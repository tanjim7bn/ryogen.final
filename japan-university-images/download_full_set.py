#!/usr/bin/env python3
"""
Completes the "Japan University Images" collection on a machine with normal
internet access (this could not run inside the Claude sandbox because the
network egress policy there blocks Wikipedia/Wikimedia and every other image
host).

For each university below it downloads:
  * the official logo/emblem from its English Wikipedia article
    -> "Japan University Logos/<university name> logo.<ext>"
  * up to PHOTOS_PER_UNI campus/building/dorm/event photos from Wikimedia
    Commons -> "Japan University Pictures/<university name> <subject>.<ext>"

Every filename IS the alt text for that image, and alt-texts.csv is
(re)generated with columns: category, filename, alt_text, university, source.
Finally the two folders are zipped into "Japan University Images.zip".

Usage:
    pip install requests
    python3 download_full_set.py

Licensing note: Wikimedia Commons photos are free-licensed but usually
require attribution; each CSV row carries the file's description page URL —
check it before publishing a photo. University logos are trademarks: fine
for referring to the university (e.g. on a study-abroad listing) but not for
implying endorsement.
"""

import csv
import io
import os
import re
import sys
import zipfile

import requests

HEADERS = {"User-Agent": "RyogenAssetFetcher/1.0 (study-abroad site asset collection)"}
EN_API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

LOGO_DIR = "Japan University Logos"
PIC_DIR = "Japan University Pictures"
PHOTOS_PER_UNI = 2
MIN_PHOTO_WIDTH = 800
MIN_LOGO_WIDTH = 150

# (display name used in alt text, English Wikipedia article title)
# All of these offer English-taught degree programs.
UNIVERSITIES = [
    ("tokyo international university", "Tokyo International University"),
    ("ritsumeikan asia pacific university", "Ritsumeikan Asia Pacific University"),
    ("kyoto university of advanced science", "Kyoto University of Advanced Science"),
    ("waseda university", "Waseda University"),
    ("sophia university", "Sophia University"),
    ("temple university japan campus", "Temple University, Japan Campus"),
    ("keio university", "Keio University"),
    ("university of tokyo", "University of Tokyo"),
    ("kyoto university", "Kyoto University"),
    ("osaka university", "Osaka University"),
    ("tohoku university", "Tohoku University"),
    ("nagoya university", "Nagoya University"),
    ("kyushu university", "Kyushu University"),
    ("hokkaido university", "Hokkaido University"),
    ("university of tsukuba", "University of Tsukuba"),
    ("hiroshima university", "Hiroshima University"),
    ("international christian university", "International Christian University"),
    ("meiji university", "Meiji University"),
    ("rikkyo university", "Rikkyo University"),
    ("hosei university", "Hosei University"),
    ("doshisha university", "Doshisha University"),
    ("ritsumeikan university", "Ritsumeikan University"),
    ("kwansei gakuin university", "Kwansei Gakuin University"),
    ("kansai university", "Kansai University"),
    ("akita international university", "Akita International University"),
    ("soka university", "Soka University"),
    ("toyo university", "Toyo University"),
    ("chuo university", "Chuo University"),
    ("tokyo university of science", "Tokyo University of Science"),
    ("nagoya university of commerce and business", "Nagoya University of Commerce and Business"),
    ("international university of japan", "International University of Japan"),
    ("sendai university", "Sendai University"),
    ("tokai university", "Tokai University"),
]

PHOTO_QUERIES = ["{} campus", "{} building", "{} dormitory", "{} classroom",
                 "{} festival", "{} students"]

LOGO_WORDS = re.compile(r"logo|emblem|crest|seal|mon\b|symbol|wordmark|mark", re.I)


def api(url, **params):
    params.update(format="json")
    r = requests.get(url, params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()


def file_info(titles, site=COMMONS_API):
    """Return {title: (url, descriptionurl, width, mime)} for File: titles."""
    out = {}
    for i in range(0, len(titles), 50):
        data = api(site, action="query", titles="|".join(titles[i:i + 50]),
                   prop="imageinfo", iiprop="url|size|mime")
        for page in data.get("query", {}).get("pages", {}).values():
            ii = page.get("imageinfo")
            if ii:
                out[page["title"]] = (ii[0]["url"], ii[0]["descriptionurl"],
                                      ii[0].get("width", 0), ii[0].get("mime", ""))
    return out


def sanitize(name):
    name = re.sub(r"[^a-z0-9 .-]", "", name.lower())
    return re.sub(r"\s+", " ", name).strip()


def download(url, path):
    r = requests.get(url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)


def fetch_logo(alt_name, article, rows):
    have = [f for f in os.listdir(LOGO_DIR) if f.startswith(alt_name + " logo")]
    if have:
        print(f"  logo already present: {have[0]}")
        return
    data = api(EN_API, action="query", titles=article, prop="images", imlimit=100)
    pages = data.get("query", {}).get("pages", {})
    images = [im["title"] for p in pages.values() for im in p.get("images", [])]
    candidates = [t for t in images if LOGO_WORDS.search(t)] or images[:1]
    for site in (EN_API, COMMONS_API):
        info = file_info(candidates, site)
        for title in candidates:
            if title not in info:
                continue
            url, desc, width, mime = info[title]
            if "svg" not in mime and width < MIN_LOGO_WIDTH:
                continue
            ext = os.path.splitext(url)[1].lower() or ".png"
            fname = f"{alt_name} logo{ext}"
            download(url, os.path.join(LOGO_DIR, fname))
            rows.append(["Japan University Logos", fname, f"{alt_name} logo",
                         alt_name.title(), desc])
            print(f"  logo -> {fname}")
            return
    print(f"  !! no logo found for {article}", file=sys.stderr)


def fetch_photos(alt_name, article, rows):
    got = len([f for f in os.listdir(PIC_DIR) if f.startswith(alt_name)])
    seen = set()
    for q in PHOTO_QUERIES:
        if got >= PHOTOS_PER_UNI:
            break
        subject = q.split(" ", 99)[-1]  # campus / building / dormitory / ...
        data = api(COMMONS_API, action="query", generator="search",
                   gsrsearch=q.format(article), gsrnamespace=6, gsrlimit=8)
        titles = [p["title"] for p in
                  data.get("query", {}).get("pages", {}).values()]
        info = file_info(titles)
        for title, (url, desc, width, mime) in info.items():
            if got >= PHOTOS_PER_UNI:
                break
            if title in seen or LOGO_WORDS.search(title):
                continue
            if width < MIN_PHOTO_WIDTH or mime not in ("image/jpeg", "image/png"):
                continue
            seen.add(title)
            ext = os.path.splitext(url)[1].lower()
            alt = f"{alt_name} {subject}"
            fname = sanitize(f"{alt} {got + 1}") + ext
            download(url, os.path.join(PIC_DIR, fname))
            rows.append(["Japan University Pictures", fname, alt,
                         alt_name.title(), desc])
            print(f"  photo -> {fname}")
            got += 1
    if got == 0:
        print(f"  !! no photos found for {article}", file=sys.stderr)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(LOGO_DIR, exist_ok=True)
    os.makedirs(PIC_DIR, exist_ok=True)

    rows = []
    if os.path.exists("alt-texts.csv"):
        with open("alt-texts.csv", newline="", encoding="utf-8") as f:
            rows = [r for r in csv.reader(f)][1:]

    for alt_name, article in UNIVERSITIES:
        print(article)
        try:
            fetch_logo(alt_name, article, rows)
            fetch_photos(alt_name, article, rows)
        except Exception as e:
            print(f"  !! error for {article}: {e}", file=sys.stderr)

    with open("alt-texts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "filename", "alt_text", "university", "source"])
        w.writerows(rows)

    with zipfile.ZipFile("Japan University Images.zip", "w",
                         zipfile.ZIP_DEFLATED) as z:
        for d in (LOGO_DIR, PIC_DIR):
            for fn in sorted(os.listdir(d)):
                z.write(os.path.join(d, fn))
        z.write("alt-texts.csv")
    print("\nDone -> Japan University Images.zip")


if __name__ == "__main__":
    main()
