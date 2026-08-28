# Japan University Images

Image pack for Japanese universities with English-taught programs, in two
categories:

- **`Japan University Logos/`** — official university logos. Each filename is
  the image's alt text, e.g. `tokyo international university logo.png` →
  `alt="tokyo international university logo"`.
- **`Japan University Pictures/`** — campus, dorm, classroom, library, gate and
  event photos, same convention, e.g. `waseda university dormitory 2.jpg` →
  `alt="waseda university dormitory"`.

`alt-texts.csv` lists every image with its category, alt text, university and
source URL. `preview.html` shows every image next to its alt text so you can
check the matches at a glance. `Japan University Images.zip` bundles it all.

## Run this to build the full set

```bash
pip install requests
python3 download_full_set.py
```

42 universities, logo plus 4 photos each, roughly 5–10 minutes on a normal
connection. Options:

```bash
python3 download_full_set.py --photos 6        # more photos per university
python3 download_full_set.py --only waseda     # one university
python3 download_full_set.py --logos-only
python3 download_full_set.py --min-width 1600  # stricter quality bar
```

It is resumable — files already on disk are skipped, so Ctrl-C and rerun is
safe. Add or remove universities by editing the `UNIVERSITIES` list at the top
of the script.

### How it picks images

- **Logos** come from each university's English Wikipedia article, preferring
  the SVG version, which Wikimedia renders to a clean 1000px PNG.
- **Photos** come from the university's Wikimedia Commons category (and its
  subcategories), filtered to real photographs at least 1000px wide with a
  sane aspect ratio, de-duplicated by file hash, and spread across subjects so
  you get a campus shot, a dorm, a classroom and so on rather than four photos
  of the same building. The subject in the filename is inferred from the
  Commons file title, which is what makes the alt text specific.

## What is already in this folder

Committed here are images gathered earlier and **visually verified** one by
one: 10 logos (Tokyo International University, Ritsumeikan Asia Pacific
University, KUAS, Waseda, Temple University Japan Campus, Kyoto University,
Hokkaido, Tsukuba, Toyo, Akita International) and 3 high-resolution Tokyo
International University campus photos. Running the script fills in the rest
and leaves these in place.

The set is partial because the Claude Code sandbox that assembled it is rate
limited hard by Wikimedia's shared-IP throttling (repeated multi-minute
penalties per file). That is not a problem from a normal home or office
connection.

## Licensing

- Commons photos are free-licensed but nearly always require attribution —
  each CSV row links the file's description page, which names the author and
  licence.
- University logos are trademarks: fine for identifying a university in a
  listing, not for implying endorsement.
