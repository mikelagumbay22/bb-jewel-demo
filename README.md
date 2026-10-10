# BB Jewel (Bittu Bathinda) — Premium package demo concept

Static multi-page demo (noindex). Build: `cd site && python3 build.py --export` → `dist/` (relative paths, `.nojekyll`).
QA (lean): `python3 qa/bancheck.py`, `python3 qa/audit.py` (axe 390 + 1440), `python3 qa/shots.py http://127.0.0.1:8115/ screenshots`, `python3 qa/sig_shot.py`.
site_url: https://mikelagumbay22.github.io/bb-jewel-demo/ · preview: http://127.0.0.1:8115/

## Signature effect (Home)
Pinned scroll scene (300vh desktop / 200vh mobile): an empty velvet bust, two chain strands fly in, the pendant drops and spins into place,
sparkles pop, then it crossfades to the finished necklace and the headline appears. Layers in assets/sig/:
- base-*.webp (empty bust) and final-*.webp (same scene with the necklace): the final one was made by EDITING the base (GPT Image 2.5), so they align (bust outline matches; only faint background bokeh differs).
- chain.webp (used twice, mirrored for the left strand), pendant.webp, sparkle.webp: transparent GPT Image 2.5 layers.
Reduced motion: no pin, the finished necklace and copy are shown statically. CLS 0 (pin height set by an inline head class).

## Hero video
assets/video/hero-loop.mp4 (Seedance 1.5 Pro, 4 s, 720p source → 960×720, no audio, 820 KB) + hero-poster.webp.
Only loaded when motion is allowed; Pause button; reduced motion shows the poster only.

## Owner-editable gallery
dist/collections.json + dist/img/collections/. Collections.js re-reads the JSON on every visit; see admin-guide.html (unlinked).

Images: 5 Higgsfield GPT Image 2.5 photos (no faces) badged "Illustrative image, not a photo of BB Jewel's pieces"; video badged "Illustrative video, not footage of BB Jewel's pieces".
Logo: a demo wordmark (work/logo.py), not the business's logo.
To confirm: opening hours, reviews (no quotes used), collection styles/details (each category), piercing services/pricing/age policy, the store's story.
