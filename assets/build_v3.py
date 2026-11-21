#!/usr/bin/env python3
"""Version 3 memes for gta6-meme-x-01: fake official documents + make.fun band.

Variant A: "OFFICIAL DELAY NOTICE" letter from Rockstar Games (parody letterhead).
Variant B: "PRE-ORDER RECEIPT" from a game store, 13 years unshipped.
Both share a dark make.fun band at the bottom with the real ghost mascot large.

Canvas 1536x960 (judge sees 768x480, so text is huge and word count low).
Ghost asset: the real make.fun mark from the v1/v2 repo assets.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

W, H = 1536, 960
BAND_Y = 576  # top 60% document, bottom 40% make.fun band

GHOST_PATH = "/home/hatch/workspace/makefun-gta6-meme/assets/ghost-cutout.png"
OUT_DIR = "/home/hatch/workspace/gta6-meme-v3"

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
DBOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (30, 30, 34)
GREY = (105, 100, 90)
RED = (198, 32, 40)
MAGENTA = (214, 51, 132)
PINK = (255, 110, 180)
GREEN = (64, 224, 140)
GREEN_D = (16, 150, 84)
BAND_BG = (26, 24, 34)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 20:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f, size
        size -= 2
    return font(path, size), size


def tracked(draw, cx, y, text, f, tracking, fill):
    """Draw letterspaced text centered at cx."""
    widths = [draw.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=f, fill=fill)
        x += wch + tracking
    return total


def noise(img, region, amount=7, seed=6, n=9000):
    random.seed(seed)
    x0, y0, x1, y1 = region
    px = img.load()
    for _ in range(n):
        x = random.randrange(x0, x1)
        y = random.randrange(y0, y1)
        d = random.randint(-amount, amount)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + d)), max(0, min(255, g + d)), max(0, min(255, b + d)))


def make_stamp(text, fpath, size, color, angle, fill=None, alpha=255, border=None):
    """Outline (or filled) rubber stamp, rotated. angle>0 = counter-clockwise."""
    f = font(fpath, size)
    meas = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = meas.textlength(text, font=f)
    bw = border if border is not None else max(6, size // 9)
    pad_x = int(size * 0.42)
    pad_y = int(size * 0.26)
    sw = int(tw + 2 * pad_x + 2 * bw)
    sh = int(size + 2 * pad_y + 2 * bw)
    layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if fill is not None:
        d.rounded_rectangle([bw // 2, bw // 2, sw - bw // 2 - 1, sh - bw // 2 - 1],
                            radius=16, fill=fill)
    d.rounded_rectangle([bw // 2, bw // 2, sw - bw // 2 - 1, sh - bw // 2 - 1],
                        radius=16, outline=color + (255,), width=bw)
    d.text(((sw - tw) / 2, pad_y + bw - size * 0.06), text, font=f, fill=color + (255,))
    if alpha < 255:
        a = layer.getchannel("A").point(lambda v: v * alpha // 255)
        layer.putalpha(a)
    return layer.rotate(angle, expand=True, resample=Image.BICUBIC)


def paste_center(base, layer, cx, cy):
    base.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)


# ---------------------------------------------------------------- band
def draw_band(img, line1, line2_segments, variant):
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle([0, BAND_Y, W, H], fill=BAND_BG)
    draw.rectangle([0, BAND_Y, W, BAND_Y + 6], fill=MAGENTA)

    # real ghost mascot, large, left side
    ghost = Image.open(GHOST_PATH)
    gh = 336
    gw = int(ghost.width * gh / ghost.height)
    ghost = ghost.resize((gw, gh), Image.LANCZOS)
    img.paste(ghost, (34, BAND_Y + 24), ghost)
    draw = ImageDraw.Draw(img, "RGBA")

    tx = 470
    max_w = W - tx - 26
    # line 1
    f1, _ = fit_font(draw, line1, DBOLD, 84 if variant == "B" else 76, max_w)
    draw.text((tx, BAND_Y + 30), line1, font=f1, fill=(255, 255, 255))
    # line 2 with magenta "make.fun" segment
    plain2 = "".join(t for t, _ in line2_segments)
    f2, _ = fit_font(draw, plain2, DBOLD, 80 if variant == "B" else 76, max_w)
    x = tx
    for text, color in line2_segments:
        draw.text((x, BAND_Y + 122), text, font=f2, fill=color)
        x += draw.textlength(text, font=f2)
    # line 3: PAID huge in green
    f3 = font(DBOLD, 118)
    draw.text((tx, BAND_Y + 212), "PAID", font=f3, fill=GREEN)

    # green paid stamp, white sticker style, bottom right
    stamp = make_stamp("PAID $512.40", DBOLD, 60, GREEN_D, 7,
                       fill=(255, 255, 255, 246))
    paste_center(img, stamp, 1195, BAND_Y + 276)


# ---------------------------------------------------------------- variant A
def variant_a():
    img = Image.new("RGB", (W, H), (250, 248, 242))
    noise(img, (0, 0, W, BAND_Y), amount=5, seed=11)
    draw = ImageDraw.Draw(img, "RGBA")

    # letter frame
    draw.rectangle([26, 26, W - 26, BAND_Y - 24], outline=INK, width=3)
    draw.rectangle([38, 38, W - 38, BAND_Y - 36], outline=(150, 148, 140), width=1)

    # letterhead
    f_head = font(SERIF_B, 64)
    tracked(draw, W / 2, 58, "ROCKSTAR GAMES", f_head, 10, INK)
    f_off = font(SANS_B, 30)
    tracked(draw, W / 2, 146, "OFFICIAL NOTICE", f_off, 12, (110, 105, 95))
    draw.line([120, 198, W - 120, 198], fill=INK, width=3)
    draw.line([120, 205, W - 120, 205], fill=INK, width=1)

    # small official details
    f_ref = font(SANS_R, 25)
    draw.text((120, 216), "Ref: GTA-VI/2013", font=f_ref, fill=GREY)
    ref2 = "21 November 2026"
    draw.text((W - 120 - draw.textlength(ref2, font=f_ref), 216), ref2, font=f_ref, fill=GREY)

    # headline
    f_hl, _ = fit_font(draw, "GTA VI DELAYED AGAIN", DBOLD, 124, 1380)
    hl = "GTA VI DELAYED AGAIN"
    draw.text(((W - draw.textlength(hl, font=f_hl)) / 2, 252), hl, font=f_hl, fill=INK)

    # body lines
    f_sub = font(SANS_R, 47)
    sub = "New release date: to be announced. Again."
    draw.text(((W - draw.textlength(sub, font=f_sub)) / 2, 402), sub, font=f_sub, fill=INK)
    f_small = font(SANS_I, 35)
    small = "Thank you for waiting since 2013."
    draw.text(((W - draw.textlength(small, font=f_small)) / 2, 472), small, font=f_small, fill=GREY)

    # red stamp over the headline
    stamp = make_stamp("DELAYED AGAIN", DBOLD, 88, RED, -12, alpha=195)
    paste_center(img, stamp, 790, 322)

    draw_band(img,
              "Meanwhile, my AI agent",
              [("on ", (255, 255, 255)), ("make.fun", PINK), (" already got", (255, 255, 255))],
              "A")
    return img


# ---------------------------------------------------------------- variant B
def variant_b():
    img = Image.new("RGB", (W, H), (228, 224, 216))
    noise(img, (0, 0, W, BAND_Y), amount=6, seed=23)
    draw = ImageDraw.Draw(img, "RGBA")

    RX0, RX1, RY0, RY1 = 288, 1248, 30, 536
    # receipt shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rectangle([RX0 + 10, RY0 + 14, RX1 + 10, RY1 + 20], fill=(50, 45, 35, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    # receipt paper with zigzag bottom edge
    pts = [(RX0, RY0), (RX1, RY0), (RX1, RY1)]
    x = RX1
    while x > RX0:
        pts.append((x - 12, RY1 + 12))
        pts.append((x - 24, RY1))
        x -= 24
    pts.append((RX0, RY1))
    draw.polygon(pts, fill=(253, 253, 250))

    IX0, IX1 = RX0 + 60, RX1 - 60
    CX = (RX0 + RX1) / 2

    f_store, _ = fit_font(draw, "GAME STORE", MONO_B, 68, IX1 - IX0)
    tracked(draw, CX, 58, "GAME STORE", f_store, 6, INK)
    f_pre = font(MONO_B, 32)
    tracked(draw, CX, 142, "PRE-ORDER RECEIPT", f_pre, 8, (60, 60, 60))

    def dashed(y):
        x = IX0
        while x < IX1:
            draw.line([x, y, min(x + 14, IX1), y], fill=(90, 90, 90), width=3)
            x += 24

    dashed(200)

    rows = [
        ("Item:", "GTA VI", MONO_B, INK),
        ("Pre-ordered:", "2013", MONO, INK),
        ("Paid:", "$70.00", MONO, INK),
        ("Status:", "STILL NOT SHIPPED", MONO_B, RED),
    ]
    y = 226
    for label, value, vf, vc in rows:
        f_lab = font(MONO, 45)
        draw.text((IX0, y), label, font=f_lab, fill=INK)
        fv = font(vf, 45)
        draw.text((IX1 - draw.textlength(value, font=fv), y), value, font=fv, fill=vc)
        y += 66

    dashed(492)
    # barcode decoration
    random.seed(4)
    bx = CX - 190
    while bx < CX + 190:
        bw = random.choice([3, 3, 5, 8])
        draw.rectangle([bx, 506, bx + bw, 532], fill=INK)
        bx += bw + random.choice([4, 6, 9])

    # red stamp across the upper-middle of the receipt (keeps $70.00 / status clear)
    stamp = make_stamp("13 YEARS LATER…", DBOLD, 74, RED, -11, alpha=198)
    paste_center(img, stamp, CX, 262)

    draw_band(img,
              "My AI agent on",
              [("make.fun", PINK), (" already got", (255, 255, 255))],
              "B")
    return img


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    for name, fn in [("variant-a", variant_a), ("variant-b", variant_b)]:
        img = fn()
        img.save(f"{OUT_DIR}/{name}.png")
        small = img.resize((768, 480), Image.LANCZOS)
        small.save(f"{OUT_DIR}/{name}-small.png")
        print("saved", name, img.size)
