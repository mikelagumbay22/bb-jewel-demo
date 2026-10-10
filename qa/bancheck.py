"""Static ban/rule checks over dist/ for the BB Jewel demo."""
import json, re, html as H
from pathlib import Path
D = Path("/workspace/sites/bb-jewel/dist")
BANNER = "Premium package demo concept"
FOOTER = "Demo concept, not affiliated with or approved by BB Jewel (Bittu Bathinda)."
BADGE = "Illustrative image, not a photo of BB Jewel's pieces"
VBADGE = "Illustrative video, not footage of BB Jewel's pieces"
TEL = 'href="tel:+19052266566"'
fails, lines = [], []
def ok(c, m): lines.append(("PASS " if c else "FAIL ") + m); c or fails.append(m)
pages = sorted(D.glob("*.html"))
texts = {f: f.read_text() for f in D.rglob("*") if f.suffix in (".html", ".css", ".js", ".svg", ".json", ".txt", ".xml")}
alltext = "\n".join(texts.values()); low = alltext.lower()
ok(not re.search(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", alltext, re.I), "no e-mail address anywhere in dist")
for w in ["mailto", "hotmail", "gmail", "aggregaterating", "openinghoursspecification", "higgsfield"]:
    ok(w not in low, f"no '{w}' anywhere")
vis = H.unescape(" ".join(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|head)\b.*?</\1>", " ", texts[f], flags=re.S)) for f in texts if f.suffix == ".html"))
for pat, why in [(r"\$\s?\d|\d+\.\d\d\b(?! on Google)", "prices"), (r"github\.io", "github.io in visible copy"), (r"since (19|20)\d\d|award|voted|#1 ", "years/awards"),
                 (r"\bchef\b|\bowner\b|family[- ]owned", "staff/owner claims"), (r"\bstock (image|photo)", "'stock' wording"), (r"open (now|today|daily|7 days)", "invented hours"), (r"\bfree\b|warrant|guarantee", "invented claims"), (r"\b(10|14|18|22|24)\s?(k|kt|karat|carat)\b|hallmark|certified|\bpure\b", "karat/purity claims"), (r"steril|hygien|hypoallergenic|licensed|pain[- ]?free|\bsafe\b|clean(ed|ing)? (needle|equipment)", "health/sterilisation claims")]:
    ok(not re.search(pat, vis, re.I), f"no {why} in visible text")
ok(all(TEL in p.read_text() for p in pages), "tap-to-call on every page")
idx = H.unescape((D / "index.html").read_text())
ok("4.7 on Google from 268 reviews" in re.sub(r"<[^>]+>", "", idx), "rating as visible text on Home")
ok("reviews to confirm" in vis.lower(), "'Reviews to confirm' placeholder")
ok(all(re.search(r"google\.com/maps/search/\?api=1&(amp;)?query=BB\+Jewel\+7050\+Airport", (D / f).read_text()) for f in ["index.html", "visit.html"]), "Leave us a Google review -> Maps search (Home, Visit)")
ok("Leave us a Google review" in idx, "review button label")
for k in ["Malton", "Mississauga", "Bittu Bathinda"]:
    ok(k in idx, f"Home mentions {k}")
# hero video
v = re.search(r"<video\b[^>]*>", idx).group(0)
ok(all(a in v for a in ["muted", "playsinline", "loop", 'preload="none"', 'poster="img/video/hero-poster.webp"', 'width="960"', 'height="720"']) and "autoplay" not in v, "hero video: muted/playsinline/loop/preload none/poster, no autoplay attr")
ok('data-src="img/video/hero-loop.mp4"' in idx and (D / "img/video/hero-loop.mp4").stat().st_size < 1_500_000, f"hero MP4 lazy (data-src), {(D / 'img/video/hero-loop.mp4').stat().st_size // 1024} KB")
ok("data-video-toggle" in idx and "Pause video" in idx, "Pause button present")
ok(VBADGE in H.unescape(idx), "video badge")
# signature
ok('data-sig' in idx and idx.count('class="sig__part') == 3 and "sig__final" in idx and "Piece by piece" in idx, "signature scroll scene (3 parts, final layer, headline in HTML)")
ok(all((D / f"img/sig/{n}.webp").exists() for n in ["base-wide-1600", "base-wide-900", "base-tall-900", "final-wide-1600", "final-wide-900", "final-tall-900", "chain", "pendant", "sparkle"]), "all signature layers shipped")
ok(BADGE in H.unescape(idx.split('class="sig"')[1].split("</section>")[0]), "signature scene badged")
# gallery
cj = json.loads((D / "collections.json").read_text())
ok(len(cj["items"]) == 6 and all(it["details"] == "To confirm" for it in cj["items"]), "collections.json: 6 categories, details To confirm")
ok({it["category"] for it in cj["items"]} == {"Gold chains", "Bangles", "Rings", "Earrings", "Nose pins", "Kids' jewellery"}, "generic categories")
ok(all((D / it["image"]).exists() and (D / it["image_small"]).exists() for it in cj["items"]), "every gallery image shipped")
col = H.unescape((D / "collections.html").read_text())
ok("Premium feature: you can update this gallery yourself" in col and "Demo · Premium feature" in col, "visible demo-labelled Premium feature note")
ok(col.count('class="gcard reveal') == 6 and "data-gallery" in col, "gallery pre-rendered (6) + live JSON hook")
ag = (D / "admin-guide.html").read_text()
ok("collections.json" in ag and 'href="admin-guide.html"' not in "".join(re.findall(r'<nav\b.*?</nav>', idx, re.S)), "admin-guide.html exists, not in nav")
pi = H.unescape((D / "piercing.html").read_text())
ok("Ask us about aftercare" in pi, "'Ask us about aftercare' on Piercing")
ok("<fieldset disabled>" in pi and "This form is disabled in this demo" in pi, "appointment form disabled with note")
for fid in ["a-name", "a-phone", "a-service", "a-date", "a-time", "a-msg"]:
    ok(f'<label for="{fid}"' in pi, f"appointment field {fid} labelled")
vi = (D / "visit.html").read_text()
ok(re.search(r'<iframe src="https://maps\.google\.com/maps\?q=[^"]+output=embed" title="[^"]+" loading="lazy"', vi) is not None, "keyless map embed, titled, lazy")
ok("google.com/maps/dir/?api=1&amp;destination=" in vi, "directions link")
ok("data-status" not in alltext and "open now" not in low, "no live open/closed badge")
ok("opening hours" in vis.lower(), "hours To-confirm placeholder")
ok((D / ".nojekyll").exists(), ".nojekyll present")
for f in pages:
    s = f.read_text(); u = H.unescape(s); n = f.name
    ok('<meta name="robots" content="noindex, nofollow">' in s, f"{n}: noindex")
    ok(BANNER in u and s.index('class="demo-banner"') < s.index('class="skip-link"'), f"{n}: demo banner")
    ok(FOOTER in u, f"{n}: footer disclaimer")
    for k in ("og:title", "twitter:title", "og:site_name"):
        m = re.search(rf'(?:property|name)="{k}" content="([^"]+)"', s)
        ok(m and "(demo concept)" in m.group(1), f"{n}: {k} has '(demo concept)'")
    ok("(demo concept)" in re.search(r"<title>(.*?)</title>", s).group(1), f"{n}: <title> has '(demo concept)'")
    refs = re.findall(r'(?:href|src|poster)="([^"]+)"', s) + [u2.split()[0] for ss in re.findall(r'srcset="([^"]+)"', s) for u2 in ss.split(",")]
    bad = [r for r in refs if r.startswith("/") or (not re.match(r"^(https?:|tel:|#)", r) and not (D / r.split("#")[0].split("?")[0]).exists())]
    ok(not bad, f"{n}: all refs relative and resolvable {bad[:3]}")
    for img in re.findall(r"<img\b[^>]*>", s):
        ok(re.search(r'\swidth="\d+"', img) and re.search(r'\sheight="\d+"', img), f"{n}: img has width/height")
    photos = [i for i in re.findall(r'<img\b[^>]*src="img/([^"]+)"', s) if not i.startswith("logo")]
    medias = re.findall(r'<div class="media[^"]*"[^>]*>(.*?)</div>', s, re.S)
    photos = [i for i in photos if not i.startswith("sig/")]
    ok(len(photos) == len(medias) and all(BADGE in H.unescape(m) for m in medias), f"{n}: every photo badged ({len(photos)})")
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        d = json.loads(ld)
        ok(d["@type"] == ["JewelryStore"] and set(d) <= {"@context", "@type", "name", "address", "telephone", "image", "alternateName", "sameAs", "hasMap"} and d["image"].endswith("img/logo.png") and d["address"]["streetAddress"] == "7050 Airport Rd", f"{n}: JSON-LD keys {sorted(d)}")
big = [(f.name, f.stat().st_size) for f in D.rglob("*") if f.suffix in (".webp", ".jpg", ".png") and f.stat().st_size >= 150_000 and f.name != "logo.png"]
ok(not big, f"all images under 150 KB {big}")
print("\n".join(lines)); print(f"\n{len(lines) - len(fails)} passed, {len(fails)} failed")
