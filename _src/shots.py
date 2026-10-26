"""Zrzuty ekran po ekranie. python _src/shots.py home,wesele/ 1440 [intro]
Pliki podawane przeglądarce prosto z dysku (page.route) – bez uruchamiania serwera."""
import sys, os, mimetypes
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'http://demo.local/finezja-sala-bankietowa/'
pages = sys.argv[1].split(','); w = int(sys.argv[2]); h = 900 if w > 800 else 844
OUT = os.path.join(ROOT, '_src', 'sh'); os.makedirs(OUT, exist_ok=True)

def serve(route):
    u = route.request.url.split('?')[0].split('#')[0]
    rel = u[len(HOST):] if u.startswith(HOST) else None
    if rel is None: return route.abort() if 'demo.local' in u else route.continue_()
    f = os.path.join(ROOT, rel)
    if os.path.isdir(f) or rel.endswith('/') or rel == '': f = os.path.join(f, 'index.html')
    if not os.path.exists(f): return route.fulfill(status=404, body='404')
    route.fulfill(status=200, body=open(f, 'rb').read(), headers={'content-type': mimetypes.guess_type(f)[0] or 'application/octet-stream'})

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=w < 800, has_touch=w < 800)
    ctx.route('**/*', serve)
    pg = ctx.new_page()
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    for name in pages:
        url = HOST + (name if name != 'home' else '') + '?team=1'
        pg.goto(url, wait_until='load', timeout=60000)
        if len(sys.argv) > 3:
            for t in (200, 700, 1300, 2000, 2600):
                pg.wait_for_timeout(t if t == 200 else 550); pg.screenshot(path=f'{OUT}/intro_{t}.png')
        pg.wait_for_timeout(2800)
        H = pg.evaluate('document.documentElement.scrollHeight'); frames = []; y = 0
        while y < H and len(frames) < 44:
            pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(1250)
            f = f'{OUT}/_f{len(frames)}.png'; pg.screenshot(path=f); frames.append(f); y += int(h * .85)
            H = pg.evaluate('document.documentElement.scrollHeight')
        n = name.strip('/').replace('/', '_') or 'home'
        sc = 0.5 if w > 800 else 0.55
        ims = [Image.open(f) for f in frames]; tw, th = int(w * sc), int(h * sc)
        per = 4 if w > 800 else 5
        for k in range(0, len(ims), per * 2):
            grp = ims[k:k + per * 2]; cols = min(len(grp), per); rows = (len(grp) + per - 1) // per
            sheet = Image.new('RGB', (cols * tw + (cols - 1) * 6, rows * th + (rows - 1) * 6), 'white')
            for j, im in enumerate(grp): sheet.paste(im.resize((tw, th)), ((j % per) * (tw + 6), (j // per) * (th + 6)))
            sheet.save(f'{OUT}/{n}_{w}_{k // (per * 2)}.png')
        for f in frames: os.remove(f)
        print(n, w, 'H', H, 'frames', len(frames))
    print('ERR', errs[:10])
    b.close()
