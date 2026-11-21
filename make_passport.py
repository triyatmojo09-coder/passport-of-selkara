#!/usr/bin/env python3
"""Generator for the Republic of Selkara passport spread (entry.png).

Build-time only: uses Pillow + system DejaVu fonts to draw one open
passport spread, 1024x768. The submitted program (main.py) does NOT
use Pillow; it only copies this generated entry.png to the output.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 768
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FD}/DejaVuSerif-Bold.ttf"
SERIF = f"{FD}/DejaVuSerif.ttf"
SANS = f"{FD}/DejaVuSans.ttf"
SANS_B = f"{FD}/DejaVuSans-Bold.ttf"
MONO_B = f"{FD}/DejaVuSansMono-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

# ---------- MRZ with ICAO 7-3-1 check digits ----------
VALS = {}
for c in "0123456789":
    VALS[c] = int(c)
for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    VALS[c] = 10 + i
VALS["<"] = 0

def check_digit(s):
    weights = [7, 3, 1]
    total = sum(VALS[ch] * weights[i % 3] for i, ch in enumerate(s))
    return str(total % 10)

def build_mrz():
    line1_raw = "P<SLKMAREN<<ILSA<TERE"
    line1 = line1_raw + "<" * (44 - len(line1_raw))
    doc = "S0482137<"
    doc_cd = check_digit(doc)
    nat = "SLK"
    dob = "910314"
    dob_cd = check_digit(dob)
    sex = "F"
    exp = "330603"
    exp_cd = check_digit(exp)
    optional = "<" * 14
    opt_cd = check_digit(optional)
    body = doc + doc_cd + nat + dob + dob_cd + sex + exp + exp_cd + optional + opt_cd
    composite_src = doc + doc_cd + dob + dob_cd + exp + exp_cd + optional + opt_cd
    composite = check_digit(composite_src)
    line2 = body + composite
    assert len(line1) == 44 and len(line2) == 44, (line1, line2)
    return line1, line2

MRZ1, MRZ2 = build_mrz()

# ---------- helpers ----------
def centered(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return w

def stamp(base, cx, cy, w, h, lines, color, angle, font_size=13, double=False):
    """Draw a rotated ink stamp onto base (RGBA)."""
    pad = 30
    sw, sh = w + pad * 2, h + pad * 2
    s = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    ink = color + (185,)
    d.rounded_rectangle([pad, pad, pad + w, pad + h], radius=8, outline=ink, width=3)
    if double:
        d.rounded_rectangle([pad + 5, pad + 5, pad + w - 5, pad + h - 5], radius=5, outline=ink, width=1)
    f1 = F(SANS_B, font_size)
    f2 = F(SANS_B, font_size + 3)
    n = len(lines)
    total_h = sum((font_size + 6) if i == n - 1 else (font_size + 4) for i in range(n))
    y = pad + (h - total_h) / 2
    for i, ln in enumerate(lines):
        f = f2 if i == n - 1 else f1
        tw = d.textlength(ln, font=f)
        d.text((pad + (w - tw) / 2, y), ln, font=f, fill=ink)
        y += (font_size + 6) if i == n - 1 else (font_size + 4)
    # slight ink texture: erase a few specks
    r = s.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))

def main():
    img = Image.new("RGBA", (W, H), (247, 242, 223, 255))
    d = ImageDraw.Draw(img, "RGBA")

    # page backgrounds: left slightly plain, right with guilloche
    d.rectangle([0, 0, 512, H], fill=(250, 246, 230, 255))
    d.rectangle([512, 0, W, H], fill=(248, 244, 226, 255))
    # outer border
    d.rectangle([8, 8, W - 9, H - 9], outline=(120, 110, 80, 255), width=2)
    d.rectangle([14, 14, W - 15, H - 15], outline=(170, 160, 120, 160), width=1)

    # guilloche on right page: thin pale blue-green sine waves
    for k in range(26):
        y0 = 30 + k * 28
        pts = []
        for x in range(520, 1017):
            y = y0 + 7 * math.sin((x - 520) / 46.0 + k * 0.9)
            pts.append((x, y))
        d.line(pts, fill=(168, 205, 198, 110), width=1)
    for k in range(10):
        x0 = 540 + k * 50
        pts = []
        for y in range(24, 660):
            x = x0 + 6 * math.sin(y / 52.0 + k * 1.1)
            pts.append((x, y))
        d.line(pts, fill=(180, 200, 215, 42), width=1)

    # centre fold
    for i in range(18):
        a = int(70 * (1 - i / 18))
        d.line([(512 - 9 + i, 0), (512 - 9 + i, H)], fill=(120, 105, 70, a), width=1)
        d.line([(512 + 9 - i, 0), (512 + 9 - i, H)], fill=(255, 255, 255, a), width=1)
    d.line([(512, 0), (512, H)], fill=(110, 95, 60, 140), width=1)

    INK = (28, 38, 66, 255)
    DARK = (20, 28, 52, 255)
    LABEL = (88, 92, 100, 255)
    RULE = (90, 100, 120, 180)

    # ================= RIGHT PAGE (data) =================
    RCX = 768  # centre of right page
    # emblem: circle, waves, star
    ex, ey, er = RCX, 52, 26
    d.ellipse([ex - er, ey - er, ex + er, ey + er], outline=(30, 70, 110, 255), width=2)
    for j, yy in enumerate([ey + 2, ey + 9, ey + 16]):
        pts = [(ex - 16 + t, yy + 3 * math.sin(t / 5.0 + j)) for t in range(0, 33, 2)]
        d.line(pts, fill=(30, 110, 130, 255), width=2)
    # star above waves
    sx, sy, sr = ex, ey - 13, 6
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = sr if i % 2 == 0 else sr * 0.45
        star.append((sx + rad * math.cos(ang), sy + rad * math.sin(ang)))
    d.polygon(star, fill=(30, 70, 110, 255))

    centered(d, RCX, 84, "REPUBLIC OF SELKARA", F(SERIF_B, 21), DARK)
    centered(d, RCX, 110, "RÉPUBLIQUE DE SELKARA", F(SERIF, 12), (60, 70, 90, 255))
    centered(d, RCX, 130, "PASSPORT  ·  PASSEPORT", F(SANS_B, 13), (30, 70, 110, 255))
    d.line([(544, 152), (992, 152)], fill=RULE, width=1)

    # ---- portrait: line-engraving style, dark blue ink on guilloche ----
    px0, py0, px1, py1 = 540, 166, 672, 340
    d.rectangle([px0, py0, px1, py1], outline=(30, 50, 90, 255), width=2)
    # clip drawing to photo box via overlay image
    ph = Image.new("RGBA", (px1 - px0, py1 - py0), (252, 250, 240, 60))
    pd = ImageDraw.Draw(ph)
    pw, phh = px1 - px0, py1 - py0
    cx = pw // 2
    blue = (25, 45, 95, 255)
    # shoulders / collar
    pd.arc([cx - 52, 118, cx + 52, 196], start=180, end=360, fill=blue, width=3)
    pd.line([(cx - 52, 157), (cx - 20, 128)], fill=blue, width=3)
    pd.line([(cx + 52, 157), (cx + 20, 128)], fill=blue, width=3)
    pd.line([(cx - 20, 128), (cx, 148), (cx + 20, 128)], fill=blue, width=2)  # collar V
    pd.line([(cx - 34, 150), (cx - 34, 174)], fill=blue, width=2)
    pd.line([(cx + 34, 150), (cx + 34, 174)], fill=blue, width=2)
    # neck
    pd.line([(cx - 10, 108), (cx - 10, 130)], fill=blue, width=3)
    pd.line([(cx + 10, 108), (cx + 10, 130)], fill=blue, width=3)
    # face oval
    pd.ellipse([cx - 30, 34, cx + 30, 112], outline=blue, width=3)
    # hair + bun
    pd.arc([cx - 31, 26, cx + 31, 78], start=180, end=360, fill=blue, width=4)
    pd.ellipse([cx - 11, 8, cx + 11, 30], outline=blue, width=3)
    pd.arc([cx - 11, 8, cx + 11, 30], start=20, end=160, fill=blue, width=1)
    # hair parting line (engraving detail)
    pd.line([(cx, 30), (cx, 42)], fill=blue, width=1)
    pd.arc([cx - 28, 32, cx, 52], start=200, end=330, fill=blue, width=1)
    pd.arc([cx, 32, cx + 28, 52], start=210, end=340, fill=blue, width=1)
    # eyes / brows / nose / mouth (symmetric, minimal)
    pd.line([(cx - 19, 66), (cx - 7, 66)], fill=blue, width=2)
    pd.line([(cx + 7, 66), (cx + 19, 66)], fill=blue, width=2)
    pd.ellipse([cx - 15, 72, cx - 11, 78], fill=blue)
    pd.ellipse([cx + 11, 72, cx + 15, 78], fill=blue)
    pd.line([(cx, 78), (cx - 2, 90), (cx + 2, 90)], fill=blue, width=2)
    pd.arc([cx - 9, 92, cx + 9, 104], start=15, end=165, fill=blue, width=2)
    # fine horizontal engraving lines at photo bottom
    for yy in range(158, 172, 4):
        pd.line([(6, yy), (pw - 6, yy)], fill=(25, 45, 95, 90), width=1)
    img.alpha_composite(ph, (px0, py0))
    d = ImageDraw.Draw(img, "RGBA")
    centered(d, (px0 + px1) // 2, py1 + 4, "MAREN I. T.", F(SANS, 8), LABEL)

    # ---- data fields ----
    def field(x, y, label, value, size=15):
        d.text((x, y), label, font=F(SANS_B, 8), fill=LABEL)
        d.text((x, y + 11), value, font=F(SANS_B, size), fill=INK)

    fx = 688
    field(fx, 166, "TYPE / TYPE", "P")
    field(fx + 88, 166, "CODE / CODE", "SLK")
    field(fx + 168, 166, "PASSPORT No", "S0482137", 14)
    d.line([(fx, 202), (992, 202)], fill=RULE, width=1)
    field(fx, 208, "SURNAME / NOM", "MAREN")
    field(fx, 244, "GIVEN NAMES / PRÉNOMS", "ILSA TERE", 14)
    field(fx, 280, "NATIONALITY / NATIONALITÉ", "SELKARAN", 13)
    field(fx, 312, "SEX / SEXE", "F")
    field(540, 356, "DATE OF BIRTH / DATE DE NAISSANCE", "14 MAR 1991")
    field(772, 356, "PLACE OF BIRTH / LIEU", "PORT LISS")
    d.line([(540, 394), (992, 394)], fill=RULE, width=1)
    field(540, 400, "PROFESSION / PROFESSION", "TIDE WARDEN", 13)
    field(772, 400, "AUTHORITY / AUTORITÉ", "MINISTRY OF TIDES", 11)
    field(540, 438, "DATE OF ISSUE / DÉLIVRANCE", "03 JUN 2023")
    field(772, 438, "DATE OF EXPIRY / EXPIRATION", "03 JUN 2033")
    field(540, 476, "ISSUING OFFICE / BUREAU", "PORT LISS", 12)
    d.line([(540, 512), (992, 512)], fill=RULE, width=1)
    d.text((540, 520), "Holder's signature / Signature du titulaire:", font=F(SANS, 9), fill=LABEL)
    # signature squiggle
    pts = [(560 + t, 548 + 6 * math.sin(t / 9.0) - t * 0.04) for t in range(0, 110, 3)]
    d.line(pts, fill=(25, 45, 95, 220), width=2)
    d.text((540, 566), "Dates in this document follow the Selkaran tide calendar.", font=F(SERIF, 10), fill=(70, 70, 60, 255))
    d.text((540, 582), "Les dates suivent le calendrier des marées selkaran.", font=F(SERIF, 10), fill=(70, 70, 60, 255))

    # ---- MRZ strip ----
    d.rectangle([512, 640, W, 748], fill=(252, 250, 240, 255))
    d.line([(512, 640), (W, 640)], fill=RULE, width=1)
    fm = F(MONO_B, 15)
    d.text((536, 664), MRZ1, font=fm, fill=(15, 15, 15, 255))
    d.text((536, 692), MRZ2, font=fm, fill=(15, 15, 15, 255))
    # redraw outer border over the MRZ strip so the page edge stays intact
    d.rectangle([8, 8, W - 9, H - 9], outline=(120, 110, 80, 255), width=2)
    d.rectangle([14, 14, W - 15, H - 15], outline=(170, 160, 120, 160), width=1)
    d.line([(512, 0), (512, H)], fill=(110, 95, 60, 140), width=1)

    # ================= LEFT PAGE (visas) =================
    centered(d, 256, 34, "VISAS", F(SERIF_B, 20), DARK)
    centered(d, 256, 62, "VISAS", F(SERIF, 11), (60, 70, 90, 255))
    d.line([(32, 86), (480, 86)], fill=RULE, width=1)

    # visa sticker
    vx0, vy0, vx1, vy1 = 40, 104, 472, 238
    d.rectangle([vx0, vy0, vx1, vy1], fill=(240, 248, 244, 255), outline=(30, 110, 90, 255), width=2)
    d.rectangle([vx0 + 5, vy0 + 5, vx1 - 5, vy1 - 5], outline=(30, 110, 90, 160), width=1)
    centered(d, 256, vy0 + 12, "KORDAVA", F(SERIF_B, 17), (15, 80, 65, 255))
    centered(d, 256, vy0 + 38, "VISA  ·  SINGLE ENTRY", F(SANS_B, 11), INK)
    d.line([(vx0 + 20, vy0 + 60), (vx1 - 20, vy0 + 60)], fill=RULE, width=1)
    d.text((vx0 + 22, vy0 + 68), "VALID 90 DAYS FROM ENTRY", font=F(SANS_B, 11), fill=INK)
    d.text((vx0 + 22, vy0 + 88), "HOLDER: MAREN, ILSA TERE   ·   SLK S0482137", font=F(SANS, 10), fill=INK)
    d.text((vx0 + 22, vy0 + 106), "FEE PAID 12 CROWNS  ·  HAVENHOLM CONSULATE", font=F(SANS_B, 10), fill=(15, 80, 65, 255))

    d.text((40, 254), "ENTRY AND EXIT STAMPS / CACHETS", font=F(SANS_B, 9), fill=LABEL)
    d.line([(40, 270), (472, 270)], fill=RULE, width=1)

    BLUE = (35, 70, 160)
    PURPLE = (105, 55, 140)
    RED = (165, 40, 45)
    GREEN = (25, 120, 70)

    stamp(img, 138, 330, 196, 62, ["SELKARA · PORT LISS", "DEPARTED", "17 AUG 2025"], BLUE, -5, double=True)
    stamp(img, 368, 336, 206, 62, ["KORDAVA · HAVENHOLM", "ARRIVED", "18 AUG 2025"], PURPLE, 4, double=True)
    stamp(img, 140, 452, 212, 62, ["FREE CITY OF BRANNIC", "ARRIVED", "02 SEP 2025"], RED, 3, double=True)
    stamp(img, 368, 458, 196, 62, ["SELKARA · PORT LISS", "ARRIVED", "05 SEP 2025"], BLUE, -4, double=True)

    d = ImageDraw.Draw(img, "RGBA")
    d.line([(40, 540), (472, 540)], fill=RULE, width=1)
    d.text((40, 550), "Administrative notes / Notes administratives:", font=F(SANS_B, 9), fill=LABEL)
    d.text((40, 568), "Tide-tax receipt is stamped below at the port of departure.", font=F(SANS, 10), fill=INK)
    stamp(img, 256, 640, 250, 52, ["TIDE TAX PAID · PORT LISS", "17 AUG 2025"], GREEN, -2)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((40, 706), "This page is reserved for visas and official endorsements.", font=F(SERIF, 9), fill=(90, 90, 80, 255))

    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print("MRZ1:", MRZ1)
    print("MRZ2:", MRZ2)
    print("saved", OUT, os.path.getsize(OUT))

if __name__ == "__main__":
    main()
