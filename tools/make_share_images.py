#!/usr/bin/env python3
"""Makes the link-preview pictures (1200 x 630) shown when a page is shared on Facebook, WhatsApp, LinkedIn, X, etc.
Run: python3 tools/make_share_images.py   (writes docs/assets/share/*.jpg)"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "docs" / "assets"
OUT = A / "share"
F = ROOT / "tools" / "fonts"
W, H = 1200, 630
NAVY, DEEP, FG, MUTED = (16, 48, 77), (10, 34, 56), (245, 249, 252), (175, 198, 217)

CARDS = {
    # name: (eyebrow, title, line, accent colour, picture(s))
    "site": ("People of the World", "Knowledge. Morality.\nUnity. Peace.", "Seven doors into the work of Shareef Ali Rashada", (108, 192, 74), ["logo"]),
    "seekers": ("The Portal Opens · free to read", "The story you were\nnever told.", "Jesus, Lucifer, Adam and Eve, and Melchizedek", (242, 169, 59), ["cover-portal"]),
    "urantia": ("For Urantia Book readers", "The story you love,\ntold a new way.", "And an easy way to share it with the people you love", (217, 102, 140), ["cover-portal"]),
    "science": ("Graviton Pressure Theory", "How does gravity\nreally work?", "Gravity as a push from outside, with a mechanism you can test", (46, 134, 222), ["cover-gpt"]),
    "builders": ("End Poverty by Design", "A world without\npoverty by 2050.", "Civic Credits · Poverty Elimination Centers · LifeLink", (76, 175, 80), ["logo"]),
    "music": ("That Brother Ali", "Music to ease\nyour mind.", "Jazz, acoustic and new-age albums, free to stream", (224, 78, 63), ["logo"]),
    "easykey": ("EasyKey Music", "See the key.\nPress the key.", "Play piano without reading a staff. First song free.", (155, 107, 211), ["cover-easykey"]),
    "ai": ("The Open Library", "Every book, paper\nand plan. Free.", "Plain text for people, search engines and AI", (41, 182, 207), ["logo"]),
    "play": ("The Decision Game", "Decide. Fast.", "Free brain training with an online leaderboard", (28, 143, 169), ["logo"]),
    "books": ("Books by Shareef Ali Rashada", "Imagine. Understand.\nBuild.", "Novels, revelation, physics and music", (108, 192, 74), ["cover-pow", "cover-portal", "cover-gpt"]),
    "shop": ("The People of the World shop", "Books and gifts that\ncarry the message.", "Every purchase supports the mission", (108, 192, 74), ["cover-portal", "cover-pow"]),
}


def font(name, size):
    return ImageFont.truetype(str(F / name), size)


def picture(img, names):
    if names == ["logo"]:
        logo = Image.open(A / "logo.webp").convert("RGBA").resize((330, 330), Image.LANCZOS)
        img.alpha_composite(logo, (W - 330 - 90, (H - 330) // 2 - 10))
        return W - 330 - 90
    covers = [Image.open(A / f"{n}.webp").convert("RGBA") for n in names]
    hgt = 440 if len(covers) == 1 else 380
    covers = [c.resize((round(c.width * hgt / c.height), hgt), Image.LANCZOS) for c in covers]
    step = 120 if len(covers) > 1 else 0
    total = covers[0].width + step * (len(covers) - 1)
    x0 = W - 90 - total
    for i, c in enumerate(covers):
        x, y = x0 + i * step, (H - hgt) // 2 - 10 + (len(covers) - 1 - i) * 12 - (len(covers) - 1) * 6
        shadow = Image.new("RGBA", (c.width + 60, c.height + 60), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle((30, 36, 30 + c.width, 36 + c.height), 10, fill=(0, 0, 0, 120))
        img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)), (x - 30, y - 30))
        mask = Image.new("L", c.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 8, fill=255)
        img.paste(c, (x, y), mask)
    return x0


def card(name, eyebrow, title, line, accent, pics):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(img)
    for y in range(H):  # gentle vertical gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(round(NAVY[i] * (1 - t) + DEEP[i] * t) for i in range(3)) + (255,))
    d.rectangle((0, 0, 14, H), fill=accent)
    left = picture(img, pics)
    d = ImageDraw.Draw(img)
    x = 80
    room = left - x - 50
    d.text((x, 92), eyebrow.upper(), font=font("Inter-SemiBold.otf", 24), fill=accent, spacing=0)
    size = 72
    while True:  # largest title size that leaves clear space before the picture
        tf = font("fraunces600.ttf", size)
        if max(d.textlength(l, font=tf) for l in title.split("\n")) <= room or size <= 40: break
        size -= 2
    d.multiline_text((x, 140), title, font=tf, fill=FG, spacing=10)
    tb = d.multiline_textbbox((x, 140), title, font=tf, spacing=10)
    lf = font("Inter-Medium.otf", 28)
    words, lines, cur = line.split(), [], ""
    for w in words:  # wrap to the text column
        test = (cur + " " + w).strip()
        if d.textlength(test, font=lf) > min(560, room) and cur: lines.append(cur); cur = w
        else: cur = test
    lines.append(cur)
    d.multiline_text((x, tb[3] + 30), "\n".join(lines), font=lf, fill=MUTED, spacing=8)
    small = Image.open(A / "logo.webp").convert("RGBA").resize((52, 52), Image.LANCZOS)
    img.alpha_composite(small, (x, H - 52 - 56))
    d.text((x + 68, H - 52 - 56 + 12), "peopleoftheworld.net", font=font("Inter-SemiBold.otf", 24), fill=FG)
    img.convert("RGB").save(OUT / f"{name}.jpg", quality=88, optimize=True, progressive=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for k, v in CARDS.items():
        card(k, *v)
    print("made", len(CARDS), "share images in", OUT)
