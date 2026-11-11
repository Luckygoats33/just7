import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()


def R(a, b, n=1):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, n)


css = '''<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800;900&display=swap">
<style>
/* Restyle to match the new homepage: Will's mint, sky, plum and sun, logo font throughout, bold color bands. */
:root{--sage:#5FB389;--sage-ink:#2F7D57;--sage-tint:#E3F4EA;--sun:#FFC94A;--plum:#5B2A5E;--t-sky:#1F6FA8;--f-body:"Nunito",ui-rounded,"SF Pro Rounded",system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--sage:#6CC296;--sage-ink:#7FD3A6;--sage-tint:#16291F;--t-sky:#86C5F0}}
:root[data-theme="dark"]{--sage:#6CC296;--sage-ink:#7FD3A6;--sage-tint:#16291F;--t-sky:#86C5F0}
body{font:600 18px/1.6 var(--f-body)}
.pbar{background:var(--ink);font-family:var(--f-display);font-weight:800}
.hero-pdp{background:var(--sky);color:#fff;padding-block:24px clamp(48px,7vw,80px)!important}
.hero-pdp .crumbs,.hero-pdp .crumbs a{color:#EAF5FD}
.hero-pdp .pdp>.buy{background:var(--card);color:var(--ink);border-radius:28px;padding:clamp(20px,4vw,32px);box-shadow:0 18px 40px rgba(0,0,0,.18)}
.hero-pdp .gal .photo{box-shadow:0 18px 40px rgba(0,0,0,.18)}
.hero-pdp .pg-t{border-color:rgba(255,255,255,.5)}
.hero-pdp .pg-t[aria-current=true]{border-color:var(--sun)}
.pdp h1{font-weight:900;letter-spacing:-.02em}
.save b{font-weight:900;color:var(--ink)}
.save .per{font:900 1.05rem var(--f-display);color:var(--sage-ink)}
.promise7{display:flex;gap:12px;align-items:center;background:var(--sun);color:#2A2205;border-radius:16px;padding:12px 16px;font:800 .98rem/1.3 var(--f-display)}
.promise7 b{font-size:1.9rem;line-height:1;font-weight:900}
.cband{display:grid;grid-template-columns:5fr 7fr 9fr;height:20px}
.cband span:nth-child(1){background:#5FB389}.cband span:nth-child(2){background:var(--sun)}.cband span:nth-child(3){background:#5B2A5E}
.sec-count{background:var(--card)}
.sec-count .ben.feature{background:var(--plum)}
.sec-out{background:#5FB389;color:#10291D;padding-block:clamp(56px,9vw,100px)!important}
.sec-out h2,.sec-out .eyebrow{color:#10291D}
.sec-faq{padding-block:clamp(56px,9vw,100px)!important}
.sec-faq h2,.sec-out h2{font-size:clamp(2.4rem,7vw,4.4rem);font-weight:900;letter-spacing:-.03em}
.btn{font-weight:900}
</style>
'''
R('<div class="pbar">', css + '<div class="pbar">')
R('<section class="section" style="padding-top:24px">', '<section class="section hero-pdp" style="padding-top:24px">')
R('<section class="section" style="padding-top:0"><div class="wrap"><div class="ben feature">',
  '<div class="cband" aria-hidden="true"><span></span><span></span><span></span></div><section class="section sec-count" style="padding-top:clamp(48px,8vw,90px)"><div class="wrap"><div class="ben feature">')
R('<section class="section" style="padding-top:0"><div class="wrap"><div class="stack" style="gap:24px"><div class="stack"><p class="eyebrow">Left out on purpose</p>',
  '<section class="section sec-out"><div class="wrap"><div class="stack" style="gap:24px"><div class="stack"><p class="eyebrow">Left out on purpose</p>')
R('<section class="section" style="padding-top:0"><div class="wrap"><div class="stack" style="gap:12px;max-width:760px"><h2>Quick answers</h2>',
  '<section class="section sec-faq"><div class="wrap"><div class="stack" style="gap:12px;max-width:760px"><h2>Quick answers</h2>')
# prices
R('<b>Subscribe and save <span class="ph">[X]% off</span></b><small>A pouch on your schedule. Skip, pause or cancel anytime (planned).</small>',
  '<b>Subscribe and save 21%: $15</b><small>A pouch on your schedule, same price every delivery. Free shipping. Skip or cancel anytime.</small>')
R('<b>One pouch</b><small>Try it once, no strings.</small>', '<b>One pouch: $19</b><small>Try it once. Free shipping on 2 or more.</small>')
R('<legend>Deliver every <span class="ph">placeholder</span></legend>', '<legend>Deliver every</legend>')
R('<div class="save"><b>Price set at launch</b><span class="mute">Subscription discount: <span class="ph">[X]%</span></span></div>',
  '<div class="save"><b data-price>$15</b><span class="per" data-per>$0.25 a load</span><span class="mute">30 sheets, up to 60 loads</span></div>')
R('<small>Price set at launch</small></div><button class="btn sm"', '<small data-barprice>$15 a pouch, $0.25 a load</small></div><button class="btn sm"')
R('<p class="mline">', '<p class="promise7"><b>90</b><span>days to love it. If you don\'t, email us and keep the pouch. Full refund on any order.</span></p>\n<p class="mline">')
# swap price when plan changes
js = '''<script>(function(){var f=document.querySelector("[data-buy]");if(!f)return;var pr=f.querySelector("[data-price]"),per=f.querySelector("[data-per]"),bar=document.querySelector("[data-barprice]");function upd(){var sub=f.querySelector("input[name=plan][value=sub]");var on=sub&&sub.checked;if(pr)pr.textContent=on?"$15":"$19";if(per)per.textContent=on?"$0.25 a load":"$0.32 a load";if(bar)bar.textContent=on?"$15 a pouch, $0.25 a load":"$19 a pouch, $0.32 a load"}f.querySelectorAll("input[name=plan]").forEach(function(r){r.addEventListener("change",upd)});upd()})();</script>'''
idx = s.rfind('</body>')
s = (s[:idx] + js + s[idx:]) if idx > -1 else s + js
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
