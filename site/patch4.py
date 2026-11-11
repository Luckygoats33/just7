import re
p = 'home-template.html'
s = open(p, encoding='utf-8').read()
a = s.index('<section class="sec lineup" id="products">')
b = s.index('</section>', a) + len('</section>')
show = '''<section class="sec lineup" id="products"><div class="w showcase">
  <div class="sc-img"><picture><source srcset="assets/just-7-product-1.webp" type="image/webp"><img src="assets/just-7-product-1.jpg" alt="Just 7 pouch with two sheets: 30 sheets, 60 loads" width="1200" height="1200" loading="lazy"></picture></div>
  <div class="sc-copy">
    <p class="eyebrow">Meet the sheet</p>
    <h2 class="big-letters">Just 7.</h2>
    <p class="sc-lead">The everyday sheet. Seven ingredients, fragrance-free, 30 sheets for up to 60 loads.</p>
    <ul class="sc-facts"><li><b>30</b><span>sheets a pouch</span></li><li><b>60</b><span>loads</span></li><li><b>$0.25</b><span>a load on subscription</span></li></ul>
    <div class="cta-row"><a class="btn sun" href="products/just-7/index.html">Shop Just 7</a><a class="btn ghost" href="#ingredients">What's inside</a></div>
  </div>
</div></section>'''
s = s[:a] + show + s[b:]
css = '''
/* showcase */
.showcase{display:grid;gap:clamp(28px,5vw,56px);align-items:center}
@media (min-width:860px){.showcase{grid-template-columns:1fr 1fr}}
.sc-img{border-radius:28px;overflow:hidden;box-shadow:0 0 0 5px var(--sun),0 24px 50px rgba(0,0,0,.35);transform:rotate(-1.5deg)}
.sc-copy{display:grid;gap:18px;min-width:0}
.sc-copy .big-letters{color:var(--paper)}
.sc-lead{font-size:1.2rem;color:var(--paper);opacity:.85}
.sc-facts{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:12px}
.sc-facts li{background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.18);border-radius:18px;padding:12px 18px;display:grid}
.sc-facts b{font:900 2rem/1 var(--f-display);color:var(--sun)}
.sc-facts span{font-size:.9rem;opacity:.85}
'''
s = s.replace('/* footer */', css + '\n/* footer */', 1)
s = s.replace(' For heavy food and protein stains, pretreat or wait for Just 9 with enzymes.', ' For heavy food and protein stains, pretreat first.')
open(p, 'w', encoding='utf-8').write(s)
print('Just 5' in s, 'Just 9' in s)
