# Ryogen Landing Page — Conversation Memory Log

## Project at a glance
Building the marketing landing page for **Ryogen** (ryogen.ai), a free **"AI Study Abroad Co-Pilot"** for students. The user is the founder (Tanjim, based in Dhaka); a separate tech team handles backend/database. This work was pure front-end: one self-contained HTML file, iterated from a rough concept through **v9** (`ryogen-v9-hybrid.html`, the current stable file).

Build workflow: a Python script (`build_v9.py`) generates one self-contained HTML file with all assets inlined as base64, verified via Playwright (Chromium) screenshots + pixel/DOM analysis at 1440px desktop and 390px mobile. Build scripts run assertions on every build (they print `dashes: 0 | coords: 0 | agency/counselor mentions: 0`).

## How the problem evolved (chronological)
1. **Early concepts** → rejected a globe-with-orbiting-cards hero (cards occluded the globe, looked "weird"/AI-made).
2. **User supplied three reference files** and locked direction: v4-style morphing title, a black-theme hero, and a 360° university-card carousel to be used *later* (not in hero). Also: Poppins, no em dashes, no coordinates, proper menu, PNG logos with real data.
3. **v5 dark** → full dark theme, morphing title, dark hero flight-map, 360 ring moved to its own section.
4. **v6 hybrid** → user wanted a **mix**: keep the dark hero but lighten the rest into a trust-forward edtech body; rewrite collaborators section to be institutional; remove Bangladesh/South Asia framing; fix a blurry hero glow and "AI-looking" floating cards.
5. **v7** → real wordmark (extracted from a JPG), radar-sweep hero replacing floating country cards, global copy, first iOS hardening pass.
6. **v8** → user sent **actual brand files**; swapped in the official lockup, replaced two destination beams with a radar + anonymous node field, fixed the CTA background and the morph.
7. **v9** → user sent **real iPhone screenshots** showing large blank areas; diagnosed and fixed the scroll-reveal system so content is visible regardless of iOS quirks.

## Locked constraints (cumulative — do not violate)
- **Font: Poppins only.** User explicitly rejected Plus Jakarta Sans + JetBrains Mono as "Claude fonts."
- **No em/en dashes** anywhere. Build asserts count = 0. Use commas/periods instead.
- **No coordinates** (e.g. "35°N/139°E") anywhere. Build asserts = 0.
- **No geographic targeting** — not "Bangladesh," not "South Asia," not "built in Dhaka" in student-facing copy. Ryogen is "for every student, everywhere / around the world / worldwide." Build asserts these = 0.
- **Collaborators section must be abstract/institutional.** Never say "agencies," "counselors," or "coaching centers" (students shouldn't see that Ryogen sells to counselors). Use "schools, universities, and education organizations," and product terms: **Student CRM, Cohort Analytics, Branded Shortlists, Partnership Program, Partner Workspace.** But phrase benefits so an agency still recognizes it's for them ("manage every student you guide," "grow on real outcomes"). Build asserts agency/counselor mentions = 0.
- **Brand red: #E30613.**
- **Hero title:** "The [morphing word] way to study abroad" with a red italic typewriter word cycling `smarter → faster → clearer → data-driven → honest` + blinking cursor. Locked hook.
- **360° ring carousel belongs in its own section**, never the hero.
- University logos must be **user-uploaded PNGs** (external CDNs/Wikimedia/Clearbit/favicon services are blocked in the build environment).

## Brand assets (bundled here)
- `logos_png.json` — 24 university logos, trimmed to bounds on white, base64. **All keys verified via labeled contact sheet.** Keys: waseda, tsukuba, hokkaido, kuas (Kyoto U of Advanced Science), tokyo_intl, toyo, kyoto, temple (Japan); monash_my, petronas (=Universiti Teknologi PETRONAS/UTP), utm, mmu, taylors, sunway (Malaysia); harvard, michigan, asu, lakeland (US); toronto, mcgill, waterloo, manitoba (Canada); bristol, coventry (UK).
- `brand_dark.txt` — **official RYOGEN lockup for dark backgrounds** (white "RYO" + red "GEN" + red icon), base64 PNG (1304×240). Extracted from `PNG_2_HQ.png` by keying out its black background. Verified clean (zero fringing). Used in nav (26px) and footer (30px).
- `icon_full.txt` — Ryogen icon, base64.

### Original brand source files (user still has these; re-upload if needed)
Four official lockup PNGs, all black-background, RGB, 8000px wide:
- **PNG_1_HQ** = dark-RYO + red-GEN (light-bg use)
- **PNG_2_HQ** = white-RYO + red-GEN (dark-bg — the one currently USED)
- **PNG_3_HQ** = red-RYO + dark-GEN (light-bg variant)
- **PNG_4_HQ** = red-RYO + white-GEN (dark-bg variant)
- Plus `ICON_1_HQ.png` (icon only) and `SOURCE.ai`.
Only PNG_2 has been processed. The others are available if a light-background nav or favicon is needed later. To process any of them: key out pure black via `alpha = max(r,g,b)` (logo is only white + red, both far from black → clean keying), trim to content bounds, downscale, base64-encode.

Flag SVGs (JP, MY, US, UK, CA, AU) are hand-built inline in the build script (no coordinates).

## Current page structure (v9)
Dark sticky nav (official logo, "For Students" dropdown = 7 tools, "For Collaborators" dropdown = institutional items, Scholarships, Roadmap & Blogs, Log in, Get Started Free) → **DARK hero** (radar sweep from center over 12 anonymous university nodes that ping in sync as the sweep passes — country-agnostic, scalable; morphing title; "Trusted by 2,400+ students worldwide"; CTAs; one quiet "Live, matching students to universities worldwide" scan tag) → **DARK stats band** (count-up: 800 universities, 24 avg matches, 2,400+ students matched worldwide, Free) → **LIGHT body**: logo marquee (grayscale, JS-cloned track), toolkit (7 tools, SmartMatch as prime red card), how-it-works + SmartMatch terminal demo (real logos + real tuition), 360° ring showcase (`#explore`, dark cards / white logo plates; mobile = horizontal swipe row), destinations (Japan + Malaysia live, US/UK/CA/AU "charting next"), scholarships (`#scholarships`), collaborators (`#partners`, institutional) → **DARK CTA** "Your route abroad starts here" (email capture, red glow) → **DARK footer**. Dark hero/CTA/footer bookend the light body.

## The 7 free student tools
SmartMatch (flagship — ranks universities you actually qualify for with an honest fit score), University Search, Essay Builder, Essay Review, Admission Dashboard, Scholarship Search, Country Roadmaps.

## Illustrative data — MUST be replaced before launch (flag every time)
- **Tuition (approx, international/yr):** Waseda ¥1.29M, Kyoto ¥536K, Tsukuba ¥536K, Hokkaido ¥536K, KUAS ¥1.48M, Toyo ¥1.10M, Temple Japan ¥1.55M, Tokyo Intl ¥1.2M; Monash MY RM42K, UTP RM34K, UTM RM16K, MMU RM32K, Taylor's RM48K, Sunway RM40K.
- Fit scores (92/91/86/79 etc.), the 2,400+ students / 87% avg match / workspace pipeline numbers (1,240 profiles / 980 shortlists / 640 apps / 210 enrolments), and the demo profile (GPA 3.72, IELTS 7.0, Computer Science, ¥1.3M budget) — all fictional/illustrative.

## Key technical insights & solutions
- **iOS "black sections" bug (fixed v7/v8):** light sections relied on a shared `.light` utility using a CSS `var()` for background; iOS dropped it. Fix: literal hex backgrounds on every section, `<meta name="color-scheme" content="light">`, `-webkit-` prefixes on `backdrop-filter` and 3D transforms, and halving payload by cloning the logo marquee via JS.
- **iOS "blank content" bug (the v9 fix — most important):** every scroll-reveal element was stuck at `opacity:0` and counters stuck at "0" because it all depended on `IntersectionObserver`, which iOS Safari delays/drops on image-heavy pages. **Solution pattern (reusable):** content **visible by default**; only hide once JS confirms it's running (`root.className += ' js'` → `.js .reveal{opacity:0}`); a **scroll-driven reveal using `getBoundingClientRect`** as the primary mechanism (reliable on iOS), with `IntersectionObserver` demoted to a smoothness enhancement; counters **seeded with real values** in HTML so they're correct even with no JS; every animation block wrapped in its own try/catch.
- **`inView` triggers on `r.top < h*0.9` alone** (not `&& r.bottom > 0`), so elements scrolled past during fast scrolling still reveal and are never missed.
- **Never use `className.indexOf('in')`** to detect the `.in` class — it false-matches substrings like `cta-in`. Use `classList.contains('in')`.
- **Morph init:** start with `del=true` and `ci=textContent.length` so it deletes the seeded word first and cycles (a `del=false` start froze it on "smarter").
- **CTA specificity trap:** a blanket `div.section{background:#FBFBF9}` overrode `.cta`'s dark background (white text dissolving). Removed the blanket rule; `.light` literal hex covers iOS safety.
- **Logo keying:** provided PNGs had black backgrounds; keyed out via `alpha = max(r,g,b)`.

## Environment constraints
- **Playwright WebKit won't download** in the sandbox, so the real Safari engine can't be tested. Reproduce iOS failures by deleting `window.IntersectionObserver` via `add_init_script` and by loading with `java_script_enabled=False`. This was sufficient to diagnose and verify both iOS bugs.
- **The image-viewer tool was intermittently returning empty** during the session, so verification leaned on pixel-sampling (PIL/numpy std-dev, color classification, band scans) and DOM `getComputedStyle` checks. The user's real-device screenshots were the single most valuable diagnostic input.
- Network limited to github/npm/pypi.

## User's working style & preferences (observed)
- **Founder-level ownership:** freely overrides earlier decisions (reversed "no dark theme," switched the locked font). Treat the latest instruction as authoritative.
- **Tests on a real iPhone and sends screenshots** — the most valuable feedback. Cares a lot about mobile UX.
- **Gives batched, numbered, specific feedback.** Appreciates each point addressed explicitly, in order.
- **Design taste:** dislikes anything that "looks AI-made" — hovering floating cards, occlusion, generic beams. Wants interesting-but-restrained motion ("don't overdo it"). Likes premium, edtech, trust-forward aesthetics.
- **Forward-thinking about scale:** wants the design to not need edits as more countries launch. Design country-agnostic wherever possible.
- **Brand-precise:** wants actual assets (logo, fonts, colors), not approximations.

## Collaboration approaches that worked well
- **Diagnose before fixing:** reason from symptom pattern to root cause, then prove the fix with reproductions (no-IO, no-JS scenarios).
- **Radical honesty about limitations:** flag when screenshots can't be seen or real Safari can't be tested; label all placeholder data.
- **Verification as first-class work:** confirm every change via DOM + pixel analysis across desktop/mobile and failure scenarios.
- **Reference-driven:** user supplies examples (reference HTML, logo sheets, screenshots); match them precisely.

## Clarifications/corrections the user made
- Font is Poppins (not the "Claude fonts" initially used).
- Reversed the earlier "no dark theme" call → dark hero + light body hybrid.
- Collaborators must stay institutional/abstract, but still legible to agencies.
- Remove ALL single-country/region framing → global.
- Use the *actual* provided logo, not the JPG-extracted one.
- Two hero beams imply a fixed country count — make it scalable.
- Restore the morphing title (it had silently broken).

## Next steps (identified, not yet done)
1. **User tests v9 on their real iPhone** and confirms the blank-sections fix. (Primary open item.)
2. Replace all illustrative data with real figures (tuition, 2,400+/87%, workspace metrics) before launch.
3. Remove the dev tag (bottom-left "Remove before ship" note) for production.
4. **Sub-pages** are the likely next build — offered SmartMatch, University Search, or the collaborator/partner page. Not started.
5. Optionally process the other three brand lockups (PNG_1/3/4) for a light-background nav or favicon.
6. Consider a real SVG logo (current one is a raster crop; fine at nav size, less crisp when large).

## Standing guidance for the next session
Keep responses concise and honest about tradeoffs. Always flag placeholder/illustrative data. Keep the dev tag labeled "Remove before ship." Reference edtech norms (ApplyBoard/Leap/Clever-style: light trust-forward body, audience-segmented, abstract partner language). When something breaks on the user's device, rely on their screenshots, diagnose to root cause, reproduce the failure in Chromium (delete IntersectionObserver / disable JS), fix, and verify with pixel + DOM analysis before presenting. Build from `build_v9.py`; copy to `build_v10.py` to preserve history.
