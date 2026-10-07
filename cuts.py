# Cuts every photograph the site uses into WebP variants (true downscale, sharpen after resize).
# Run: python3 cuts.py   (idempotent; skips files that exist unless --force)
import os, sys, json
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from data import PROJECTS, SERVICES

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, 'assets/raw'); SR = os.path.join(ROOT, 'assets/sr_out')
OUT = os.path.join(ROOT, 'img/p'); os.makedirs(OUT, exist_ok=True)
FORCE = '--force' in sys.argv
WIDTHS = [480, 800, 1200, 1600]
SIZES = {}

def load(pid):
    sr = os.path.join(SR, pid + '.png')
    if os.path.exists(sr):
        return Image.open(sr).convert('RGB')
    p = os.path.join(RAW, pid + '.jpg') if os.path.exists(os.path.join(RAW, pid + '.jpg')) else os.path.join(ROOT, 'assets', pid + '.png')
    return ImageOps.exif_transpose(Image.open(p)).convert('RGB')

def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.04)
    return ImageEnhance.Color(im).enhance(1.03)

def crop_aspect(im, aspect, fx=.5, fy=.5):
    w, h = im.size
    if w / h > aspect:
        nw = round(h * aspect); x = round((w - nw) * fx); return im.crop((x, 0, x + nw, h))
    nh = round(w / aspect); y = round((h - nh) * fy); return im.crop((0, y, w, y + nh))

def cut(name, im, widths, q=84):
    im = grade(im)
    made = []
    for w in widths:
        if w > im.width:
            continue
        out = os.path.join(OUT, f'{name}-{w}.webp')
        made.append(w)
        if os.path.exists(out) and not FORCE:
            continue
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r = r.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
        r.save(out, 'WEBP', quality=q, method=6)
    if im.width not in made and im.width < max(widths) and im.width > (made[-1] if made else 0) * 1.15:
        out = os.path.join(OUT, f'{name}-{im.width}.webp')
        if not os.path.exists(out) or FORCE:
            r = im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=30, threshold=2)); r.save(out, 'WEBP', quality=q, method=6)
        made.append(im.width)
    SIZES[name] = {'w': im.width, 'h': im.height, 'widths': made}
    return made

def key(pid): return pid.lower().replace('_', '-')

used = set()
for p in PROJECTS:
    for pid, _ in p['photos']: used.add(pid)
    used.add(p['cover']); used.add(p['second'])
for s in SERVICES:
    used.update(s['photos'])

for pid in sorted(used):
    widths = WIDTHS + ([2000] if pid == 'P00_01' else [])
    cut(key(pid), load(pid), widths)

# hero, desktop: 16:10 band from the Harrogate unit
cut('hero-d', crop_aspect(load('P00_01'), 16 / 10, fy=.40), [1280, 1920, 2560], q=86)
# before / during / after: aligned 1:1 (assets/pair_*.png), cut to 4:5
for n in ['before', 'after', 'during']:
    cut('pair-' + n, crop_aspect(Image.open(os.path.join(ROOT, f'assets/pair_{n}.png')).convert('RGB'), 4 / 5), [600, 900, 1200, 1600])
# services strip thumbnails are the native cuts; signature crops
cut('sig-fit', crop_aspect(load('P00_04'), 1, fy=.42), [600, 900, 1200])
cut('sig-made', crop_aspect(load('P28_03'), 1, fy=.5), [500, 800, 1100])

json.dump(SIZES, open(os.path.join(ROOT, 'img/sizes.json'), 'w'), indent=0)
print(len(SIZES), 'images cut')
