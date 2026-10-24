#!/usr/bin/env python3
"""Square 3000 x 3000 cover for the audiobook feed (Apple Podcasts and Spotify need a square image of 1400-3000 px)."""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
ROOT = pathlib.Path(__file__).resolve().parent.parent
A, F = ROOT / "docs" / "assets", ROOT / "tools" / "fonts"
S = 3000
cover = Image.open(A / "cover-portal.webp").convert("RGB")
bg = cover.resize((S, round(S * cover.height / cover.width)), Image.LANCZOS).crop((0, 400, S, 400 + S))
bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(60))).enhance(0.38)
h = 1900
front = cover.resize((round(cover.width * h / cover.height), h), Image.LANCZOS)
x, y = 260, (S - h) // 2
shadow = Image.new("RGBA", (front.width + 200, front.height + 200), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle((100, 120, 100 + front.width, 120 + front.height), 30, fill=(0, 0, 0, 170))
bg.paste(shadow.filter(ImageFilter.GaussianBlur(40)), (x - 100, y - 100), shadow.filter(ImageFilter.GaussianBlur(40)))
mask = Image.new("L", front.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, front.width - 1, front.height - 1), 26, fill=255)
bg.paste(front, (x, y), mask)
d = ImageDraw.Draw(bg)
tx = x + front.width + 170
d.text((tx, 980), "THE", font=ImageFont.truetype(str(F / "Inter-SemiBold.otf"), 120), fill=(242, 169, 59))
d.text((tx, 1110), "AUDIO\nBOOK", font=ImageFont.truetype(str(F / "fraunces600.ttf"), 330), fill=(245, 249, 252), spacing=10)
d.text((tx, 1900), "Complete · 63 chapters", font=ImageFont.truetype(str(F / "Inter-Medium.otf"), 92), fill=(210, 222, 233))
d.text((tx, 2040), "Free to listen", font=ImageFont.truetype(str(F / "Inter-Medium.otf"), 92), fill=(210, 222, 233))
bg.save(A / "audiobook-cover.jpg", quality=86, optimize=True, progressive=True)
print("saved", A / "audiobook-cover.jpg")
