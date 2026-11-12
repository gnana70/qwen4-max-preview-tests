"""Record a model-built HTML page to MP4 with deterministic virtual time.

Usage: python record_html.py <answer.md|page.html> <out.mp4> [--seconds 26] [--fps 30]

requestAnimationFrame, performance.now and Date.now are replaced by a virtual clock,
so every frame is captured exactly 1/fps apart however slow the headless browser is.
Math.random is seeded so the run can be repeated. Keys are pressed like a person would:
F at 6 s (fish), B at 14 s (giant bird), Space at 22 s (free flocking); change with --keys.
Also writes <out>.json: console errors, JS time per frame, and which keys changed the picture.
"""
import sys, re, json, subprocess, statistics, argparse, pathlib
from playwright.sync_api import sync_playwright

INIT = r"""
(() => {
  let s = 20261111 >>> 0;
  Math.random = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const realNow = performance.now.bind(performance);
  let now = 0, id = 0; const cbs = new Map(); const t0 = 1762851600000;
  performance.now = () => now; Date.now = () => t0 + now;
  window.requestAnimationFrame = cb => { cbs.set(++id, cb); return id; };
  window.cancelAnimationFrame = i => cbs.delete(i);
  window.__errors = [];
  window.addEventListener('error', e => window.__errors.push(String(e.message)));
  window.__step = dt => { now += dt; const list = [...cbs.values()]; cbs.clear();
    const a = realNow(); for (const cb of list) { try { cb(now); } catch (e) { window.__errors.push(String(e)); } }
    return realNow() - a; };
})();
"""

def extract_html(path):
    src = pathlib.Path(path).read_text(encoding='utf-8')
    if path.endswith('.html'): return src
    blocks = re.findall(r"```(?:html)?\s*\n(.*?)```", src, re.S)
    if not blocks: raise SystemExit('no code block found in ' + path)
    return max(blocks, key=len)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--seconds', type=float, default=26); ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--keys', default='KeyF@6,KeyB@14,Space@22', help='key@seconds,...')
    ap.add_argument('--w', type=int, default=1920); ap.add_argument('--h', type=int, default=1080)
    a = ap.parse_args()
    html = extract_html(a.src)
    page_file = pathlib.Path(a.out).with_suffix('.html'); page_file.write_text(html, encoding='utf-8')
    # 'Key@t' = tap at t seconds; 'Key@t1-t2' = hold from t1 to t2
    events = {}
    for kv in a.keys.split(','):
        k, t = kv.split('@')
        if '-' in t:
            t1, t2 = (float(x) for x in t.split('-'))
            events.setdefault(int(round(t1 * a.fps)), []).append(('down', k)); events.setdefault(int(round(t2 * a.fps)), []).append(('up', k))
        else:
            events.setdefault(int(round(float(t) * a.fps)), []).append(('press', k))
    keys = {f: ' '.join(f'{act}:{k}' for act, k in ev) for f, ev in events.items()}
    n = int(a.seconds * a.fps); dt = 1000 / a.fps
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(a.fps),
                           '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16',
                           '-pix_fmt', 'yuv420p', a.out], stdin=subprocess.PIPE)
    step_ms, console, diffs = [], [], {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        pg = b.new_page(viewport={'width': a.w, 'height': a.h})
        pg.on('console', lambda m: console.append(f'{m.type}: {m.text}') if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: console.append(f'pageerror: {e}'))
        pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
        pg.add_init_script(INIT)
        pg.goto(page_file.resolve().as_uri()); pg.wait_for_timeout(300)
        pg.mouse.move(a.w / 2, a.h / 2)
        prev = None
        for f in range(n):
            for act, k in events.get(f, []):
                getattr(pg.keyboard, act)(k)
            step_ms.append(pg.evaluate(f'window.__step({dt})'))
            shot = pg.screenshot(type='jpeg', quality=92)
            ff.stdin.write(shot)
            if f in keys or f - 1 in keys: diffs[f] = len(shot)
        errors = pg.evaluate('window.__errors')
        b.close()
    ff.stdin.close(); ff.wait()
    report = dict(src=a.src, frames=n, fps=a.fps, key_frames={str(k): v for k, v in keys.items()},
                  js_ms_per_frame_median=round(statistics.median(step_ms), 2),
                  js_ms_per_frame_p95=round(sorted(step_ms)[int(len(step_ms) * .95)], 2),
                  errors=errors[:20], console=console[:20])
    pathlib.Path(a.out).with_suffix('.json').write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))

if __name__ == '__main__':
    main()
