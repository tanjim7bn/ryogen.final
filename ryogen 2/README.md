# Ryogen

Source for **ryogen.ai**, a free AI Study Abroad Co-Pilot for students.

This repo is split into two tracks:

| Track | Path | What it is |
|---|---|---|
| **Marketing site** | [`/site`](./site) | The public landing page and its sub-pages. Plain static HTML + CSS + JS, assembled from shared partials. Deploys as-is. |
| **App** | [`/app`](./app) | Student Dashboard + Partner CRM. Authenticated applications, built later as prototypes for the tech team to wire to real data. Placeholder for now. |
| **Archive** | `/_archive` | The original single-file build script (`build_v9_monolithic.py`) and the project memory log, kept for history. Not part of the deploy. |

---

## The marketing site (`/site`)

Everything the browser serves lives under `/site`. Assets are referenced by
**root-relative paths** (`/assets/...`, `/css/...`, `/js/...`), never inlined,
so paths work no matter how deep a page is nested.

```
site/
  index.html            <- BUILT landing page (do not hand-edit, it is generated)
  build.py              <- assembler: partials + pages -> final HTML
  partials/             <- shared chrome, edit these ONCE
    head.html             (the <head> + a {{NAV}} marker)
    nav.html              (the top navigation)
    footer.html
    tail.html             (closing scripts/tags)
  pages/                <- per-page unique content (the bit between nav and footer)
    landing.html          -> builds to index.html
  css/styles.css        <- all styles (shared across every page)
  js/main.js            <- all behaviour (morph, counters, scroll reveal, marquee)
  assets/
    logos/                24 university PNGs
    brand/                ryogen-dark.png (nav/footer lockup), icon.png
```

### How it works

`build.py` stitches each `pages/<name>.html` between the shared `head` + `nav`
and `footer` + `tail`, then writes the final page to the site root. Edit the
nav or footer once in `partials/` and every page updates on the next build. No
copy-paste across pages.

```bash
cd site
python3 build.py
```

Output:

```
  built index.html              54,309 bytes
1 page(s) | dashes: 0
```

The build **asserts zero em/en dashes** in the output and fails loudly if any
slip in, one of the project's locked style rules.

### Add a new page (e.g. a SmartMatch page)

1. Create `pages/smartmatch.html` with just the body content (everything that
   sits between the nav and the footer).
2. Add a title/description entry to the `META` dict in `build.py`.
3. `python3 build.py` -> produces `smartmatch.html` at the site root.

`pages/landing.html` is special: it builds to `index.html`. Every other page
builds to `<name>.html`.

### Preview locally

```bash
cd site
python3 -m http.server 8000
# open http://localhost:8000
```

Serve from **inside `/site`** so the root-relative asset paths resolve.

### Deploy

The web root is `/site`. Point the host at that directory (or set it as the
project root) and it serves as static files, no build step required at deploy
time, since `build.py` produces plain HTML committed to the repo.

---

## Locked project conventions (do not break)

These are long-standing product rules baked into the build:

- **Font: Poppins only** (loaded via Google Fonts in `partials/head.html`).
- **No em dashes or en dashes** anywhere. `build.py` asserts this on every run.
- **No coordinates** and **no single-country/region framing** in student-facing
  copy. The site is global ("students worldwide").
- **Collaborators/partner language stays institutional and abstract**: Student
  CRM, Cohort Analytics, Branded Shortlists, Partnership Program. Never the
  words "agency", "counsellor", or "coaching centre" in student-facing copy.
- **Brand red: `#E30613`.**

## Before launch (open items)

- Replace illustrative data with real figures: tuition numbers, the
  "2,400+ students / 87% match" stats, and the partner-workspace pipeline
  metrics. All current values are placeholders.
- Remove the dev tag (the bottom-left "Remove before ship" note) in the built
  page for production.
