# -*- coding: utf-8 -*-
"""v2 tabs: exact copy fixes on blog/page leftovers, dropped-post card removal, card title sync, stale JSON-LD removal
(seo_pass then regenerates FAQPage/Organization/WebSite from the visible copy). Idempotent. Run before seo_pass."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); DOCS = os.path.normpath(os.path.join(HERE, "..", "..", "docs"))
PEND = '<sup class="p"><a href="/pages/claims/" title="Pending proof before publishing" aria-label="Pending proof before publishing">†</a></sup>'

EB = "blogs/compare/earth-breeze-ingredients-vs-just-7/index.html"
FIXES = {
 EB: [
  ("Just 7 has seven, film included.", "Just 7 has seven, and no film at all."),
  ("Both counts include the tab&#x27;s film. Theirs is polyvinyl alcohol (PVA). Ours is a pullulan film made from fermented starch.",
   "Earth Breeze&#x27;s count includes its sheet&#x27;s film, polyvinyl alcohol (PVA). Just 7 is a pressed tab, so there&#x27;s no film to count."),
  ("<td>Sheet film</td><td>Polyvinyl alcohol (PVA)</td><td>Pullulan film made from fermented starch</td>", "<td>Format</td><td>Sheet with a polyvinyl alcohol (PVA) film</td><td>Pressed tab, no film</td>"),
  ("<td>Sodium citrate, sodium carbonate</td>", "<td>Sodium carbonate, citric acid, sodium citrate</td>"),
  ("<td>Kaolin clay, glycerin, water</td><td>Plant glycerin, water</td>", "<td>Kaolin clay, glycerin, water</td><td>Microcrystalline cellulose (binder), water</td>"),
  ('<ul><li><strong>Pullulan film made from fermented starch:</strong> holds the tab together and is designed to dissolve in the wash.' + PEND + '</li><li><strong>Water:</strong> carries everything while the tab is made.</li><li><strong>Plant glycerin:</strong> keeps the tab flexible so it doesn&#x27;t crack.</li><li><strong>Decyl glucoside:</strong> our main cleaner, a sugar-based glucoside.</li><li><strong>Lauryl glucoside:</strong> its close cousin, with a bit more cleaning power.</li><li><strong>Sodium citrate:</strong> softens hard water so the cleaners can work.</li><li><strong>Sodium carbonate:</strong> washing soda. It boosts cleaning and lifts greasy grime.</li></ul>',
   '<ul><li><strong>Sodium carbonate:</strong> washing soda. Lifts grease and softens water.</li><li><strong>Citric acid:</strong> makes a light fizz with the washing soda to break the tab apart, and helps with hard water.</li><li><strong>Sodium citrate:</strong> ties up hard-water minerals so the cleaners can work.</li><li><strong>Microcrystalline cellulose:</strong> holds the tab together, then swells in water to pop it apart.</li><li><strong>Lauryl glucoside:</strong> our main cleaner.</li><li><strong>Decyl glucoside:</strong> a second glucoside cleaner, picked for cold water.</li><li><strong>Water:</strong> a little, about 2%, that comes in with the cleaners.</li></ul>'),
  ("<strong>The film:</strong> they use PVA, we use a pullulan film made from fermented starch", "<strong>The film:</strong> they use PVA; Just 7 is a pressed tab with no film"),
  ("We started with what a tab has to do: clean, soften water and hold together.", "We started with what a tab has to do: clean, soften water, hold together and then break apart."),
  ("<li><strong>Count the film.</strong> It ends up in your wash water too.</li>", "<li><strong>Count the film, if there is one.</strong> It ends up in your wash water too.</li>"),
  ("<strong>Why count the film as an ingredient?</strong> It goes in your washer, and Earth Breeze counts its film too.", "<strong>Why count a film as an ingredient?</strong> It goes in your washer, and Earth Breeze counts its film too. Just 7 has none to count."),
 ],
 "blogs/compare/tru-earth-vs-earth-breeze-vs-just-7/index.html": [
  ("Both brands&#x27; lists include polyvinyl alcohol. Ours uses a pullulan film made from fermented starch.", "Both brands&#x27; lists include polyvinyl alcohol. Just 7 is a pressed tab with no film."),
  ("<td>Just 7</td><td>Pullulan</td>", "<td>Just 7</td><td>None (pressed tab)</td>"),
  ("Article 1 explains PVA and why we chose a different film.", 'Want the PVA background? <a href="/blogs/planet/are-laundry-sheets-plastic/">Read both sides</a>.'),
  ("All three lists include water, glycerin and sodium citrate.", "All three lists include water and sodium citrate."),
  ("$15 for 30 tabs, up to 60 loads", "$15 for 60 tabs, up to 60 loads"),
  ("If the shortest label and a non-PVA film matter most to you, Just 7 is built for that.", "If the shortest label and no film at all matter most to you, Just 7 is built for that."),
  ("<strong>Just 7</strong> is vegan, with no animal testing, no fragrance and no essential oils.", "<strong>Just 7</strong> has nothing from animals, no fragrance and no essential oils."),
 ],
 "blogs/compare/big-brand-laundry-sheets-vs-eco-brands/index.html": [("Pullulan, no PVA", "No film, no PVA")],
 "blogs/compare/earth-breeze-alternatives-5-checks-before-you-switch/index.html": [
  ("Yes. Some use pullulan films instead. Just 7 is one of them.", "Yes. Some use other films. Just 7 skips the film entirely: it&#x27;s a pressed tab."),
  ("Pullulan, no PVA", "None (pressed tab)"),
  ("Is it PVA, or something like pullulan or plant starch?", "Is it PVA, another film, or no film at all?"),
 ],
 "blogs/compare/how-to-judge-non-toxic-laundry-sheets/index.html": [("no fragrance and a pullulan film made from fermented starch", "no fragrance and no film")],
 "blogs/compare/laundry-strips-vs-laundry-sheets-is-there-a-difference/index.html": [("PVA or a starch-based film like pullulan?", "PVA, another film, or none? (Pressed tabs like Just 7 skip the film.)")],
 "blogs/home/why-fewer-ingredients-the-case-for-a-short-label/index.html": [
  ("<tr><td>Plant glycerin</td><td>Keeps the tab flexible</td></tr><tr><td>Water</td><td>Helps make the tab</td></tr><tr><td>Decyl glucoside</td><td>Lifts dirt</td></tr><tr><td>Lauryl glucoside</td><td>Lifts oily dirt</td></tr><tr><td>Sodium citrate</td><td>Softens water</td></tr><tr><td>Sodium carbonate</td><td>Boosts cleaning</td></tr><tr><td>Pullulan film</td><td>Holds it all together</td></tr>",
   "<tr><td>Sodium carbonate</td><td>Lifts grease, softens water</td></tr><tr><td>Citric acid</td><td>Fizz to break the tab apart</td></tr><tr><td>Sodium citrate</td><td>Ties up hard-water minerals</td></tr><tr><td>Microcrystalline cellulose</td><td>Holds the tab together, then pops it apart</td></tr><tr><td>Lauryl glucoside</td><td>Main cleaner</td></tr><tr><td>Decyl glucoside</td><td>Cold-water cleaner</td></tr><tr><td>Water</td><td>Comes in with the cleaners</td></tr>"),
  ("<strong>PVA film,</strong> because we chose a pullulan film instead", "<strong>Film and PVA,</strong> because a pressed tab doesn&#x27;t need a wrapper"),
 ],
 "blogs/life/why-we-named-it-just-7/index.html": [
  ("<tr><td>Decyl glucoside</td><td>Cleans</td></tr><tr><td>Lauryl glucoside</td><td>Cleans</td></tr><tr><td>Sodium carbonate</td><td>Softens water, boosts cleaning</td></tr><tr><td>Sodium citrate</td><td>Softens water</td></tr><tr><td>Plant glycerin</td><td>Keeps the tab flexible</td></tr><tr><td>Water</td><td>Helps make the tab</td></tr><tr><td>Pullulan film</td><td>Holds it together, no PVA</td></tr>",
   "<tr><td>Sodium carbonate</td><td>Lifts grease, softens water</td></tr><tr><td>Citric acid</td><td>Fizz to break the tab apart</td></tr><tr><td>Sodium citrate</td><td>Ties up hard-water minerals</td></tr><tr><td>Microcrystalline cellulose</td><td>Holds the tab together</td></tr><tr><td>Lauryl glucoside</td><td>Main cleaner</td></tr><tr><td>Decyl glucoside</td><td>Cold-water cleaner</td></tr><tr><td>Water</td><td>Comes in with the cleaners</td></tr>"),
 ],
 "blogs/life/laundry-in-an-rv-or-van/index.html": [
  ("Yes, tear off what you need.", "Yes. Dissolve one tab in warm water first."),
  ("<strong>Light and flat.</strong>", "<strong>Small and dry.</strong>"), ("<strong>Pre-measured.</strong> Tear a piece for small loads.", "<strong>Pre-measured.</strong> One tab per load."),
 ],
 "blogs/pets/what-to-do-if-your-pet-chews-a-laundry-tab-or-pod/index.html": [("Tabs are dry and flat, but", "Tabs are small and dry, but")],
 "blogs/planet/are-laundry-sheets-plastic/index.html": [
  ("Just 7 uses a pullulan film made from fermented starch." + PEND + " Pullulan is made by fermenting starch. It&#x27;s the same family as dissolving breath strips.",
   "We first planned a sheet, then moved Just 7 to a pressed tab so there&#x27;s no film at all: no PVA, nothing to wrap it." + PEND),
  ("A non-PVA film doesn&#x27;t automatically mean biodegradable.", "No film doesn&#x27;t automatically mean biodegradable."),
  ("<strong>Simplicity.</strong> A pullulan film fits a short label.", "<strong>Simplicity.</strong> No film means one less ingredient to explain."),
  ("<strong>Honesty.</strong> It&#x27;s easier to explain a film you can look up.", "<strong>Honesty.</strong> Seven ingredients, all on the label, nothing wrapped around them."),
  ("<strong>Is Just 7 PVA-free?</strong> Yes. It uses a pullulan film made from fermented starch.", "<strong>Is Just 7 PVA-free?</strong> Yes. It&#x27;s a pressed tab with no film."),
 ],
 "blogs/planet/cold-water-washing-save-energy-without-losing-clean/index.html": [("Most are designed to. Sheet in first, and tear it if your water is very cold.", "Most are designed to. Put it in first, and dissolve a tab in warm water first if your water is very cold.")],
 "blogs/planet/laundry-sheets-vs-pods-vs-liquid-an-environmental-comparison/index.html": [("A pullulan-film sheet like Just 7 sidesteps it.", "A pressed tab with no film, like Just 7, sidesteps it.")],
 "blogs/planet/zero-waste-laundry-10-swaps-that-actually-help/index.html": [("Look for cardboard packaging and a pullulan film.", "Look for cardboard packaging and no PVA film.")],
 "blogs/vegan/vegan-laundry-detergent/index.html": [
  ("<li><strong>Plant glycerin,</strong> not animal." + PEND + "</li><li><strong>Decyl and lauryl glucoside,</strong> sugar-based cleaners.</li><li><strong>Sodium citrate and sodium carbonate,</strong> simple salts.</li><li><strong>Pullulan film made from fermented starch.</strong>" + PEND + "</li>",
   "<li><strong>No glycerin</strong> at all.</li><li><strong>Decyl and lauryl glucoside,</strong> sugar-based cleaners.</li><li><strong>Sodium carbonate, citric acid and sodium citrate,</strong> simple salts and acids.</li><li><strong>Microcrystalline cellulose</strong> to hold the tab together.</li><li><strong>No film.</strong> The tab is pressed, not wrapped.</li>"),
 ],
 "blogs/ingredients/whats-in-laundry-detergent-sheets/index.html": [
  ("Just 7 uses a pullulan film made from fermented starch." + PEND, "Just 7 skips the film entirely: it&#x27;s a pressed tab."),
  ("<tr><td>Pullulan</td><td>Film</td><td>Yes</td></tr><tr><td>Glycerin</td><td>Keeps sheet flexible</td><td>Yes (vegan)</td></tr>", "<tr><td>Pullulan</td><td>Film</td><td>No</td></tr><tr><td>Glycerin</td><td>Keeps sheet flexible</td><td>No</td></tr><tr><td>Citric acid</td><td>Fizz, water softening</td><td>Yes</td></tr><tr><td>Microcrystalline cellulose</td><td>Binder for pressed tabs</td><td>Yes</td></tr>"),
  ("<td>Polyvinyl alcohol (PVA)</td><td>Film</td><td>No</td>", "<td>Polyvinyl alcohol (PVA)</td><td>Film</td><td>No (no film)</td>"),
 ],
 "blogs/ingredients/why-is-there-clay-in-some-detergents/index.html": [
  ("Kaolin&#x27;s job is structure, so it didn&#x27;t make our seven", "Kaolin is mostly there for bulk, so it didn&#x27;t make our seven. Our one binder, microcrystalline cellulose, also swells to help the tab break apart"),
  ("<td>Holds it together</td><td>Pullulan film, glycerin</td>", "<td>Holds it together</td><td>Films and glycerin in film-based formats; binders like cellulose in pressed tabs</td>"),
 ],
 "pages/planet/index.html": [("60 tabs weigh about half a pound.", "60 tabs weigh about 240 g (8.5 oz).")],
}
# rel -> (title or None, description or None). og:/twitter: titles and descriptions follow.
META = {
 "index.html": ("Just 7 Laundry Tabs: Seven Ingredients, Fragrance-Free", "Pressed laundry tabs with seven ingredients, every one named. One tab, one load. No film, no PVA, no plastic jug. Fragrance-free, nothing from animals. 7% of every sale goes to animal sanctuaries."),
 "products/just-7/index.html": (None, "Just 7 Laundry Tabs: pressed tabs with seven ingredients, fragrance-free, nothing from animals. 60 tabs, 1 per load. $19, or $15 with subscribe and save. Pre-order now. Coming soon."),
 "contact/index.html": (None, "Contact Just 7 Laundry Tabs."),
 "collections/all/index.html": ("Shop Just Seven: Just 7 Laundry Tabs and What's Next", None),
 "blogs/compare/index.html": (None, "Tabs vs sheets, pods, powder and liquid, and how to compare any brand. Plain-English comparisons from Just Seven."),
 "blogs/compare/laundry-tabs-vs-laundry-sheets/index.html": (None, "Both are dry and pre-measured. The big difference is the film. Here's how tabs and sheets compare, and why we chose a tab."),
 "blogs/compare/tru-earth-vs-earth-breeze-vs-just-7/index.html": (None, "Two laundry sheet brands and one pressed tab. We put each brand's own published ingredient list side by side so you can count, compare and choose."),
 "pages/learn/index.html": (None, "Plain-English guides to laundry detergent ingredients, pet-friendly washing, vegan and cruelty-free detergent, PVA and plastic, stain rescue and more."),
 "pages/compare/index.html": ("Laundry Tabs vs Sheets, Pods and Liquid: How Just 7 Compares", "How Just 7 Laundry Tabs compare with laundry sheets, pods and liquid detergent: the film, the jug, dosing, fragrance and the ingredient count."),
 "pages/how-to-use/index.html": ("How to Use Just 7 Laundry Tabs: Dosing and Tips", "How many Just 7 tabs to use, where to put them, cold water, HE machines, hand-washing and pretreating stains."),
 "pages/ingredients/index.html": (None, "The seven ingredients in Just 7 Laundry Tabs: sodium carbonate, citric acid, sodium citrate, microcrystalline cellulose, lauryl and decyl glucoside, and water. What each one does."),
 "pages/vegan/index.html": (None, "Nothing in Just 7 Laundry Tabs comes from animals: no glycerin, no musks, sugar-based cleaners and no film. See all seven ingredients."),
 "pages/business/index.html": ("Just 7 for Business: Bulk Laundry Tabs", None),
 "pages/pet-friendly/index.html": ("Pet-Friendly Laundry Tabs: No Essential Oils, No Fragrance", None),
 "pages/about/index.html": (None, "Just Seven makes laundry tabs with as few ingredients as possible, and 7% of every sale goes to animal sanctuaries and nonprofits. Our mission and our rules."),
 "pages/why-just-7/index.html": (None, "Why Just 7 Laundry Tabs: 7 ingredients, no film or PVA, no fragrance, nothing from animals, and 7% of every sale to animal sanctuaries."),
 "pages/planet/index.html": (None, "No film, no PVA, no plastic jug: pressed tabs in a pouch, with honest status on biodegradability and cold-water testing."),
}
def esc(t): return t.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#x27;")
def apply_meta(s, rel):
    if rel not in META: return s
    t, d = META[rel]
    if t:
        s = re.sub(r"<title>.*?</title>", "<title>" + t.replace("&", "&amp;") + "</title>", s, count=1)
        for k in ("og:title", "twitter:title"): s = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*(")', lambda m: m.group(1) + esc(t) + m.group(2), s)
    if d:
        for k in ("description", "og:description", "twitter:description"): s = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*(")', lambda m: m.group(1) + esc(d) + m.group(2), s)
    return s


FIXES2 = {
 "blogs/compare/laundry-balls-and-eggs-do-they-work/index.html": [("A short-list sheet with a pullulan film.", "A short-list pressed tab with no film, like Just 7.")],
 "blogs/compare/laundry-strips-vs-laundry-sheets-is-there-a-difference/index.html": [("Call it a tab or a strip. Either way, it&#x27;s seven ingredients with a pullulan film and no PVA.", "Just 7 isn&#x27;t a sheet or a strip. It&#x27;s a pressed tab: seven ingredients, no film and no PVA.")],
 "blogs/home/why-fewer-ingredients-the-case-for-a-short-label/index.html": [
  ("<strong>What are the 7 ingredients in Just 7?</strong> Plant glycerin, water, decyl glucoside, lauryl glucoside, sodium citrate, sodium carbonate and a pullulan film made from fermented starch.", "<strong>What are the 7 ingredients in Just 7?</strong> Sodium carbonate, citric acid, sodium citrate, microcrystalline cellulose, lauryl glucoside, decyl glucoside and water."),
  ("<strong>Why not fewer?</strong> Our gentle formula has five. Just 7 adds two for extra cleaning power.", "<strong>Why not fewer?</strong> Each of the seven has a job in a pressed tab: clean, soften water, hold together and break apart."),
 ],
 "blogs/compare/laundry-sheets-vs-laundry-powder-which-is-better/index.html": [("One tab, done", "One sheet, done")],
 "blogs/planet/cold-water-washing-save-energy-without-losing-clean/index.html": [
  ("<li><strong>Sheet in first,</strong> at the bottom of the drum.</li><li><strong>Use one tab</strong> for very cold water.</li>", "<li><strong>Tab in first,</strong> at the bottom of the drum.</li><li><strong>Pre-dissolve it</strong> in a cup of warm water for very cold or quick washes.</li>"),
  ("Just 7 is designed to dissolve in cold water.", "Just 7 is designed to break up in cold water, with a light fizz to help."),
  ("rubbing in a damp piece of sheet", "working in a tab dissolved in a spoonful of warm water"),
 ],
 "blogs/planet/laundry-sheets-vs-pods-vs-liquid-an-environmental-comparison/index.html": [("Sheets have a bonus move: use one tab for small loads.", "Sheets have a bonus move: tear one for small loads."), ("Can I pretreat with a tab?", "Can I pretreat with a sheet?")],
 "blogs/planet/what-does-biodegradable-really-mean-on-a-detergent-label/index.html": [("We&#x27;re designing Just 7 to break down, with a starch-based pullulan film.", "We&#x27;re designing Just 7 to break down, and it&#x27;s a pressed tab with no film."), ("We're designing Just 7 to break down, with a starch-based pullulan film.", "We're designing Just 7 to break down, and it's a pressed tab with no film.")],
 "blogs/planet/where-does-laundry-detergent-go-after-the-drain/index.html": [("Glucoside cleaners, sodium citrate and washing soda as softeners, a pullulan film made from fermented starch and no phosphates", "Glucoside cleaners, washing soda, citric acid and sodium citrate, no film and no phosphates")],
 "blogs/planet/zero-waste-laundry-10-swaps-that-actually-help/index.html": [("Jugs to sheets.", "Jugs to tabs."), ("Pick a pullulan or starch film to skip PVA.", "Pick a pressed tab with no film to skip PVA."), ("rub in a small piece of sheet", "work in a little dissolved detergent")],
 "blogs/planet/are-laundry-sheets-plastic/index.html#2": [],
 "blogs/planet/how-to-save-water-on-laundry-day/index.html": [("Measured sheets make this easy", "Pre-measured tabs make this easy")],
 "blogs/vegan/hidden-animal-ingredients-in-cleaning-products/index.html": [("Our film is made from fermented starch.", "There&#x27;s no glycerin and no film."), ("Our film is made from fermented starch.", "There's no glycerin and no film.")],
 "blogs/vegan/a-simple-vegan-cleaning-routine-for-the-whole-house/index.html": [("vegan sheets with a short label", "a short-label detergent with nothing from animals")],
}
FIXES2["blogs/planet/are-laundry-sheets-plastic/index.html"] = [("Just 7 uses a pullulan film made from fermented starch instead.", "Just 7 skips the question: it&#x27;s a pressed tab with no film."), ("Just 7 uses a pullulan film made from fermented starch instead.", "Just 7 skips the question: it's a pressed tab with no film.")]
FIXES2.pop("blogs/planet/are-laundry-sheets-plastic/index.html#2", None)
FIXES2.setdefault("blogs/ingredients/whats-in-laundry-detergent-sheets/index.html", []).extend([
  ("Some newer ones use films like pullulan, made by fermenting starch.", "Some newer ones use other dissolving films. Pressed tabs skip the film."),
  ("<tr><td>Pullulan</td><td>Film</td><td>No</td></tr>", ""),
  ("PVA, PVOH, pullulan or starch.", "PVA, PVOH, another film, or none at all."),
])
for k, v in FIXES2.items(): FIXES.setdefault(k, []).extend(v)

GLOBAL = [
 (r"\b[Oo]ur gentle (?:sheet|tab)\b", lambda m: ("O" if m.group(0)[0] == "O" else "o") + "ur gentle formula"),
 (r"one tab of our gentle formula", "a dose of our gentle formula"),
 (r"Which Just sheet\b", "Which Just formula"),
 (r'<div class="band" role="list" aria-label="The Just lineup">', '<div class="band" role="group" aria-label="The Just lineup">'), (r'<button type="button" role="listitem" data-tip=', '<button type="button" data-tip='), (r"Pack sheets, skip the jug", "Pack tabs, skip the jug"),
 (r"Tabs, tabs, pods and liquid", "Tabs, sheets, pods and liquid"),
 (r"<h1([^>]*)>Laundry Sheets vs Pods vs Liquid: How Just 7 Compares</h1>", r"<h1\1>Laundry Tabs vs Sheets, Pods and Liquid: How Just 7 Compares</h1>"),
]
DROPPED_TITLE = r"(?:What Is Pullulan|Plant Glycerin in Laundry Sheets|PVA-Free Laundry Sheets|Our gentle (?:sheet|formula|tab) vs Just 7)"

def drop_cards(s):
    s = re.sub(r'<a class="post" href="[^"]*"[^>]*>(?:(?!</a>).)*?<h3>' + DROPPED_TITLE + r'(?:(?!</a>).)*?</a>', "", s, flags=re.S)
    s = re.sub(r'<li><a href="[^"]*"><span><h3>' + DROPPED_TITLE + r'(?:(?!</li>).)*?</li>', "", s, flags=re.S)
    return s

def h1_of(url, cache):
    if url not in cache:
        p = os.path.join(DOCS, url.strip("/"), "index.html"); t = None
        if os.path.isfile(p):
            m = re.search(r"<h1[^>]*>(.*?)</h1>", open(p, encoding="utf-8").read(), re.S); t = m.group(1).strip() if m else None
        cache[url] = t
    return cache[url]

def sync(s, cache):
    rx = re.compile(r'(<a (?:class="post" )?href="(/blogs/[^"]+/)"[^>]*>(?:(?!</a>).)*?<h3>)(.*?)(</h3>)', re.S)
    return rx.sub(lambda m: m.group(1) + (h1_of(m.group(2), cache) or m.group(3)) + m.group(4), s)

BAD_LD = re.compile(r"(?i)sheets?(?!\.com)|pullulan|glycerin|\btear|\bhalf\b")
def strip_stale_ld(s, rel):
    if rel.startswith("pages/faq/"): return s
    def f(m):
        try: j = json.loads(m.group(1))
        except Exception: return m.group(0)
        t = j.get("@type")
        body = m.group(1).replace("just7sheets", "")
        if t in ("FAQPage",) and BAD_LD.search(body): return ""
        if rel == "index.html" and t in ("Organization", "WebSite"): return ""
        return m.group(0)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', f, s, flags=re.S)

def run():
    cache, n = {}, 0
    for dp, dn, fns in os.walk(DOCS):
        if os.path.isfile(os.path.join(dp, ".stub")): continue
        for fn in fns:
            if not fn.endswith(".html"): continue
            p = os.path.join(dp, fn); rel = os.path.relpath(p, DOCS).replace(os.sep, "/")
            s0 = s = open(p, encoding="utf-8").read()
            for a, b in FIXES.get(rel, []):
                if a not in s and b not in s: print("MISS", rel, a[:70])
                s = s.replace(a, b)
            for a, b in GLOBAL: s = re.sub(a, b, s)
            s = apply_meta(s, rel); s = drop_cards(s); s = sync(s, cache); s = strip_stale_ld(s, rel)
            if s != s0: open(p, "w", encoding="utf-8").write(s); n += 1
    print("polished", n)

if __name__ == "__main__":
    run()
