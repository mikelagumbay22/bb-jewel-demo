"""Signature-effect mid-scroll shot (pieces flying in) + reduced-motion sanity check."""
import os, re
from playwright.sync_api import sync_playwright
from PIL import Image
CHROME = eval(re.search(r"CHROME = (.*)", open(os.path.join(os.path.dirname(__file__), "shots.py")).read()).group(1), {"os": os})
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.add_init_script("window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput) window.__cls+=e.value}).observe({type:'layout-shift',buffered:true})")
    pg.goto("http://127.0.0.1:8115/", wait_until="networkidle"); pg.wait_for_timeout(800)
    for q in (0.1, 0.25, 0.4, 0.48):
        pg.evaluate("p=>{const s=document.querySelector('[data-sig]');window.scrollTo(0,s.offsetTop+p*(s.offsetHeight-innerHeight))}", q); pg.wait_for_timeout(500)
    pg.screenshot(path="/tmp/_sig.png"); Image.open("/tmp/_sig.png").convert("RGB").save("screenshots/signature-midscroll-desktop.jpg", quality=84, optimize=True)
    print("screenshots/signature-midscroll-desktop.jpg", os.path.getsize("screenshots/signature-midscroll-desktop.jpg") // 1024, "KB  CLS", round(pg.evaluate("window.__cls"), 4))
    r = b.new_page(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    r.goto("http://127.0.0.1:8115/", wait_until="networkidle"); r.wait_for_timeout(600)
    print("reduced:", r.evaluate("""[document.documentElement.classList.contains('scrub-ok'), document.querySelector('video').currentSrc || 'no-src', document.querySelector('[data-video-toggle]').hidden,
      getComputedStyle(document.querySelector('.sig__final')).opacity, getComputedStyle(document.querySelector('.sig__copy')).opacity, document.querySelector('[data-sig]').offsetHeight,
      [...document.getAnimations()].filter(a=>a.playState==='running').length]"""))
    b.close()
