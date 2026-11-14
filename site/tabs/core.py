"""v2 tabs: page-level rewrites of the hand-built pages in docs/. Idempotent-ish: each edit asserts its source text
exists unless the target text is already present."""
import os, re, json, html
from data import *
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.normpath(os.path.join(HERE, "..", "..", "docs"))
MISS = []

def rd(rel): return open(os.path.join(D, rel), encoding="utf-8").read()
def wr(rel, s): open(os.path.join(D, rel), "w", encoding="utf-8", newline="").write(s)

def R(s, old, new, rel="", allow_missing=False):
    if old in s: return s.replace(old, new)
    if new in s or allow_missing: return s
    MISS.append(f"{rel}: {old[:90]}"); return s

def RX(s, pat, new, rel="", flags=re.S, count=1):
    n, k = re.subn(pat, new, s, count=count, flags=flags)
    if not k: MISS.append(f"{rel}: /{pat[:80]}/")
    return n

def bar_spans(style="home"):
    return "".join(f'<span style="width:{i["p"]}%;background:{i["c"]}"></span>' for i in ING)

def aria_formula():
    return "Formula by percent: " + ", ".join(f'{i["name"].lower()} {i["p"]}' for i in ING)

TAB_CSS = ('<style id="j7-tabs">'
  '.sh i,.dose .sh i{width:52px!important;height:52px!important;border-radius:50%!important;transform:none!important;'
  'background:radial-gradient(circle at 36% 32%,#fff 0,#F1F5F6 55%,#D3DEE4 100%)!important;box-shadow:inset 0 0 0 3px #3A9BDC,0 6px 14px rgba(20,60,90,.18)!important}'
  '.sh i+i{margin-left:-10px}.sh i.half{display:none!important}'
  '.hpic{position:relative;width:100%;max-width:560px;justify-self:center}'
  '.hpic img{display:block;width:100%;height:auto;aspect-ratio:1;object-fit:cover;border-radius:22px;box-shadow:0 30px 60px rgba(15,50,80,.35),0 0 0 4px rgba(255,255,255,.9)}'
  '.hpic .sticker{position:absolute;left:-14px;bottom:-18px}'
  '@media (max-width:899px){.hpic{max-width:420px}}'
  '</style>')

def add_tab_css(s):
    s = re.sub(r'<style id="j7-tabs">.*?</style>', '', s, flags=re.S)
    return s.replace("</head>", TAB_CSS + "\n</head>", 1)

def pic(n, alt, sizes="(max-width: 700px) 92vw, 560px", lazy=True, extra=""):
    l = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return (f'<picture><source type="image/webp" srcset="/assets/just-7-product-{n}-300.webp 300w, /assets/just-7-product-{n}-600.webp 600w, /assets/just-7-product-{n}.webp 1200w" sizes="{sizes}">'
            f'<img src="/assets/just-7-product-{n}.jpg" alt="{html.escape(alt)}" width="1200" height="1200"{l}{extra}></picture>')

# ------------------------------------------------------------------ home
def home():
    rel = "index.html"; s = rd(rel)
    s = R(s, '<h1><span class="rest">Laundry sheets with <span class="big7">just 7</span> ingredients.</span></h1>',
             '<h1><span class="rest">Laundry tabs with <span class="big7">just 7</span> ingredients.</span></h1>', rel)
    s = R(s, '<p class="lead">Tear one off, drop it in the washer, done. No jug, no measuring, no fragrance, nothing from animals.</p>',
             '<p class="lead">One pressed tab, one load. No film, no PVA, no plastic jug. No measuring, no fragrance, nothing from animals.</p>', rel)
    # hero video (old sheet pouch) -> new tabs photo
    s = RX(s, r'<div class="hvid"><video data-hvid.*?</div>(?:<script id="j7-hvid-js">.*?</script>)?',
           '<div class="hpic">' + pic(1, GALLERY[0][2], "(max-width: 899px) 92vw, 560px", lazy=False) +
           '<span class="sticker price"><span><b>$0.25</b><small>a load</small></span></span></div>', rel)
    s = R(s, 'alt="Just 7 pouch with two sheets: 30 sheets, 60 loads"', 'alt="Close-up of plain white pressed Just 7 tabs"', rel)
    s = R(s, '/assets/just-7-product-1-300.webp 300w, /assets/just-7-product-1-600.webp 600w, /assets/just-7-product-1.webp 1200w" sizes="(max-width: 700px) 92vw, 560px"><img src="/assets/just-7-product-1.jpg" alt="Close-up',
             '/assets/just-7-product-8-300.webp 300w, /assets/just-7-product-8-600.webp 600w, /assets/just-7-product-8.webp 1200w" sizes="(max-width: 700px) 92vw, 560px"><img src="/assets/just-7-product-8.jpg" alt="Close-up', rel)
    s = R(s, '<p class="eyebrow">Meet the sheet</p>', '<p class="eyebrow">Meet the tab</p>', rel)
    s = R(s, '<p class="sc-lead">The everyday sheet. Seven ingredients, fragrance-free, 30 sheets for up to 60 loads.</p>',
             '<p class="sc-lead">The everyday tab. Seven ingredients, pressed into one 4 g tab. 60 tabs for up to 60 loads, with a light fizz to help it break up in cold water.' + DAG + '</p>', rel)
    s = R(s, '<li><b>30</b><span>sheets a pouch</span></li>', '<li><b>60</b><span>tabs a pouch</span></li>', rel)
    # comparison labels
    s = R(s, '<ol><li><span>1</span>Pullulan film</li><li><span>2</span>Lauryl glucoside</li><li><span>3</span>Decyl glucoside</li><li><span>4</span>Washing soda</li><li><span>5</span>Plant glycerin</li><li><span>6</span>Sodium citrate</li><li><span>7</span>Water</li></ol>',
             '<ol>' + "".join(f'<li><span>{k+1}</span>{i["name"]}</li>' for k, i in enumerate(ING)) + '</ol>', rel)
    s = R(s, '<b>No perfume on your sheets.</b>', '<b>No perfume on your laundry.</b>', rel)
    s = R(s, '<b>No jug. No drips.</b><p>One flat pouch the size of an envelope replaces a heavy plastic bottle.</p>',
             '<b>No film. No PVA. No jug.</b><p>A pressed tab needs no wrapper. One flat pouch replaces a heavy plastic bottle.</p>', rel)
    s = R(s, '<p>The biggest laundry sheet brand publishes 15 ingredients for its fragrance-free sheet, counting the film. We count the film too, and we stop at seven.</p>',
             '<p>The biggest laundry sheet brand publishes 15 ingredients for its fragrance-free sheet, PVA film included. Our tab has no film at all, and we stop at seven.</p>', rel)
    # ingredients section
    i = s.find('<section class="sec" id="ingredients">'); j = s.find('</section>', i) + len('</section>')
    if i > -1:
        cards = "".join(
            f'<article class="ing2" style="--c:{x["c"]};--p:{x["p"]}"><div class="ring">{svg64(x["icon"])}</div><div class="ing2-t"><span class="num">{k+1}</span><h3>{x["name"]}</h3><p>{x["short"]}</p></div><b class="pc">{x["pct"].replace("about ", "~")}</b></article>'
            for k, x in enumerate(ING))
        sec = ('<section class="sec" id="ingredients"><div class="w">\n  <div class="ing-head">\n    <p class="eyebrow">What\'s in every tab</p>\n'
               '    <h2>7 ingredients that get your laundry clean.</h2>\n'
               f'    <p style="color:var(--mute)">Washing soda and two sugar-based cleaners do the cleaning, citrate handles hard water, citric acid makes the fizz, and cellulose holds it all in a pressed tab. No film, nothing else. Percentages are our working formula, confirmed with our manufacturer before launch.{DAG}</p>\n'
               f'    <div class="formula" role="img" aria-label="{aria_formula()}">\n      {bar_spans()}\n    </div>\n  </div>\n'
               f'  <div class="ings2">{cards}<article class="ing2 total"><div><h3>= 100%</h3><p>Seven names. Nothing under "proprietary blend".</p></div></article></div>\n</div></section>')
        s = s[:i] + sec + s[j:]
    else: MISS.append("home: ingredients section")
    s = R(s, '<h2 style="margin-top:12px">Not in the sheet. Not ever.</h2>', '<h2 style="margin-top:12px">Not in the tab. Not ever.</h2>', rel)
    s = R(s, '<div class="outs"><span>PVA film</span>', '<div class="outs"><span>Film or PVA</span>', rel)
    s = R(s, '<h2>Tear, drop, done.</h2>', '<h2>Drop, wash, done.</h2>', rel)
    s = R(s, '<div class="dose"><div class="sh"><i class="half"></i></div><b>Half</b><small>Small load</small></div>\n', '', rel)
    s = R(s, '<div class="dose"><div class="sh"><i></i></div><b>One</b><small>Regular load</small></div>', '<div class="dose"><div class="sh"><i></i></div><b>One tab</b><small>Small or regular load</small></div>', rel)
    s = R(s, '<div class="dose"><div class="sh"><i></i><i></i></div><b>Two</b><small>Big or extra-dirty load</small></div>', '<div class="dose"><div class="sh"><i></i><i></i></div><b>Two tabs</b><small>Big or extra-dirty load</small></div>', rel)
    s = R(s, '<ol class="steps"><li>Sheet into the drum first</li>', '<ol class="steps"><li>Tab into the drum first</li>', rel)
    s = R(s, 'No first-order trick that doubles later. One pouch is 30 sheets, up to 60 loads.', 'No first-order trick that doubles later. One pouch is 60 tabs, up to 60 loads.', rel)
    s = R(s, 'Our house guides cover the jobs every home has, one sheet at a time.', 'Our house guides cover the jobs every home has, one load at a time.', rel)
    s = R(s, '<span class="tip">Half a sheet is plenty for a towel load.</span>', '<span class="tip">One tab is plenty for a towel load.</span>', rel)
    s = R(s, '<span>One sheet, warm wash.</span>', '<span>One tab, warm wash.</span>', rel)
    s = R(s, '<span>Two sheets, extra rinse.</span>', '<span>Two tabs, extra rinse.</span>', rel)
    s = R(s, "<p>It's designed to dissolve in warm or cold water, and we're running a cold-water test to show it. For very cold washes, tear the sheet in half and don't overfill the drum.</p>",
             "<p>It's designed to break up and dissolve in warm or cold water: citric acid and washing soda fizz on contact, and the cellulose swells to pop the tab apart. We're running a cold-water test to show it. For very cold washes, put the tab in first and don't overfill the drum.</p>", rel)
    s = R(s, '<h3>What\'s in laundry detergent sheets?</h3><p>Every common ingredient by job, and which ones we skip.</p>',
             '<h3>What\'s in laundry detergent?</h3><p>Every common ingredient by job, and which ones we skip.</p>', rel)
    s = R(s, '<p>How to read the label, glycerin included.</p>', '<p>How to read the label, name by name.</p>', rel)
    s = R(s, '<title>Just 7 Laundry Sheets: Seven Ingredients, Fragrance-Free</title>', '<title>Just 7 Laundry Tabs: Seven Ingredients, Fragrance-Free</title>', rel)
    s = add_tab_css(s)
    wr(rel, s)

# ------------------------------------------------------------------ product page
def pdp():
    rel = "products/just-7/index.html"; s = rd(rel)
    # gallery
    i = s.find('<div class="photo pg-main">'); j = s.find('</div><script>', s.find('<div class="pg-thumbs">', i))
    if i > -1 and j > -1:
        main = '<div class="photo pg-main">' + pic(1, GALLERY[0][2], lazy=False, extra=" data-pg-main") + '</div>'
        th = "".join(f'<button type="button" class="pg-t" data-pg="{n}" aria-label="Show image {k+1}: {lab}"{" aria-current=\"true\"" if k == 0 else ""}><picture><source type="image/webp" srcset="/assets/just-7-product-{n}-300.webp" sizes="80px"><img src="/assets/just-7-product-{n}.jpg" alt="" width="1200" height="1200" loading="lazy"></picture></button>'
                     for k, (n, lab, _) in enumerate(GALLERY))
        s = s[:i] + main + '<div class="pg-thumbs">' + th + s[j:]
    else: MISS.append("pdp gallery")
    alts = {str(n): a for n, _, a in GALLERY}
    s = RX(s, r'var alts=\[[^\]]*\];', 'var alts=' + json.dumps(alts) + ';', rel)
    s = R(s, 'm.alt=alts[i-1];', 'm.alt=alts[i];', rel)
    s = RX(s, r'<script>\(function\(\)\{var b=document\.querySelector\("\.pg-v"\).*?</script>', '', rel)
    s = R(s, '.pg-thumbs{display:grid;grid-template-columns:repeat(6,1fr);', '.pg-thumbs{display:grid;grid-template-columns:repeat(4,1fr);', rel)
    s = R(s, '<h1 style="font-size:clamp(2.1rem,7vw,3.2rem)">Just 7 laundry detergent sheets</h1>', '<h1 style="font-size:clamp(2.1rem,7vw,3.2rem)">Just 7 Laundry Tabs</h1>', rel)
    s = R(s, '<p class="lead">Seven ingredients, fragrance-free, nothing from animals. For everyday loads in any washer.</p>',
             '<p class="lead">Pressed laundry detergent tabs with seven ingredients. One tab, one load. No film, no PVA, no plastic jug. Fragrance-free, nothing from animals.</p>', rel)
    chips = "".join(f'<a class="chip" href="/pages/ingredients/#{x["id"]}"><i style="background:{x["c"]}"></i>{x["name"]}</a>' for x in ING)
    s = RX(s, r'<div class="chips"><a class="chip" href="/pages/ingredients/#pullulan-film">.*?</div>', '<div class="chips">' + chips + '</div>', rel)
    s = R(s, '<span class="mute">30 sheets, up to 60 loads</span>', '<span class="mute">60 tabs, up to 60 loads</span>', rel)
    rows = "".join(f'<div class="lrow"><span class="n">{k+1}</span><span class="nm">{x["name"]}<span class="job">{x["short"]}</span></span><span class="pc">{x["pct"].replace("about ", "~")}</span></div>' for k, x in enumerate(ING))
    s = RX(s, r'(<div class="label" role="group" aria-label="Just 7 ingredient label"><h3>Ingredients</h3>).*?(<p class="note")', r'\1' + rows.replace("\\", "\\\\") + r'\2', rel)
    s = R(s, 'Share of a roughly 2 g sheet, working formula', 'Share of a 4 g tab, working formula, cleaners counted as active', rel)
    s = RX(s, r'<p>Drop one sheet straight into the drum before your clothes\. Half for small loads, two for big or messy ones\.',
           "<p>Drop one tab straight into the drum before your clothes. One for a small or regular load, two for big or messy ones.", rel)
    s = R(s, '<span class="nm">Pouch</span><span>About 6.4 x 9.6 in, about 1/8 in thick</span>', '<span class="nm">Pouch</span><span>Flat pouch, about 7.7 x 11.2 in</span>', rel)
    s = R(s, '<span class="nm">Sheets</span><span>30 sheets, each 5.5 x 4.25 in</span>', '<span class="nm">Tabs</span><span>60 pressed tabs, each 4 g and about 30 mm (1.2 in) across</span>', rel)
    s = RX(s, r'<span>½ sheet small · 1 regular · 2 large or messy', '<span>1 tab small or regular · 2 large or messy', rel)
    s = R(s, '<span>To be confirmed. Peel-and-seal flap keeps sheets dry.</span>', '<span>To be confirmed. Reseal it after each use to keep the tabs dry.</span>', rel)
    s = R(s, '<p>The best-known laundry sheet lists 15 ingredients in its own ingredient table, film included. Just 7 lists seven.</p>',
             '<p>The best-known laundry sheet lists 15 ingredients in its own ingredient table, PVA film included. Just 7 is a pressed tab with no film, and it lists seven.</p>', rel)
    s = R(s, '<b>PVA plastic film</b><p>Our sheet is pullulan, not polyvinyl alcohol.</p>', '<b>Film or PVA</b><p>A pressed tab, so there\'s no film to dissolve and no polyvinyl alcohol.</p>', rel)
    s = R(s, '<b>Animal anything</b><p>Not even the glycerin.', '<b>Animal anything</b><p>Nothing from animals, in any of the seven.', rel)
    s = R(s, "<p>Nothing in Just 7 comes from animals. That includes the glycerin, which can be made from animal fat elsewhere. We're collecting",
             "<p>Nothing in Just 7 comes from animals, in any of the seven ingredients. We're collecting", rel)
    s = R(s, "<title>Just 7 Laundry Detergent Sheets | Subscribe and Save</title>", "<title>Just 7 Laundry Tabs | Subscribe and Save</title>", rel)
    s = R(s, '"name": "Just 7 laundry sheets", "img"', '"name": "Just 7 Laundry Tabs", "img"', rel, allow_missing=True)
    wr(rel, s)

# ------------------------------------------------------------------ ingredients
def ingredients():
    rel = "pages/ingredients/index.html"; s = rd(rel)
    s = R(s, "<h2 style=\"font-size:1.2rem\">What's in a sheet</h2>", "<h2 style=\"font-size:1.2rem\">What's in a tab</h2>", rel)
    bar = "".join(f'<span style="--w:{x["p"]}%;--k:{k};width:{x["p"]}%;background:{x["c"]}" title="{x["name"]} {x["pct"]}"><em>{x["p"] if x["p"] >= 7 else ""}</em></span>' for k, x in enumerate(ING))
    aria = "Share of a tab: " + ", ".join(f'{x["name"]} {x["p"]} percent' for x in ING)
    s = RX(s, r'<div class="bar" role="img" aria-label="[^"]*">.*?</div>', f'<div class="bar" role="img" aria-label="{aria}">{bar}</div>', rel)
    leg = "".join(f'<span style=display:contents><a href="/pages/ingredients/#{x["id"]}" style="text-decoration:none;color:inherit"><i style="background:{x["c"]}"></i>{x["name"]}</a></span>' for x in ING)
    s = RX(s, r'<div class="legend">.*?</div>', f'<div class="legend">{leg}</div>', rel)
    s = R(s, "Share of a roughly 2 g sheet in our working formula. We'll match it to the final supplier documents before launch.", PCT_NOTE, rel)
    chips = "".join(f'<a class="chip" href="#{x["id"]}"><i style="background:{x["c"]}"></i>{k+1}. {x["name"]}</a>' for k, x in enumerate(ING))
    s = RX(s, r'<div class="chips"><a class="chip" href="#pullulan-film">.*?</div>', f'<div class="chips">{chips}</div>', rel)
    rows = []
    for k, x in enumerate(ING):
        dag = DAG if x["id"] in ("citric-acid", "decyl-glucoside", "cellulose", "lauryl-glucoside") else ""
        srcdag = DAG if "We'll share" in x["src"] else ""
        rows.append(f'<article class="irow" id="{x["id"]}" style="--c:{x["c"]}">\n<div class="scene" style="color:{x["c"]}"><span class="ring" data-p="{x["p"]}" style="--p:{x["p"]}"></span><svg viewBox="0 0 100 100" aria-hidden="true">{SCENE100[x["icon"]]}</svg></div>\n'
                    f'<div class="stack" style="gap:16px"><div class="head"><span class="num">{k+1}</span><div><h2>{x["name"]}</h2><p class="quip">{x["quip"]}{" · " + x["inci"] if x["inci"] != x["name"] else ""}</p></div>\n'
                    f'<span class="chip" style="margin-left:auto">{x["pct"]} of a tab</span><span class="pill">{x["pill"]}</span></div>\n'
                    f'<div class="facts"><div><h3>What it does</h3><p>{html.escape(x["does"], quote=False)}{dag}</p></div><div><h3>Where it comes from</h3><p>{html.escape(x["src"], quote=False)}{srcdag}</p></div><div><h3>Why it\'s here</h3><p>{html.escape(x["why"], quote=False)}</p></div></div></div></article>')
    s = RX(s, r'<div class="ing"><article class="irow".*?</article></div>', '<div class="ing">' + "".join(rows) + '</div>', rel)
    # explainer
    import importlib.util
    sp = importlib.util.spec_from_file_location("ex", os.path.join(HERE, "..", "explainer.py")); ex = importlib.util.module_from_spec(sp); sp.loader.exec_module(ex)
    b = ex.build(); fig = b[b.find('<figure class="xv"'):b.find('</figure>') + 9]
    s = RX(s, r'<figure class="xv".*?</figure>', fig.replace("\\", "\\\\"), rel)
    s = R(s, '<b>PVA plastic film</b><p>Our sheet is pullulan, not polyvinyl alcohol.</p>', '<b>Film or PVA</b><p>A pressed tab, so there\'s no film to dissolve and no polyvinyl alcohol.</p>', rel)
    s = R(s, '<b>Animal anything</b><p>Not even the glycerin.', '<b>Animal anything</b><p>Nothing from animals, in any of the seven.', rel)
    s = R(s, "Want the bigger picture? Read <a href=\"/blogs/ingredients/whats-in-laundry-detergent-sheets/\">What&#x27;s in Laundry Detergent Sheets? A Plain-English Ingredient Guide</a>.",
             "Want the bigger picture? Read <a href=\"/blogs/ingredients/whats-in-laundry-detergent-sheets/\">What&#x27;s in Laundry Detergent? A Plain-English Ingredient Guide</a>.", rel)
    wr(rel, s)

# ------------------------------------------------------------------ how to use
def howto():
    rel = "pages/how-to-use/index.html"; s = rd(rel)
    s = R(s, '<div role="listitem"><div class="sh" aria-hidden="true"><i class="half"></i></div><b>½ sheet</b><small>Small load</small></div>\n', '', rel)
    s = R(s, '<b>1 sheet</b><small>Regular load</small>', '<b>1 tab</b><small>Small or regular load</small>', rel)
    s = R(s, '<b>2 sheets</b><small>Big or messy load</small>', '<b>2 tabs</b><small>Big or messy load</small>', rel)
    s = R(s, '<h3>Sheet first</h3><p>Straight into the drum, before your clothes. Not the detergent drawer.</p>', '<h3>Tab first</h3><p>Straight into the drum, before your clothes. Not the detergent drawer.</p>', rel)
    s = R(s, '<summary>How many sheets per load?</summary><div class="a"><p>Half a sheet for a small load, one for a regular load, two for a big or extra-dirty load.',
             '<summary>How many tabs per load?</summary><div class="a"><p>One tab for a small or regular load, two for a big or extra-dirty load.', rel)
    s = R(s, '<summary>Where do I put the sheet?</summary>', '<summary>Where do I put the tab?</summary>', rel)
    s = R(s, "We're running a cold-water test and will share it. If you're washing very cold, tear the sheet in half and don't overstuff the drum.",
             "Citric acid and washing soda fizz on contact with water, and the cellulose swells to pop the tab apart. We're running a cold-water test and will share it. If you're washing very cold, put the tab in first so it sits in the water, and don't overstuff the drum.", rel)
    s = R(s, "<p>Yes. Dissolve a sheet (or half) in warm water in the sink first, then add your clothes, soak, rinse and dry.</p>",
             "<p>Yes. Drop one tab into a sink or basin of warm water and let it fizz and dissolve first, then add your clothes, soak, rinse and dry.</p>", rel)
    s = R(s, "<p>Wet the stain, rub a small piece of a sheet into it, and let it sit a few minutes before washing.",
             "<p>Dissolve a tab in a little warm water, dab it onto the wet stain, and let it sit a few minutes before washing.", rel)
    s = R(s, "<summary>How should I store the sheets?</summary><div class=\"a\"><p>Keep the pouch sealed and dry, away from steam and humidity, and out of reach of kids and pets. Damp hands and damp air soften the film.</p>",
             "<summary>How should I store the tabs?</summary><div class=\"a\"><p>Keep the pouch sealed and dry, away from steam and humidity, and out of reach of kids and pets. Grab a tab with dry hands: water starts the fizz.</p>", rel)
    s = R(s, "<p>Both. Put the sheet in the drum first, then the clothes.</p>", "<p>Both. Put the tab in the drum first, then the clothes.</p>", rel)
    s = R(s, "<title>How to Use Just 7 Laundry Sheets: Dosing and Tips</title>", "<title>How to Use Just 7 Laundry Tabs: Dosing and Tips</title>", rel)
    wr(rel, s)

# ------------------------------------------------------------------ compare
def compare():
    rel = "pages/compare/index.html"; s = rd(rel)
    s = R(s, '<h1>Sheets, pods and liquid, side by side.</h1>', '<h1>Tabs, sheets, pods and liquid, side by side.</h1>', rel)
    s = R(s, '<tr><th scope="row">The film</th><td>Pullulan, from fermented starch</td><td>Usually PVA</td><td>PVA</td><td>No film</td></tr>',
             '<tr><th scope="row">Film or wrapper</th><td>None. A pressed tab</td><td>Usually a PVA film</td><td>PVA</td><td>No film</td></tr>', rel)
    s = R(s, '<th scope="col">Other sheets</th>', '<th scope="col">Laundry sheets</th>', rel)
    s = R(s, '<tr><th scope="row">Easy to pretreat a stain</th><td>Rub in a damp piece', '<tr><th scope="row">Easy to pretreat a stain</th><td>Dissolve a tab in a little water', rel)
    s = R(s, "<p>The best-known laundry sheet's fragrance-free version lists 15 ingredients in the brand's own detailed ingredient table, counting its PVA film. Just 7 lists seven, counting our pullulan film.</p>",
             "<p>The best-known laundry sheet's fragrance-free version lists 15 ingredients in the brand's own detailed ingredient table, counting its PVA film. Just 7 is a pressed tab with no film, and it lists seven, water included.</p>", rel)
    s = R(s, "<title>Laundry Sheets vs Pods vs Liquid: How Just 7 Compares</title>", "<title>Laundry Tabs vs Sheets, Pods and Liquid: How Just 7 Compares</title>", rel)
    wr(rel, s)

# ------------------------------------------------------------------ planet
def planet():
    rel = "pages/planet/index.html"; s = rd(rel)
    s = R(s, '<h1>Drop the jug. Skip the PVA.</h1>', '<h1>No film. No PVA. No jug.</h1>', rel)
    s = R(s, "Here's the whole trip a Just 7 sheet takes, what we can say today, and what we're still testing before we say more.",
             "Here's the whole trip a Just 7 tab takes, what we can say today, and what we're still testing before we say more.", rel)
    s = R(s, '<p class="mute">A thin, flat pouch about 6.4 x 9.6 in, with no plastic window. We\'re choosing the material now.</p>',
             '<p class="mute">A flat pouch about 7.7 x 11.2 in, with no plastic window. We\'re choosing the material now.</p>', rel)
    s = R(s, '<p class="mute">The flap reseals to keep sheets dry between washes.', '<p class="mute">The pouch reseals to keep tabs dry between washes.', rel)
    s = R(s, '<h3>The sheet</h3><p class="mute">Pullulan film, made from fermented starch. No PVA.</p><div class="pills"><span class="pill ok">By design</span><span class="pill wait">Film spec in writing</span></div>',
             '<h3>The tab</h3><p class="mute">Seven ingredients pressed into a 4 g tab. No film, no wrapper, no PVA.</p><div class="pills"><span class="pill ok">By design</span><span class="pill wait">Final formula in writing</span></div>', rel)
    s = R(s, '<p class="mute">Designed to dissolve in warm or cold water.', '<p class="mute">A light fizz breaks it apart. Designed to dissolve in warm or cold water.', rel)
    s = R(s, "We're having the finished sheet tested to OECD 301B", "We're having the finished tab tested to OECD 301B", rel)
    s = R(s, '<p class="mute">No heavy jug of water to ship. The pouch is about 1/8 in thick.</p>', '<p class="mute">No heavy jug of water to ship. 60 tabs weigh about half a pound.</p>', rel)
    s = R(s, "<p>That's the design: a pullulan film instead of PVA, a thin pouch instead of a jug. We'll call it plastic-free once the film specs and the pouch material are confirmed in writing.",
             "<p>That's the design: a pressed tab with no film or PVA, and a flat pouch instead of a jug. We'll call it plastic-free once the final formula and the pouch material are confirmed in writing.", rel)
    s = R(s, "<p>It's designed to biodegrade. We're having the finished sheet tested", "<p>It's designed to biodegrade. We're having the finished tab tested", rel)
    s = R(s, "We'd rather skip the debate. Read", "We'd rather skip it entirely: our tab has no film at all. Read", rel)
    s = R(s, "<p>Our film is pullulan, not plastic, and it's designed to dissolve in the wash.", "<p>There's no film at all. The tab is washing soda, citric acid, citrate, cellulose and two cleaners, designed to dissolve in the wash.", rel)
    s = R(s, "<p>A thin, flat pouch with no plastic window and a peel-and-seal flap to keep moisture out.", "<p>A flat pouch with no plastic window that reseals to keep moisture out.", rel)
    wr(rel, s)

# ------------------------------------------------------------------ why just 7
def why():
    rel = "pages/why-just-7/index.html"; s = rd(rel)
    s = R(s, "Most laundry sheets are fine. We just think", "Most detergents are fine. We just think", rel)
    s = R(s, "<p>Nothing from animals. Not even the glycerin.</p>", "<p>Nothing from animals, in any of the seven.</p>", rel)
    s = R(s, "<h3>Planet</h3><p>Drop the jug. Skip the PVA.</p>", "<h3>Planet</h3><p>No film. No PVA. No jug.</p>", rel)
    s = R(s, "<h3>Compare</h3><p>Sheets, pods and liquid, side by side.</p>", "<h3>Compare</h3><p>Tabs, sheets, pods and liquid, side by side.</p>", rel)
    s = R(s, '<span>Common on sheet labels</span>', '<span>Common on sheet and pod labels</span>', rel)
    s = R(s, '<span class="us">7, film included</span>', '<span class="us">7, water included</span>', rel)
    s = R(s, '<h3>The sheet\'s film</h3><div class="cols"><span class="them">PVA (polyvinyl alcohol), a synthetic polymer</span><span class="us">Pullulan, a film made from fermented starch</span></div>',
             '<h3>Film</h3><div class="cols"><span class="them">PVA (polyvinyl alcohol), a synthetic polymer</span><span class="us">None. It\'s a pressed tab</span></div>', rel)
    s = R(s, '<h3>Glycerin source</h3><div class="cols"><span class="them">Usually not stated</span><span class="us">Nothing from animals', '<h3>Animal-derived ingredients</h3><div class="cols"><span class="them">Often not stated</span><span class="us">None', rel)
    wr(rel, s)

# ------------------------------------------------------------------ about / vegan / pets / shop / misc
def misc():
    rel = "pages/about/index.html"; s = rd(rel)
    s = R(s, "<p>Just Seven makes laundry sheets with as few ingredients as possible, every one named and explained. Nothing from animals, and nothing that's hard on pets. Our mission is simple: make the cleanest laundry sheet you can read in ten seconds, and give back to the animals while we're at it.</p>",
             "<p>Just Seven makes laundry detergent with as few ingredients as possible, every one named and explained. Nothing from animals, and nothing that's hard on pets. Our mission is simple: make the cleanest laundry tab you can read in ten seconds, and give back to the animals while we're at it.</p>", rel)
    s = R(s, "Just 7 is our first sheet.</p>", "Just 7 Laundry Tabs are our first product.</p>", rel)
    s = R(s, "<li>Nothing made from animals, anywhere. The glycerin isn't from animals.</li>", "<li>Nothing made from animals, anywhere.</li>", rel)
    s = R(s, "<li>A dissolving pullulan film. No PVA.</li>", "<li>No film and no PVA. Our tabs are pressed, not wrapped.</li>", rel)
    s = R(s, "<li>No fragrance or dyes in our core sheets.</li>", "<li>No fragrance or dyes in our core products.</li>", rel)
    wr(rel, s)

    rel = "pages/vegan/index.html"; s = rd(rel)
    rr = "".join(f'<div class="rr"><span>{k+1}. {x["name"]}</span><span>{ {"Mineral":"Mineral","Fermentation":"Fermented","Binder":"Cellulose","Sugar-based":"Sugar-based","Water":"Water"}[x["pill"]]}</span></div>' for k, x in enumerate(ING))
    s = RX(s, r'<div class="rr"><span>1\. Pullulan film</span>.*?(<div class="tot">)', rr + r'\1', rel)
    s = R(s, "<div><b>Glycerin</b><small>Can be made from animal fat. Ours isn't from animals.", "<div><b>Glycerin</b><small>Can be made from animal fat. We don't use it at all.", rel)
    s = R(s, "<p>Nothing in Just 7 comes from animals. That includes the glycerin, which can be made from animal fat elsewhere. We're collecting",
             "<p>Nothing in Just 7 comes from animals, in any of the seven ingredients. We're collecting", rel)
    s = R(s, "<summary>Is the glycerin in Just 7 vegan?</summary><div class=\"a\"><p>Yes. Nothing in Just 7 comes from animals. We'll share the supplier spec when we have it.",
             "<summary>Is there glycerin in Just 7?</summary><div class=\"a\"><p>No. Our tabs don't use glycerin, which can be made from animal fat in other detergents. Nothing in Just 7 comes from animals. We'll share supplier statements when we have them.", rel)
    wr(rel, s)

    rel = "pages/pet-friendly/index.html"; s = rd(rel)
    li = "".join(f'<li>{x["name"]}: {x["quip"].lower().replace("the ", "the ", 1)}</li>' for x in ING)
    s = RX(s, r'<li>Pullulan film: the sheet itself</li>.*?<li>Water: the carrier</li>', li, rel)
    s = R(s, "Shake off hair, one sheet (two for big beds)", "Shake off hair, one tab (two for big beds)", rel)
    s = R(s, "<h3>If your pet chews a sheet</h3>", "<h3>If your pet chews a tab</h3>", rel, allow_missing=True)
    s = R(s, "Take the sheet away, check their mouth", "Take the tab away, check their mouth", rel, allow_missing=True)
    s = R(s, "a fragrance-free sheet with a short list is a simple choice. Keep the sheets themselves away from curious paws.", "a fragrance-free tab with a short list is a simple choice. Keep the tabs themselves away from curious paws.", rel, allow_missing=True)
    wr(rel, s)

    rel = "collections/all/index.html"; s = rd(rel)
    s = R(s, "<h1>One sheet now. More on the way.</h1>", "<h1>One tab now. More on the way.</h1>", rel)
    s = R(s, "<p class=\"lead\">Just 7 ships first. Each sheet that follows gets its true ingredient count on the front.</p>", "<p class=\"lead\">Just 7 Laundry Tabs ship first. Everything that follows gets its true ingredient count on the front.</p>", rel)
    s = R(s, 'alt="Just 7 pouch" width="672" height="864"', 'alt="Just 7 Laundry Tabs pouch" width="672" height="864"', rel)
    s = R(s, '<p class="mute">Seven ingredients, fragrance-free, for everyday loads.</p>', '<p class="mute">Pressed laundry tabs. Seven ingredients, fragrance-free, no film. 60 tabs a pouch.</p>', rel)
    s = R(s, "<p class=\"mute\">Bring the dirt. Adds enzymes and a water softener for grass, food and pet messes. Not for wool or silk.</p>", "<p class=\"mute\">Bring the dirt. A tougher formula for grass, food and pet messes, in the works.</p>", rel)
    s = R(s, '<span class="mute">30 sheets, up to 60 loads', '<span class="mute">60 tabs, up to 60 loads', rel)
    s = R(s, "<title>Shop Just Seven: Just 7 Laundry Sheets and What&#x27;s Next</title>", "<title>Shop Just Seven: Just 7 Laundry Tabs and What&#x27;s Next</title>", rel)
    wr(rel, s)

    rel = "pages/claims/index.html"; s = rd(rel)
    s = R(s, "<b>Waiting on:</b> Final formula and film spec in writing", "<b>Waiting on:</b> Final tab formula in writing from our manufacturer", rel)
    s = R(s, "<h3>No fragrance, essential oils, musks, dyes or PVA</h3>", "<h3>No fragrance, essential oils, musks, dyes, film or PVA</h3>", rel)
    s = R(s, "<b>Waiting on:</b> Film spec showing 0% PVA, plus packaging confirmation", "<b>Waiting on:</b> Final formula showing no film or PVA, plus packaging confirmation", rel)
    s = R(s, "<b>Waiting on:</b> OECD 301B test on the finished sheet, film included", "<b>Waiting on:</b> OECD 301B test on the finished tab", rel)
    s = R(s, "<b>Waiting on:</b> Our own cold-water dissolving test", "<b>Waiting on:</b> Our own cold-water break-up and dissolving test on the finished tab", rel)
    wr(rel, s)

# mission block shared by several pages
SHARED = [
    ("Seven ingredients in the sheet, seven percent to the animals.", "Seven ingredients in the tab, seven percent to the animals."),
    ('<small>Sheets, pods and liquid</small>', '<small>Tabs, sheets, pods and liquid</small>'),
    ('"name": "Just 7 laundry sheets", "img"', '"name": "Just 7 Laundry Tabs", "img"'),
]
def shared():
    n = 0
    for r, _, fs in os.walk(D):
        for f in fs:
            if not f.endswith(".html"): continue
            p = os.path.join(r, f); s = open(p, encoding="utf-8").read(); o = s
            for a, b in SHARED: s = s.replace(a, b)
            s = add_tab_css(s)
            if s != o: open(p, "w", encoding="utf-8", newline="").write(s); n += 1
    print("shared:", n, "pages")

if __name__ == "__main__":
    home(); pdp(); ingredients(); howto(); compare(); planet(); why(); misc(); shared()
    print("MISSES:", len(MISS)); print("\n".join(MISS))
