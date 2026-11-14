# -*- coding: utf-8 -*-
"""v2 tabs: hand-written bodies for the renamed product posts. Idempotent. Run after blogs_v2.py."""
import os, re, json, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); DOCS = os.path.normpath(os.path.join(HERE, "..", "..", "docs"))
P = '<sup class="p"><a href="/pages/claims/" title="Pending proof before publishing" aria-label="Pending proof before publishing">†</a></sup>'
def L(u, t="read it"): return f'<a href="{u}">{t}</a>'

POSTS = {
"how-to/how-many-laundry-tabs-per-load": dict(
 title="How Many Laundry Tabs Per Load? A Simple Chart", h1="How Many Laundry Tabs Per Load?",
 desc="One tab or two? Here's the easy chart for every load size, plus when a second tab makes sense.",
 body=f"""<p>Good news. This is the shortest dosing guide in laundry history.</p>
<p class="quick"><strong>Quick answer:</strong> use one Just 7 tab for a small or regular load. Use two for a large, very dirty or hard-water load.</p>
<h2 id="the-chart">The chart</h2>
<div class="tablewrap"><table><tr><th scope="col">Load</th><th scope="col">Tabs</th></tr><tr><td>Small</td><td>One</td></tr><tr><td>Regular</td><td>One</td></tr><tr><td>Large</td><td>Two</td></tr><tr><td>Very dirty</td><td>Two</td></tr><tr><td>Very hard water</td><td>Two</td></tr></table></div>
<p>{P}</p>
<h2 id="how-big-is-a-normal-load">How big is a &quot;normal&quot; load?</h2>
<p>Roughly a full drum that&#x27;s loosely packed, with room for a hand at the top. If you have to push clothes down to close the lid, that&#x27;s a large load. Or a cry for help.</p>
<h2 id="when-to-use-two">When to use two</h2>
<ul><li>Muddy sports kits</li><li>Heavy bedding</li><li>Very hard water ({L('/blogs/how-to/hard-water-laundry-why-clothes-feel-stiff-and-how-to-fix-it/')})</li><li>Pet bedding</li></ul>
<h2 id="can-i-split-a-tab">Can I split a tab?</h2>
<p>We don&#x27;t recommend it. Each tab is pressed to be one dose. For a single item, hand-wash it with a tab dissolved in warm water ({L('/blogs/how-to/how-to-hand-wash-clothes-with-a-laundry-tab/')}).</p>
<h2 id="using-too-much">Using too much</h2>
<p>More isn&#x27;t better. Extra detergent can leave residue and make towels stiff ({L('/blogs/home/do-you-need-an-extra-rinse-detergent-residue-explained/')}). Stick to the chart.</p>""",
 faq=[("How many laundry tabs should I use?", "One for a small or regular load, two for a large or very dirty one."),
      ("Do I need two tabs in an HE washer?", "Usually not. One is enough for most HE loads."),
      ("Can I break a tab in half?", "We don't recommend it. Each tab is one dose."),
      ("What if my water is very hard?", "Use two tabs for dirty loads in very hard water.")]),
"how-to/do-laundry-tabs-dissolve-in-cold-water": dict(
 title="Do Laundry Tabs Dissolve in Cold Water?", h1="Do Laundry Tabs Dissolve in Cold Water?",
 desc="Why a tab can be slow in a cold, short or packed wash, how the fizz helps, and four easy fixes.",
 body=f"""<p>You open the washer and find a crumb of detergent clinging to your favorite sweater. Not the vibe.</p>
<p class="quick"><strong>Quick answer:</strong> Just 7 tabs are designed to break up in warm or cold water, helped by a light fizz.{P} When a tab is slow, it&#x27;s usually a very cold, very short or very full cycle. Put it in first and give clothes room.</p>
<h2 id="how-the-fizz-helps">How the fizz helps</h2>
<p>Each tab has citric acid and washing soda. In water they react and make a light fizz, while the cellulose binder swells. Together they push the tab apart so the cleaners can get to work.</p>
<h2 id="why-a-tab-might-be-slow">Why a tab might be slow</h2>
<ul><li><strong>Very cold water,</strong> like a winter tap.</li><li><strong>A very short cycle,</strong> like a quick wash.</li><li><strong>An overloaded drum,</strong> so water can&#x27;t move around it.</li><li><strong>The tab got trapped</strong> in a fold of wet fabric.</li></ul>
<h2 id="four-easy-fixes">Four easy fixes</h2>
<ol><li><strong>Put it in first,</strong> at the bottom of the empty drum.</li><li><strong>Don&#x27;t overload.</strong> Leave a hand&#x27;s width at the top.</li><li><strong>Pick a normal cycle</strong> over a quick one for cold washes.</li><li><strong>Pre-dissolve</strong> the tab in a cup of warm water for very cold or short cycles.</li></ol>
<h2 id="found-a-bit">Found a bit on your clothes?</h2>
<p>No stress. Rinse the item under warm water or run a rinse cycle. It washes right out.</p>
<h2 id="what-about-our-tabs">What about our tabs?</h2>
<p>We&#x27;re testing Just 7 in cold water and will publish what we find.{P}</p>""",
 faq=[("Will laundry tabs dissolve in cold water?", "Just 7 is designed to, with a light fizz to help. Very cold, short or packed cycles can slow any detergent down."),
      ("What do I do if a tab doesn't fully dissolve?", "Rinse the item, then next time put the tab in first and load less."),
      ("Can I pre-dissolve a laundry tab?", "Yes, let it fizz apart in a cup of warm water, then pour it into the drum."),
      ("Is leftover residue harmful to clothes?", "It usually rinses out. Run a rinse cycle.")]),
"how-to/can-you-use-laundry-tabs-in-a-high-efficiency-washer": dict(
 title="Can You Use Laundry Tabs in a High-Efficiency Washer?", h1="Can You Use Laundry Tabs in a High-Efficiency Washer?",
 desc="Short answer: yes, if they're low-sudsing. Here's where the tab goes in an HE washer and why suds don't matter.",
 body=f"""<p>HE washers use less water, so they need detergent that doesn&#x27;t foam up like a bubble bath.</p>
<p class="quick"><strong>Quick answer:</strong> yes. Just 7 is designed for HE and standard washers.{P} Its glucoside cleaners are low-sudsing. Put one tab in the empty drum, then add clothes.</p>
<h2 id="where-the-tab-goes">Where the tab goes</h2>
<p>In the drum, not the dispenser drawer. Front loader: drop it at the back of the empty drum. Top loader: on the bottom, then clothes on top.</p>
<h2 id="why-low-suds-matters">Why low suds matters</h2>
<p>Too much foam can cushion clothes, confuse sensors and leave residue in a low-water machine. Suds don&#x27;t equal clean.</p>
<h2 id="how-many-tabs">How many tabs?</h2>
<p>One for a small or regular load, two for a large or very dirty one ({L('/blogs/how-to/how-many-laundry-tabs-per-load/')}).</p>
<h2 id="the-fizz">What about the fizz?</h2>
<p>The light fizz is a few moments of bubbles from citric acid and washing soda as the tab breaks up. It isn&#x27;t foam and it&#x27;s over fast.</p>""",
 faq=[("Are laundry tabs safe for HE washers?", "Just 7 is designed for HE and standard washers, with low-sudsing cleaners."),
      ("Do I put the tab in the dispenser?", "No. Put it in the empty drum, then add clothes."),
      ("Why are there hardly any suds?", "Low suds is normal and what HE washers want.")]),
"how-to/how-to-use-laundry-detergent-tabs-in-any-washer": dict(
 title="How to Use Laundry Detergent Tabs in Any Washer", h1="How to Use Laundry Detergent Tabs in Any Washer",
 desc="Top-load, front-load and HE: where the tab goes, how many to use, and what to do for cold or quick cycles.",
 body=f"""<p>Three steps. Fewer if you count &quot;wash&quot; as optional. (It isn&#x27;t.)</p>
<p class="quick"><strong>Quick answer:</strong> drop one tab in the empty drum, add clothes on top and run your usual cycle. Use two tabs for a large or very dirty load.</p>
<h2 id="front-loaders">Front loaders</h2>
<p>Put the tab at the back of the empty drum, then load clothes. Skip the dispenser drawer.</p>
<h2 id="top-loaders">Top loaders</h2>
<p>Drop the tab on the bottom of the drum, or around the agitator, before clothes go in.</p>
<h2 id="he-washers">HE washers</h2>
<p>Same as above. Just 7 is low-sudsing and designed for HE.{P} ({L('/blogs/how-to/can-you-use-laundry-tabs-in-a-high-efficiency-washer/')})</p>
<h2 id="cold-or-quick-cycles">Cold or quick cycles</h2>
<p>Put the tab in first and don&#x27;t overload. For very cold or very short cycles, let it fizz apart in a cup of warm water first ({L('/blogs/how-to/do-laundry-tabs-dissolve-in-cold-water/')}).</p>
<h2 id="hand-washing">Hand washing</h2>
<p>Dissolve one tab in a sink of warm water ({L('/blogs/how-to/how-to-hand-wash-clothes-with-a-laundry-tab/')}).</p>""",
 faq=[("Where do I put a laundry tab?", "In the empty drum, before clothes. Not the dispenser."),
      ("How many tabs per load?", "One for a small or regular load, two for large or very dirty."),
      ("Can I use tabs in a top loader with an agitator?", "Yes. Drop the tab in around the agitator before adding clothes.")]),
"how-to/how-to-store-laundry-tabs-so-they-last": dict(
 title="How to Store Laundry Tabs So They Last", h1="How to Store Laundry Tabs So They Last",
 desc="Keep tabs dry, sealed and out of reach. Where to keep the pouch and what to do if a tab gets damp.",
 body=f"""<p>Tabs have one enemy: water before wash day.</p>
<p class="quick"><strong>Quick answer:</strong> keep the pouch sealed, dry and out of reach of kids and pets. Grab tabs with dry hands, and keep them away from steam.</p>
<h2 id="why-dry-matters">Why dry matters</h2>
<p>Water starts the fizz. A damp tab can soften, crumble or stick to its neighbours. It still works, but it&#x27;s messier.</p>
<h2 id="where-to-keep-it">Where to keep the pouch</h2>
<ul><li>A closed cabinet or high shelf</li><li>Away from the dryer vent and steam</li><li>Not on the floor next to the washer</li></ul>
<h2 id="a-tab-got-damp">A tab got damp?</h2>
<p>Use it in the next wash. Dry the pouch before resealing.</p>
<h2 id="kids-and-pets">Kids and pets</h2>
<p>Any detergent can harm if eaten. Keep tabs sealed and out of reach ({L('/blogs/pets/what-to-do-if-your-pet-chews-a-laundry-tab-or-pod/')}).</p>""",
 faq=[("Do laundry tabs expire?", "We'll print a best-by guide once our manufacturer confirms it. Stored sealed and dry, tabs keep well."),
      ("Can I keep tabs in the laundry room?", "Yes, if it's dry. Keep them away from steam and the dryer vent."),
      ("Can I use a tab that got damp?", "Yes, in the next wash.")]),
"how-to/laundry-tabs-for-travel-and-camping": dict(
 title="Laundry Tabs for Travel and Camping", h1="Laundry Tabs for Travel and Camping",
 desc="No leaking bottles in your bag. Laundry tabs are small, dry and easy to pack. Here's how to wash on the road.",
 body=f"""<p>Nobody wants a detergent leak all over their clean socks.</p>
<p class="quick"><strong>Quick answer:</strong> laundry tabs are small, dry and don&#x27;t spill, so they pack easily. One tab dissolved in warm water does a sink wash; one tab does a machine load.</p>
<h2 id="how-many-to-pack">How many to pack</h2>
<p>One tab per sink wash or machine load. Keep them in a small, dry, sealed container.</p>
<h2 id="sink-washing">Sink washing</h2>
<ol><li>Plug the sink and fill with warm water.</li><li>Drop in one tab and let it fizz apart.</li><li>Swish clothes, soak 15 to 30 minutes.</li><li>Rinse until the water runs clear, then roll in a towel to dry.</li></ol>
<h2 id="camping">Camping</h2>
<p>Wash in a basin, away from lakes and streams, and follow local rules for greywater.</p>
<h2 id="flying">Flying</h2>
<p>Tabs are dry, not liquid. Check current airline and TSA rules before you fly.</p>""",
 faq=[("Can I take laundry tabs on a plane?", "They're dry, not liquid. Check current airline and TSA rules before you fly."),
      ("How do I wash clothes in a hotel sink?", "Dissolve one tab in warm water, wash, rinse and roll in a towel to dry.")]),
"how-to/how-to-hand-wash-clothes-with-a-laundry-tab": dict(
 title="How to Hand-Wash Clothes With a Laundry Tab", h1="How to Hand-Wash Clothes With a Laundry Tab",
 desc="Sink, basin or bucket: dissolve one tab, soak, rinse and dry. A simple hand-wash routine.",
 body=f"""<p>Some things deserve a little hands-on care. Or you&#x27;re in a hotel. Either way.</p>
<p class="quick"><strong>Quick answer:</strong> dissolve one tab in a sink of warm water, swish clothes, soak 15 to 30 minutes, then rinse until the water runs clear.</p>
<h2 id="what-you-need">What you need</h2>
<ul><li>A clean sink, basin or bucket</li><li>One laundry tab</li><li>Water at the temperature the label allows</li></ul>
<h2 id="steps">Steps</h2>
<ol><li>Fill with water and drop in the tab. Let it fizz apart.</li><li>Add clothes and swish gently.</li><li>Soak 15 to 30 minutes.</li><li>Rinse in clean water until it runs clear.</li><li>Press out water (don&#x27;t wring) and dry flat or hang.</li></ol>
<h2 id="delicates">Delicates</h2>
<p>Use cool water for wool, silk and lace, and follow the care label.</p>""",
 faq=[("How much detergent for hand washing?", "One tab in a sink of water."),
      ("Can I hand-wash wool with Just 7?", "Yes for washable wool: cool water, gentle handling, dry flat.")]),
"compare/laundry-tabs-vs-laundry-sheets": dict(
 title="Laundry Tabs vs Laundry Sheets: Which Is Better?", h1="Laundry Tabs vs Laundry Sheets",
 desc="Both are dry and pre-measured. The big difference is the film. Here's how tabs and sheets compare, and why we chose a tab.",
 body=f"""<p>Two dry formats walk into a washer. One is flat, one is round. Which one&#x27;s for you?</p>
<p class="quick"><strong>Quick answer:</strong> both are pre-measured and low-mess. Most laundry sheets need a film to hold them together, often PVA. A pressed tab doesn&#x27;t need a film at all. That&#x27;s why Just 7 is a tab.</p>
<h2 id="side-by-side">Side by side</h2>
<div class="tablewrap"><table><tr><th scope="col"></th><th scope="col">Pressed tabs</th><th scope="col">Laundry sheets</th></tr><tr><td>Held together by</td><td>Pressure and a binder</td><td>Usually a film, often PVA</td></tr><tr><td>Dosing</td><td>One or two per load</td><td>Tear for small loads</td></tr><tr><td>Breaking up</td><td>Fizz and swell (Just 7)</td><td>Film dissolves</td></tr><tr><td>Storage</td><td>Keep dry</td><td>Keep dry</td></tr></table></div>
<h2 id="the-film-question">The film question</h2>
<p>A sheet&#x27;s film counts as an ingredient, and many brands use polyvinyl alcohol (PVA). People debate how fully PVA breaks down after the drain ({L('/blogs/planet/are-laundry-sheets-plastic/')}). A pressed tab skips that debate: no film, no PVA.</p>
<h2 id="why-we-switched">Why we switched</h2>
<p>We first planned a sheet. Moving to a pressed tab let us drop the film entirely and still keep the list to seven ingredients.</p>
<h2 id="the-tradeoffs">The tradeoffs</h2>
<p>Sheets can be torn for tiny loads; tabs are one dose each. Both need dry storage. Neither replaces a pretreat on heavy stains.</p>""",
 faq=[("Are laundry tabs better than sheets?", "It depends on what you value. Tabs need no film; sheets can be torn for small loads."),
      ("Do laundry tabs have PVA?", "Some wrapped tabs do. Just 7 tabs are pressed with no film, so no PVA."),
      ("Can I split a laundry tab?", "We don't recommend it. Each tab is one dose.")]),
"compare/just-7-faq-everything-people-ask-about-our-tabs": dict(
 title="Just 7 Laundry Tabs FAQ: Ingredients, Pets and More", h1="Just 7 FAQ: Everything People Ask About Our Tabs",
 desc="Every question about Just 7 in one place: the seven ingredients, how to use a tab, pets, the planet, shipping and the rest.",
 body=f"""<p>Got a question? Someone&#x27;s probably asked it already. Here&#x27;s the lot, short and sweet.</p>
<p class="quick"><strong>Quick answer:</strong> Just 7 is a fragrance-free pressed laundry tab with seven ingredients and no film or PVA. One tab per small or regular load, two for large, in any washer.</p>
<h2 id="ingredients">Ingredients</h2>
<p><strong>What&#x27;s in Just 7?</strong> Sodium carbonate, citric acid, sodium citrate, microcrystalline cellulose, lauryl glucoside, decyl glucoside and water ({L('/pages/ingredients/')}).</p>
<p><strong>Is there fragrance?</strong> No fragrance, no essential oils, no dyes ({L('/blogs/ingredients/why-just-7-is-fragrance-free/')}).</p>
<p><strong>Anything from animals?</strong> No. Nothing in Just 7 comes from animals.{P}</p>
<h2 id="using-it">Using it</h2>
<p><strong>How many tabs per load?</strong> One for small or regular loads, two for large or very dirty ones ({L('/blogs/how-to/how-many-laundry-tabs-per-load/')}).</p>
<p><strong>Does it work in cold water?</strong> It&#x27;s designed to break up in cold water, with a light fizz to help.{P}</p>
<p><strong>Does it work in HE washers?</strong> Yes, it&#x27;s low-sudsing.{P}</p>
<p>If you can count to one, you&#x27;ve mastered it.</p>
<h2 id="pets">Pets</h2>
<p><strong>Is Just 7 pet-friendly?</strong> It has no fragrance or essential oils. Still, store it out of reach ({L('/blogs/pets/what-to-do-if-your-pet-chews-a-laundry-tab-or-pod/')}).</p>
<h2 id="the-planet">The planet</h2>
<p><strong>Is there plastic film?</strong> No. The tab is pressed, not wrapped: no film, no PVA ({L('/blogs/planet/are-laundry-sheets-plastic/')}).</p>
<p><strong>Is it biodegradable?</strong> We&#x27;re testing the finished tab before we say so ({L('/blogs/planet/what-does-biodegradable-really-mean-on-a-detergent-label/')}).</p>
<h2 id="more">More answers</h2>
<p>Over a thousand more questions, answered in our {L('/pages/faq/', 'FAQ')}.</p>""",
 faq=[("What's in Just 7?", "Sodium carbonate, citric acid, sodium citrate, microcrystalline cellulose, lauryl glucoside, decyl glucoside and water."),
      ("How many tabs per load?", "One for small or regular loads, two for large or very dirty ones."),
      ("Is there plastic film?", "No. The tab is pressed, not wrapped: no film, no PVA.")]),
}

def apply(rel, d):
    p = os.path.join(DOCS, "blogs", rel, "index.html"); s = open(p, encoding="utf-8").read()
    e = lambda t: H.escape(t, quote=True).replace("&#x27;", "&#x27;")
    s = re.sub(r"<title>.*?</title>", f"<title>{H.escape(d['title'], quote=False)}</title>", s, count=1)
    for k in ("description", "og:description", "twitter:description"):
        s = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*(")', lambda m: m.group(1) + e(d["desc"]) + m.group(2), s)
    for k in ("og:title", "twitter:title"):
        s = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*(")', lambda m: m.group(1) + e(d["title"]) + m.group(2), s)
    s = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1) + H.escape(d["h1"], quote=False) + m.group(2), s, count=1)
    s = re.sub(r'(<span aria-current="page">).*?(</span>)', lambda m: m.group(1) + H.escape(d["h1"], quote=False) + m.group(2), s, count=1)
    body = d["body"]
    faq_html = '\n<h2 id="faq">FAQ</h2>\n' + "\n".join(f"<p><strong>{H.escape(q, quote=False)}</strong> {H.escape(a, quote=False)}</p>" for q, a in d["faq"])
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body))
    s = re.sub(r'<details class="toc">.*?</details>', f'<details class="toc"><summary>In this article</summary><ol>{toc}</ol></details>', s, count=1, flags=re.S)
    a = s.index("</details></div>") + len("</details></div>"); b = s.index('<div class="cta">')
    s = s[:a] + "\n" + body + faq_html + "\n" + s[b:]
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    def ld(m):
        try: j = json.loads(m.group(2))
        except Exception: return m.group(0)
        t = j.get("@type")
        if t == "BlogPosting": j.update(headline=d["h1"], description=d["desc"], wordCount=words)
        elif t == "BreadcrumbList": j["itemListElement"][-1]["name"] = d["h1"]
        elif t == "FAQPage": j["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]
        return m.group(1) + json.dumps(j, ensure_ascii=False) + m.group(3)
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, s, flags=re.S)
    open(p, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    for rel, d in POSTS.items(): apply(rel, d)
    print("posts rewritten:", len(POSTS))
