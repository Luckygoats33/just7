p = 'home-template.html'
s = open(p, encoding='utf-8').read()


def R(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


a = s.index('<div class="hero-copy">')
b = s.index('<div class="stage"', a)
hero = '''<div class="hero-copy">
    <h1><span class="rest">Laundry sheets with <span class="big7">just 7</span> ingredients.</span></h1>
    <p class="lead">Tear one off, drop it in the washer, done. No jug, no measuring, no fragrance, nothing from animals.</p>
    <ul class="gets">
      <li><b>Clean clothes</b><span>Made for everyday loads, HE or standard</span></li>
      <li><b>Nothing to hide</b><span>All 7 ingredients named on the front</span></li>
      <li><b>Kinder to pets</b><span>No perfume or essential oils on their bedding</span></li>
    </ul>
    <div class="checks"><span>$15 a pouch, 60 loads, free shipping</span><span>90 days to love it, keep the pouch</span></div>
    <div class="cta-row"><a class="btn sun" href="products/just-7/index.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 4.5h2.2l2.1 10.2a1.5 1.5 0 0 0 1.5 1.2h7.9a1.5 1.5 0 0 0 1.5-1.1l1.7-6.3H7"/><circle cx="10" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/></svg>Shop Just 7</a><a class="btn ghost" href="#ingredients">See all 7</a></div>
  </div>
  '''
s = s[:a] + hero + s[b:]
css = '''
/* hero: say what it is */
.hero h1{font-size:clamp(2.6rem,7vw,5rem)!important;line-height:.98!important}
.hero h1 .big7{font-size:1em!important;line-height:1!important;transform:rotate(-3deg);background:var(--sun);color:#2A2205!important;padding:0 .14em;border-radius:.16em;display:inline-block;animation:pop .8s cubic-bezier(.3,1.6,.5,1) both}
@keyframes pop{from{transform:scale(.3) rotate(-24deg)}to{transform:rotate(-3deg)}}
.gets{list-style:none;padding:0;display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,170px),1fr))}
.gets li{background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.35);border-radius:16px;padding:12px 14px;display:grid;gap:2px}
.gets b{font:900 1.12rem var(--f-display);color:#fff}
.gets span{font-size:.88rem;color:#EAF5FD;line-height:1.35}
'''
R('/* footer */', css + '\n/* footer */')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
