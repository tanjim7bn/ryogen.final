# Japan University Images

Image pack for Japanese universities with English-taught programs, in two
categories:

- **`Japan University Logos/`** — official university logos. Each filename is
  the image's alt text, e.g. `tokyo international university logo.png` →
  `alt="tokyo international university logo"`.
- **`Japan University Pictures/`** — campus / building / dorm / classroom /
  event photos, same convention, e.g. `waseda university campus 1.jpg` →
  `alt="waseda university campus"`.

`alt-texts.csv` lists every image with its category, alt text, university and
source. `Japan University Images.zip` bundles both folders plus the CSV.

## Status: partial — 9 verified logos included, the rest needs one command

The environment this pack was assembled in has a network egress policy that
blocks every image host (en.wikipedia.org, commons.wikimedia.org,
upload.wikimedia.org, university websites, Google, Unsplash, seeklogo, etc. —
only GitHub and package registries are reachable). The same limitation was
hit in an earlier session (see `_archive/RYOGEN_MEMORY_LOG.md`: "external
CDNs/Wikimedia/Clearbit/favicon services are blocked in the build
environment").

What IS included was sourced from inside the repo and from GitHub, and every
image was **visually verified** to match its alt text: Tokyo International
University, KUAS, Waseda, Sophia — no (blocked), Temple University Japan
Campus, Kyoto University, Hokkaido University, University of Tsukuba, Toyo
University, and Akita International University.

To fetch the full set (33 universities' logos + campus/dorm/classroom/event
photos from Wikimedia Commons, alt-text-named, CSV + zip regenerated
automatically), run on any machine with normal internet access:

```bash
pip install requests
python3 download_full_set.py
```

It skips files already present, so the verified logos above are kept.

## Licensing

- Commons photos are free-licensed but usually need attribution — each CSV
  row links the file's description page.
- University logos are trademarks: fine for identifying the university in a
  listing, not for implying endorsement.
