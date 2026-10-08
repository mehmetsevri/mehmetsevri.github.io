#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate favicon.svg, apple-touch-icon.png and og-image.jpg (1200x630).

Usage (from the repository root):  python tools/make_images.py
Requires Pillow. Fonts are taken from C:/Windows/Fonts when available.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img')
FONT_DIRS = ['C:/Windows/Fonts', '/usr/share/fonts/truetype/dejavu', '/Library/Fonts']


def font(names, size):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.isfile(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


BOLD = ['segoeuib.ttf', 'DejaVuSans-Bold.ttf', 'Arial Bold.ttf']
SEMI = ['seguisb.ttf', 'segoeuib.ttf', 'DejaVuSans-Bold.ttf']
REG = ['segoeui.ttf', 'DejaVuSans.ttf', 'Arial.ttf']
MONO = ['consolab.ttf', 'consola.ttf', 'DejaVuSansMono-Bold.ttf']


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient(size, stops, angle_deg=45):
    """Linear multi-stop gradient as an RGB image."""
    w, h = size
    ang = math.radians(angle_deg)
    dx, dy = math.cos(ang), math.sin(ang)
    small = Image.new('RGB', (max(2, w // 4), max(2, h // 4)))
    sw, sh = small.size
    px = small.load()
    span = abs(dx) * sw + abs(dy) * sh
    for y in range(sh):
        for x in range(sw):
            t = ((x * dx + y * dy) - min(0, dx * sw) - min(0, dy * sh)) / span
            t = max(0.0, min(1.0, t))
            for i in range(len(stops) - 1):
                p0, c0 = stops[i]
                p1, c1 = stops[i + 1]
                if p0 <= t <= p1:
                    px[x, y] = lerp(c0, c1, (t - p0) / (p1 - p0 or 1))
                    break
    return small.resize((w, h), Image.BICUBIC)


def glow(canvas, center, radius, color, alpha):
    layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius * 0.55))
    canvas.alpha_composite(layer)


def favicon_svg():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
           '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
           '<stop offset="0" stop-color="#4f46e5"/><stop offset=".52" stop-color="#2563eb"/><stop offset="1" stop-color="#047857"/>'
           '</linearGradient></defs>'
           '<rect width="64" height="64" rx="16" fill="url(#g)"/>'
           '<text x="32" y="41.5" text-anchor="middle" font-family="\'Plus Jakarta Sans\',\'Segoe UI\',Arial,Helvetica,sans-serif" '
           'font-weight="800" font-size="25" letter-spacing="-1" fill="#fff">MS</text></svg>\n')
    with open(os.path.join(IMG, 'favicon.svg'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(svg)


def touch_icon():
    s = 180
    im = gradient((s, s), [(0, (79, 70, 229)), (0.52, (37, 99, 235)), (1, (4, 120, 87))], 45).convert('RGBA')
    glow(im, (40, 30), 70, (165, 180, 252), 70)
    d = ImageDraw.Draw(im)
    f = font(BOLD, 78)
    txt = 'MS'
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(((s - (bb[2] - bb[0])) / 2 - bb[0], (s - (bb[3] - bb[1])) / 2 - bb[1] - 2), txt, font=f, fill=(255, 255, 255))
    im.convert('RGB').save(os.path.join(IMG, 'apple-touch-icon.png'), optimize=True)


def text_gradient(text, fnt, stops):
    """Render text filled with a horizontal gradient; returns RGBA image."""
    tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
    bb = tmp.textbbox((0, 0), text, font=fnt)
    w, h = bb[2] - bb[0] + 8, bb[3] - bb[1] + 8
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).text((4 - bb[0], 4 - bb[1]), text, font=fnt, fill=255)
    fill = gradient((w, h), stops, 0).convert('RGBA')
    fill.putalpha(mask)
    return fill


def og_image():
    W, H = 1200, 630
    base = gradient((W, H), [(0, (6, 9, 20)), (0.55, (14, 16, 44)), (1, (20, 22, 58))], 30).convert('RGBA')
    glow(base, (120, 40), 260, (34, 211, 238), 46)
    glow(base, (930, 210), 300, (129, 140, 248), 70)
    glow(base, (1120, 620), 240, (16, 185, 129), 52)
    # faint grid (drawn on its own layer so the alpha blends)
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 48):
        gd.line([(x, 0), (x, H)], fill=(148, 163, 255, 16))
    for y in range(0, H, 48):
        gd.line([(0, y), (W, y)], fill=(148, 163, 255, 16))
    base.alpha_composite(grid)
    # neural constellation
    rnd = random.Random(7)
    nodes = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.random() < .55) for _ in range(70)]
    net = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(net)
    for i, (x1, y1, c1) in enumerate(nodes):
        for x2, y2, _ in nodes[i + 1:]:
            dist = math.hypot(x1 - x2, y1 - y2)
            if dist < 150:
                a = int((1 - dist / 150) * 70)
                nd.line([(x1, y1), (x2, y2)], fill=((34, 211, 238) if c1 else (129, 140, 248)) + (a,), width=1)
    for x, y, c in nodes:
        col = (34, 211, 238) if c else (129, 140, 248)
        nd.ellipse([x - 2.2, y - 2.2, x + 2.2, y + 2.2], fill=col + (200,))
    base.alpha_composite(net)

    # portrait with halo + ring
    cx, cy, R = 935, 330, 250
    glow(base, (cx, cy), R, (99, 102, 241), 90)
    ring = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(14, 22, 52, 255))
    seg = [((34, 211, 238), 200, 260), ((129, 140, 248), 260, 320), ((192, 132, 252), 320, 350), ((52, 211, 153), 40, 110)]
    for col, a0, a1 in seg:
        rd.arc([cx - R, cy - R, cx + R, cy + R], a0, a1, fill=col + (255,), width=5)
    rd.ellipse([cx - R - 26, cy - R - 26, cx + R + 26, cy + R + 26], outline=(148, 163, 255, 70), width=1)
    base.alpha_composite(ring)
    try:
        # square photo, cropped to a circle that sits inside the ring
        por = Image.open(os.path.join(IMG, 'profile-square.webp')).convert('RGBA')
        d_in = 2 * (R - 8)
        side = min(por.size)
        z = int(side / 1.06)                      # same slight zoom as the site hero
        left = (por.width - z) // 2
        top = max(0, int((por.height - z) * 0.30))
        por = por.crop((left, top, left + z, top + z)).resize((d_in, d_in), Image.LANCZOS)
        mask = Image.new('L', (d_in * 4, d_in * 4), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, d_in * 4 - 1, d_in * 4 - 1], fill=255)
        por.putalpha(mask.resize((d_in, d_in), Image.LANCZOS))
        base.alpha_composite(por, (cx - d_in // 2, cy - d_in // 2))
    except OSError as exc:
        print('portrait not found:', exc, file=sys.stderr)

    d = ImageDraw.Draw(base)
    x0 = 70
    # kicker pill
    fk = font(MONO, 21)
    kick = 'AI · CYBERSECURITY · AI IN HEALTHCARE'
    kb = d.textbbox((0, 0), kick, font=fk)
    d.rounded_rectangle([x0, 74, x0 + kb[2] - kb[0] + 52, 74 + 44], radius=22, fill=(7, 11, 22, 200), outline=(148, 163, 255, 90))
    d.ellipse([x0 + 18, 90, x0 + 30, 102], fill=(52, 211, 153))
    d.text((x0 + 40, 85 - kb[1] + 2), kick, font=fk, fill=(34, 211, 238))
    # name
    fn = font(BOLD, 112)
    d.text((x0 - 4, 140), 'Mehmet', font=fn, fill=(233, 238, 255))
    sev = text_gradient('Sevri', fn, [(0, (34, 211, 238)), (0.55, (129, 140, 248)), (1, (192, 132, 252))])
    base.alpha_composite(sev, (x0 - 8, 262))
    # title line
    ft = font(SEMI, 30)
    d.text((x0, 412), 'Dr. Öğr. Üyesi · Bilgisayar Mühendisliği · RTEÜ', font=ft, fill=(233, 238, 255))
    # chips
    fc = font(SEMI, 24)
    x = x0
    for label, col in (('AI', (34, 211, 238)), ('Cybersecurity', (129, 140, 248)), ('AISEC Lab', (52, 211, 153))):
        b = d.textbbox((0, 0), label, font=fc)
        w = b[2] - b[0] + 36
        d.rounded_rectangle([x, 470, x + w, 470 + 46], radius=14, fill=(7, 11, 22, 210), outline=col + (150,), width=2)
        d.text((x + 18, 470 + 23 - (b[1] + b[3]) / 2), label, font=fc, fill=(233, 238, 255))
        x += w + 12
    # footer url + monogram
    fu = font(MONO, 22)
    d.rounded_rectangle([x0, 548, x0 + 40, 588], radius=11, fill=(79, 70, 229))
    fm = font(BOLD, 18)
    mb = d.textbbox((0, 0), 'MS', font=fm)
    d.text((x0 + 20 - (mb[2] - mb[0]) / 2 - mb[0], 568 - (mb[1] + mb[3]) / 2), 'MS', font=fm, fill=(255, 255, 255))
    d.text((x0 + 54, 556), 'mehmetsevri.github.io', font=fu, fill=(152, 164, 200))
    base.convert('RGB').save(os.path.join(IMG, 'og-image.jpg'), quality=88, optimize=True, progressive=True)


if __name__ == '__main__':
    os.makedirs(IMG, exist_ok=True)
    favicon_svg()
    touch_icon()
    og_image()
    print('ok: favicon.svg, apple-touch-icon.png, og-image.jpg')
