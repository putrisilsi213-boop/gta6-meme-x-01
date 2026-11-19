#!/usr/bin/env python3
"""Draw the GTA 6 meme for make.fun bounty gta6-meme-x-01, 100% with code.

Original joke: Rockstar delays GTA 6 yet again, while the poster's AI agent
didn't wait around - it already got paid on make.fun. The make.fun ghost
mascot (white ghost, sparkle eyes, magenta star coin) is worked into the
Vice City scene: it floats over the car, holding a bag of cash.

Output: meme.png, 1080x1080, flat colours so it stays sharp (and small)
when the judge shrinks it to 480x480.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), (10, 6, 24))
d = ImageDraw.Draw(img, "RGBA")

# ---------- sky gradient: dusk purple -> magenta -> orange ----------
stops = [(0, (24, 8, 54)), (0.35, (94, 22, 96)), (0.62, (214, 51, 108)),
         (0.78, (255, 122, 61)), (1.0, (255, 178, 92))]
horizon = 800  # where the bottom black band starts


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


for y in range(horizon):
    t = y / horizon
    for i in range(len(stops) - 1):
        if stops[i][0] <= t <= stops[i + 1][0]:
            f = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
            d.line([(0, y), (W, y)], fill=lerp(stops[i][1], stops[i + 1][1], f))
            break

# ---------- synthwave sun with slits ----------
sun_c = (540, 560)
sun_r = 210
d.ellipse([sun_c[0] - sun_r, sun_c[1] - sun_r, sun_c[0] + sun_r, sun_c[1] + sun_r],
          fill=(255, 214, 120))
gap = 6
y = sun_c[1] + 20
while y < sun_c[1] + sun_r:
    # sky-coloured slit, wider toward the bottom
    w = int(math.sqrt(max(0, sun_r ** 2 - (y - sun_c[1]) ** 2)))
    d.rectangle([sun_c[0] - w, y, sun_c[0] + w, y + gap], fill=(255, 122, 61))
    y += gap + 16
    gap += 3

# ---------- skyline silhouettes ----------
random.seed(6)
sil = (26, 8, 46)
x = -20
while x < W + 20:
    bw = random.randint(70, 150)
    bh = random.randint(90, 260)
    top = 640 - bh
    d.rectangle([x, top, x + bw, 660], fill=sil)
    # lit windows
    for wy in range(top + 14, 640, 26):
        for wx in range(x + 12, x + bw - 10, 24):
            if random.random() < 0.35:
                d.rectangle([wx, wy, wx + 9, wy + 12],
                            fill=(255, 196, 90) if random.random() < 0.7 else (120, 240, 255))
    x += bw + random.randint(4, 18)

# ---------- ocean strip ----------
for y in range(660, 730):
    t = (y - 660) / 70
    d.line([(0, y), (W, y)], fill=lerp((255, 122, 90), (32, 12, 66), t))
# sun reflection
for i, rw in enumerate([150, 110, 80, 55, 35]):
    yy = 668 + i * 12
    d.rectangle([540 - rw // 2, yy, 540 + rw // 2, yy + 5], fill=(255, 214, 120))

# ---------- road ----------
d.polygon([(0, 730), (W, 730), (W, 800), (0, 800)], fill=(16, 10, 30))
d.polygon([(0, 730), (W, 730), (W, 800), (0, 800)], outline=(255, 80, 160), width=3)
# centre dashes, receding toward the horizon
for i, w in enumerate([180, 130, 95, 65, 42]):
    yy = 792 - i * 12
    d.line([(540 - w // 2, yy), (540 + w // 2, yy)], fill=(255, 220, 130), width=3)


def bezier(p0, p1, p2, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def palm(cx, base, s):
    """One palm silhouette: curved trunk + drooping bezier fronds."""
    top = (cx + 26 * s, base - 215 * s)
    d.line(bezier((cx, base), (cx - 8 * s, base - 120 * s), top, 20),
           fill=sil, width=int(15 * s))
    for k in range(7):
        # fan from up-left around to up-right, tips drooping down
        ang = math.pi * (0.02 + 0.96 * k / 6)
        ex = top[0] + math.cos(ang) * 118 * s
        ey = top[1] + math.sin(ang) * 46 * s + 62 * s
        mx = top[0] + math.cos(ang) * 66 * s
        my = top[1] - 30 * s + math.sin(ang) * 10 * s
        d.line(bezier(top, (mx, my), (ex, ey), 20), fill=sil, width=int(11 * s))
    d.ellipse([top[0] - 11 * s, top[1] + 2, top[0] - 1 * s, top[1] + 12 * s], fill=sil)
    d.ellipse([top[0] + 1 * s, top[1] + 2, top[0] + 11 * s, top[1] + 12 * s], fill=sil)


palm(105, 738, 1.0)
palm(985, 742, 0.9)

# ---------- sports car (side profile, neon) ----------
car_y = 700  # wheels baseline
body = (255, 45, 120)
d.polygon([(180, 700), (200, 660), (330, 640), (520, 640), (640, 662),
           (830, 668), (880, 692), (860, 706), (180, 706)], fill=body)
d.polygon([(250, 662), (350, 644), (500, 644), (600, 664), (250, 664)],
          fill=(140, 240, 255))  # windshield / windows
d.line([(250, 664), (600, 664)], fill=(20, 8, 40), width=4)
# neon underglow
d.line([(190, 710), (860, 710)], fill=(255, 60, 180), width=6)
for wx in (300, 730):
    d.ellipse([wx - 42, 668, wx + 42, 752], fill=(12, 8, 20))
    d.ellipse([wx - 42, 668, wx + 42, 752], outline=(255, 220, 120), width=4)
    d.ellipse([wx - 16, 694, wx + 16, 726], fill=(200, 200, 210))
# headlight
d.polygon([(840, 676), (872, 682), (872, 692), (840, 690)], fill=(255, 244, 170))

# ---------- make.fun ghost, floating over the car, holding cash ----------
gx, gy, gs = 770, 330, 1.0  # ghost centre-top, scale
gw, gh = int(190 * gs), int(250 * gs)
# body: round top + wavy bottom
d.pieslice([gx - gw // 2, gy, gx + gw // 2, gy + gw], 180, 360, fill=(255, 255, 255))
d.rectangle([gx - gw // 2, gy + gw // 2, gx + gw // 2, gy + gh - 34], fill=(255, 255, 255))
waves = []
for i in range(5):
    waves.append((gx - gw // 2 + i * gw // 4, gy + gh - 34))
    waves.append((gx - gw // 2 + i * gw // 4 + gw // 8, gy + gh))
waves.append((gx + gw // 2, gy + gh - 34))
d.polygon(waves, fill=(255, 255, 255))
# sparkle eyes (black ovals + white star sparkles)
for ex in (gx - 42, gx + 42):
    d.ellipse([ex - 16, gy + 78, ex + 16, gy + 118], fill=(20, 10, 30))
    d.polygon([(ex, gy + 84), (ex + 5, gy + 95), (ex + 15, gy + 97),
               (ex + 6, gy + 104), (ex + 9, gy + 114), (ex, gy + 108),
               (ex - 9, gy + 114), (ex - 6, gy + 104), (ex - 15, gy + 97),
               (ex - 5, gy + 95)], fill=(255, 255, 255))
# smile
d.arc([gx - 26, gy + 118, gx + 26, gy + 158], 20, 160, fill=(20, 10, 30), width=6)
# little arm waving
d.line([(gx - gw // 2 + 6, gy + 150), (gx - gw // 2 - 34, gy + 118)],
       fill=(255, 255, 255), width=16)
# money bag in the other hand
bx, by = gx + gw // 2 - 6, gy + 150
d.polygon([(bx - 14, by - 26), (bx + 14, by - 26), (bx + 8, by - 40),
           (bx - 8, by - 40)], fill=(34, 139, 80))  # tied top
d.ellipse([bx - 44, by - 26, bx + 44, by + 52], fill=(46, 160, 90))
d.ellipse([bx - 44, by - 26, bx + 44, by + 52], outline=(24, 110, 62), width=4)
d.text((bx, by + 4), "$", font=ImageFont.truetype(BOLD, 44),
       fill=(255, 255, 255), anchor="mm")
# magenta star coin
sx, sy, sr = gx - gw // 2 - 78, gy + 30, 34
star = []
for i in range(10):
    ang = -math.pi / 2 + i * math.pi / 5
    r = sr if i % 2 == 0 else sr * 0.45
    star.append((sx + r * math.cos(ang), sy + r * math.sin(ang)))
d.polygon(star, fill=(235, 0, 139))
d.polygon(star, outline=(255, 255, 255), width=3)
d.text((sx, sy - 2), "$", font=ImageFont.truetype(BOLD, 34),
       fill=(255, 255, 255), anchor="mm")

# ---------- top meme text ----------
def text_center(y, s, size, fill=(255, 255, 255)):
    f = ImageFont.truetype(BOLD, size)
    d.text((W // 2, y), s, font=f, fill=fill, anchor="ma",
           stroke_width=8, stroke_fill=(0, 0, 0))


text_center(18, "GTA 6", 168)
text_center(196, "DELAYED AGAIN", 84)

# ---------- bottom band ----------
d.rectangle([0, 800, W, H], fill=(8, 5, 18))
d.line([(0, 800), (W, 800)], fill=(235, 0, 139), width=6)


def band_text(y, s, size, fill=(255, 255, 255)):
    f = ImageFont.truetype(BOLD, size)
    d.text((W // 2, y), s, font=f, fill=fill, anchor="ma")


band_text(824, "MEANWHILE, MY AGENT", 62)
band_text(896, "ALREADY GOT PAID ON", 62)
band_text(968, "make.fun", 92, fill=(255, 60, 170))

img.save("meme.png", optimize=True)
print("saved meme.png", img.size)
