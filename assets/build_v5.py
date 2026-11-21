#!/usr/bin/env python3
"""Version 5 meme: LEONIDA GENERAL HOSPITAL — itemised statement of charges.

Same winning formula as v4 (the bank statement), but MORE itemised: a full
hospital bill with CPT-style codes, quantities, alternating row shading, a
totals block, and a green payment band with the big make.fun ghost + red
PAID stamp. Canvas 1664x1096 (near v4's 8:5 proportions, so the judge's
768x480 shrink stays crisp).
"""
from PIL import Image, ImageDraw, ImageFont
import random

W, H = 1664, 1096
BAND_Y = 836  # document above, green payment band below

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
MONO_R = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

GHOST = "/home/hatch/workspace/makefun-gta6-meme/assets/ghost-cutout.png"
OUT = "/home/hatch/workspace/gta6-meme-v5"

INK = (34, 38, 46)
MUTED = (102, 108, 116)
GREEN = (22, 163, 92)
GREEN_DEEP = (15, 96, 58)
GREEN_BAND = (18, 116, 66)
GREEN_BRIGHT = (120, 240, 175)
RED = (200, 36, 36)
RED_BRIGHT = (238, 52, 44)
SHADE = (231, 236, 239)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, path, text, size, maxw, min_size=16):
    s = size
    while s > min_size and draw.textlength(text, font=font(path, s)) > maxw:
        s -= 2
    return font(path, s)


def spaced(draw, x, y, text, fnt, spacing, fill):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += draw.textlength(ch, font=fnt) + spacing
    return cx - spacing


def spaced_width(draw, text, fnt, spacing):
    return sum(draw.textlength(c, font=fnt) for c in text) + spacing * (len(text) - 1)


def noise(img, region, seed, n=12000, amp=6):
    random.seed(seed)
    px = img.load()
    x0, y0, x1, y1 = region
    for _ in range(n):
        x = random.randrange(x0, x1)
        y = random.randrange(y0, y1)
        d = random.randint(-amp, amp)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + d)), max(0, min(255, g + d)), max(0, min(255, b + d)))


def stamp(img, cx, cy, text, color, angle, fnt, pad_x=26, pad_y=12, width=6):
    probe = ImageDraw.Draw(img)
    tw = probe.textlength(text, font=fnt)
    th = fnt.size
    tile = Image.new("RGBA", (int(tw + pad_x * 2 + 30), int(th + pad_y * 2 + 30)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.rounded_rectangle([8, 8, tile.width - 8, tile.height - 8], radius=10,
                         outline=color + (255,), width=width)
    td.text(((tile.width - tw) / 2, (tile.height - th) / 2 - 4), text, font=fnt, fill=color + (255,))
    tile = tile.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)), tile)


MX0, MX1 = 60, W - 60  # document inner margins

# =====================================================================
# DOCUMENT — LEONIDA GENERAL HOSPITAL · ITEMISED STATEMENT OF CHARGES
# =====================================================================
img = Image.new("RGB", (W, H), (243, 245, 246))
noise(img, (0, 0, W, BAND_Y), seed=53)
draw = ImageDraw.Draw(img, "RGBA")

# ---- header: red cross + hospital name ----
draw.rectangle([70, 32, 98, 96], fill=RED)
draw.rectangle([54, 50, 114, 78], fill=RED)
f_hosp = fit(draw, SERIF_B, "LEONIDA GENERAL HOSPITAL", 60, 1150)
draw.text((142, 26), "LEONIDA GENERAL HOSPITAL", font=f_hosp, fill=INK)
f_est = font(SANS_R, 20)
est = "EST. 2013 · PORT GELLHORN, LEONIDA"
draw.text((MX1 - draw.textlength(est, font=f_est), 40), est, font=f_est, fill=MUTED)
f_sub = font(SANS_B, 27)
spaced(draw, 144, 102, "ITEMISED STATEMENT OF CHARGES", f_sub, 5, GREEN_DEEP)
draw.line([MX0, 148, MX1, 148], fill=INK, width=3)
draw.line([MX0, 155, MX1, 155], fill=INK, width=1)

# ---- patient / admission meta (two columns) ----
f_lab = font(SANS_R, 28)
f_val = font(SANS_B, 29)
f_val_red = font(SANS_B, 29)


def meta_pair(y, lab1, val1, lab2, segments2):
    draw.text((MX0, y), lab1 + " ", font=f_lab, fill=MUTED)
    x = MX0 + draw.textlength(lab1 + " ", font=f_lab)
    draw.text((x, y - 1), val1, font=f_val, fill=INK)
    # right column: measure full width, draw right-aligned
    total = draw.textlength(lab2 + " ", font=f_lab) + sum(
        draw.textlength(t, font=f_val) for t, _ in segments2)
    x = MX1 - total
    draw.text((x, y), lab2 + " ", font=f_lab, fill=MUTED)
    x += draw.textlength(lab2 + " ", font=f_lab)
    for t, c in segments2:
        draw.text((x, y - 1), t, font=f_val, fill=c)
        x += draw.textlength(t, font=f_val)


meta_pair(170, "Patient:", "A. GTA VI FAN", "Account:",
          [("LGH-2013-04811", INK)])
meta_pair(208, "Admitted:", "17 SEP 2013", "Discharged:",
          [("STILL WAITING", RED), (" (4,811 DAYS)", INK)])
meta_pair(246, "Attending:", "Dr. R. Star, MD", "Ward:",
          [("ANTICIPATION · BED 13", INK)])
draw.line([MX0, 290, MX1, 290], fill=(170, 176, 180), width=2)

# ---- itemised charges table ----
TY = 306
CODE_X, DESC_X, QTY_R, AMT_R = MX0, 218, 1170, MX1
f_th = font(SANS_B, 24)
draw.text((CODE_X, TY), "CODE", font=f_th, fill=MUTED)
draw.text((DESC_X, TY), "DESCRIPTION", font=f_th, fill=MUTED)
draw.text((QTY_R - draw.textlength("QTY", font=f_th), TY), "QTY", font=f_th, fill=MUTED)
draw.text((AMT_R - draw.textlength("AMOUNT", font=f_th), TY), "AMOUNT", font=f_th, fill=MUTED)
draw.line([MX0, TY + 34, MX1, TY + 34], fill=INK, width=2)

f_code = font(MONO_B, 25)
f_desc = font(SANS_R, 30)
f_qty = font(MONO_R, 26)
f_amt = font(MONO_B, 28)
rows = [
    ("99213", "Trailer rewatch therapy", "412 sessions", "$8,240.00"),
    ("36415", "Hope transfusion (Type H+)", "13 units", "$3,900.00"),
    ("96365", "Copium IV drip", "4,811 days", "$9,622.00"),
    ("90837", "“Definitely this year” counselling", "13 years", "$2,600.00"),
    ("70551", "Brain scan — release-date rumours found", "1", "$1,150.00"),
    ("93010", "Heart monitoring during Trailer #2", "1", "$640.00"),
    ("99284", "Emergency care: DELAY ANNOUNCEMENT shock", "3 visits", "$1,875.00"),
]
ROW_H = 44
y = TY + 48
for i, (code, desc, qty, amt) in enumerate(rows):
    if i % 2 == 0:
        draw.rectangle([MX0 - 10, y - 4, MX1 + 10, y + ROW_H - 4], fill=SHADE)
    draw.text((CODE_X, y + 5), code, font=f_code, fill=MUTED)
    draw.text((DESC_X, y), desc, font=f_desc, fill=INK)
    draw.text((QTY_R - draw.textlength(qty, font=f_qty), y + 3), qty, font=f_qty, fill=INK)
    draw.text((AMT_R - draw.textlength(amt, font=f_amt), y + 2), amt, font=f_amt, fill=INK)
    y += ROW_H
rows_end = y

# ---- totals block ----
draw.line([MX0, rows_end + 8, MX1, rows_end + 8], fill=INK, width=2)
f_tot_lab = font(SANS_R, 28)
f_tot_val = font(MONO_B, 28)
f_tot_big = font(SANS_B, 30)
f_tot_big_val = font(MONO_B, 30)

ty = rows_end + 20
draw.text((MX0, ty), "TOTAL CHARGES", font=f_tot_big, fill=INK)
tv = "$28,027.00"
draw.text((AMT_R - draw.textlength(tv, font=f_tot_big_val), ty), tv, font=f_tot_big_val, fill=INK)
games = "GAMES RECEIVED: 0"
games_x = MX0 + draw.textlength("TOTAL CHARGES", font=f_tot_big) + 80
draw.text((games_x, ty + 1), games, font=f_tot_big, fill=RED)

ty += 38
draw.text((MX0, ty), "Insurance paid:", font=f_tot_lab, fill=MUTED)
iv = "$0.00"
draw.text((660 - draw.textlength(iv, font=f_tot_val), ty), iv, font=f_tot_val, fill=INK)
draw.text((760, ty), "Charity adjustment:", font=f_tot_lab, fill=MUTED)
cv = "−$28,027.00"
draw.text((AMT_R - draw.textlength(cv, font=f_tot_val), ty), cv, font=f_tot_val, fill=GREEN_DEEP)
note = "(patient has suffered enough)"
f_note = font(SANS_I, 22)
draw.text((760, ty + 34), note, font=f_note, fill=MUTED)

ty += 76
draw.text((MX0, ty), "PATIENT RESPONSIBILITY:", font=f_tot_big, fill=INK)
pv = "$0.00 — and still no game"
draw.text((MX0 + draw.textlength("PATIENT RESPONSIBILITY: ", font=f_tot_big), ty - 1),
          pv, font=font(MONO_B, 29), fill=INK)

# =====================================================================
# GREEN PAYMENT BAND — ghost + make.fun + red PAID stamp
# =====================================================================
draw.rectangle([0, BAND_Y, W, H], fill=GREEN_BAND)
noise(img, (0, BAND_Y, W, H), seed=71, n=5000, amp=5)
draw = ImageDraw.Draw(img, "RGBA")
draw.rectangle([0, BAND_Y, W, BAND_Y + 5], fill=(255, 255, 255))

ghost = Image.open(GHOST)
gh = 204
gw = int(ghost.width * gh / ghost.height)
ghost = ghost.resize((gw, gh), Image.LANCZOS)
img.paste(ghost, (56, BAND_Y + 12), ghost)
draw = ImageDraw.Draw(img, "RGBA")

tx = 56 + gw + 46
f_pay1 = font(SANS_B, 33)
spaced(draw, tx, BAND_Y + 30, "PAYMENT RECEIVED — AGENT ACCOUNT", f_pay1, 3, (255, 255, 255))
f_mf = font(SANS_B, 62)
f_rest = font(SANS_B, 42)
y2 = BAND_Y + 82
draw.text((tx, y2), "make.fun", font=f_mf, fill=(255, 255, 255))
x2 = tx + draw.textlength("make.fun", font=f_mf)
draw.text((x2, y2 + 14), "  bounty credit", font=f_rest, fill=(255, 255, 255))
f_paid = font(SANS_B, 44)
draw.text((tx, y2 + 78), "+$512.40 · PAID IN FULL", font=f_paid, fill=GREEN_BRIGHT)

# footer fine print inside the band, bottom edge
fine = ("Leonida General Hospital · 13 Years of Continuous Care · If you have been waiting since 2013, "
        "you may be entitled to one (1) AI agent on make.fun.")
f_fine = fit(draw, SANS_I, fine, 20, MX1 - MX0)
draw.text((MX0, H - 34), fine, font=f_fine, fill=(214, 244, 226))

# red PAID stamp overlapping the band's top-right area
stamp(img, 1448, BAND_Y + 62, "PAID", RED_BRIGHT, -10, font(DEJA_B, 62), pad_x=30, pad_y=14, width=7)

img.save(f"{OUT}/meme-v5.png")
img.resize((768, 480), Image.LANCZOS).save(f"{OUT}/meme-v5-small.png")
print("V5 saved", img.size)
