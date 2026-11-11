import os, shutil
import prices
import topbar
import footnote
S = r'C:\Users\willw\AppData\Local\Temp\claude\d4d7ba6eb5afc097\275108eb-5c48-4af4-b45a-03fa3ae9be1c\scratchpad'
A = os.path.join(S, r'artifact-files\92ae9c9c-dc94-4f43-b46b-15f6e3b8e568')
V = os.path.join(S, 'verify')
OUT = os.path.join(S, 'build')
skin = open('skin.html', encoding='utf-8').read()
motion = open('motion.html', encoding='utf-8').read()
band = '<div class="cband" aria-hidden="true"><span></span><span></span><span></span></div>'
override = {'products/just-7/index.html': V, 'collections/all/index.html': V}
done = 0
for root, _, files in os.walk(A):
    for f in files:
        if not f.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(root, f), A).replace('\\', '/')
        if rel == 'index.html':
            continue  # homepage is built separately
        src = os.path.join(override.get(rel, A), rel)
        s = open(src, encoding='utf-8').read()
        if 'id="j7-skin"' not in s:
            s = s.replace('<div class="pbar">', skin + '<div class="pbar">', 1)
        if 'class="cband"' not in s:
            i = s.find('</header>')
            if i > -1:
                s = s[:i + 9] + band + s[i + 9:]
        if 'id="j7-motion"' not in s:
            i = s.rfind('</body>')
            s = (s[:i] + motion + s[i:]) if i > -1 else s + motion
        s = prices.apply(rel, s)
        s = topbar.apply(rel, s)
        s = footnote.apply(rel, s)
        out = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8', newline='').write(s)
        done += 1
# homepage gets motion too
h = open('index.html', encoding='utf-8').read()
if 'id="j7-motion"' not in h:
    h = h + '\n' + motion
h = prices.apply('index.html', h)
h = footnote.apply('index.html', h)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='').write(h)
print(done, 'pages + homepage')
