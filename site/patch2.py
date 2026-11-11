p = 'home-template.html'
s = open(p, encoding='utf-8').read()


def R(a, b, n=1):
    global s
    assert s.count(a) >= 1, a[:70]
    s = s.replace(a, b, n)


# accent serif for home-keeping touches only
R('family=Nunito:wght@500;600;700;800;900', 'family=Nunito:wght@500;600;700;800;900&family=Playfair+Display:ital,wght@1,600;1,700')
R('--f-body:"Nunito"', '--f-script:"Playfair Display",Georgia,"Times New Roman",serif;\n  --f-body:"Nunito"')

css = '''
/* announcement bar */
.topbar{background:var(--ink);color:var(--paper);text-align:center;font:800 .86rem/1.3 var(--f-display);padding-block:9px}
.topbar .w{display:flex;justify-content:center;flex-wrap:wrap;gap:4px 18px}
.topbar b{color:var(--sun)}
/* hero trust lines + mobile order */
.checks{display:grid;gap:6px;font:800 1rem var(--f-display)}
.checks span{display:flex;gap:8px;align-items:center}
.checks span::before{content:"\\2713";width:22px;height:22px;border-radius:50%;background:var(--sun);color:#2A2205;display:grid;place-items:center;font-size:.8rem;flex:none}
.hero h1 .rest em{line-height:1;display:inline-block}
@media (max-width:899px){
  .hero{padding-block:28px 44px}
  .hero-copy{gap:18px}
  .hero .stage{max-width:380px}
  .cta-row .btn{flex:1 1 100%}
  .hero .chips{display:none}
}
/* icon strip */
.icons{background:var(--card);border-bottom:1px solid var(--line)}
.icons .w{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:14px;padding-block:22px}
.icons div{display:flex;gap:10px;align-items:center;font:800 .95rem/1.2 var(--f-display)}
.icons svg{width:34px;height:34px;flex:none;color:var(--t-sky)}
/* laundry day: home-keeping guides */
.keep{background-color:var(--mint-tint);background-image:linear-gradient(90deg,color-mix(in srgb,var(--mint) 22%,transparent) 50%,transparent 50%),linear-gradient(color-mix(in srgb,var(--mint) 22%,transparent) 50%,transparent 50%);background-size:28px 28px}
.keep .head{display:grid;gap:10px;max-width:760px}
.script{font-family:var(--f-script);font-style:italic;font-weight:700;letter-spacing:0}
.keep h2 .script{color:var(--t-mint)}
.keep .eyebrow{color:var(--t-plum)}
.guides{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));margin-top:clamp(28px,5vw,44px)}
.guide{background:var(--card);border-radius:6px;padding:26px 24px 22px;display:grid;gap:10px;align-content:start;text-decoration:none;color:var(--ink);box-shadow:var(--shadow);position:relative;border-top:10px solid var(--c);transition:transform .2s}
.guide:hover{transform:translateY(-4px) rotate(-.5deg);color:var(--ink)}
.guide .kind{font:900 .74rem var(--f-display);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.guide h3{font-size:1.35rem}
.guide p{color:var(--mute);font-size:.95rem}
.guide .tip{font-family:var(--f-script);font-style:italic;font-size:1.05rem;color:var(--ink);border-top:1px dashed var(--line);padding-top:10px}
.guide .go{font:900 .95rem var(--f-display);color:var(--t-sky)}
.cal{margin-top:clamp(28px,5vw,44px);background:var(--card);border-radius:6px;box-shadow:var(--shadow);padding:clamp(20px,4vw,32px);display:grid;gap:16px}
.cal h3{font-size:1.6rem}
.cal-grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr))}
.cal-grid div{border:2px solid var(--line);border-radius:12px;padding:14px 16px;display:grid;gap:4px}
.cal-grid b{font:900 1.05rem var(--f-display)}
.cal-grid span{color:var(--mute);font-size:.92rem}
.cal-grid em{font-style:normal;font:900 .74rem var(--f-display);letter-spacing:.12em;text-transform:uppercase;color:var(--t-mint)}
'''
R('/* footer */', css + '\n/* footer */')

R('<a class="sr" href="#main">Skip to content</a>',
  '<a class="sr" href="#main">Skip to content</a>\n<div class="topbar"><div class="w"><span>Free shipping on every subscription</span><span><b>90-day</b> keep-the-pouch promise</span></div></div>')

R('<div class="cta-row">', '<div class="checks"><span>90 days to love it, keep the pouch</span><span>Same price every delivery</span></div>\n    <div class="cta-row">')

icons = '''
<div class="icons"><div class="w">
  <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="13" r="4.5"/><path d="M7 6.5h.01M10 6.5h.01"/></svg>HE and standard washers</div>
  <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v18M5 8l14 8M19 8L5 16"/></svg>Warm or cold water<sup class="p"><a href="pages/claims/index.html" title="Pending proof">&#8224;</a></sup></div>
  <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16v12H4z"/><path d="M4 7l8 6 8-6"/></svg>Fits in a drawer</div>
  <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.3 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/></svg>7% to animal sanctuaries</div>
</div></div>
'''
R('<div class="band" aria-hidden="true"><span></span><span></span><span></span></div>',
  '<div class="band" aria-hidden="true"><span></span><span></span><span></span></div>' + icons)

keep = '''
<section class="sec keep" id="laundry-day"><div class="w">
  <div class="head">
    <p class="eyebrow">Laundry day</p>
    <h2 class="big-letters">Laundry, done <span class="script">properly.</span></h2>
    <p style="color:var(--mute)">Good habits make clean clothes last. Our house guides cover the jobs every home has, one sheet at a time.</p>
  </div>
  <div class="guides">
    <a class="guide" style="--c:var(--sky)" href="blogs/stains/the-stain-rescue-cheat-sheet/index.html"><span class="kind">Stains</span><h3>The stain rescue cheat sheet</h3><p>Coffee, grass, wine and grease, and what to do in the first five minutes.</p><span class="tip">Cold water first. Heat sets a stain.</span><span class="go">Read the guide &rarr;</span></a>
    <a class="guide" style="--c:var(--mint)" href="blogs/how-to/how-to-wash-towels-so-they-stay-fluffy/index.html"><span class="kind">Linens</span><h3>Towels that stay fluffy</h3><p>Why less detergent and no softener give you softer towels.</p><span class="tip">Half a sheet is plenty for a towel load.</span><span class="go">Read the guide &rarr;</span></a>
    <a class="guide" style="--c:var(--plum)" href="blogs/pets/how-to-wash-a-dog-bed-and-blankets-the-right-way/index.html"><span class="kind">Pets</span><h3>Washing the dog bed</h3><p>Hair off first, longest cycle, extra rinse, then dry it all the way.</p><span class="tip">Shake it outside before it goes in.</span><span class="go">Read the guide &rarr;</span></a>
    <a class="guide" style="--c:var(--sun)" href="blogs/home/how-to-clean-your-washing-machine/index.html"><span class="kind">The machine</span><h3>Clean your washer monthly</h3><p>A clean drum means fresher loads. A ten-minute routine.</p><span class="tip">Leave the door open to dry between loads.</span><span class="go">Read the guide &rarr;</span></a>
  </div>
  <div class="cal">
    <h3>The <span class="script">house</span> laundry calendar</h3>
    <div class="cal-grid">
      <div><em>Weekly</em><b>Towels and bath mats</b><span>One sheet, warm wash.</span></div>
      <div><em>Every week or two</em><b>Bed sheets</b><span>Sooner if pets share the bed.</span></div>
      <div><em>Monthly</em><b>Pet beds and blankets</b><span>Two sheets, extra rinse.</span></div>
      <div><em>Monthly</em><b>The washer itself</b><span>Hot empty cycle, wipe the seal.</span></div>
      <div><em>Each season</em><b>Pillows and comforters</b><span>Check the care label first.</span></div>
    </div>
  </div>
</div></section>
'''
R('<section class="sec reviews" id="reviews">', keep + '\n<section class="sec reviews" id="reviews">')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
