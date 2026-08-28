# Japan University Images

Logos and campus photography for the **34 Japanese universities that offer
bachelor's degrees taught in English**. Two categories:

- **`Japan University Logos/`** — official university logos. Each filename is
  the image's alt text, e.g. `tokyo international university logo.png` →
  `alt="tokyo international university logo"`.
- **`Japan University Pictures/`** — campus, dorm, classroom, library, gate,
  cafeteria, sports, event and seasonal photos, same convention, e.g.
  `waseda university dormitory 2.jpg` → `alt="waseda university dormitory"`.

`alt-texts.csv` lists every image with its alt text, university, **the
English-taught bachelor's programme that university runs**, and the source
URL. `preview.html` shows every image beside its alt text for a quick visual
check. `Japan University Images.zip` bundles the lot.

## Run it

```bash
pip install requests
python3 download_full_set.py
```

Defaults to 34 universities × (1 logo + up to 12 photos), so roughly 400
images. Options:

```bash
python3 download_full_set.py --photos 20        # more per university
python3 download_full_set.py --per-subject 5    # allow more of one subject
python3 download_full_set.py --only waseda      # a single university
python3 download_full_set.py --logos-only
python3 download_full_set.py --min-width 1600   # stricter quality bar
```

Resumable — files already on disk are skipped, so Ctrl-C and rerun is safe.

## Why these universities

Each entry is included because it runs an English-medium **undergraduate**
programme, and the script records which one next to every image. No
Japanese-only universities, and no graduate-only English programmes (which is
why, for example, the International University of Japan is not here).

National and public: University of Tokyo (PEAK), Kyoto (iUP), Osaka
(International College), Tohoku (FGL), Nagoya (G30), Kyushu (International
Undergraduate Programs), Hokkaido (ISP / MJSP), Tsukuba (BPGI), Hiroshima
(IGS), Okayama (Discovery Program), Akita International, University of Aizu
(ICTG).

Private: Waseda (SILS), Sophia (FLA), Keio (PEARL / GIGA), Temple University
Japan Campus, Tokyo International University (E-Track), Ritsumeikan Asia
Pacific University (APS / APM), Ritsumeikan (Global Studies), KUAS
(Engineering), ICU, Rikkyo (GLAP), Hosei (GIS), Meiji (Global Japanese
Studies), Chuo (GLOMAC / GLIB), Doshisha (ILA), Kwansei Gakuin (SIS), Soka
(FILA), Toyo (GINOS), NUCB (Global BBA), Yamanashi Gakuin (iCLA), Miyazaki
International College, Shibaura Institute of Technology (IGP), Kansai Gaidai
(College of Global Engagement).

Edit the `UNIVERSITIES` list at the top of the script to add or drop any.

## How images are chosen

- **Logos** come from each university's English Wikipedia article, preferring
  the SVG, which Wikimedia renders to a clean 1000px PNG.
- **Photos** come from the university's Wikimedia Commons category and its
  subcategories (up to 30 of them), backfilled by Commons search for
  universities with thin categories. Files are filtered to real photographs at
  least 1000px wide with a sane aspect ratio, de-duplicated by file hash, and
  spread across subjects — capped at 3 per subject by default — so you get a
  campus shot, a dorm, a classroom, an event and so on rather than a dozen
  angles of one building. The subject in each filename is inferred from the
  Commons file title, which is what makes the alt text specific.

## What is already committed here

13 images gathered earlier and visually verified one by one: 10 logos (Tokyo
International University, Ritsumeikan APU, KUAS, Waseda, Temple Japan, Kyoto,
Hokkaido, Tsukuba, Toyo, Akita International) and 3 high-resolution Tokyo
International University campus photos. Running the script keeps these and
fills in the rest.

The set is partial because the sandbox that assembled it is rate limited hard
by Wikimedia's shared-IP throttling. That is not a problem from a normal home
or office connection.

## Licensing

- Commons photos are free-licensed but nearly always require attribution —
  each CSV row links the file's description page, which names the author and
  licence.
- University logos are trademarks: fine for identifying a university in a
  listing, not for implying endorsement.
