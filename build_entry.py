#!/usr/bin/env python3
"""Build the 20 November 2026 front page for make.fun news-image-20261120.

Draws the whole page from code with Pillow (local build tool only -- the
entry program main.py is stdlib-only and merely copies the finished
entry.png). Flat 2D vector newspaper front page: masthead, stats strip,
region tabs, 13 illustrated panels, big numbered world map, numbered
ALSO ON list with a source per item, DATE CHECK footer.

Run:  python3 build_entry.py   (writes entry.png next to this file)
"""

import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 241, 227)
PAPER = (251, 248, 239)
INK = (25, 25, 25)
NAVY = (20, 38, 62)
NAVY2 = (30, 58, 92)
RED = (179, 39, 30)
RED_D = (140, 28, 22)
TEAL = (14, 124, 123)
TEAL_D = (10, 92, 92)
GOLD = (201, 162, 39)
SAND = (217, 201, 163)
SAND_D = (198, 178, 130)
SKY = (127, 179, 213)
SKY_D = (90, 140, 175)
GREY = (107, 107, 107)
LINE = (216, 205, 180)
GREEN = (46, 125, 50)
ORANGE = (214, 106, 28)
PURPLE = (106, 76, 147)

FDIR = "/usr/share/fonts/truetype/"
SERIF_BLACK = FDIR + "noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = FDIR + "noto/NotoSerif-Bold.ttf"
SERIF = FDIR + "noto/NotoSerif-Regular.ttf"
SERIF_IT = FDIR + "noto/NotoSerif-Italic.ttf"
SANS = FDIR + "liberation/LiberationSans-Regular.ttf"
SANS_B = FDIR + "liberation/LiberationSans-Bold.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, font, maxw):
    """Greedy word wrap returning a list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, xy, lines, font, fill, spacing=2, align="left", width=None):
    """Draw stacked lines; returns y after the last line."""
    x, y = xy
    for ln in lines:
        if align == "center" and width is not None:
            draw.text((x + width / 2, y), ln, font=font, fill=fill, anchor="ma")
        else:
            draw.text((x, y), ln, font=font, fill=fill)
        y += font.size + spacing
    return y


def band(draw, box, fill, text, font, tfill=(255, 255, 255), pad=4):
    """Solid band with centred white text."""
    draw.rectangle(box, fill=fill)
    cx = (box[0] + box[2]) / 2
    cy = (box[1] + box[3]) / 2
    draw.text((cx, cy), text, font=font, fill=tfill, anchor="mm")


def tagline(draw, x, y, num, place, cat, font_num, font_rest, maxw):
    """'01 · ODISHA, INDIA · CYCLONE' style line with red number."""
    draw.text((x, y), f"{num:02d}", font=font_num, fill=RED)
    nx = x + draw.textlength(f"{num:02d}", font=font_num) + 4
    draw.text((nx, y), f"· {place} · {cat}", font=font_rest, fill=INK)


# ---------------------------------------------------------------- scenes
# Every scene draws inside box (x0, y0, x1, y1) only.

def scene_cyclone(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(232, 214, 170))                       # land (top-left)
    d.polygon([(x0, y0), (x0 + 130, y0), (x0 + 95, y1), (x0, y1)], fill=(214, 190, 140))
    d.rectangle([x0, y0 + 62, x1, y1], fill=(23, 68, 92))     # Bay of Bengal
    d.rectangle([x0, y0 + 62, x1, y0 + 66], fill=(120, 170, 190))
    # spiral
    cx, cy = x0 + 195, y0 + 62
    for r, col, wd in ((58, (255, 255, 255), 5), (44, (255, 255, 255), 5),
                       (30, (255, 255, 255), 5), (16, (255, 255, 255), 5)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=200 + 300, fill=col, width=wd)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    d.ellipse([cx - 110, cy - 4, cx - 102, cy + 4], fill=RED)  # Gopalpur dot
    d.line([cx - 106, cy, cx - 14, cy], fill=RED, width=2)
    f = F(SANS_B, 11)
    d.text((x0 + 8, y0 + 6), "ODISHA", font=f, fill=(90, 60, 20))
    d.text((x0 + 8, y0 + 20), "INDIA", font=F(SANS, 10), fill=(90, 60, 20))
    d.text((x0 + 8, y0 + 40), "Gopalpur", font=F(SERIF_IT, 11), fill=(90, 60, 20))
    d.text((x1 - 8, y1 - 16), "BAY OF BENGAL", font=F(SANS_B, 10), fill=(180, 210, 225), anchor="ra")
    band(d, [x0, y1 - 18, x1, y1], NAVY, "LANDFALL  •  GUSTS 110 KM/H",
         F(SANS_B, 10))
    d.text((x1 - 6, y0 + 4), "CYCLONE AKVAN", font=F(SANS_B, 10), fill=(255, 220, 120), anchor="ra")


def scene_kyiv(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(13, 24, 46))
    # stars
    for sx, sy in ((30, 12), (90, 22), (150, 8), (210, 18), (260, 10), (60, 34), (180, 30)):
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=(255, 255, 255))
    # missile trails
    for (sx, sy, ex, ey) in ((40, 8, 120, 55), (120, 4, 200, 50), (210, 6, 280, 48)):
        d.arc([x0 + sx - 70, y0 + sy - 60, x0 + ex + 40, y0 + ey + 30],
              start=300, end=30, fill=(255, 170, 60), width=3)
        d.ellipse([x0 + ex - 3, y0 + ey - 3, x0 + ex + 3, y0 + ey + 3], fill=(255, 200, 90))
    # skyline
    base = y1 - 18
    for bx, bw, bh in ((0, 34, 26), (36, 26, 40), (64, 30, 22), (96, 22, 48),
                       (120, 34, 30), (156, 26, 44), (184, 30, 24), (216, 28, 38),
                       (246, 30, 26), (278, 39, 34)):
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(5, 12, 26))
    # fires
    for fx in (48, 130, 232):
        d.polygon([(x0 + fx, base), (x0 + fx + 5, base - 14), (x0 + fx + 10, base)],
                  fill=(255, 150, 40))
        d.polygon([(x0 + fx + 2, base), (x0 + fx + 5, base - 8), (x0 + fx + 8, base)],
                  fill=(255, 220, 90))
    band(d, [x0, y1 - 18, x1, y1], (0, 0, 0), "01:25 LOCAL  •  3 BRIDGES HIT",
         F(SANS_B, 10))
    d.text((x1 - 6, y0 + 4), "~30 MISSILES", font=F(SANS_B, 10), fill=(255, 120, 100), anchor="ra")


def scene_cop(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=TEAL_D)
    # globe
    cx, cy, r = x0 + 62, y0 + 52, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 160, 200))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.polygon([(cx - 26, cy - 18), (cx - 8, cy - 26), (cx + 6, cy - 12), (cx - 4, cy + 2),
               (cx - 24, cy + 2)], fill=(120, 200, 120))
    d.polygon([(cx + 4, cy + 8), (cx + 22, cy + 2), (cx + 28, cy + 18), (cx + 10, cy + 26),
               (cx + 2, cy + 16)], fill=(120, 200, 120))
    d.arc([cx - r, cy - r, cx + r, cy + r], start=90, end=270, fill=(255, 255, 255), width=1)
    # thermometer
    tx = x0 + 150
    d.rounded_rectangle([tx, y0 + 8, tx + 16, y1 - 26], radius=8, fill=(255, 255, 255))
    d.rectangle([tx + 3, y0 + 14, tx + 13, y1 - 40], fill=RED)
    d.ellipse([tx - 6, y1 - 40, tx + 22, y1 - 12], fill=RED)
    d.ellipse([tx - 6, y1 - 40, tx + 22, y1 - 12], outline=(255, 255, 255), width=2)
    # COP31 box
    d.rectangle([x1 - 118, y0 + 6, x1 - 8, y0 + 46], fill=(255, 255, 255))
    d.text((x1 - 63, y0 + 10), "COP31", font=F(SANS_B, 17), fill=RED_D, anchor="ma")
    d.text((x1 - 63, y0 + 30), "ANTALYA  •  NOV 20", font=F(SANS_B, 9), fill=INK, anchor="ma")
    band(d, [x0, y1 - 18, x1, y1], RED_D, "FINAL DAY  •  DEADLOCK", F(SANS_B, 10))
    d.text((x1 - 8, y1 - 34), "$120BN FINANCE GAP", font=F(SANS_B, 10),
           fill=(255, 220, 120), anchor="ra")


def scene_markets(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(16, 16, 20))
    # falling chart (left half only; labels live on the right)
    pts = [(x0 + 12 + i * 12, y0 + 24 + (i * i) * 0.7 + i * 2) for i in range(7)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(255, 70, 60), width=3)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(255, 255, 255))
    d.text((x0 + 10, y0 + 6), "ASIA  −7% WK", font=F(SANS_B, 11), fill=(255, 255, 255))
    f = F(SANS_B, 11)
    for i, (lbl, val) in enumerate((("NIKKEI", "−4.5%"), ("KOSPI", "−4.7%"),
                                    ("SOFTBANK", "−16%"))):
        yy = y0 + 52 + i * 15
        d.text((x1 - 84, yy), lbl, font=f, fill=(200, 200, 200))
        d.text((x1 - 8, yy), val, font=f, fill=(255, 90, 80), anchor="ra")
    band(d, [x0, y1 - 18, x1, y1], RED, "WORST WEEK SINCE 2020", F(SANS_B, 10))


def scene_mercury(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(12, 16, 34))
    for sx, sy in ((16, 10), (60, 20), (120, 8), (170, 16), (30, 40), (150, 34)):
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=(255, 255, 255))
    # dotted trajectory
    for i in range(9):
        px = x0 + 14 + i * 12
        py = y0 + 78 - i * 5
        d.ellipse([px, py, px + 3, py + 3], fill=(255, 220, 120))
    # spacecraft
    d.polygon([(x0 + 118, y0 + 30), (x0 + 138, y0 + 24), (x0 + 138, y0 + 36)],
              fill=(255, 220, 120))
    d.rectangle([x0 + 104, y0 + 26, x0 + 118, y0 + 34], fill=(200, 200, 200))
    # Mercury
    cx, cy, r = x0 + 148, y0 + 58, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 160, 148))
    for ox, oy, orad in ((-12, -8, 6), (8, 4, 8), (-4, 12, 5), (12, -12, 4)):
        d.ellipse([cx + ox - orad, cy + oy - orad, cx + ox + orad, cy + oy + orad],
                  fill=(140, 132, 120))
    d.text((x0 + 8, y0 + 6), "6BN MILES", font=F(SANS_B, 11), fill=(255, 220, 120))
    band(d, [x0, y1 - 18, x1, y1], NAVY2, "ORBIT INSERTION SATURDAY", F(SANS_B, 10))


def scene_euuk(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(24, 44, 84))
    # EU flag
    d.rectangle([x0 + 10, y0 + 10, x0 + 82, y0 + 62], fill=(0, 51, 153))
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = x0 + 46 + 22 * math.cos(a)
        sy = y0 + 36 + 20 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    # UK flag (simplified)
    d.rectangle([x0 + 96, y0 + 10, x0 + 168, y0 + 62], fill=(1, 33, 105))
    d.line([x0 + 96, y0 + 10, x0 + 168, y0 + 62], fill=(255, 255, 255), width=8)
    d.line([x0 + 168, y0 + 10, x0 + 96, y0 + 62], fill=(255, 255, 255), width=8)
    d.line([x0 + 132, y0 + 10, x0 + 132, y0 + 62], fill=(255, 255, 255), width=12)
    d.line([x0 + 96, y0 + 36, x0 + 168, y0 + 36], fill=(255, 255, 255), width=12)
    d.line([x0 + 132, y0 + 10, x0 + 132, y0 + 62], fill=(200, 16, 46), width=6)
    d.line([x0 + 96, y0 + 36, x0 + 168, y0 + 36], fill=(200, 16, 46), width=6)
    d.text((x0 + 8, y0 + 70), "BRUSSELS", font=F(SANS_B, 10), fill=(255, 255, 255))
    band(d, [x0, y1 - 18, x1, y1], (0, 51, 153), "RESET TALKS", F(SANS_B, 10))


def scene_cpi(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=PAPER)
    bars = [(1.6, "JUL"), (1.8, "AUG"), (2.1, "SEP"), (2.3, "OCT")]
    bw, gap = 30, 14
    for i, (v, lbl) in enumerate(bars):
        bx = x0 + 14 + i * (bw + gap)
        bh = int(v * 22)
        col = RED if i == 3 else (200, 120, 110)
        d.rectangle([bx, y1 - 22 - bh, bx + bw, y1 - 22], fill=col)
        d.text((bx + bw / 2, y1 - 20), lbl, font=F(SANS_B, 9), fill=INK, anchor="ma")
    d.text((x1 - 8, y0 + 4), "2% TARGET", font=F(SANS_B, 10), fill=GREY, anchor="ra")
    d.text((x0 + 8, y0 + 4), "CPI 2.3%", font=F(SANS_B, 12), fill=RED_D)
    band(d, [x0, y1 - 18, x1, y1], NAVY, "BOJ HIKE EYED", F(SANS_B, 10))


def scene_rates(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(24, 24, 30))
    d.text((x0 + 8, y0 + 6), "3.50%  5Y", font=F(SANS_B, 12), fill=(255, 200, 90))
    d.rectangle([x0 + 8, y0 + 26, x1 - 8, y0 + 38], fill=(60, 60, 70))
    d.rectangle([x0 + 8, y0 + 26, x0 + 8 + 150, y0 + 38], fill=RED)
    d.text((x0 + 8, y0 + 44), "3.00%  1Y", font=F(SANS_B, 12), fill=(255, 200, 90))
    d.rectangle([x0 + 8, y0 + 64, x1 - 8, y0 + 76], fill=(60, 60, 70))
    d.rectangle([x0 + 8, y0 + 64, x0 + 8 + 128, y0 + 76], fill=TEAL)
    band(d, [x0, y1 - 18, x1, y1], (60, 60, 70), "18 MO UNCHANGED", F(SANS_B, 10))


def scene_cricket(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(46, 125, 50))
    d.rectangle([x0, y0 + 58, x1, y1], fill=(120, 170, 90))     # outfield
    d.rectangle([x0 + 60, y0 + 58, x0 + 130, y1], fill=(214, 190, 140))  # pitch
    for yy in range(y0 + 62, y1, 8):
        d.line([x0 + 60, yy, x0 + 130, yy], fill=(190, 165, 115), width=1)
    # stumps
    for sx in (78, 84, 90):
        d.line([x0 + sx, y1 - 30, x0 + sx, y1 - 20], fill=(255, 240, 180), width=3)
    # batsman
    d.ellipse([x0 + 108, y0 + 52, x0 + 120, y0 + 64], fill=(30, 30, 30))
    d.line([x0 + 114, y0 + 64, x0 + 112, y0 + 82], fill=(30, 30, 30), width=5)
    d.line([x0 + 112, y0 + 82, x0 + 106, y1 - 4], fill=(30, 30, 30), width=4)
    d.line([x0 + 112, y0 + 82, x0 + 120, y1 - 4], fill=(30, 30, 30), width=4)
    d.line([x0 + 114, y0 + 68, x0 + 128, y0 + 78], fill=(30, 30, 30), width=4)
    d.line([x0 + 128, y0 + 78, x0 + 140, y0 + 88], fill=(210, 180, 120), width=4)
    d.ellipse([x0 + 148, y0 + 84, x0 + 154, y0 + 90], fill=RED)  # ball
    d.rectangle([x0 + 8, y0 + 6, x0 + 62, y0 + 26], fill=(255, 255, 255))
    d.text((x0 + 35, y0 + 8), "118", font=F(SANS_B, 14), fill=RED_D, anchor="ma")
    d.text((x0 + 35, y0 + 24), "RECORD", font=F(SANS_B, 8), fill=INK, anchor="ma")
    band(d, [x0, y1 - 18, x1, y1], (30, 90, 40), "FIRST NZ TON IN ALL 3 FORMATS",
         F(SANS_B, 9))


def scene_bukele(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(30, 90, 168))
    d.text((x0 + 8, y0 + 6), "2027", font=F(SANS_B, 13), fill=(255, 255, 255))
    # ballot box
    d.rectangle([x0 + 58, y0 + 30, x0 + 130, y0 + 84], fill=(255, 255, 255))
    d.rectangle([x0 + 52, y0 + 24, x0 + 136, y0 + 34], fill=(220, 220, 220))
    d.rectangle([x0 + 84, y0 + 28, x0 + 104, y0 + 31], fill=(30, 30, 30))
    d.line([x0 + 70, y0 + 58, x0 + 82, y0 + 72], fill=TEAL, width=5)
    d.line([x0 + 82, y0 + 72, x0 + 116, y0 + 40], fill=TEAL, width=5)
    # ballot paper
    d.polygon([(x0 + 140, y0 + 12), (x0 + 168, y0 + 20), (x0 + 160, y0 + 44),
               (x0 + 134, y0 + 36)], fill=(255, 255, 255))
    band(d, [x0, y1 - 18, x1, y1], NAVY, "THIRD TERM", F(SANS_B, 10))


def scene_boat(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(120, 180, 210))
    d.rectangle([x0, y0, x1, y0 + 26], fill=(250, 240, 210))
    d.text((x0 + 8, y0 + 5), "YENNE COAST", font=F(SANS_B, 10), fill=(120, 80, 20))
    # sea
    d.rectangle([x0, y0 + 26, x1, y1], fill=(24, 90, 130))
    for wy in (44, 60, 76):
        for wx in range(0, 190, 26):
            d.arc([x0 + wx, y0 + wy, x0 + wx + 24, y0 + wy + 12], start=180, end=360,
                  fill=(180, 220, 240), width=2)
    # boat
    d.polygon([(x0 + 55, y0 + 52), (x0 + 135, y0 + 52), (x0 + 120, y0 + 68),
               (x0 + 70, y0 + 68)], fill=(120, 60, 30))
    d.line([x0 + 95, y0 + 52, x0 + 95, y0 + 30], fill=(60, 40, 20), width=3)
    d.polygon([(x0 + 95, y0 + 30), (x0 + 95, y0 + 50), (x0 + 118, y0 + 50)],
              fill=(255, 255, 255))
    # lifebuoy
    d.ellipse([x0 + 150, y0 + 56, x0 + 172, y0 + 78], fill=(255, 255, 255))
    d.ellipse([x0 + 157, y0 + 63, x0 + 165, y0 + 71], fill=(24, 90, 130))
    band(d, [x0, y1 - 18, x1, y1], (10, 60, 90), "4 DEAD  •  DOZENS MISSING",
         F(SANS_B, 10))


def scene_strike(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(20, 20, 24))
    # Italian flag
    d.rectangle([x0 + 10, y0 + 8, x0 + 34, y0 + 40], fill=(0, 140, 70))
    d.rectangle([x0 + 34, y0 + 8, x0 + 58, y0 + 40], fill=(255, 255, 255))
    d.rectangle([x0 + 58, y0 + 8, x0 + 82, y0 + 40], fill=(205, 35, 40))
    d.text((x0 + 92, y0 + 10), "SCIOPERO", font=F(SANS_B, 16), fill=(255, 255, 255))
    # placards
    for i, px in enumerate((16, 66, 116, 156)):
        d.rectangle([x0 + px, y0 + 52, x0 + px + 26, y0 + 74], fill=(255, 255, 255))
        d.line([x0 + px + 13, y0 + 74, x0 + px + 13, y0 + 88], fill=(200, 200, 200), width=3)
    d.text((x0 + 92, y0 + 30), "100 SQUARES", font=F(SANS_B, 10), fill=(255, 220, 120))
    band(d, [x0, y1 - 18, x1, y1], RED, "24-HR GENERAL STRIKE", F(SANS_B, 10))


def scene_pill(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(10, 70, 80))
    # cells
    for cx, cy, r in ((28, 26, 9), (160, 20, 7), (170, 60, 9), (20, 66, 7), (90, 14, 5)):
        d.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r],
                  outline=(120, 200, 200), width=2)
        d.ellipse([x0 + cx - 2, y0 + cy - 2, x0 + cx + 2, y0 + cy + 2],
                  fill=(120, 200, 200))
    # capsule
    d.rounded_rectangle([x0 + 30, y0 + 34, x0 + 160, y0 + 62], radius=14, fill=(255, 255, 255))
    d.rounded_rectangle([x0 + 30, y0 + 34, x0 + 95, y0 + 62], radius=14, fill=RED)
    d.text((x0 + 95, y0 + 42), "DARAXONRASIB", font=F(SANS_B, 8), fill=INK, anchor="ma")
    band(d, [x0, y1 - 18, x1, y1], TEAL, "TUMOURS SHRINK IN EARLY TRIAL",
         F(SANS_B, 10))


# ---------------------------------------------------------------- world map
# Rough continent polygons in (lon, lat); drawn equirectangular.

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80), (-75, 72),
     (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 25), (-85, 30), (-90, 21),
     (-95, 16), (-100, 20), (-105, 22), (-115, 30), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-60, 74)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20), (-48, -28),
     (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -20), (-77, -12), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 58), (28, 60), (30, 62), (28, 66), (20, 70), (12, 70), (5, 60),
     (-5, 58), (-10, 54), (-10, 43)],
    [(-17, 15), (-15, 25), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (38, 22), (43, 12), (48, 11), (51, 10), (45, 0), (40, -10),
     (36, -18), (32, -26), (28, -33), (20, -35), (15, -27), (12, -18), (13, -10),
     (9, 4), (0, 6), (-8, 5), (-15, 10)],
    [(30, 36), (36, 36), (42, 41), (48, 38), (54, 37), (58, 26), (60, 25), (66, 25),
     (72, 20), (76, 10), (80, 8), (85, 20), (89, 22), (92, 16), (95, 16), (100, 8),
     (103, 2), (105, 10), (108, 12), (109, 18), (114, 22), (120, 28), (122, 32),
     (127, 35), (130, 38), (135, 43), (140, 45), (142, 50), (140, 55), (135, 60),
     (130, 65), (125, 70), (120, 73), (110, 74), (100, 76), (90, 75), (80, 73),
     (70, 72), (60, 69), (50, 68), (40, 68), (32, 66), (30, 62), (28, 55),
     (30, 50), (35, 45), (30, 40)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]

PINS = [  # (number, lat, lon)
    (1, 19.3, 84.9), (2, 50.4, 30.5), (3, 36.9, 30.7), (4, 37.5, 127.0),
    (6, 50.8, 4.4), (7, 35.7, 139.7), (8, 39.9, 116.4), (9, -41.3, 174.8),
    (10, 13.7, -89.2), (11, 14.7, -17.4), (12, 41.9, 12.5), (13, 41.4, 2.2),
]


def draw_map(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=NAVY)
    mx0, my0, mx1, my1 = x0 + 4, y0 + 4, x1 - 4, y1 - 26
    mw, mh = mx1 - mx0, my1 - my0

    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw, my0 + (90 - lat) / 180 * mh)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=SAND)
    # equator + graticule hint
    d.line([mx0, my0 + mh / 2, mx1, my0 + mh / 2], fill=(60, 90, 130), width=1)
    f = F(SANS_B, 9)
    for num, lat, lon in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), str(num), font=F(SANS_B, 8), fill=(255, 255, 255), anchor="mm")
    # space badge (Mercury, panel 5)
    d.ellipse([x0 + 10, y1 - 22, x0 + 26, y1 - 6], fill=RED, outline=(255, 255, 255), width=1)
    d.text((x0 + 18, y1 - 14), "5", font=f, fill=(255, 255, 255), anchor="mm")
    d.text((x0 + 30, y1 - 20), "SPACE", font=F(SANS_B, 8), fill=(255, 255, 255))
    d.text((x0 + 30, y1 - 11), "Mercury", font=F(SANS, 8), fill=(200, 210, 225))
    d.text((x1 - 6, y1 - 20), "1–3 Lead  •  4–13 Feature Stories",
           font=F(SANS, 8), fill=(200, 210, 225), anchor="ra")
    d.text((x1 - 6, y1 - 11), "Pins 1–13 mark the drawn stories",
           font=F(SANS, 8), fill=(200, 210, 225), anchor="ra")


# ---------------------------------------------------------------- data
# 13 drawn panels: (scene, place, category, headline, deck, source)

PANELS_WIDE = [
    (scene_cyclone, "ODISHA, INDIA", "CYCLONE",
     "Cyclone Akvan makes landfall in eastern India",
     "Severe storm crosses near Gopalpur; 300,000+ evacuated, winds gusting "
     "110 km/h, 423 rescue teams deployed.",
     "IMD, The Hindu"),
    (scene_kyiv, "KYIV, UKRAINE", "WAR",
     "Russia's barrage hits Kyiv bridges; at least 8 dead",
     "Overnight waves hit energy and transport sites; three bridges struck, "
     "embassies damaged.",
     "Kyiv Post, Reuters"),
    (scene_cop, "ANTALYA, TÜRKİYE", "CLIMATE",
     "COP31 reaches its final day deadlocked",
     "Draft omits fossil-fuel phase-out; $120bn adaptation finance "
     "unresolved; hosts push clean-power goal.",
     "UN News, Reuters"),
]

PANELS_SMALL = [
    (scene_markets, "SEOUL / TOKYO", "MARKETS",
     "AI sell-off sinks Asia to worst week since 2020",
     "Nikkei −4.5%, KOSPI −4.7%, SoftBank −16%; MSCI Asia down 7%.",
     "Reuters"),
    (scene_mercury, "MERCURY", "SPACE",
     "BepiColombo reaches Mercury after 8 years",
     "ESA/JAXA probe ends 6bn-mile trip; orbit insertion set for Saturday.",
     "ESA, BBC"),
    (scene_euuk, "BRUSSELS", "EUROPE",
     "Burnham holds first EU–UK reset summit",
     "Costa & von der Leyen host UK PM; agrifood & carbon-market links eyed.",
     "EU Council"),
    (scene_cpi, "TOKYO", "ECONOMY",
     "Japan inflation hits 2.3%; BoJ hike eyed",
     "Oct headline CPI rises from 2.1%; core stays above 2% for second month.",
     "Reuters"),
    (scene_rates, "BEIJING", "RATES",
     "China holds lending rates for 18th month",
     "1-year LPR stays at 3.0%, 5-year at 3.5% as expected.",
     "PBOC, Reuters"),
    (scene_cricket, "WELLINGTON", "CRICKET",
     "Phillips makes history with 118 vs India",
     "First NZ batter with centuries in all 3 formats; NZ post 368.",
     "ICC, AP"),
    (scene_bukele, "SAN SALVADOR", "POLITICS",
     "Bukele registers for third-term bid",
     "Files with electoral tribunal for Feb 2027 vote; rights groups object.",
     "AP"),
    (scene_boat, "SENEGAL", "MIGRATION",
     "Migrant boat capsizes off Senegal; 4 dead",
     "Dozens missing from ~50–100 aboard as Canary arrivals surge.",
     "Al Jazeera"),
    (scene_strike, "ROME", "LABOUR",
     "Italy's CGIL holds 24-hr general strike",
     "Unions rally across ~100 squares against 2027 budget; transit hit.",
     "CGIL, AFP"),
    (scene_pill, "BARCELONA", "HEALTH",
     "Pancreatic cancer pill shrinks tumours",
     "Daraxonrasib + chemo beats chemo alone in early trial.",
     "Reuters"),
]

# ALSO ON items 14–36: (place, headline, source) — one line each.
ALSO_ON = [
    ("BRAZIL", "Lula meets Chief Raoni as Indigenous land is recognised", "Al Jazeera"),
    ("SEOUL", "Ruling party moves to impeach Chief Justice Cho Hee-dae", "SBS"),
    ("BOUGAINVILLE", "Rio Tinto pledges $370m for Panguna mine legacy", "Reuters"),
    ("CANBERRA", "CBO warns AUKUS sub sales could shrink US fleet", "Reuters"),
    ("FLORIDA", "St. Johns River hits record 18.3 ft; schools shut", "AP"),
    ("IOWA", "US Army sets noon detonation of 68 unstable barrels", "AP"),
    ("TONGA", "Pacific kingdom declares emergency as drought bites", "RNZ"),
    ("WASHINGTON", "Pentagon puts US war cost vs Iran at $34.8bn", "Reuters"),
    ("LONDON", "UK & Norway fund £100m+ for two Ukrainian vessels", "BBC"),
    ("COPENHAGEN", "Denmark approves Greenland defence bill", "AFP"),
    ("JAKARTA", "Indonesia passes asset-forfeiture bill", "Reuters"),
    ("GLOBAL", "UN marks World Children's Day across states", "UN News"),
    ("CINCINNATI", "Zoo's famed hippo Fiona dies after swallowing hat", "AP"),
    ("SENEGAL", "President Faye enacts supplementary budget", "AFP"),
    ("HORMUZ", "Four attacks on vessels in 96 hours, centre says", "UKMTO"),
    ("NEW DELHI", "Pakistan minister to lead SCO dialogue delegation", "The Hindu"),
    ("QATAR", "U17 World Cup: Austria stun Argentina 2–0", "FIFA"),
    ("PORT-AU-PRINCE", "Police say raid killed 34 gang suspects", "AP"),
    ("WARSAW", "Missile crash 'likely intentional provocation': PM", "AP"),
    ("TAIWAN", "Short-sell curbs take effect; bombers tracked", "Reuters"),
    ("TURIN", "Alcaraz–Cobolli close ATP Finals groups", "ATP"),
    ("LOS ANGELES", "Thomas Markle ruled fit to stand trial", "BBC"),
    ("WELLINGTON", "Nicholls' 175* lifts NZ to 368 vs India", "ICC"),
]

STATS = [
    ("300,000+", "evacuated before Cyclone Akvan"),
    ("8", "killed in the Kyiv barrage"),
    ("-7%", "Asia shares' worst week"),
    ("2.3%", "Japan Oct CPI; BoJ eyed"),
    ("118", "Phillips' century vs India"),
    ("8 yrs", "BepiColombo at Mercury"),
]

TABS = [("EUROPE", 8, NAVY), ("AMERICAS", 8, RED), ("ASIA-PACIFIC", 8, TEAL),
        ("MIDEAST", 3, ORANGE), ("AFRICA", 2, GREEN), ("OCEANIA", 5, PURPLE),
        ("WORLD", 2, (90, 90, 90))]


# ---------------------------------------------------------------- panels

def draw_panel(img, d, box, num, scene, place, cat, headline, deck, source,
               ill_h, hl_size, deck_size):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PAPER, outline=(200, 190, 165))
    # draw the scene on its own tile so nothing can spill past the frame
    ill_w = x1 - x0 - 2
    tile = Image.new("RGB", (ill_w, ill_h), PAPER)
    scene(ImageDraw.Draw(tile), [0, 0, ill_w, ill_h])
    img.paste(tile, (x0 + 1, y0 + 1))
    ty = y0 + ill_h + 5
    tagline(d, x0 + 6, ty, num, place, cat, F(SANS_B, 10), F(SANS_B, 10),
            x1 - x0 - 12)
    hy = ty + 15
    hl = wrap(d, headline, F(SERIF_BOLD, hl_size), x1 - x0 - 12)
    hy = text_lines(d, (x0 + 6, hy), hl, F(SERIF_BOLD, hl_size), INK, spacing=1)
    dk = wrap(d, deck, F(SANS, deck_size), x1 - x0 - 12)
    text_lines(d, (x0 + 6, hy + 2), dk, F(SANS, deck_size), (60, 60, 60), spacing=1)
    d.text((x0 + 6, y1 - 15), f"({source})", font=F(SERIF_IT, 9), fill=GREY)


def draw_also_on(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=PAPER, outline=(200, 190, 165))
    d.rectangle([x0, y0, x1, y0 + 22], fill=NAVY)
    d.text((x0 + 8, y0 + 4), "ALSO ON FRIDAY 20 NOVEMBER  —  23 MORE STORIES",
           font=F(SANS_B, 11), fill=(255, 255, 255))
    d.text((x1 - 8, y0 + 5), "World Briefs (14–36)", font=F(SERIF_IT, 10),
           fill=(220, 220, 220), anchor="ra")
    col_w = (x1 - x0 - 16) // 2
    f_num = F(SANS_B, 10)
    f_txt = F(SANS, 10)
    f_src = F(SERIF_IT, 9)
    row_h = 11
    for i, (place, head, src) in enumerate(ALSO_ON):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        cx = x0 + 8 + col * (col_w + 8)
        cy = y0 + 27 + row * row_h
        num = 14 + i
        d.text((cx, cy), f"{num}", font=f_num, fill=RED)
        tx = cx + 20
        d.text((tx, cy), place + "  ", font=f_num, fill=INK)
        hx = tx + d.textlength(place + "  ", font=f_num)
        # shorten headline until it fits with the source
        avail = (x0 + 8 + col * (col_w + 8) + col_w) - hx
        h = head
        while h and d.textlength(h + f"  ({src})", font=f_txt) > avail:
            h = h.rsplit(" ", 1)[0] if " " in h else h[:-1]
        d.text((hx, cy), h, font=f_txt, fill=INK)
        sx = hx + d.textlength(h, font=f_txt)
        d.text((sx, cy), f"  ({src})", font=f_src, fill=GREY)


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # top bar
    d.text((M, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 11), fill=RED)
    d.text((W - M, 8), "FRIDAY'S NEWS  •  ONE PAGE  •  36 STORIES  •  7 REGIONS",
           font=F(SANS_B, 11), fill=INK, anchor="ra")
    # masthead
    d.text((W // 2, 30), "Friday 20 November 2026", font=F(SERIF_BLACK, 62),
           fill=INK, anchor="ma")
    d.text((W // 2, 98), "Cyclone Akvan strikes India  •  Ballistic missiles hit Kyiv  •  "
           "COP31 deadlocked on final day  •  Asian AI sell-off",
           font=F(SERIF_IT, 17), fill=(90, 40, 30), anchor="ma")
    d.line([M, 126, W - M, 126], fill=INK, width=2)
    # stats strip
    sy0, sy1 = 134, 172
    cw = (W - 2 * M) // 6
    for i, (num, lbl) in enumerate(STATS):
        cx0 = M + i * cw
        if i:
            d.line([cx0 - 4, sy0 + 4, cx0 - 4, sy1 - 4], fill=LINE, width=1)
        d.text((cx0 + cw / 2, sy0 + 2), num, font=F(SERIF_BLACK, 24),
               fill=RED_D, anchor="ma")
        d.text((cx0 + cw / 2, sy0 + 30), lbl, font=F(SANS, 9), fill=(70, 70, 70),
               anchor="ma")
    d.line([M, sy1 + 2, W - M, sy1 + 2], fill=LINE, width=1)
    # region tabs
    ty0, ty1 = 180, 200
    tx = M
    for name, n, col in TABS:
        label = f"{name} {n}"
        wdt = d.textlength(label, font=F(SANS_B, 10)) + 14
        d.rectangle([tx, ty0, tx + wdt, ty1], fill=col)
        d.text((tx + wdt / 2, ty0 + 4), label, font=F(SANS_B, 10),
               fill=(255, 255, 255), anchor="ma")
        tx += wdt + 4
    d.text((W - M, ty0 + 4), "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE",
           font=F(SANS_B, 9), fill=INK, anchor="ra")
    # wide panels
    wy0, wy1 = 206, 394
    pw = (W - 2 * M - 16) // 3
    for i, (scene, place, cat, hl, dk, src) in enumerate(PANELS_WIDE):
        x0 = M + i * (pw + 8)
        draw_panel(img, d, [x0, wy0, x0 + pw, wy1], i + 1, scene, place, cat, hl, dk,
                   src, ill_h=88, hl_size=17, deck_size=11)
    # small panels, two rows of five
    spw = (W - 2 * M - 32) // 5
    sph0, sph1 = 402, 580
    sph2, sph3 = 588, 766
    for i, (scene, place, cat, hl, dk, src) in enumerate(PANELS_SMALL):
        row = 0 if i < 5 else 1
        col = i % 5
        x0 = M + col * (spw + 8)
        y0, y1 = (sph0, sph1) if row == 0 else (sph2, sph3)
        draw_panel(img, d, [x0, y0, x0 + spw, y1], i + 4, scene, place, cat, hl, dk,
                   src, ill_h=88, hl_size=14, deck_size=10)
    # bottom: map + also on
    by0, by1 = 774, 950
    map_w = 332
    d.text((M, by0 - 2), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=INK)
    d.text((M + map_w, by0 - 2), "Pins 1–13 (Lead & Feature)",
           font=F(SERIF_IT, 10), fill=GREY)
    draw_map(d, [M, by0 + 16, M + map_w, by1])
    draw_also_on(d, [M + map_w + 8, by0 + 16, W - M, by1])
    # footer
    fy = by1 + 8
    d.text((M, fy), "DATE CHECK", font=F(SANS_B, 10), fill=RED)
    dc = ("First reported Thursday 19 Nov, NOT shown as Friday's news: the "
          "Trump–Xi–Putin Shenzhen summit itself • Anthropic's $83 IPO pricing "
          "& Nasdaq debut • ICJ Myanmar Rohingya genocide verdict • GTA VI "
          "midnight launch • $190.4m Van Gogh sale • Voyager 1 one light-day "
          "confirmation • Senate 48–51 Iran war-powers vote.")
    lines = wrap(d, dc, F(SANS, 10), W - 2 * M - 82)
    d.text((M + 82, fy), lines[0], font=F(SANS, 10), fill=INK)
    d.text((M + 82, fy + 13), lines[1] if len(lines) > 1 else "",
           font=F(SANS, 10), fill=INK)
    sy = fy + 30
    d.text((M, sy), "Every story here happened, or was first reported, on Friday "
           "20 November 2026 in at least one time zone. Claims are attributed, "
           "not stated as fact.",
           font=F(SANS, 9), fill=GREY)
    d.text((M, sy + 12), "Sources: Reuters, AP, AFP, BBC, IMD, UN News, Al Jazeera, "
           "ICC, EU Council, PBOC.   Original vector drawings.",
           font=F(SANS, 9), fill=GREY)
    return img


if __name__ == "__main__":
    page = build()
    page.save("entry.png", optimize=True)
    import os
    print("wrote entry.png:", os.path.getsize("entry.png"), "bytes",
          page.size)
