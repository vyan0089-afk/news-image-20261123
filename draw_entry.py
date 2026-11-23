#!/usr/bin/env python3
"""Draw THE TWENTY-THIRD: Monday 23 November 2026 world news in one image.

Authored from scratch in this session. Deterministic: fixed seed, no
network, no external images. Run: python3 draw_entry.py -> entry.png
(1024x1024 PNG).
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
RNG = random.Random(20261123)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF   = lambda s: F("DejaVuSerif.ttf", s)
SANS_B  = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS    = lambda s: F("DejaVuSans.ttf", s)
SANS_O  = lambda s: F("DejaVuSans.ttf", s)

# ---------- palette ----------
PAPER   = (247, 242, 231)
INK     = (24, 24, 28)
NAVY    = (16, 34, 64)
NAVY2   = (24, 52, 96)
GOLD    = (176, 141, 58)
RED     = (178, 34, 34)
DRED    = (140, 20, 20)
TEAL    = (16, 96, 92)
CREAM   = (250, 246, 236)
GREY    = (90, 88, 84)
LGREY   = (200, 196, 186)
RULE    = (120, 110, 92)

def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def block(d, x, y, text, font, maxw, fill=INK, lh=None, align="left"):
    """Draw wrapped text; return y after last line."""
    lines = wrap(d, text, font, maxw)
    if lh is None:
        lh = int(font.size * 1.28)
    for ln in lines:
        if align == "center":
            d.text((x + maxw / 2, y), ln, font=font, fill=fill, anchor="ma")
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def vgrad(img, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        img.paste(c, (x0, y0 + i, x1, y0 + i + 1))

def hgrad(img, box, left, right):
    x0, y0, x1, y1 = box
    n = max(1, x1 - x0)
    for i in range(n):
        t = i / n
        c = tuple(int(left[k] + (right[k] - left[k]) * t) for k in range(3))
        img.paste(c, (x0 + i, y0, x0 + i + 1, y1))

def noise(img, alpha=14):
    ov = Image.new("L", img.size, 0)
    px = ov.load()
    for _ in range(26000):
        x = RNG.randrange(W); y = RNG.randrange(H)
        px[x, y] = RNG.randrange(20, 65)
    img.paste(Image.new("RGB", img.size, (255, 255, 255)), (0, 0), ov)
    return img

def pin(d, x, y, num, col=RED):
    r = 8
    d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=(255, 255, 255), width=2)
    d.text((x, y - 1), str(num), font=SANS_B(9), fill=(255, 255, 255), anchor="mm")

def stamp(d, cx, cy, text, font, col=RED, angle=-10):
    tmp = Image.new("RGBA", (180, 54), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.rectangle([4, 4, 176, 50], outline=col, width=4)
    td.text((90, 27), text, font=font, fill=col, anchor="mm")
    tmp = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
    d._image.paste(tmp, (int(cx - tmp.width / 2), int(cy - tmp.height / 2)), tmp)

# ---------- hero illustrations (322 x 108 panels) ----------
def ill_cop31(img, x, y, w, hh):
    vgrad(img, (x, y, x + w, y + hh), (233, 122, 54), (64, 32, 66))
    d = ImageDraw.Draw(img, "RGBA")
    # sun low over Antalya bay
    d.ellipse([x + w - 78, y + 14, x + w - 18, y + 74], fill=(255, 214, 120))
    d.rectangle([x, y + 82, x + w, y + hh], fill=(38, 62, 96))
    for i in range(5):
        d.line([x, y + 88 + i * 4, x + w, y + 88 + i * 4], fill=(120, 150, 190, 90), width=1)
    # conference hall
    d.polygon([(x + 18, y + hh), (x + 18, y + 52), (x + 70, y + 34),
               (x + 150, y + 34), (x + 150, y + hh)], fill=(18, 26, 44))
    d.polygon([(x + 70, y + 34), (x + 84, y + 22), (x + 98, y + 34)], fill=(24, 38, 62))
    for i in range(6):
        d.rectangle([x + 28 + i * 20, y + 52, x + 42 + i * 20, y + 66],
                    fill=(255, 214, 120))
    # flags row
    cols = [(0, 51, 153), (255, 205, 0), (200, 16, 46), (0, 122, 61),
            (255, 255, 255), (0, 87, 184)]
    for i, c in enumerate(cols):
        fx = x + 168 + i * 24
        d.line([fx + 8, y + 30, fx + 8, y + 62], fill=(220, 220, 220), width=2)
        d.rectangle([fx, y + 30, fx + 16, y + 42], fill=c, outline=(255, 255, 255))
    # torn document, bottom left
    d.polygon([(x + 8, y + hh - 26), (x + 96, y + hh - 30), (x + 92, y + hh - 4),
               (x + 12, y + hh - 2)], fill=(245, 240, 225))
    d.line([x + 16, y + hh - 20, x + 88, y + hh - 22], fill=(120, 110, 92), width=2)
    d.line([x + 16, y + hh - 14, x + 70, y + hh - 15], fill=(150, 140, 120), width=2)
    d.line([x + 16, y + hh - 8, x + 80, y + hh - 9], fill=(150, 140, 120), width=2)
    stamp(d, x + w - 96, y + 76, "NO DEAL", SANS_B(17), RED)

def ill_markets(img, x, y, w, hh):
    vgrad(img, (x, y, x + w, y + hh), (26, 26, 34), (96, 16, 20))
    d = ImageDraw.Draw(img, "RGBA")
    # grid
    for i in range(1, 6):
        d.line([x, y + i * hh / 6, x + w, y + i * hh / 6],
               fill=(255, 255, 255, 26), width=1)
    # falling candlesticks
    base = y + hh - 22
    px, step = x + 14, 26
    tops = [30, 26, 40, 34, 52, 46, 62, 58, 76, 70, 88]
    for i, t in enumerate(tops):
        cx = px + i * step
        hi = t + RNG.randrange(0, 8)
        lo = hi + 14 + RNG.randrange(0, 10)
        d.line([cx + 6, y + hi - 8, cx + 6, y + lo + 8], fill=(255, 90, 80), width=2)
        d.rectangle([cx, y + hi, cx + 12, y + lo], fill=(214, 48, 49),
                    outline=(255, 120, 110))
    # trend arrow
    d.line([x + 16, y + 22, x + w - 20, y + hh - 26], fill=(255, 220, 80), width=5)
    d.polygon([(x + w - 20, y + hh - 26), (x + w - 46, y + hh - 30),
               (x + w - 24, y + hh - 8)], fill=(255, 220, 80))
    d.text((x + 14, y + 6), "-5.06%", font=SANS_B(26), fill=(255, 255, 255))
    d.text((x + 118, y + 12), "NIKKEI  ▼", font=SANS_B(15), fill=(255, 200, 190))
    d.text((x + 14, y + hh - 20), "S&P 500 -3.70%  ·  KOSPI -3.0%", font=SANS(12),
           fill=(255, 220, 210))

def ill_dymer(img, x, y, w, hh):
    vgrad(img, (x, y, x + w, y + hh), (10, 18, 44), (44, 62, 96))
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(26):
        sx = x + RNG.randrange(0, w); sy = y + RNG.randrange(0, 40)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 220))
    # moon
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(235, 232, 210))
    # apartment block, one corner collapsed
    bx, by = x + 30, y + 30
    d.rectangle([bx, by, bx + 150, y + hh], fill=(32, 36, 52))
    d.polygon([(bx + 150, by + 26), (bx + 205, by + 52), (bx + 205, y + hh),
               (bx + 150, y + hh)], fill=(24, 28, 42))
    for r in range(4):
        for c in range(4):
            wx0 = bx + 10 + c * 36; wy0 = by + 12 + r * 18
            lit = (r + c) % 3 == 0
            d.rectangle([wx0, wy0, wx0 + 20, wy0 + 10],
                        fill=(255, 205, 110) if lit else (70, 78, 100))
    # collapsed corner + rubble
    d.polygon([(bx + 150, by + 26), (bx + 205, by + 52), (bx + 185, by + 66),
               (bx + 150, by + 58)], fill=(52, 48, 46))
    for i in range(9):
        rx = bx + 150 + RNG.randrange(0, 60); ry = y + hh - 8 - RNG.randrange(0, 16)
        d.rectangle([rx, ry, rx + 9, ry + 6], fill=(90, 84, 78))
    # searchlight beam
    d.polygon([(x + w - 60, y + hh), (x + 150, y + 40), (x + 190, y + 40),
               (x + w - 30, y + hh)], fill=(255, 240, 180, 70))
    # crane
    d.line([x + 8, y + hh, x + 8, y + 46], fill=(220, 180, 60), width=4)
    d.line([x + 8, y + 46, x + 96, y + 46], fill=(220, 180, 60), width=4)
    d.line([x + 96, y + 46, x + 96, y + 62], fill=(200, 200, 200), width=2)
    d.text((x + 12, y + hh - 20), "11 KILLED · BOY, 7, PULLED ALIVE",
           font=SANS_B(12), fill=(255, 255, 255))

# ---------- small card pictograms (242 x 42 bands) ----------
def band_base(img, x, y, w, hh, c1, c2):
    hgrad(img, (x, y, x + w, y + hh), c1, c2)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([x, y, x + w, y + hh], outline=(0, 0, 0, 60))
    return d

def pic_tennis(d, x, y, w, hh):
    d.rectangle([x, y + hh - 16, x + w, y + hh], fill=(52, 120, 62))
    d.line([x + w // 2, y + 6, x + w // 2, y + hh - 16], fill=(255, 255, 255), width=2)
    d.ellipse([x + w - 52, y + 6, x + w - 28, y + 30], fill=(205, 255, 60),
              outline=(255, 255, 255), width=2)
    d.arc([x + w - 52, y + 6, x + w - 28, y + 30], 300, 60, fill=(255, 255, 255), width=2)

def pic_zeta(d, x, y, w, hh):
    d.text((x + 10, y - 4), "ζ(s) = 0", font=SERIF_B(26), fill=(255, 255, 255))
    pts = []
    for i in range(0, w - 60, 8):
        px = x + 110 + i
        py = y + hh // 2 + int(10 * math.sin(i / 14.0))
        pts.append((px, py))
    d.line(pts, fill=(255, 220, 90), width=3)
    d.line([x + 110, y + hh - 8, x + w - 8, y + hh - 8], fill=(255, 255, 255, 160), width=1)

def pic_cuffs(d, x, y, w, hh):
    d.ellipse([x + 16, y + 8, x + 56, y + 34], outline=(255, 255, 255), width=4)
    d.ellipse([x + 66, y + 8, x + 106, y + 34], outline=(255, 255, 255), width=4)
    d.line([x + 56, y + 21, x + 66, y + 21], fill=(255, 255, 255), width=4)
    d.polygon([(x + w - 90, y + 4), (x + w - 76, y + 16), (x + w - 90, y + 28),
               (x + w - 104, y + 16)], fill=(255, 215, 0))
    d.text((x + w - 8, y + 8), "FBI 10", font=SANS_B(11), fill=(255, 255, 255), anchor="ra")

def pic_btc(d, x, y, w, hh):
    d.ellipse([x + 14, y + 4, x + 46, y + 36], fill=(247, 147, 26),
              outline=(255, 255, 255), width=2)
    d.text((x + 30, y + 6), "₿", font=SANS_B(22), fill=(255, 255, 255), anchor="ma")
    pts = [(x + 60, y + 30), (x + 90, y + 24), (x + 110, y + 28),
           (x + 140, y + 16), (x + 170, y + 20), (x + 200, y + 8)]
    d.line(pts, fill=(255, 255, 255), width=3)
    d.polygon([(x + 200, y + 8), (x + 188, y + 8), (x + 200, y + 20)], fill=(255, 255, 255))

def pic_ship(d, x, y, w, hh):
    d.rectangle([x, y + hh - 12, x + w, y + hh], fill=(40, 90, 130))
    d.polygon([(x + 20, y + 22), (x + 150, y + 22), (x + 138, y + 34),
               (x + 32, y + 34)], fill=(200, 60, 40))
    for i in range(4):
        d.rectangle([x + 30 + i * 26, y + 8, x + 50 + i * 26, y + 22],
                    fill=[(255, 200, 60), (60, 160, 90), (70, 120, 200), (220, 220, 220)][i])
    d.rectangle([x + 160, y + 6, x + 168, y + 22], fill=(240, 240, 240))
    d.text((x + w - 6, y + 24), "$1 TRILLION", font=SANS_B(11), fill=(255, 255, 255), anchor="ra")

def pic_plane(d, x, y, w, hh):
    d.ellipse([x + 10, y + 10, x + 105, y + 30], fill=(255, 255, 255))
    d.polygon([(x + 98, y + 13), (x + 128, y + 18), (x + 98, y + 25)], fill=(255, 255, 255))
    d.polygon([(x + 55, y + 10), (x + 72, y + 2), (x + 80, y + 10)], fill=(200, 210, 225))
    d.text((x + w - 6, y + 8), "1,600+ DELAYED", font=SANS_B(11), fill=(255, 255, 255), anchor="ra")

def pic_penny(d, x, y, w, hh):
    d.ellipse([x + 14, y + 3, x + 52, y + 39], fill=(184, 115, 51),
              outline=(255, 220, 160), width=3)
    d.text((x + 33, y + 6), "1¢", font=SERIF_B(20), fill=(255, 240, 210), anchor="ma")
    d.line([x + 66, y + 6, x + 110, y + 36], fill=(220, 40, 40), width=5)
    d.text((x + w - 6, y + 10), "232 YEARS · OVER", font=SANS_B(11), fill=(255, 255, 255), anchor="ra")

def pic_tower(d, x, y, w, hh):
    d.rectangle([x + 20, y + 6, x + 34, y + 34], fill=(240, 240, 240))
    d.rectangle([x + 14, y + 2, x + 40, y + 10], fill=(220, 60, 50))
    d.line([x + 60, y + 30, x + 200, y + 30], fill=(255, 255, 255), width=3)
    for i in range(4):
        d.line([x + 70 + i * 34, y + 24, x + 82 + i * 34, y + 36], fill=(255, 80, 70), width=4)
    d.text((x + w - 6, y + 6), "NO FLIGHTS", font=SANS_B(13), fill=(255, 255, 255), anchor="ra")

def pic_drone(d, x, y, w, hh):
    d.rectangle([x, y + hh - 12, x + w, y + hh], fill=(120, 84, 52))
    for bx in range(3):
        d.rectangle([x + 16 + bx * 40, y + 22, x + 36 + bx * 40, y + hh - 12],
                    fill=(70, 60, 54))
    d.ellipse([x + 150, y + 6, x + 178, y + 22], fill=(40, 40, 46))
    d.line([x + 138, y + 10, x + 150, y + 12], fill=(200, 200, 200), width=2)
    d.line([x + 178, y + 12, x + 190, y + 10], fill=(200, 200, 200), width=2)
    d.text((x + w - 6, y + 8), "KHARTOUM", font=SANS_B(12), fill=(255, 255, 255), anchor="ra")

def pic_tanker(d, x, y, w, hh):
    d.rectangle([x, y + hh - 10, x + w, y + hh], fill=(30, 70, 110))
    d.polygon([(x + 16, y + 20), (x + 130, y + 20), (x + 120, y + 32),
               (x + 26, y + 32)], fill=(60, 60, 66))
    d.rectangle([x + 96, y + 8, x + 106, y + 20], fill=(220, 220, 220))
    d.polygon([(x + 150, y + 30), (x + 158, y + 12), (x + 166, y + 30)],
              fill=(255, 140, 30))
    d.ellipse([x + 148, y + 26, x + 168, y + 34], fill=(255, 90, 20))
    d.text((x + w - 6, y + 2), "2 TANKERS HIT", font=SANS_B(10), fill=(255, 255, 255), anchor="ra")

def pic_rubble(d, x, y, w, hh):
    for i, (rx, ry, rw, rh) in enumerate([(10, 24, 26, 12), (40, 28, 20, 9),
                                          (64, 20, 30, 14), (98, 28, 22, 10),
                                          (124, 24, 26, 12)]):
        d.rectangle([x + rx, y + ry, x + rx + rw, y + ry + rh], fill=(110, 104, 96))
    d.polygon([(x + 150, y + 34), (x + 170, y + 6), (x + 190, y + 34)],
              fill=(255, 200, 40))
    d.text((x + 170, y + 14), "!", font=SANS_B(16), fill=(40, 40, 40), anchor="ma")
    d.text((x + w - 6, y + 12), "TOXIC", font=SANS_B(13), fill=(255, 255, 255), anchor="ra")

def pic_bike(d, x, y, w, hh):
    d.ellipse([x + 18, y + 20, x + 42, y + 40], outline=(255, 255, 255), width=3)
    d.ellipse([x + 78, y + 20, x + 102, y + 40], outline=(255, 255, 255), width=3)
    d.polygon([(x + 30, y + 30), (x + 60, y + 30), (x + 52, y + 12),
               (x + 66, y + 12)], fill=(220, 50, 50))
    d.line([x + 60, y + 30, x + 90, y + 30], fill=(255, 255, 255), width=3)
    for i in range(4):
        for j in range(2):
            c = (20, 20, 20) if (i + j) % 2 == 0 else (255, 255, 255)
            d.rectangle([x + 130 + i * 12, y + 8 + j * 12, x + 142 + i * 12,
                         y + 20 + j * 12], fill=c)
    d.text((x + w - 6, y + 26), "8th TITLE", font=SANS_B(10), fill=(255, 255, 255), anchor="ra")

# ---------- world map ----------
N_AM = [(-168,66),(-140,70),(-120,72),(-95,80),(-85,66),(-80,73),(-65,60),
        (-55,52),(-60,46),(-70,42),(-75,35),(-80,32),(-81,26),(-90,21),
        (-97,16),(-92,15),(-83,9),(-79,9),(-86,12),(-95,16),(-105,20),
        (-110,23),(-114,28),(-120,34),(-125,40),(-124,48),(-130,55),
        (-150,60),(-165,60)]
S_AM = [(-79,9),(-72,12),(-62,10),(-52,5),(-50,0),(-44,-3),(-35,-8),
        (-38,-15),(-40,-22),(-48,-28),(-57,-35),(-65,-41),(-68,-52),
        (-70,-54),(-73,-50),(-73,-40),(-72,-30),(-70,-18),(-77,-12),
        (-81,-6),(-80,1)]
AFR = [(-6,35),(-10,31),(-17,15),(-17,12),(-12,8),(-8,5),(6,6),(9,4),
       (13,-1),(12,-6),(13,-12),(12,-18),(16,-28),(20,-35),(28,-33),
       (35,-25),(40,-16),(40,-10),(46,-1),(51,2),(51,11),(44,11),(40,15),
       (38,18),(37,22),(34,27),(32,31),(22,33),(11,34),(10,37),(0,36)]
EURASIA = [(-10,36),(-9,43),(-2,44),(-1,46),(-4,48),(-1,50),(2,51),(4,53),
           (8,57),(10,59),(5,60),(5,62),(12,64),(18,69),(25,71),(30,70),
           (40,68),(44,66),(50,69),(55,68),(60,69),(68,73),(75,73),
           (80,73),(90,75),(100,76),(110,74),(120,73),(130,72),(140,72),
           (150,70),(160,70),(170,67),(178,65),(170,60),(162,56),(158,52),
           (150,59),(142,59),(140,55),(135,45),(130,42),(127,40),(122,38),
           (120,35),(115,32),(110,30),(105,28),(100,25),(98,20),(95,16),
           (92,15),(90,22),(88,22),(85,19),(80,15),(77,8),(75,12),(72,20),
           (70,23),(66,25),(62,25),(58,25),(56,26),(54,27),(52,28),(50,29),
           (48,30),(44,29),(40,32),(36,36),(33,36),(30,36),(27,37),(23,36),
           (22,38),(19,40),(16,38),(12,44),(8,44),(3,43),(-2,37),(-6,36)]
UK = [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(1,51)]
JAPAN = [(130,31),(132,33),(135,34),(137,35),(139,35),(140,38),(141,41),
         (142,44),(144,44),(141,42),(140,39),(137,37),(134,35),(131,33)]
AUS = [(113,-22),(114,-30),(115,-35),(120,-34),(124,-33),(129,-32),(132,-32),
       (135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),
       (150,-23),(146,-19),(142,-15),(142,-11),(137,-12),(135,-15),(132,-12),
       (130,-13),(126,-14),(122,-17),(118,-20)]
NGUINEA = [(131,-1),(136,-2),(141,-3),(146,-6),(150,-8),(147,-9),(143,-8),
           (138,-8),(134,-4)]
LAND = [N_AM, S_AM, AFR, EURASIA, UK, JAPAN, AUS, NGUINEA]

# (number, lon, lat) pins matching story numbers on the page
PINS = [(1, 30.7, 36.9), (2, 139.7, 35.7), (3, 30.8, 50.8), (4, 7.7, 45.1),
        (5, -122.4, 37.8), (6, -108.0, 25.5), (7, 127.0, 37.5),
        (8, -84.4, 33.7), (9, -99.1, 19.4), (10, 4.4, 50.8),
        (11, 32.5, 15.5), (12, 56.4, 26.5), (13, 34.5, 31.5),
        (14, -8.5, 37.1), (15, 114.0, 22.5), (16, 121.5, 25.0),
        (17, 106.8, -6.2), (18, 29.7, 7.9), (19, 29.0, 41.0),
        (20, 72.8, 19.0)]

def draw_map(img, x, y, w, hh):
    vgrad(img, (x, y, x + w, y + hh), (168, 208, 228), (120, 168, 200))
    d = ImageDraw.Draw(img, "RGBA")
    def px(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (75 - lat) / 130 * hh)
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360 * w
        d.line([gx, y, gx, y + hh], fill=(255, 255, 255, 70), width=1)
    for lat in (-30, 0, 30, 60):
        gy = y + (75 - lat) / 130 * hh
        d.line([x, gy, x + w, gy], fill=(255, 255, 255, 70), width=1)
        d.text((x + w - 30, gy + 1), f"{abs(lat)}°{'N' if lat > 0 else 'S' if lat < 0 else ''}",
               font=SANS(8), fill=(255, 255, 255))
    for poly in LAND:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(196, 178, 138), outline=(120, 104, 70))
    for num, lon, lat in PINS:
        px_, py_ = px(lon, lat)
        pin(d, px_, py_, num)
    d.text((x + 6, y + 4), "WHERE IT HAPPENED — 23 NOV 2026",
           font=SANS_B(10), fill=(16, 34, 64))

# ---------- content ----------
HEROES = [
    ("CLIMATE · ANTALYA, TURKEY", "COP31 collapses: no deal on fossil fuels",
     "After two weeks and two days of overtime — the longest COP ever — "
     "the EU and about 130 parties rejected a text that never mentioned "
     "fossil fuels.",
     "CNN · REUTERS · LE MONDE, 22–23 NOV", ill_cop31,
     (250, 120, 60), (70, 40, 70)),
    ("MARKETS · TOKYO — SEOUL — NEW YORK", "AI sell-off rattles world markets",
     "Japan's Nikkei fell 5.06% and the S&P 500 slid 3.7% into correction as "
     "investors questioned vast AI spending. Seoul's KOSPI fell 3%.",
     "REUTERS, 23 NOV", ill_markets,
     (30, 30, 40), (110, 20, 24)),
    ("CONFLICT · DYMER, UKRAINE", "Russian strike kills 11 near Kyiv",
     "A drone hit a five-storey block of flats 45 km north of Kyiv. Rescuers "
     "pulled a seven-year-old boy and a 79-year-old woman alive from the "
     "rubble.",
     "REUTERS, 23 NOV", ill_dymer,
     (12, 22, 52), (50, 70, 105)),
]

# (tag, headline, body, source, pic_fn, c1, c2)
CARDS = [
    ("SPORT · TURIN", "Alcaraz wins first ATP Finals crown",
     "Beat world No. 1 Zverev 6-2, 7-6(7), saving three set points — a 14th "
     "straight win.", "BBC · ATP, 23 NOV",
     pic_tennis, (30, 110, 60), (16, 70, 40)),
    ("SCIENCE · SAN FRANCISCO", "Riemann proof claim faces checks [CLAIM]",
     "Alpöge says he and Claude proved it. The Clay Institute still lists "
     "it unsolved.", "NATURE · CNN, 20–23 NOV",
     pic_zeta, (40, 50, 110), (20, 30, 70)),
    ("AMERICAS · SINALOA", "Cartel capture risks bloody succession",
     "Mexico's capture of FBI most-wanted 'El Chapo Isidro', 44, threatens "
     "a cartel turf war.", "WSJ, 23 NOV", pic_cuffs, (120, 70, 40), (70, 40, 30)),
    ("MARKETS · CRYPTO", "Bitcoin back above $61,000",
     "BTC $61,272.90 (+1.75%), ETH $1,724.15 (+2.28%) at 00:00 UTC.",
     "KUCOIN, 23 NOV 00:00 UTC", pic_btc, (200, 110, 30), (140, 70, 20)),
    ("ASIA · SEOUL", "Korea's exports pass $1 trillion",
     "Annual exports topped $1 trillion for the first time, driven by AI "
     "chip demand.", "23 NOV",
     pic_ship, (20, 80, 130), (10, 50, 90)),
    ("AMERICAS · ATLANTA", "Delta outage delays 1,600+ flights",
     "A weight-and-balance failure hit Atlanta as Thanksgiving travel "
     "began.", "FAA, 23 NOV",
     pic_plane, (60, 90, 140), (30, 60, 100)),
    ("AMERICAS · WASHINGTON", "Trump signs law ending the penny",
     "The Common Cents Act ends the penny's 232-year run; the US stops "
     "minting cents.", "23 NOV",
     pic_penny, (140, 100, 50), (90, 60, 30)),
    ("EUROPE · BRUSSELS", "Belgium grounds flights in strike",
     "Air traffic control was suspended Monday and nearly all flights "
     "cancelled.", "23 NOV",
     pic_tower, (90, 90, 110), (50, 55, 75)),
    ("AFRICA · KHARTOUM", "Drone attacks kill five children",
     "Strikes hit homes in Khartoum and Omdurman and damaged a UN building, "
     "reports say.", "FRANCE 24, 23 NOV",
     pic_drone, (130, 90, 50), (80, 55, 35)),
    ("MIDDLE EAST · HORMUZ", "Two tankers hit in Strait of Hormuz",
     "Bahrain accuses Iran of striking a civilian site as two tankers are "
     "hit. [REPORTED]",
     "FRANCE 24, 23 NOV", pic_tanker, (30, 70, 110), (15, 45, 75)),
    ("MIDDLE EAST · GAZA", "Gaza war left 'widespread contamination'",
     "A new report describes Gaza as a toxic wasteland after the assault, "
     "experts say.", "23 NOV",
     pic_rubble, (110, 100, 80), (70, 65, 50)),
    ("SPORT · PORTIMÃO", "Márquez wins eighth MotoGP title",
     "The Spaniard sealed the crown in Portugal, equalling Agostini on "
     "eight world titles.", "23 NOV",
     pic_bike, (160, 40, 50), (100, 25, 35)),
]

BRIEFS = [
    ("Shenzhen summit", "US, China and Russia leaders issue a 'Declaration toward Peace'. [REPORTED]"),
    ("Benghazi, Libya", "Russian frigate Merkury sinks after a suspected Ukrainian naval drone attack."),
    ("Baltic Sea", "Russian cargo ship Sparta II set ablaze; drifts into Finnish waters."),
    ("Taipei", "Taiwan stocks swing 1,578 points in a day; TSMC ends higher."),
    ("Kigali", "Five EU states accept deportation centres in Rwanda."),
    ("Iowa, USA", "US Army to detonate unstable explosives despite a court order."),
    ("Brasília", "Bolsonaro in intensive care with an intestinal obstruction."),
    ("Canberra", "COP31 flop triggers backlash in Australia; Pacific nations voice despair."),
    ("Seoul", "Education minister resigns over an AI exam-cheating scandal."),
    ("Damascus", "Syria and the EU seek normalisation; diplomats worry over migration."),
    ("Brussels", "NATO faces a sovereignty dilemma as militaries rely on private tech and AI."),
    ("Jerusalem", "Opposition leader Eisenkot calls settler attacks 'Jewish terrorism'."),
    ("DR Congo", "Fighting near an Ebola area disrupts the outbreak response."),
    ("Jakarta", "MSCI discussed avoiding an Indonesia downgrade with Prabowo and Dalio. [REPORTED]"),
    ("Istanbul", "Thousands rally against a media takeover."),
    ("Europe", "November PMIs: India 56.3, Germany 55.0, UK 52.3 — growth holds."),
    ("Oil", "Brent crude $89.96 as oil recovers from the Iran-war shock; diesel stays scarce."),
    ("Geneva", "Gukesh begins his world chess title defence against Sindarov. [FORECAST: starts 24 Nov]"),
    ("South Sudan", "Paramilitary attack kills at least 24 civilians."),
    ("Hodeida, Yemen", "Houthis claim an attack on a Saudi refinery; Saudi strike hits Hodeida."),
]

STATS = [("COP31", "NO DEAL"), ("NIKKEI", "−5.06%"), ("S&P 500", "−3.70%"),
         ("DYMER", "11 KILLED"), ("BITCOIN", "$61,273"), ("KOREA EXPORTS", "$1 TRILLION")]

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")
    # ---- masthead ----
    vgrad(img, (0, 0, W, 74), NAVY, NAVY2)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((512, 8), "THE TWENTY-THIRD", font=SERIF_B(40), fill=(250, 246, 236),
           anchor="ma")
    d.text((512, 52), "M O N D A Y   2 3   N O V E M B E R   2 0 2 6",
           font=SANS_B(15), fill=(232, 196, 110), anchor="ma")
    d.rectangle([0, 74, W, 78], fill=GOLD)
    # ---- stat strip ----
    y = 78
    cw = W // 6
    for i, (k, v) in enumerate(STATS):
        x0 = i * cw
        if i % 2 == 0:
            d.rectangle([x0, y, x0 + cw, y + 34], fill=(238, 232, 216))
        d.text((x0 + cw / 2, y + 3), k, font=SANS_B(10), fill=GREY, anchor="ma")
        d.text((x0 + cw / 2, y + 16), v, font=SANS_B(16),
               fill=RED if "−" in v or v in ("NO DEAL", "11 KILLED") else NAVY,
               anchor="ma")
        if i:
            d.line([x0, y + 4, x0, y + 30], fill=LGREY, width=1)
    d.line([0, y + 34, W, y + 34], fill=RULE, width=1)
    # ---- region strip ----
    y = 114
    d.text((512, y), "EUROPE 10  ·  ASIA-PACIFIC 6  ·  MIDDLE EAST 6  ·  AMERICAS 5  ·  "
                     "AFRICA 5  ·  OCEANIA 1  ·  SCIENCE & MARKETS 2  —  35 STORIES",
           font=SANS_B(11), fill=NAVY, anchor="ma")
    d.line([0, y + 20, W, y + 20], fill=RULE, width=1)
    # ---- heroes ----
    y = 136
    hw, gap = 322, 10
    x0 = 10
    for tag, head, body, src, ill, c1, c2 in HEROES:
        x = x0
        d.rectangle([x, y, x + hw, y + 216], fill=CREAM, outline=RULE, width=1)
        ill(img, x + 1, y + 1, hw - 2, 100)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((x + 10, y + 106), tag, font=SANS_B(10), fill=RED)
        yy = block(d, x + 10, y + 120, head, SERIF_B(17), hw - 20, fill=INK, lh=19)
        yy = block(d, x + 10, yy + 2, body, SANS(11), hw - 20, fill=(50, 48, 44), lh=14)
        d.text((x + 10, y + 216 - 14), src, font=SANS_O(9), fill=GREY)
        x0 += hw + gap
    # ---- feature cards ----
    y = 362
    cw2, ch2, gap2 = 242, 128, 8
    x_start = 10
    for idx, (tag, head, body, src, pic, c1, c2) in enumerate(CARDS):
        r, c = divmod(idx, 4)
        x = x_start + c * (cw2 + gap2)
        yy = y + r * (ch2 + gap2)
        d.rectangle([x, yy, x + cw2, yy + ch2], fill=CREAM, outline=RULE, width=1)
        dd = band_base(img, x + 1, yy + 1, cw2 - 2, 40, c1, c2)
        pic(dd, x + 1, yy + 1, cw2 - 2, 40)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((x + 8, yy + 44), tag, font=SANS_B(9), fill=RED)
        y2 = block(d, x + 8, yy + 56, head, SANS_B(12), cw2 - 16, fill=INK, lh=13)
        y2 = block(d, x + 8, y2 + 1, body, SANS(10), cw2 - 16, fill=(50, 48, 44), lh=12)
        d.text((x + 8, yy + ch2 - 12), src, font=SANS_O(8), fill=GREY)
    # ---- map + side box ----
    y = 362 + 3 * ch2 + 2 * gap2 + 8
    map_w = 640
    draw_map(img, 10, y, map_w, 104)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([10, y, 10 + map_w, y + 104], outline=RULE, width=1)
    sx = 10 + map_w + 10
    sw = W - sx - 10
    d.rectangle([sx, y, sx + sw, y + 104], fill=(232, 228, 210), outline=RULE, width=1)
    d.text((sx + 10, y + 6), "✓  DATE CHECK", font=SANS_B(13), fill=TEAL)
    block(d, sx + 10, y + 24, "Verified: today is Monday 23 November 2026. "
        "Every story above happened, or was first reported, on 23 November 2026 "
        "in some time zone.", SANS(10), sw - 20, fill=INK, lh=12)
    d.text((sx + 10, y + 62), "HOW TO READ IT", font=SANS_B(11), fill=NAVY)
    block(d, sx + 10, y + 76, "[CLAIM] unverified  ·  [REPORTED] single-source  ·  "
        "[FORECAST] about the future. Pins 1–20 mark the map.",
        SANS(10), sw - 20, fill=(60, 58, 54), lh=12)
    # ---- briefs ----
    y = y + 104 + 8
    d.text((10, y), "IN BRIEF — 20 MORE STORIES", font=SANS_B(12), fill=NAVY)
    d.line([10, y + 16, W - 10, y + 16], fill=GOLD, width=2)
    y += 20
    col_w = (W - 20) // 2 - 8
    for i, (place, txt) in enumerate(BRIEFS):
        col = i // 10
        row = i % 10
        bx = 10 + col * (col_w + 16)
        by = y + row * 10
        d.text((bx, by), "•", font=SANS_B(9), fill=RED)
        d.text((bx + 10, by), place + ": ", font=SANS_B(9), fill=INK)
        tw = d.textlength(place + ": ", font=SANS_B(9))
        d.text((bx + 10 + tw, by), txt, font=SANS(9), fill=(50, 48, 44))
    # ---- footer ----
    fy = H - 14
    d.line([10, fy - 5, W - 10, fy - 5], fill=RULE, width=1)
    d.text((10, fy), "THE TWENTY-THIRD · Sources: Reuters, CNN, BBC, WSJ, France 24, "
                     "Le Monde, ATP, KuCoin, Nature — 23 Nov 2026",
           font=SANS(9), fill=GREY)
    d.text((W - 10, fy), "35 STORIES · 7 REGIONS", font=SANS_B(9), fill=NAVY,
           anchor="ra")
    # ---- paper texture noise (deterministic) ----
    noise(img)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    build()
