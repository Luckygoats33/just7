"""Brand rule (Will, Nov 11): no Pet-safe or Plant-based icons. Inpaints the two outer
icons on the pouch front (keeps Vegan and No musks, which stay centered as a pair).
Originals are kept as *-orig.jpg next to the source."""
import cv2, numpy as np, os, shutil
R = "/workspace/just7"
SRC = f"{R}/product-images/src/just-7-pouch-front.jpg"
ORIG = SRC.replace(".jpg", "-orig.jpg")
if not os.path.exists(ORIG): shutil.copy2(SRC, ORIG)
src = cv2.imread(ORIG)
rects = [(14, 545, 128, 650), (352, 545, 466, 650)]
mask = np.zeros(src.shape[:2], np.uint8)
for x0, y0, x1, y1 in rects: mask[y0:y1, x0:x1] = 255
def clean(img, m):
    return cv2.inpaint(img, cv2.dilate(m, np.ones((3, 3), np.uint8)), 5, cv2.INPAINT_TELEA)
cv2.imwrite(SRC, clean(src, mask), [cv2.IMWRITE_JPEG_QUALITY, 92])
sift = cv2.SIFT_create()
k1, d1 = sift.detectAndCompute(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY), None)
for name in ["just-7-pouch.jpg"]:
    p = f"{R}/product-images/src/{name}"; o = p.replace(".jpg", "-orig.jpg")
    if not os.path.exists(o): shutil.copy2(p, o)
    ban = cv2.imread(o)
    k2, d2 = sift.detectAndCompute(cv2.cvtColor(ban, cv2.COLOR_BGR2GRAY), None)
    m = [a for a, b in cv2.BFMatcher().knnMatch(d1, d2, k=2) if a.distance < 0.7 * b.distance]
    H, inl = cv2.findHomography(np.float32([k1[x.queryIdx].pt for x in m]), np.float32([k2[x.trainIdx].pt for x in m]), cv2.RANSAC, 4.0)
    print(name, len(m), int(inl.sum()))
    wm = cv2.warpPerspective(mask, H, (ban.shape[1], ban.shape[0]))
    cv2.imwrite(p, clean(ban, ((wm > 0) * 255).astype(np.uint8)), [cv2.IMWRITE_JPEG_QUALITY, 92])
