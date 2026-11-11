p = 'home-template.html'
s = open(p, encoding='utf-8').read()


def R(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


R('.script{font-family:var(--f-script);font-style:italic;font-weight:700;letter-spacing:0}',
  '.script{font-family:var(--f-script);font-style:italic;font-weight:700;letter-spacing:0;line-height:1.1}')
R('.keep .head{display:grid;gap:10px;max-width:760px}', '.keep .head{display:grid;gap:16px;max-width:760px}')
css = '''
/* faq */
.faq .w{display:grid;gap:clamp(24px,4vw,40px)}
@media (min-width:860px){.faq .w{grid-template-columns:.8fr 1.2fr;align-items:start}}
.faq .eyebrow{color:var(--t-sky)}
.qa{border-bottom:3px solid var(--ink)}
.qa:first-child{border-top:3px solid var(--ink)}
.qa summary{cursor:pointer;list-style:none;padding:18px 48px 18px 0;font:900 1.2rem/1.3 var(--f-display);position:relative}
.qa summary::-webkit-details-marker{display:none}
.qa summary::after{content:"+";position:absolute;right:4px;top:10px;font:900 2rem var(--f-display);color:var(--t-sky);transition:transform .25s}
.qa[open] summary::after{transform:rotate(45deg)}
.qa p{padding-bottom:18px;color:var(--mute)}
'''
R('/* footer */', css + '\n/* footer */')
faq = '''
<section class="sec faq" id="faq"><div class="w">
  <div style="display:grid;gap:14px"><p class="eyebrow">Quick answers</p><h2 class="big-letters">Asked a lot.</h2><p style="color:var(--mute)">More in the <a href="pages/faq/index.html">full FAQ</a>, or tap Ask Just.</p></div>
  <div>
    <details class="qa"><summary>Does it clean as well as liquid detergent?</summary><p>Just 7 is made for everyday loads. We'll publish independent cleaning test results before launch rather than make claims early. For heavy food and protein stains, pretreat or wait for Just 9 with enzymes.</p></details>
    <details class="qa"><summary>Does it dissolve in cold water?</summary><p>It's designed to dissolve in warm or cold water, and we're running a cold-water test to show it. For very cold washes, tear the sheet in half and don't overfill the drum.</p></details>
    <details class="qa"><summary>Is it OK for homes with cats and dogs?</summary><p>We made it with pets in mind: no fragrance, no essential oils, nothing from animals. Like any detergent it isn't food, so keep the pouch sealed and out of reach.</p></details>
    <details class="qa"><summary>How does the subscription work?</summary><p>Pick every 4, 8 or 12 weeks. Each pouch is $15 on every delivery, with free shipping. Skip or cancel anytime before it ships.</p></details>
    <details class="qa"><summary>What if I don't like it?</summary><p>You have 90 days. Email us and we'll refund the order. Keep the pouch, no return needed.</p></details>
  </div>
</div></section>
'''
R('<section class="sec wl" id="waitlist">', faq + '\n<section class="sec wl" id="waitlist">')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
