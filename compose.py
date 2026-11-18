#!/usr/bin/env python3
"""Compose the three candidate news-image variants for 18 Nov 2026.

Build tool only: it assembles AI-generated editorial illustrations (assets/)
with crisp PIL-rendered text into 1024x1024 PNGs. The shipped entry.png is
copied verbatim by main.ts; this script is not part of the entry program.
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(BASE, "assets")
OUT = os.path.join(BASE, "variants")
os.makedirs(OUT, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def load(name):
    return Image.open(os.path.join(A, name)).convert("RGB")


def cover(img, w, h, focus="center"):
    """Crop img to exactly w x h. focus bottom keeps the lower band."""
    iw, ih = img.size
    s = max(w / iw, h / ih)
    img = img.resize((round(iw * s), round(ih * s)), Image.LANCZOS)
    x = (img.width - w) // 2
    if focus == "bottom":
        y = img.height - h
    else:
        y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# --- palette ---
NAVY = (20, 36, 61)
PAPER = (246, 241, 231)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARKRED = (142, 31, 22)
GOLD = (232, 182, 76)
GREY = (90, 86, 78)
LINE = (216, 210, 196)
WHITE = (255, 255, 255)

STORIES = [
    dict(key="gulf", kicker="MIDDLE EAST · GULF WAR", color=RED,
         head="U.S. strikes Iran; Iran hits Kuwait and Bahrain",
         sub="U.S. jets hit a missile site on Qeshm Island; Iran fired back at Gulf bases hosting U.S. forces.",
         short="U.S. jets hit Qeshm Island; Iran hit Gulf bases.",
         img="media-generation-gulf-strikes-0-44488a70-d22c-43a7-85d4-8222857b49bc.webp"),
    dict(key="bridge", kicker="UKRAINE · RUSSIA WAR", color=RED,
         head="Ukraine strike brings down part of Crimea bridge",
         sub="A span of the Kerch bridge collapsed into the strait on a second day of attacks.",
         short="A span of the Kerch bridge fell into the strait.",
         img="media-generation-crimea-bridge-0-bb7ac253-e1f0-48ec-912a-3bb7d1bc3239.webp"),
    dict(key="summit", kicker="CHINA · DIPLOMACY", color=NAVY,
         head="Xi hosts Putin in Shenzhen; Trump to join",
         sub="The three leaders prepare for three-way talks on Ukraine, Iran and trade.",
         short="Three-way talks next on Ukraine, Iran, trade.",
         img="media-generation-shenzhen-summit-0-64d16c6c-2344-4cd3-89ba-e94eb5797374.webp"),
    dict(key="alaska", kicker="U.S. POLITICS", color=NAVY, focus="bottom",
         head="Democrat Peltola wins Alaska Senate seat",
         sub="The win gives Democrats a 56–44 Senate majority.",
         short="Democrats now hold a 56–44 Senate majority.",
         img="media-generation-alaska-senate-0-efc6b8ba-ae7c-492a-b4b4-80d6876f575c.webp"),
    dict(key="ebola", kicker="HEALTH · AFRICA", color=DARKRED,
         head="Ebola in DR Congo doubles: 11,000 cases",
         sub="More than 5,400 have died; three in four infected children under five do not survive.",
         short="5,400 dead; 3 in 4 infected under-5s die.",
         img="media-generation-ebola-drc-0-7e52dcdd-1b5f-4ead-a06f-ebd0829b6d1f.webp"),
    dict(key="cyclone", kicker="PACIFIC · WEATHER", color=NAVY,
         head="Cyclone Xavier, Category 5, hits Cook Islands",
         sub="The strongest storm of the season slams the northern Cook Islands.",
         short="The season's strongest storm hits the islands.",
         img="media-generation-cyclone-xavier-0-604665c0-dcb2-4ec5-9780-3675324b80cd.webp"),
]
BY_KEY = {s["key"]: s for s in STORIES}

DATE = "WEDNESDAY 18 NOVEMBER 2026"
TAGLINE = "THE WORLD IN ONE DAY"


def banner(draw, y, h, date_size=40, tag_size=19):
    draw.rectangle([0, y, 1024, y + h], fill=NAVY)
    f1, f2 = font(FB, date_size), font(FR, tag_size)
    w1 = draw.textlength(DATE, font=f1)
    draw.text(((1024 - w1) / 2, y + 10), DATE, font=f1, fill=WHITE)
    w2 = draw.textlength(TAGLINE, font=f2)
    draw.text(((1024 - w2) / 2, y + h - tag_size - 14), TAGLINE, font=f2, fill=GOLD)


def story_cell(canvas, draw, s, x, y, w, img_h, head_size, sub_size,
               kicker_size=17, pad=12, sub_text=None):
    img = cover(load(s["img"]), w, img_h, s.get("focus", "center"))
    canvas.paste(img, (x, y))
    ty = y + img_h + 10
    fk = font(FB, kicker_size)
    draw.text((x + pad, ty), s["kicker"], font=fk, fill=s["color"])
    ty += kicker_size + 6
    fh = font(FB, head_size)
    lines = wrap(draw, s["head"], fh, w - 2 * pad)
    ty = text_block(draw, x + pad, ty, lines, fh, INK)
    ty += 3
    fs = font(FR, sub_size)
    slines = wrap(draw, sub_text if sub_text is not None else s["sub"], fs, w - 2 * pad)
    text_block(draw, x + pad, ty, slines, fs, GREY)
    return ty


def save_png(img, name):
    path = os.path.join(OUT, name)
    img.save(path, "PNG", optimize=True)
    size = os.path.getsize(path)
    if size > 1_048_576:
        q = img.convert("P", palette=Image.ADAPTIVE, colors=256)
        q.save(path, "PNG", optimize=True)
        size = os.path.getsize(path)
    print(name, img.size, size, "bytes")
    return path


# ================= VARIANT A — newspaper front page =================
def variant_a():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    banner(d, 0, 96)
    g = BY_KEY["gulf"]
    img.paste(cover(load(g["img"]), 1024, 300), (0, 96))
    # hero headline band
    d.rectangle([0, 396, 1024, 498], fill=WHITE)
    d.line([0, 498, 1024, 498], fill=LINE, width=2)
    d.text((16, 404), g["kicker"], font=font(FB, 20), fill=RED)
    d.text((16, 430), g["head"], font=font(FB, 32), fill=INK)
    d.text((16, 468), g["sub"], font=font(FR, 18), fill=GREY)
    # grid 2x2
    order = ["bridge", "summit", "alaska", "ebola"]
    for i, key in enumerate(order):
        cx = (i % 2) * 512
        cy = 498 + (i // 2) * 237
        if i % 2 == 1:
            d.line([512, cy, 512, cy + 237], fill=LINE, width=2)
        if i >= 2:
            d.line([0, cy, 1024, cy], fill=LINE, width=2)
        s = BY_KEY[key]
        cell = Image.new("RGB", (512, 237), WHITE)
        cd = ImageDraw.Draw(cell)
        story_cell(cell, cd, s, 0, 0, 512, 122, 23, 17, kicker_size=15, pad=14,
                   sub_text=s["short"])
        img.paste(cell, (cx, cy))
    # footer strip: cyclone
    c = BY_KEY["cyclone"]
    d.rectangle([0, 972, 1024, 1024], fill=DARKRED)
    img.paste(cover(load(c["img"]), 150, 52), (0, 972))
    d.text((166, 980), "PACIFIC", font=font(FB, 15), fill=GOLD)
    d.text((166, 998), c["head"], font=font(FB, 22), fill=WHITE)
    save_png(img, "variant-a.png")


# ================= VARIANT B — six-panel mosaic =================
def variant_b():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    banner(d, 0, 88, date_size=36, tag_size=17)
    for i, s in enumerate(STORIES):
        cx = (i % 2) * 512
        cy = 88 + (i // 2) * 312
        if i % 2 == 1:
            d.line([512, cy, 512, cy + 312], fill=LINE, width=2)
        if i >= 2:
            d.line([0, cy, 1024, cy], fill=LINE, width=2)
        cell = Image.new("RGB", (512, 312), WHITE)
        cd = ImageDraw.Draw(cell)
        story_cell(cell, cd, s, 0, 0, 512, 196, 24, 18, kicker_size=16, pad=14,
                   sub_text=s["short"])
        img.paste(cell, (cx, cy))
    save_png(img, "variant-b.png")


# ================= VARIANT C — lead story + list =================
def variant_c():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    banner(d, 0, 88, date_size=36, tag_size=17)
    g = BY_KEY["gulf"]
    img.paste(cover(load(g["img"]), 600, 600), (0, 88))
    # lead headline block under hero
    d.rectangle([0, 688, 600, 1024], fill=WHITE)
    d.line([0, 688, 600, 688], fill=RED, width=6)
    d.text((18, 706), g["kicker"], font=font(FB, 20), fill=RED)
    fh = font(FB, 40)
    lines = wrap(d, g["head"], fh, 600 - 36)
    ty = text_block(d, 18, 736, lines, fh, INK, leading=48)
    fs = font(FR, 22)
    slines = wrap(d, g["sub"], fs, 600 - 36)
    text_block(d, 18, ty + 12, slines, fs, GREY, leading=28)
    # right column: 5 stacked stories
    rest = ["bridge", "summit", "alaska", "ebola", "cyclone"]
    for i, key in enumerate(rest):
        ry = 88 + i * 187
        if i:
            d.line([600, ry, 1024, ry], fill=LINE, width=2)
        s = BY_KEY[key]
        img.paste(cover(load(s["img"]), 150, 187), (600, ry))
        tx = 766
        d.text((tx, ry + 12), s["kicker"], font=font(FB, 16), fill=s["color"])
        fh2 = font(FB, 24)
        lines = wrap(d, s["head"], fh2, 1024 - tx - 14)
        ty = text_block(d, tx, ry + 36, lines, fh2, INK, leading=29)
        fs2 = font(FR, 18)
        slines = wrap(d, s["short"], fs2, 1024 - tx - 14)
        text_block(d, tx, ty + 6, slines, fs2, GREY, leading=22)
    d.line([600, 88, 600, 1024], fill=LINE, width=2)
    save_png(img, "variant-c.png")


if __name__ == "__main__":
    variant_a()
    variant_b()
    variant_c()
