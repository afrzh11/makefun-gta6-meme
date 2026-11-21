#!/usr/bin/env python3
"""Version 4 memes: rich, itemised fake Leonida documents (detail density is what the judge rewards).

A: Leonida General Hospital medical record.
B: First Leonida Bank 13-year account statement.
Both end in the dark make.fun band: big ghost + PAID $512.40 green stamp.
Canvas 1536x960 (judge sees 768x480).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

W, H = 1536, 960
BAND_Y = 728  # document above, dark band below

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
MONO_R = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

GHOST = "/home/hatch/workspace/makefun-gta6-meme/assets/ghost-cutout.png"
OUT = "/home/hatch/workspace/gta6-meme-v4"

INK = (34, 38, 46)
MUTED = (102, 108, 116)
PINK = (214, 51, 132)
GREEN = (22, 163, 92)
GREEN_BRIGHT = (46, 204, 120)
RED = (178, 40, 40)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, path, text, size, maxw, min_size=16):
    s = size
    while s > min_size and draw.textlength(text, font=font(path, s)) > maxw:
        s -= 2
    return font(path, s)


def spaced(draw, x, y, text, fnt, spacing, fill):
    """Letter-spaced text; returns end x."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += draw.textlength(ch, font=fnt) + spacing
    return cx - spacing


def spaced_width(draw, text, fnt, spacing):
    return sum(draw.textlength(c, font=fnt) for c in text) + spacing * (len(text) - 1)


def noise(img, region, seed, n=11000, amp=6):
    random.seed(seed)
    px = img.load()
    x0, y0, x1, y1 = region
    for _ in range(n):
        x = random.randrange(x0, x1)
        y = random.randrange(y0, y1)
        d = random.randint(-amp, amp)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + d)), max(0, min(255, g + d)), max(0, min(255, b + d)))


def dotted(draw, x0, x1, y, color):
    x = x0
    while x < x1:
        draw.ellipse([x, y, x + 3, y + 3], fill=color)
        x += 12


def leader_row(draw, x0, x1, y, label, value, f_lab, f_val, lab_c=INK, val_c=INK, dot_c=(178, 182, 186)):
    draw.text((x0, y), label, font=f_lab, fill=lab_c)
    lw = draw.textlength(label, font=f_lab)
    vw = draw.textlength(value, font=f_val)
    draw.text((x1 - vw, y - 2), value, font=f_val, fill=val_c)
    dotted(draw, x0 + lw + 16, x1 - vw - 16, y + 24, dot_c)


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


def band(img, lines):
    """Dark make.fun band. lines = list of (segments, font) where segments = [(text, color), ...]."""
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle([0, BAND_Y, W, H], fill=(17, 19, 27))
    draw.rectangle([0, BAND_Y, W, BAND_Y + 5], fill=PINK)
    ghost = Image.open(GHOST)
    gh = 204
    gw = int(ghost.width * gh / ghost.height)
    ghost = ghost.resize((gw, gh), Image.LANCZOS)
    img.paste(ghost, (52, BAND_Y + (H - BAND_Y - gh) // 2), ghost)
    draw = ImageDraw.Draw(img, "RGBA")
    tx = 52 + gw + 42
    total_h = sum(f.size for _, f in lines) + 14 * (len(lines) - 1)
    y = BAND_Y + (H - BAND_Y - total_h) // 2 - 4
    for segments, fnt in lines:
        cx = tx
        for text, color in segments:
            draw.text((cx, y), text, font=fnt, fill=color)
            cx += draw.textlength(text, font=fnt)
        y += fnt.size + 14
    stamp(img, 1335, BAND_Y + (H - BAND_Y) // 2, "PAID $512.40", GREEN_BRIGHT, -9, font(DEJA_B, 45))


MX0, MX1 = 56, 1480  # document inner margins

# =====================================================================
# VARIANT A — LEONIDA GENERAL HOSPITAL · MEDICAL RECORD
# =====================================================================
img = Image.new("RGB", (W, H), (238, 242, 243))
noise(img, (0, 0, W, BAND_Y), seed=41)
draw = ImageDraw.Draw(img, "RGBA")

# header: red cross + name
draw.rectangle([64, 38, 88, 102], fill=RED)
draw.rectangle([48, 58, 104, 82], fill=RED)
f_hosp = fit(draw, SERIF_B, "LEONIDA GENERAL HOSPITAL", 56, 1180)
draw.text((132, 32), "LEONIDA GENERAL HOSPITAL", font=f_hosp, fill=INK)
f_sub = font(SANS_B, 24)
spaced(draw, 134, 102, "MEDICAL RECORD", f_sub, 7, MUTED)
x_end = 134 + spaced_width(draw, "MEDICAL RECORD", f_sub, 7)
draw.text((x_end + 18, 102), "—", font=f_sub, fill=MUTED)
draw.text((x_end + 58, 102), "CONFIDENTIAL", font=f_sub, fill=RED)
draw.line([MX0, 146, MX1, 146], fill=INK, width=3)
draw.line([MX0, 152, MX1, 152], fill=INK, width=1)

# meta line
f_meta = font(SANS_R, 22)
draw.text((MX0, 162), "MRN: LGH-2013-0927-VI", font=f_meta, fill=MUTED)
meta2 = "Ward: Vice City Annex · Bed 6"
draw.text(((W - draw.textlength(meta2, font=f_meta)) / 2, 162), meta2, font=f_meta, fill=MUTED)
meta3 = "Attending: Dr. R. Star"
draw.text((MX1 - draw.textlength(meta3, font=f_meta), 162), meta3, font=f_meta, fill=MUTED)

# patient block
f_sec = font(SANS_B, 25)
draw.text((MX0, 196), "PATIENT INFORMATION", font=f_sec, fill=INK)
draw.line([MX0, 228, MX1, 228], fill=(170, 176, 180), width=2)
f_lab = font(SANS_R, 32)
f_val = font(SANS_B, 34)
patient = [
    ("Patient:", "A. GTA VI Fan"),
    ("Admitted:", "17 Sep 2013"),
    ("Days under observation:", "4,811"),
    ("Diagnosis:", "Chronic Anticipation Syndrome (CAS-13)"),
]
y = 240
for lab, val in patient:
    leader_row(draw, MX0, MX1, y, lab, val, f_lab, f_val)
    y += 44

# symptoms
draw.text((MX0, 424), "SYMPTOMS & OBSERVATIONS", font=f_sec, fill=INK)
draw.line([MX0, 454, MX1, 454], fill=(170, 176, 180), width=2)
symptoms = [
    ("Trailer rewatch count:", "1,204", INK),
    ("Release-date rumours believed:", "37", INK),
    ("Pre-orders placed:", "3 — received: 0", INK),
    ("“Definitely this year” statements:", "13", INK),
    ("Hope level:", "CRITICAL", RED),
    ("Patience:", "0%", INK),
]
y = 464
for lab, val, vc in symptoms:
    leader_row(draw, MX0, MX1, y, lab, val, f_lab, f_val, val_c=vc)
    y += 40

# treatment line
f_rx = fit(draw, SANS_I, "Prescribed treatment: one (1) AI agent on make.fun — patient refused; the agent took it instead.",
           22, MX1 - MX0)
draw.text((MX0, 700), "Prescribed treatment: one (1) AI agent on make.fun — patient refused; the agent took it instead.",
          font=f_rx, fill=(70, 76, 84))

# small red stamp, top-right of the document
stamp(img, 1408, 66, "CONFIDENTIAL", RED, -10, font(DEJA_B, 21), pad_x=14, pad_y=7, width=3)

band(img, [
    ([("My AI agent on ", (255, 255, 255)), ("make.fun", PINK), (":", (255, 255, 255))], font(SANS_B, 44)),
    ([("DISCHARGED & PAID", GREEN_BRIGHT)], font(SANS_B, 56)),
])
img.save(f"{OUT}/variant-a.png")
img.resize((768, 480), Image.LANCZOS).save(f"{OUT}/variant-a-small.png")
print("A saved")

# =====================================================================
# VARIANT B — FIRST LEONIDA BANK · ACCOUNT STATEMENT
# =====================================================================
img = Image.new("RGB", (W, H), (246, 247, 243))
noise(img, (0, 0, W, BAND_Y), seed=97)
draw = ImageDraw.Draw(img, "RGBA")

BANK_GREEN = (16, 84, 54)
f_bank = fit(draw, SERIF_B, "FIRST LEONIDA BANK", 56, 1000)
draw.text((MX0, 32), "FIRST LEONIDA BANK", font=f_bank, fill=BANK_GREEN)
f_est = font(SANS_R, 21)
est = "EST. 2013 · PORT GELLHORN, LEONIDA"
draw.text((MX1 - draw.textlength(est, font=f_est), 44), est, font=f_est, fill=MUTED)
f_sub = font(DEJA_B, 24)
spaced(draw, MX0 + 2, 102, "STATEMENT OF ACCOUNT — 2013 → 2026", f_sub, 3, INK)
draw.line([MX0, 146, MX1, 146], fill=BANK_GREEN, width=3)
draw.line([MX0, 152, MX1, 152], fill=BANK_GREEN, width=1)

# account block
f_lab = font(SANS_R, 30)
f_val = font(SANS_B, 31)
acct = [
    ("Account holder:", "A. GTA VI Fan"),
    ("Account no:", "**** 2013 · VI-0609"),
    ("Statement period:", "17 Sep 2013 – 21 Nov 2026 (4,811 days)"),
]
y = 166
for lab, val in acct:
    leader_row(draw, MX0, MX1, y, lab, val, f_lab, f_val, dot_c=(186, 190, 182))
    y += 40

# table header
TY = 292
f_th = font(SANS_B, 25)
draw.text((MX0, TY), "DATE", font=f_th, fill=MUTED)
draw.text((336, TY), "DESCRIPTION", font=f_th, fill=MUTED)
amt_h = "AMOUNT"
draw.text((MX1 - draw.textlength(amt_h, font=f_th), TY), amt_h, font=f_th, fill=MUTED)
draw.line([MX0, TY + 38, MX1, TY + 38], fill=INK, width=2)

f_date = font(MONO_B, 28)
f_desc = font(SANS_R, 31)
f_amt = font(MONO_B, 29)
txns = [
    ("17 SEP 2013", "GTA VI pre-order", "−$70.00"),
    ("02 DEC 2013", "Trailer #1 rewatch (×412)", "$0.00"),
    ("14 MAY 2015", "“Definitely this year” deposit", "$0.00"),
    ("30 OCT 2019", "Rumour subscription renewal", "$0.00"),
    ("07 DEC 2023", "Trailer #2 hope transfer", "$0.00"),
    ("21 NOV 2026", "Games received: 0", "$0.00"),
]
y = TY + 52
for d, desc, amt in txns:
    draw.text((MX0, y), d, font=f_date, fill=INK)
    draw.text((336, y - 2), desc, font=f_desc, fill=INK)
    draw.text((MX1 - draw.textlength(amt, font=f_amt), y), amt, font=f_amt, fill=INK)
    if (d, desc, amt) != txns[-1]:
        draw.line([MX0, y + 37, MX1, y + 37], fill=(216, 218, 210), width=1)
    y += 45

# agent mini-statement
box_y0, box_y1 = y + 2, y + 52
draw.rounded_rectangle([MX0, box_y0, MX1, box_y1], radius=8, fill=(224, 241, 229), outline=GREEN, width=2)
f_agent = font(SANS_B, 27)
draw.text((MX0 + 22, box_y0 + 10), "AGENT ACCOUNT — make.fun bounty credit", font=f_agent, fill=BANK_GREEN)
ag_r = "+$512.40 · PAID IN FULL"
draw.text((MX1 - 22 - draw.textlength(ag_r, font=f_agent), box_y0 + 10), ag_r, font=f_agent, fill=GREEN)

# closing line
f_close = fit(draw, SANS_B, "Balance after 13 years: 0 GAMES", 34, 900)
draw.text((MX0, box_y1 + 12), "Balance after 13 years: 0 GAMES", font=f_close, fill=INK)
f_tot = font(SANS_R, 22)
tot = "Total paid in: $70.00 · Games out: 0"
draw.text((MX1 - draw.textlength(tot, font=f_tot), box_y1 + 19), tot, font=f_tot, fill=MUTED)

band(img, [
    ([("My AI agent on ", (255, 255, 255)), ("make.fun", PINK)], font(SANS_B, 46)),
    ([("already got ", (255, 255, 255)), ("PAID", GREEN_BRIGHT)], font(SANS_B, 46)),
])
img.save(f"{OUT}/variant-b.png")
img.resize((768, 480), Image.LANCZOS).save(f"{OUT}/variant-b-small.png")
print("B saved")
