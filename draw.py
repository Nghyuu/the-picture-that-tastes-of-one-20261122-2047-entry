"""Render a hero shot of a glistening honeycomb with dripping honey on dark slate.

Procedural Pillow render: warm directional light, amber hex cells with glossy
highlights, thick honey drips and a pooled honey puddle. No text anywhere.
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
random.seed(20261122)

img = Image.new("RGB", (W, H), (18, 16, 14))
d = ImageDraw.Draw(img, "RGBA")

# ---- dark slate background with warm radial glow behind the comb ----
cx, cy = 512, 500
for r in range(720, 0, -6):
    t = r / 720.0
    warm = (int(58 + 60 * (1 - t)), int(38 + 34 * (1 - t)), int(22 + 14 * (1 - t)))
    dark = (16, 14, 13)
    col = tuple(int(dark[i] + (warm[i] - dark[i]) * (1 - t) ** 2.2) for i in range(3))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

# slate slab: slightly lighter rounded rectangle, low in frame
d.rounded_rectangle([60, 640, 964, 1000], radius=28, fill=(34, 31, 29))
d.rounded_rectangle([60, 640, 964, 660], radius=14, fill=(52, 47, 42))
# slate speckle
for _ in range(2500):
    x = random.randint(60, 964); y = random.randint(640, 1000)
    v = random.randint(20, 70)
    d.point((x, y), fill=(v, v - 2, v - 4))

# ---- honeycomb: big hexagonal cells, two rows of comb, tilted slightly ----
def hex_points(cx, cy, s):
    return [(cx + s * math.cos(math.radians(60 * i - 30)),
             cy + s * math.sin(math.radians(60 * i - 30))) for i in range(6)]

comb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(comb)

S = 86  # cell radius
# honeycomb occupies a chunky slab, centre-left, tilted -8 degrees
cells = []
rows = 6
cols = 7
for row in range(rows):
    for col in range(cols):
        x = 250 + col * S * 1.52 + (row % 2) * S * 0.76
        y = 210 + row * S * 1.32
        # taper: skip corners for a chunky organic slab shape
        if (row == 0 and col in (0, 6)) or (row == 5 and col in (0, 6)):
            continue
        if (row == 0 and col in (1, 5)) and random.random() < 0.5:
            continue
        cells.append((x, y))

# rotate the whole comb layer -8 deg around centre
for (x, y) in cells:
    # depth: lower rows darker gold, upper rows catch the light
    depth = (y - 180) / 520.0
    base = (int(214 - 55 * depth), int(146 - 42 * depth), int(28 - 8 * depth))
    dark = (int(150 - 40 * depth), int(96 - 28 * depth), int(12))
    # cell wall: thick amber rim
    pts = hex_points(x, y, S)
    cd.polygon(pts, fill=base + (255,))
    inner = hex_points(x, y, S * 0.78)
    # cell interior: deep glossy honey, darker at bottom of each cell
    cd.polygon(inner, fill=(int(120 - 20 * depth), int(66 - 12 * depth), 8, 255))
    # honey surface glint: small bright ellipse upper-left of each cell
    gx, gy = x - S * 0.28, y - S * 0.30
    cd.ellipse([gx - 16, gy - 9, gx + 16, gy + 9], fill=(255, 214, 120, 210))
    cd.ellipse([gx - 7, gy - 4, gx + 7, gy + 4], fill=(255, 240, 190, 230))
    # lower rim shadow for depth
    cd.line([pts[2], pts[3], pts[4]], fill=dark + (255,), width=7)

# thick waxy top edge highlight along the comb's top cells
for (x, y) in cells:
    if y < 330:
        pts = hex_points(x, y, S)
        cd.line([pts[0], pts[1], pts[2]], fill=(255, 226, 140, 255), width=6)

comb = comb.rotate(-8, center=(512, 470), resample=Image.BICUBIC)
img = Image.alpha_composite(img.convert("RGBA"), comb)
d = ImageDraw.Draw(img, "RGBA")

# ---- honey drips falling from the comb onto the slate ----
drip_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(drip_layer)
drips = [(330, 700, 22, 130), (470, 730, 28, 110), (610, 720, 20, 120),
         (700, 680, 15, 100), (250, 660, 13, 110)]
for (x, y0, w, length) in drips:
    # glossy strand
    dd.rounded_rectangle([x - w // 2, y0, x + w // 2, y0 + length], radius=w // 2,
                         fill=(226, 158, 32, 255))
    dd.rounded_rectangle([x - w // 2 + 4, y0, x - w // 2 + 10, y0 + length],
                         radius=3, fill=(255, 214, 110, 255))
    # droplet at the bottom
    dd.ellipse([x - w, y0 + length - 6, x + w, y0 + length + w],
               fill=(232, 164, 34, 255))
    dd.ellipse([x - w // 2, y0 + length + 2, x - w // 6, y0 + length + w // 2],
               fill=(255, 226, 130, 255))
drip_layer = drip_layer.rotate(-8, center=(512, 470), resample=Image.BICUBIC)
img = Image.alpha_composite(img, drip_layer)
d = ImageDraw.Draw(img, "RGBA")

# ---- pooled honey puddle on the slate, glossy with highlight ----
# irregular blob, not a perfect disc
px, py = 512, 880
blob = []
for i in range(48):
    a = 2 * math.pi * i / 48
    r = 300 + 42 * math.sin(a * 3 + 0.7) + 26 * math.sin(a * 7 + 2.1)
    blob.append((px + r * math.cos(a), py + 58 * math.sin(a) * (1 + 0.12 * math.cos(a * 2))))
d.polygon(blob, fill=(196, 128, 22, 255))
blob2 = [(px + (x - px) * 0.88, py + (y - py) * 0.8) for (x, y) in blob]
d.polygon(blob2, fill=(216, 146, 28, 255))
blob3 = [(px + (x - px) * 0.72, py + (y - py) * 0.62) for (x, y) in blob]
d.polygon(blob3, fill=(232, 164, 36, 255))
# long warm highlight across the puddle
d.ellipse([px - 200, py - 26, px + 60, py + 6], fill=(255, 222, 130, 220))
d.ellipse([px - 120, py - 14, px + 20, py + 2], fill=(255, 244, 200, 240))
# a few small honey beads near the puddle
for (bx, by, br) in [(830, 830, 26), (880, 880, 18), (180, 860, 20), (150, 800, 13)]:
    d.ellipse([bx - br, by - br // 2, bx + br, by + br // 2], fill=(224, 156, 30, 255))
    d.ellipse([bx - br // 2, by - br // 3, bx - br // 6, by], fill=(255, 224, 130, 255))

# ---- warm light: soft glow top-right, gentle vignette ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([560, -260, 1180, 340], fill=(255, 190, 90, 60))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img = Image.alpha_composite(img, glow)

vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
vd.rectangle([0, 0, W, H], outline=(0, 0, 0, 110), width=90)
vig = vig.filter(ImageFilter.GaussianBlur(70))
img = Image.alpha_composite(img, vig)

# ---- fine grain so surfaces don't band ----
img = img.convert("RGB")
pxs = img.load()
for _ in range(9000):
    x = random.randint(0, W - 1); y = random.randint(0, H - 1)
    r, g, b = pxs[x, y]
    n = random.randint(-7, 7)
    pxs[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))

img.save("/tmp/entry_preview.png")
img.save("/home/hatch/workspace/makefun/the-picture-that-tastes-of-one-20261122-2047-build/entry.png",
         optimize=True)
print("saved")
