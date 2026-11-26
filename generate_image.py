#!/usr/bin/env python3
"""Draw a 1024x1024 front page summing up world news on 26 November 2026.

Pure Pillow drawing, no network, no photos, no copied artwork.
Deterministic: fixed text, fixed geometry, fixed colours, no timestamps
and no randomness, so two runs write byte-identical PNG files.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

INK = (17, 17, 17)
PAPER = (247, 243, 232)
NAVY = (27, 42, 74)
RED = (180, 35, 24)
TEAL = (14, 116, 110)
GOLD = (176, 132, 32)
LIGHT = (255, 255, 255)
CARD = (255, 255, 255)
GREY = (90, 90, 90)
LINE = (200, 192, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width) or [""])
    out = []
    for line in lines:
        while draw.textlength(line, font=fnt) > width and " " in line:
            cut = line.rfind(" ", 0, int(len(line) * width / max(1, draw.textlength(line, font=fnt))))
            if cut <= 0:
                break
            out.append(line[:cut])
            line = line[cut + 1:]
        out.append(line)
    return out


def draw_text(draw, xy, text, fnt, fill=INK, anchor="la"):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def centred(draw, y, text, fnt, fill=INK):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def pictogram(draw, box, kind):
    """Small pictogram drawn in code inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    if kind == "tariff":
        base = y1 - 18
        bars = [(0.22, 52, NAVY), (0.45, 78, RED), (0.68, 38, TEAL)]
        for frac, hgt, col in bars:
            bx = x0 + int((x1 - x0) * frac)
            draw.rectangle([bx, base - hgt, bx + 34, base], fill=col)
        draw.line([x0 + 8, base, x1 - 8, base], fill=INK, width=4)
        draw.text((cx, y0 + 4), "%", font=font(SANS_B, 44), fill=RED, anchor="ma")
    elif kind == "oil":
        draw.rectangle([cx - 34, cy - 10, cx + 34, cy + 42], fill=NAVY)
        draw.rectangle([cx - 34, cy - 26, cx + 34, cy - 10], fill=RED)
        draw.ellipse([cx - 12, cy - 52, cx + 12, cy - 24], fill=(255, 170, 0))
        draw.polygon([(cx - 16, cy - 26), (cx, cy - 62), (cx + 16, cy - 26)], fill=(255, 170, 0))
        draw.line([x0 + 10, y1 - 10, x1 - 10, y1 - 10], fill=INK, width=4)
    elif kind == "fire":
        draw.polygon([(cx, y0 + 6), (cx + 30, cy + 10), (cx + 14, cy + 34),
                      (cx + 34, cy + 18), (cx + 10, y1 - 22), (cx - 10, y1 - 22),
                      (cx - 34, cy + 18), (cx - 14, cy + 34), (cx - 30, cy + 10)],
                     fill=(255, 120, 0))
        draw.ellipse([cx - 14, cy + 8, cx + 14, cy + 40], fill=(255, 200, 0))
        draw.line([x0 + 10, y1 - 10, x1 - 10, y1 - 10], fill=INK, width=4)
    elif kind == "space":
        draw.ellipse([x0 + 6, y0 + 6, x1 - 6, y1 - 6], outline=NAVY, width=4)
        draw.polygon([(cx - 10, cy - 44), (cx + 10, cy - 44), (cx + 6, cy + 6),
                      (cx - 6, cy + 6)], fill=RED)
        draw.polygon([(cx - 10, cy - 44), (cx, cy - 62), (cx + 10, cy - 44)], fill=NAVY)
        draw.polygon([(cx - 10, cy - 10), (cx - 30, cy + 18), (cx - 10, cy + 6)], fill=TEAL)
        draw.polygon([(cx + 10, cy - 10), (cx + 30, cy + 18), (cx + 10, cy + 6)], fill=TEAL)
        draw.ellipse([cx - 4, cy + 14, cx + 4, cy + 26], fill=(255, 170, 0))
        draw.ellipse([x0 + 14, y0 + 18, x0 + 22, y0 + 26], fill=GOLD)
        draw.ellipse([x1 - 24, y1 - 26, x1 - 16, y1 - 18], fill=GOLD)
    elif kind == "shirt":
        draw.polygon([(cx - 44, y0 + 22), (cx - 18, y0 + 8), (cx + 18, y0 + 8),
                      (cx + 44, y0 + 22), (cx + 30, y0 + 44), (cx + 26, y0 + 40),
                      (cx + 26, y1 - 26), (cx - 26, y1 - 26), (cx - 26, y0 + 40),
                      (cx - 30, y0 + 44)], fill=TEAL)
        draw.arc([cx - 18, y0 + 2, cx + 18, y0 + 30], 0, 180, fill=LIGHT, width=4)
        draw.line([cx + 34, y1 - 14, cx + 52, y1 - 34], fill=RED, width=6)
        draw.polygon([(cx + 52, y1 - 34), (cx + 40, y1 - 34), (cx + 52, y1 - 22)], fill=RED)
    elif kind == "bank":
        base = y1 - 16
        for i in range(3):
            bx = x0 + 14 + i * 38
            draw.rectangle([bx, cy - 18, bx + 24, base], fill=NAVY)
        draw.polygon([(x0 + 6, cy - 18), (cx, y0 + 10), (x1 - 6, cy - 18)], fill=RED)
        draw.line([x0 + 10, base, x1 - 10, base], fill=INK, width=4)


def card(draw, x, y, w, h, tag, headline, body, pic):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=NAVY)
    draw_text(draw, (x + 12, y + 6), tag, font(SANS_B, 15), fill=LIGHT)
    px0, py0 = x + w - 128, y + 42
    pictogram(draw, (px0, py0, px0 + 112, py0 + 112), pic)
    hl = wrap(draw, headline, font(SANS_B, 20), w - 156)
    ty = y + 44
    for line in hl[:2]:
        draw_text(draw, (x + 12, ty), line, font(SANS_B, 20))
        ty += 24
    by = ty + 6
    for line in wrap(draw, body, font(SANS, 15), w - 156)[:5]:
        draw_text(draw, (x + 12, by), line, font(SANS, 15), fill=(40, 40, 40))
        by += 18


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=8)

    centred(d, 22, "THE WORLD IN ONE PAGE", font(SERIF_B, 52), fill=NAVY)
    centred(d, 92, "Six stories from around the world", font(SANS, 20), fill=GREY)
    d.line([32, 128, W - 32, 128], fill=RED, width=4)
    centred(d, 140, "THURSDAY, 26 NOVEMBER 2026", font(SANS_B, 30), fill=RED)

    # Lead story: US tariffs
    lx, ly, lw, lh = 32, 182, 960, 196
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=LINE, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 32], fill=RED)
    draw_text(d, (lx + 12, ly + 6), "LEAD  |  TRADE", font(SANS_B, 16), fill=LIGHT)
    pictogram(d, (lx + lw - 170, ly + 44, lx + lw - 30, ly + 184), "tariff")
    ty = ly + 44
    for line in wrap(d, "US proposes new tariffs on 14 partners", font(SANS_B, 29), lw - 190):
        draw_text(d, (lx + 14, ty), line, font(SANS_B, 29))
        ty += 35
    by = ty + 4
    lead = ("Washington proposed new duties on 14 major trading partners after a "
            "Section 301 probe into excess factory capacity. China faces the "
            "highest rate, an extra 20 percent. The duties are proposed, not yet "
            "in force, with a hearing first. Source: Reuters.")
    for line in wrap(d, lead, font(SANS, 18), lw - 190):
        draw_text(d, (lx + 14, by), line, font(SANS, 18), fill=(40, 40, 40))
        by += 23

    # Four cards in a 2 by 2 grid
    cw, ch, gap = 472, 208, 16
    card(d, 32, 394, cw, ch, "ENERGY",
         "Houthis claim Saudi refinery attack; oil jumps",
         "Yemen's Houthis said they attacked Saudi Arabia's Ras Tanura refinery, "
         "its largest. Brent crude settled 3.5 percent higher at $94.61 a barrel. Reuters.",
         "oil")
    card(d, 520, 394, cw, ch, "EGYPT",
         "31 killed in Cairo tanker fire",
         "A fuel tanker crashed and caught fire on Cairo's Ring Road in Giza, "
         "killing at least 31 people and injuring 21, Egypt's health ministry said. CNN.",
         "fire")
    card(d, 32, 618, cw, ch, "SPACE",
         "First Pakistani boards China's space station",
         "Muhammad Zeeshan Ali flew on Shenzhou-24 and became the first Pakistani "
         "in orbit and the first foreign astronaut to board Tiangong. Reuters.",
         "space")
    card(d, 520, 618, cw, ch, "LABOUR",
         "Bangladesh raises garment pay 36 percent",
         "After weeks of protests, Bangladesh raised the garment minimum wage to "
         "17,000 taka a month from 12,500 taka. It takes effect 1 December. Reuters.",
         "shirt")

    # Bottom wide card: South Korea
    bx, byy, bw, bh = 32, 842, 960, 112
    d.rectangle([bx, byy, bx + bw, byy + bh], fill=CARD, outline=LINE, width=2)
    d.rectangle([bx, byy, bx + bw, byy + 30], fill=TEAL)
    draw_text(d, (bx + 12, byy + 6), "ECONOMY  |  SOUTH KOREA", font(SANS_B, 15), fill=LIGHT)
    pictogram(d, (bx + bw - 128, byy + 36, bx + bw - 16, byy + 106), "bank")
    draw_text(d, (bx + 12, byy + 38), "South Korea raises rates to 3.25 percent",
              font(SANS_B, 22))
    body = ("The Bank of Korea raised its base rate by 25 basis points to 3.25 percent "
            "on 26 November, resuming tightening as inflation stayed above target. Reuters.")
    yy = byy + 68
    for line in wrap(d, body, font(SANS, 16), bw - 140):
        draw_text(d, (bx + 12, yy), line, font(SANS, 16), fill=(40, 40, 40))
        yy += 20

    centred(d, 966, "Sources: Reuters, CNN, AP, Nature. All six stories reported 26 November 2026.",
            font(SANS, 14), fill=GREY)
    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
