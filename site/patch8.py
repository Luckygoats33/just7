p = 'home-template.html'
s = open(p, encoding='utf-8').read()


def R(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# 1. Why switch: list both labels
theirs = ['Polyvinyl alcohol (PVA) film', 'Sodium lauryl sulfate', 'C12-16 pareth-9', 'Glucoside cleaner', 'Second glucoside cleaner',
          'Betaine cleaner', 'Amine oxide cleaner', 'Sodium citrate', 'Tetrasodium glutamate diacetate', 'Citric acid',
          'Protease enzyme', 'Amylase enzyme', 'Kaolin clay', 'Glycerin', 'Water']
ours = ['Pullulan film', 'Lauryl glucoside', 'Decyl glucoside', 'Washing soda', 'Plant glycerin', 'Sodium citrate', 'Water']
li_t = ''.join(f'<li><span>{i+1}</span>{n}</li>' for i, n in enumerate(theirs))
li_o = ''.join(f'<li><span>{i+1}</span>{n}</li>' for i, n in enumerate(ours))
labels = f'''<div class="labels">
    <div class="lbl them"><p class="lbl-h">The leading sheet brand<small>Fragrance-free version, from its own published ingredient table</small></p><ol>{li_t}</ol><p class="lbl-n">15 ingredients</p></div>
    <div class="lbl us"><p class="lbl-h">Just 7<small>Our whole label. Nothing hidden.</small></p><ol>{li_o}</ol><p class="lbl-n">7 ingredients. Done.</p><a class="btn" href="pages/ingredients/index.html">What each one does</a></div>
  </div>'''
R('<div class="reasons">', labels + '\n  <div class="reasons">')

# 2. Every ingredient has a job: icons and percentage rings
icons = {
    'film': '<rect x="10" y="14" width="44" height="34" rx="6"/><path d="M18 24h28M18 32h28M18 40h18"/>',
    'grease': '<path d="M32 10c8 12 14 19 14 27a14 14 0 0 1-28 0c0-8 6-15 14-27z"/><path d="M26 40a7 7 0 0 0 7 6"/>',
    'gentle': '<path d="M32 12l4 12 12 4-12 4-4 12-4-12-12-4 12-4z"/><circle cx="48" cy="46" r="3"/><circle cx="16" cy="48" r="2"/>',
    'soda': '<path d="M14 50h36"/><path d="M20 50l4-26h16l4 26"/><path d="M27 24v-8h10v8"/><path d="M26 36h12"/>',
    'flex': '<path d="M12 44c10-24 30-24 40 0"/><path d="M12 44c10-10 30-10 40 0"/><circle cx="32" cy="22" r="3"/>',
    'citrus': '<circle cx="32" cy="34" r="16"/><path d="M32 18v32M16 34h32M21 23l22 22M43 23L21 45"/>',
    'water': '<path d="M32 10c10 14 16 22 16 30a16 16 0 0 1-32 0c0-8 6-16 16-30z"/><path d="M22 44h20"/>',
}
items = [('film', 'Pullulan film', 'The sheet itself. From fermented plant starch, made to dissolve in the wash.', 35, '#3A9BDC'),
         ('grease', 'Lauryl glucoside', 'Lifts body oils and grease. Made from plant sugar.', 17, '#5FB389'),
         ('gentle', 'Decyl glucoside', 'The gentle everyday cleaner. No sulfates.', 17, '#2F7D57'),
         ('soda', 'Washing soda', 'Softens water so everyday grime lets go.', 10, '#5B2A5E'),
         ('flex', 'Plant glycerin', 'Keeps the sheet soft and bendy. Plants only.', 10, '#9E6AA1'),
         ('citrus', 'Sodium citrate', 'Handles hard water and keeps the pH steady.', 7, '#D9A21B'),
         ('water', 'Water', 'Carries it all while the sheet is made, then mostly dries off.', 4, '#6D9FC4')]
cards = ''
for i, (ic, name, job, pc, c) in enumerate(items):
    cards += (f'<article class="ing2" style="--c:{c};--p:{pc}">'
              f'<div class="ring"><svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icons[ic]}</svg></div>'
              f'<div class="ing2-t"><span class="num">{i+1}</span><h3>{name}</h3><p>{job}</p></div>'
              f'<b class="pc">{pc}%</b></article>')
cards += '<article class="ing2 total"><div><h3>= 100%</h3><p>Seven names. Nothing under "proprietary blend".</p></div></article>'
a = s.index('<div class="ings">')
b = s.index('</div>\n</div></section>', a)
s = s[:a] + '<div class="ings2">' + cards + s[b:]

css = '''
/* label vs label */
.labels{display:grid;gap:18px;margin-top:clamp(24px,4vw,40px);align-items:start}
@media (min-width:860px){.labels{grid-template-columns:1fr 1fr}}
.lbl{background:#fff;color:#22302B;border-radius:8px;padding:22px 24px;box-shadow:0 14px 30px rgba(42,34,5,.18);display:grid;gap:12px;font-family:var(--f-display)}
.lbl-h{font:900 1.5rem/1.1 var(--f-display);border-bottom:6px solid #22302B;padding-bottom:10px}
.lbl-h small{display:block;font:700 .85rem/1.3 var(--f-body);color:#55625D;margin-top:4px}
.lbl ol{list-style:none;padding:0;margin:0;display:grid}
.lbl li{display:grid;grid-template-columns:30px 1fr;gap:8px;padding:6px 0;border-bottom:1px solid #E2E7E2;font-weight:800;font-size:1rem}
.lbl li span{color:#9AA6A1;font-variant-numeric:tabular-nums}
.lbl.them{transform:rotate(-1deg)}
.lbl.them li{color:#55625D}
.lbl.us{transform:rotate(1deg);box-shadow:0 0 0 5px var(--plum),0 14px 30px rgba(42,34,5,.18)}
.lbl.us li span{color:var(--plum)}
.lbl-n{font:900 1.3rem var(--f-display)}
.lbl.us .lbl-n{color:var(--plum)}
.lbl .btn{justify-self:start}
.reasons{margin-top:clamp(36px,6vw,64px)}
/* ingredient cards with icons and rings */
.ings2{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr))}
.ing2{background:var(--card);border-radius:24px;padding:20px;display:grid;grid-template-columns:96px 1fr auto;gap:16px;align-items:center;border:2px solid var(--line);transition:transform .25s cubic-bezier(.3,1.4,.5,1),border-color .2s}
.ing2:hover{transform:translateY(-5px) rotate(-.6deg);border-color:var(--c)}
.ring{width:96px;height:96px;border-radius:50%;display:grid;place-items:center;background:conic-gradient(var(--c) calc(var(--p)*1%),color-mix(in srgb,var(--c) 14%,transparent) 0);position:relative}
.ring::before{content:"";position:absolute;inset:9px;border-radius:50%;background:var(--card)}
.ring svg{width:48px;height:48px;color:var(--c);position:relative}
.ing2-t{display:grid;gap:4px;min-width:0}
.ing2-t .num{font:900 .8rem var(--f-display);letter-spacing:.1em;text-transform:uppercase;color:var(--c)}
.ing2-t .num::before{content:"No. "}
.ing2-t h3{font-size:1.3rem}
.ing2-t p{color:var(--mute);font-size:.92rem;line-height:1.4}
.ing2 .pc{font:900 2rem/1 var(--f-display);color:var(--c);font-variant-numeric:tabular-nums}
.ing2.total{background:var(--ink);border-color:var(--ink);color:var(--paper);grid-template-columns:1fr}
.ing2.total h3{font-size:2.4rem;color:var(--sun)}
.ing2.total p{color:var(--paper);opacity:.85}
@media (max-width:420px){.ing2{grid-template-columns:72px 1fr;}.ring{width:72px;height:72px}.ring svg{width:36px;height:36px}.ing2 .pc{grid-column:2;font-size:1.5rem}}
'''
R('/* footer */', css + '\n/* footer */')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
