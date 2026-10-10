"""Demo wordmark for BB Jewel (concept for this demo only, not their logo). Text as outlines (Cormorant Garamond / Jost, SIL OFL)."""
import sys, io
sys.path.insert(0, '/workspace/sites/bb-jewel/work')
from textpath import path
import cairosvg
from PIL import Image
OUT = '/workspace/sites/bb-jewel/assets/'
GOLD, IVORY, INK = '#E2BE6E', '#F8F1E4', '#120A0D'
def f(v): return ('%.2f' % v).rstrip('0').rstrip('.')
def mark(x, y, s=1):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(s)})" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-linejoin="round">'
            f'<path d="M8 18 18 6h16l10 12-18 26z"/><path d="M8 18h36M18 6l8 12 8-12M26 18v26" stroke-width="1.4"/></g>')
d1, a1, _ = path('cormorantgaramond-600-latin.ttf', 'BB Jewel', 38, 62, 34, 0.02)
d2, a2, _ = path('jost-500-latin.ttf', 'JEWELLERY \u00b7 PIERCING', 9.5, 63, 50, 0.32)
w = 62 + max(a1, a2) + 4; h = 56
body = mark(2, 4) + f'<path fill="{IVORY}" d="{d1}"/><path fill="{GOLD}" d="{d2}"/>'
svg = lambda b: (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {h}" width="{w:.0f}" height="{h}" role="img" aria-labelledby="t">'
                 f'<title id="t">BB Jewel</title><!-- Demo concept wordmark, not the business logo. -->{b}</svg>\n')
open(OUT + 'logo.svg', 'w').write(svg(body))
png = cairosvg.svg2png(bytestring=svg(f'<rect width="{f(w)}" height="{h}" fill="{INK}"/>' + body).encode(), output_width=round(w * 4))
Image.open(io.BytesIO(png)).convert('RGB').save(OUT + 'logo.png', optimize=True)
def icon(size):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"><rect width="64" height="64" rx="14" fill="{INK}"/>{mark(6, 6, 1.1)}</svg>'
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=size, output_height=size)))
icon(512).save(OUT + 'favicon-512.png', optimize=True); icon(180).convert('RGB').save(OUT + 'apple-touch-icon.png', optimize=True)
icon(64).save(OUT + 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
cairosvg.svg2png(bytestring=open(OUT + 'logo.svg').read().encode(), write_to='/tmp/bb_logo.png', output_width=600, background_color=INK)
