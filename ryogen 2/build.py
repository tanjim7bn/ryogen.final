#!/usr/bin/env python3
"""
Ryogen site assembler.
Combine shared partials (head/nav/footer/tail) with each page's unique body in
pages/*.html and write deployable HTML to the site root.

  - Edit shared chrome ONCE in partials/ (nav, footer, <head>).
  - Edit a page's content in pages/<name>.html.
  - Add a page: drop pages/<name>.html, add a META entry, run this.
  - Run: python3 build.py

Assets live in /assets and are referenced by root-relative path, never inlined.
pages/landing.html -> index.html ; every other page -> <name>.html
"""
import os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
def read(p): return open(os.path.join(HERE, p), encoding='utf-8').read()

head, nav      = read('partials/head.html'), read('partials/nav.html')
footer, tail   = read('partials/footer.html'), read('partials/tail.html')

# per-page <title> + meta description. key 'index' == pages/landing.html
META = {
    'index':      ('Ryogen, AI Study Abroad Co-Pilot',
                   'Ryogen is a free AI study abroad co-pilot. Find universities you actually qualify for, build essays, and track applications, all in one place.'),
    'partners':    ('For Collaborators, Ryogen',
                   'Ryogen partners with schools, universities, and education organizations worldwide. One workspace to guide every student with data.'),
    # 'smartmatch': ('SmartMatch, Ryogen', 'SmartMatch ranks the universities you actually qualify for with an honest fit score.'),
}
DASH = ('\u2014', '\u2013')  # em/en dash must never ship

def assemble(page_path):
    name = os.path.splitext(os.path.basename(page_path))[0]
    out  = 'index.html' if name == 'landing' else f'{name}.html'
    key  = 'index' if name == 'landing' else name
    title, desc = META.get(key, ('Ryogen', 'Ryogen, AI Study Abroad Co-Pilot'))
    h = head.replace('<title>Ryogen, AI Study Abroad Co-Pilot</title>',
                     f'<title>{title}</title><meta name="description" content="{desc}">')
    h = h.replace('<!-- {{NAV}} -->', nav)
    html = h + read(page_path) + footer + tail
    for d in DASH:
        assert d not in html, f'DASH in {out}: fix the source partial/page'
    with open(os.path.join(HERE, out), 'w', encoding='utf-8') as fh:
        fh.write(html)
    return out, len(html)

if __name__ == '__main__':
    built = [assemble(p) for p in sorted(glob.glob(os.path.join(HERE, 'pages', '*.html')))]
    for n, sz in built: print(f'  built {n:22s} {sz:>7,} bytes')
    print(f'{len(built)} page(s) | dashes: 0')
