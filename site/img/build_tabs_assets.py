"""v2 tabs: product-images/*.png (1200 px renders) + pouch v3 art -> docs/assets (jpg + webp at 1200/600/300).
Run from repo root: python3 site/img/build_tabs_assets.py"""
import os
from PIL import Image
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PI, A = os.path.join(R, "product-images"), os.path.join(R, "docs", "assets")
SRC = {1: "01-hero", 2: "02-ingredients", 3: "03-how-to-use", 4: "04-size-value", 5: "05-giveback", 6: "06-fizz", 7: "07-ingredients-flatlay", 8: "08-closeup"}
os.makedirs(os.path.join(PI, "web"), exist_ok=True)
for n, f in SRC.items():
    im = Image.open(os.path.join(PI, f + ".png")).convert("RGB").resize((1200, 1200), Image.LANCZOS)
    im.save(os.path.join(A, f"just-7-product-{n}.jpg"), quality=80, optimize=True, progressive=True)
    im.save(os.path.join(PI, "web", f"just-7-product-{n}.jpg"), quality=80, optimize=True, progressive=True)
    im.save(os.path.join(A, f"just-7-product-{n}.webp"), quality=76, method=6)
    im.save(os.path.join(PI, "web", f"just-7-product-{n}.webp"), quality=76, method=6)
    for w in (600, 300):
        im.resize((w, w), Image.LANCZOS).save(os.path.join(A, f"just-7-product-{n}-{w}.webp"), quality=74, method=6)
# pouch shots (cart thumbnail, shop card) from the v3 tabs print art, on the site paper colour
front = Image.open(os.path.join(PI, "src", "tabs", "pouch-front.jpg")).convert("RGB")
back = Image.open(os.path.join(PI, "src", "tabs", "pouch-back.jpg")).convert("RGB")
def card(img, W, H, pad=0.06, bg=(250, 250, 247)):
    c = Image.new("RGB", (W, H), bg); h = int(H * (1 - 2 * pad)); w = int(h * img.width / img.height)
    if w > W * (1 - 2 * pad): w = int(W * (1 - 2 * pad)); h = int(w * img.height / img.width)
    c.paste(img.resize((w, h), Image.LANCZOS), ((W - w) // 2, (H - h) // 2)); return c
p = card(front, 672, 864); p.save(os.path.join(A, "just-7-pouch.jpg"), quality=82, optimize=True); p.save(os.path.join(A, "just-7-pouch.webp"), quality=78, method=6)
p.resize((336, 432), Image.LANCZOS).save(os.path.join(A, "just-7-pouch-336.webp"), quality=78, method=6)
for nm, img in (("front", front), ("back", back)):
    q = card(img, 480, 720, pad=0.0); q.save(os.path.join(A, f"just-7-pouch-{nm}.jpg"), quality=82, optimize=True); q.save(os.path.join(A, f"just-7-pouch-{nm}.webp"), quality=78, method=6)
card(front, 240, 360, pad=0.0).save(os.path.join(A, "just-7-pouch-front-240.webp"), quality=78, method=6)
for f in sorted(os.listdir(A)):
    if f.startswith(("just-7-product", "just-7-pouch")): print(f, os.path.getsize(os.path.join(A, f)) // 1024, "KB")
# waitlist "Learn more" tiles are crops of the gallery renders
Image.open(os.path.join(PI, "03-how-to-use.png")).convert("RGB").crop((40, 330, 1160, 1030)).resize((560, 350), Image.LANCZOS).save(os.path.join(A, "tile-learn.webp"), quality=78, method=6)
Image.open(os.path.join(PI, "02-ingredients.png")).convert("RGB").crop((0, 40, 1200, 790)).resize((560, 350), Image.LANCZOS).save(os.path.join(A, "tile-ingredients.webp"), quality=78, method=6)
