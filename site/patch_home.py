import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()


def R(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)


R('family=Nunito:wght@700;800;900&family=Inter:wght@400;500;600', 'family=Nunito:wght@500;600;700;800;900')
R('--f-body:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;', '--f-body:"Nunito",ui-rounded,"SF Pro Rounded",system-ui,sans-serif;')
R('font:400 17px/1.6 var(--f-body)', 'font:600 18px/1.6 var(--f-body)')
R('.hero{position:relative;overflow:hidden;', '.hero{position:relative;overflow:hidden;background:var(--sky);color:var(--on-color);')
R('.hero h1{font-size:clamp(3rem,9.5vw,6rem);line-height:.92}',
  '.hero h1{font-size:clamp(3.4rem,11vw,7.4rem);line-height:.9;color:var(--on-color)}\n.hero .eyebrow{color:var(--sun)}\n.hero .lead{color:#EAF5FD}')
R('.hero h1 .big7{display:inline-block;color:var(--sky);', '.hero h1 .big7{display:inline-block;color:var(--sun);')
R('.hero h1 .rest em{font-style:normal;color:var(--mint)}',
  '.hero h1 .rest em{font-style:normal;color:#10291D;background:var(--mint);padding:0 .12em;border-radius:.14em}')
R('border-radius:46% 54% 50% 50%/52% 46% 54% 48%;background:var(--sky);', 'border-radius:46% 54% 50% 50%/52% 46% 54% 48%;background:#FFFFFF;')
R('.chip.s{color:var(--sky-deep);background:var(--sky-tint)}\n.chip.m{color:var(--mint-deep);background:var(--mint-tint)}\n.chip.p{color:var(--plum);background:var(--plum-tint)}\n:root:not([data-theme="light"]) .chip{color:var(--ink)}',
  '.hero .chip{color:var(--on-color);border-color:rgba(255,255,255,.75);background:rgba(255,255,255,.12)}')
R('<p class="eyebrow" style="color:var(--mint-deep)">Laundry detergent sheets</p>', '<p class="eyebrow">Laundry detergent sheets</p>')
R('.btn.ghost{background:var(--card);color:var(--ink);box-shadow:inset 0 0 0 2.5px var(--ink),0 5px 0 var(--ink)}\n.btn.ghost:hover{color:var(--ink)}',
  '.btn.ghost{background:#FFFFFF;color:#22302B;box-shadow:0 5px 0 rgba(0,0,0,.2)}\n.btn.ghost:hover{color:#22302B}\n.btn.sun{background:var(--sun);color:#2A2205;box-shadow:0 5px 0 #B98A12}\n.btn.sun:hover{color:#2A2205;box-shadow:0 7px 0 #B98A12}')
R('<a class="btn" href="products/just-7/index.html"><svg', '<a class="btn sun" href="products/just-7/index.html"><svg')
R('.eyebrow{', '.big-letters{font:900 clamp(3rem,10vw,6.6rem)/.9 var(--f-display);letter-spacing:-.035em}\n.eyebrow{')

extra = open(sys.argv[2], encoding='utf-8').read()
css, lineup, reviews = extra.split('<!--SPLIT-->')
R('/* footer */', css + '\n/* footer */')
R('<section class="sec count">', lineup + '\n<section class="sec count">')
R('<section class="sec wl" id="waitlist">', reviews + '\n<section class="sec wl" id="waitlist">')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
