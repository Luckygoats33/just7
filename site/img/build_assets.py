"""Write docs/assets product images: full jpg + webp, plus 600w and 300w webp for srcset."""
from PIL import Image
R="/workspace/just7"; A=f"{R}/docs/assets"
src={1:"01-hero",2:"02-ingredients",3:"03-how-to-use",4:"04-size-value",5:"05-giveback"}
for i,n in src.items():
    im=Image.open(f"{R}/product-images/{n}.png").convert("RGB")
    base=f"{A}/just-7-product-{i}"
    if i in (1,2,4):
        im.save(base+".jpg",quality=82,optimize=True,progressive=True); im.save(base+".webp",quality=80,method=6)
        im.save(f"{R}/product-images/web/just-7-product-{i}.jpg",quality=82,optimize=True,progressive=True); im.save(f"{R}/product-images/web/just-7-product-{i}.webp",quality=80,method=6)
    for w in (600,300):
        im.resize((w,w),Image.LANCZOS).save(f"{base}-{w}.webp",quality=78,method=6)
for n in ("just-7-pouch","just-7-pouch-front"):
    im=Image.open(f"{R}/product-images/src/{n}.jpg").convert("RGB")
    im.save(f"{A}/{n}.jpg",quality=85,optimize=True,progressive=True); im.save(f"{A}/{n}.webp",quality=82,method=6)
    w=im.width//2; im.resize((w,im.height*w//im.width),Image.LANCZOS).save(f"{A}/{n}-{w}.webp",quality=80,method=6)
