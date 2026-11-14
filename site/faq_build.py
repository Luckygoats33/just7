"""Builds the Just 7 FAQ from site/faq/c*.py (one module per category).
Writes docs/assets/faq.json (all answers, used by Ask Just), the hub docs/pages/faq/index.html
and one page per category at docs/pages/faq/<slug>/index.html, from site/faq/shell.html.
Idempotent. Order after any rebuild: creators.py -> seo_pass.py -> faq_build.py -> ask_just.py -> sitemap_robots.py"""
import os, re, json, html, glob, difflib, importlib.util, sys
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.normpath(os.path.join(HERE, "..", "docs"))
SITE = "https://just7sheets.com"; TARGET = 1111
BANNED = re.compile(r"pet[\s-]?safe|plant[\s-]?based|plant[\s-]?derived|derived from plant[s]|made from plant[s]|plant[\s-]?sourced|come[s]? from plants|plants onl[y]", re.I)
SUP = '<sup class="p"><a href="/pages/claims/" title="Pending proof: see our claims page" aria-label="Pending proof: see our claims page">†</a></sup>'
PRE = "Pre-order now. Coming soon."

def load():
    cats = []
    for f in sorted(glob.glob(os.path.join(HERE, "faq", "c*.py"))):
        sp = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        cats.append((m.CAT, m.QA))
    return cats

def exists(path):
    p = path.split("#")[0]
    return os.path.exists(os.path.join(D, p.strip("/"), "index.html")) or os.path.isfile(os.path.join(D, p.strip("/")))

def render(a, errs, q):
    def link(m):
        t, u = m.group(1), m.group(2)
        if not exists(u): errs.append(f"bad link {u} in: {q}")
        if BANNED.search(u): errs.append(f"banned slug {u} in: {q}")
        return f'<a href="{u}">{html.escape(t, quote=False)}</a>'
    parts = re.split(r"(\[[^\]]+\]\([^)]+\))", a); out = []
    for p in parts:
        m = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", p)
        out.append(link(m) if m else html.escape(p, quote=False))
    s = "".join(out).replace("†", SUP)
    return s

def plain(h): return html.unescape(re.sub(r"<sup.*?</sup>", "", re.sub(r"<(?!sup)[^>]+>", "", h)) if False else re.sub(r"<[^>]+>", "", re.sub(r"<sup.*?</sup>", "", h)))

def norm(q): return re.sub(r"[^a-z0-9 ]", "", q.lower().replace("just 7", "")).strip()

def slug(q, used):
    s = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:64].rstrip("-"); b = s; i = 2
    while s in used: s = f"{b}-{i}"; i += 1
    used.add(s); return s

def build_items():
    cats = load(); errs = []; items = []; seen = {}; used = set(); dups = []
    for (cs, ct, cd), qa in cats:
        for q, a in qa:
            n = norm(q)
            if n in seen: dups.append((q, seen[n])); continue
            key = " ".join(sorted(set(n.split())))
            if key in seen: dups.append((q, seen[key])); continue
            seen[key] = q
            seen[n] = q
            h = render(a, errs, q)
            if BANNED.search(q) or BANNED.search(a): errs.append("banned phrase: " + q)
            items.append({"id": slug(q, used), "q": q, "a": h, "c": cs})
    return cats, items, errs, dups

def ld(o): return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + "</script>"

def faq_ld(its): return ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": i["q"], "acceptedAnswer": {"@type": "Answer", "text": plain(i["a"])}} for i in its]})

def crumbs(trail): return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": n + 1, "name": t, "item": SITE + u} for n, (t, u) in enumerate(trail)]})

CSS = """<style id="j7-faq-css">
.faqlay2,.faqlay2>*,.faqnav{min-width:0}
.faqnav{position:sticky;top:0;z-index:5;background:var(--bg,#fff);padding:8px 0;margin:0 -4px}
.faqnav ul{list-style:none;margin:0;padding:0 4px 4px;display:flex;gap:6px;overflow-x:auto;scrollbar-width:thin}
.faqnav a{display:inline-flex;gap:6px;align-items:center;white-space:nowrap;text-decoration:none;color:var(--ink);font:700 .9rem var(--f-display);padding:8px 12px;border:1px solid var(--line);border-radius:999px;background:var(--card);min-height:40px}
.faqnav a[aria-current]{background:var(--ink);color:#fff;border-color:var(--ink)}
.faqnav small{color:inherit;opacity:.8}
@media (min-width:960px){.faqlay2{display:grid;grid-template-columns:260px 1fr;gap:32px;align-items:start}.faqnav{top:90px;background:none;margin:0}.faqnav ul{flex-direction:column;overflow:visible;max-height:calc(100vh - 120px);overflow-y:auto}.faqnav a{border:0;background:none;justify-content:space-between;border-radius:10px}.faqnav a:hover{background:var(--sage-tint)}}
.fcards{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));list-style:none;padding:0;margin:0}
.fcards a{display:block;height:100%;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 18px}
.fcards a:hover{border-color:var(--ink)}.fcards b{display:block;font:800 1.08rem var(--f-display)}.fcards span{display:block;color:var(--mute);font-size:.92rem;margin-top:4px}
.fres{display:grid;gap:10px}.fres .src{display:block;margin-top:6px;font-size:.88rem}
</style>"""

def nav(cats_count, cur):
    lis = "".join(f'<li><a href="/pages/faq/{s}/"{" aria-current=\"page\"" if s == cur else ""}>{html.escape(t)}<small>{n}</small></a></li>' for s, t, n in cats_count)
    return f'<nav class="faqnav" aria-label="FAQ topics"><ul><li><a href="/pages/faq/"{" aria-current=\"page\"" if cur == "" else ""}>All topics<small>{sum(n for *_, n in cats_count)}</small></a></li>{lis}</ul></nav>'

def qa_html(i): return f'<details class="qa" id="{i["id"]}"><summary>{html.escape(i["q"], quote=False)}</summary><div class="a"><p>{i["a"]}</p></div></details>'

SEARCH = '<div class="search field" style="max-width:640px"><label class="sr" for="{id}">{label}</label><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg><input id="{id}" type="text" placeholder="{ph}" autocomplete="off"></div>'

HUBJS = """<script>(function(){var i=document.getElementById("faq-all"),o=document.getElementById("faq-results"),c=document.getElementById("faq-cats"),d,p,t;if(!i)return;
function L(){return p||(p=fetch("/assets/faq.json").then(function(r){return r.json()}).then(function(j){d=j;return j}))}
function e(s){return s.replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function run(){var v=i.value.trim().toLowerCase();if(v.length<2){o.hidden=true;o.innerHTML="";c.hidden=false;return}L().then(function(j){var w=v.split(/\\s+/),n={};j.cats.forEach(function(x){n[x[0]]=x[1]});var r=j.items.filter(function(x){var s=(x.q+" "+x.a.replace(/<[^>]+>/g," ")).toLowerCase();return w.every(function(k){return s.indexOf(k)>-1})});
o.innerHTML='<p class="mute" role="status">'+(r.length?r.length+" answer"+(r.length>1?"s":"")+(r.length>30?", showing 30":""):'No answers match. Try fewer words, or <a href="/pages/contact/">ask a person</a>.')+"</p>"+r.slice(0,30).map(function(x){return'<details class="qa"><summary>'+e(x.q)+'</summary><div class="a"><p>'+x.a+'<span class="src"><a href="/pages/faq/'+x.c+"/#"+x.id+'">More in '+e(n[x.c])+"</a></span></p></div></details>"}).join("");o.hidden=false;c.hidden=true})}
i.addEventListener("focus",L,{once:true});i.addEventListener("input",function(){clearTimeout(t);t=setTimeout(run,160)})})();</script>"""

def page(shell, title, desc, url_path, main, lds):
    s = shell
    s = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title, quote=False)}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE}{url_path}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{SITE}{url_path}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(title)}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(desc)}">', s, count=1)
    s = re.sub(r'<meta name="twitter:(title|description)" content="[^"]*">', "", s)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", s, flags=re.S)
    s = re.sub(r'<style id="j7-faq-css">.*?</style>', "", s, flags=re.S)
    s = s.replace("</head>", CSS + "\n" + "".join(lds) + "\n</head>", 1)
    a = s.find("<main"); b = s.find("</main>")
    s = s[:a] + '<main id="main">' + main + s[b:]
    return s

def run():
    cats, items, errs, dups = build_items()
    for d in dups: print("DUP:", d)
    if errs: print("\n".join(errs)); sys.exit(1)
    if len(items) != TARGET: print("COUNT", len(items), "!=", TARGET); sys.exit(2)
    shell = open(os.path.join(HERE, "faq", "shell.html"), encoding="utf-8").read()
    by = {}; [by.setdefault(i["c"], []).append(i) for i in items]
    cc = [(c[0], c[1], len(by[c[0]])) for c, _ in cats]
    meta = {c[0]: c for c, _ in cats}
    json.dump({"v": 1, "n": len(items), "cats": [[s, t] for s, t, _ in cc], "items": items}, open(os.path.join(D, "assets", "faq.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    total = f"{len(items):,}"
    # hub
    top_ids = ["what-is-just-7", "what-are-the-7-ingredients-in-just-7", "how-many-tabs-per-load", "is-just-7-like-earth-breeze", "laundry-sheets-vs-tide-pods", "does-just-7-dissolve-in-cold-water", "is-just-7-vegan", "is-just-7-pet-friendly", "how-much-does-just-7-cost", "what-is-the-7-promise", "when-do-orders-ship", "is-just-7-pva-free"]
    idx = {i["id"]: i for i in items}; top = [idx[t] for t in top_ids]
    cards = "".join(f'<li><a href="/pages/faq/{s}/"><b>{html.escape(t)}</b><span>{n} answers · {html.escape(meta[s][2])}</span></a></li>' for s, t, n in cc)
    hub = (f'<section class="section" style="padding-top:24px"><div class="wrap stack" style="gap:22px">'
           f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span aria-current="page">FAQ</span></nav>'
           f'<div class="stack"><p class="eyebrow">{total} questions, answered</p><h1>Ask us anything.</h1>'
           f'<p class="lead">Every answer about Just 7 Laundry Tabs in one place: the seven ingredients, dosing, stains, pets, vegan, pricing, shipping and how we compare. {PRE}</p></div>'
           + SEARCH.format(id="faq-all", label=f"Search all {total} answers", ph=f"Search {total} answers: cold water, Earth Breeze, cats…") +
           f'<div id="faq-results" class="fres" aria-live="polite" hidden></div>'
           f'<div id="faq-cats" class="stack" style="gap:22px"><h2>Browse by topic</h2><ul class="fcards">{cards}</ul>'
           f'<h2>Most asked</h2><div class="stack" style="gap:8px">{"".join(qa_html(i) for i in top)}</div>'
           f'<div class="cta"><b style="font-family:var(--f-display)">Still stuck?</b><p class="mute" style="font-size:.92rem">Ask Just answers only from these {total} answers and never guesses. Or <a href="/pages/contact/">reach a person</a>.</p><button class="btn sm" type="button" data-ask="">Ask Just</button></div></div>'
           f'</div></section>' + HUBJS)
    hub_title = f"Just 7 FAQ: {total} Answers About Our Laundry Tabs"
    hub_desc = f"{total} answers about Just 7 Laundry Tabs: the 7 ingredients, dosing, cold water, stains, pets, vegan, no film or PVA, pricing, shipping, the 7 Promise and comparisons."
    out = page(shell, hub_title, hub_desc, "/pages/faq/", hub, [faq_ld(top), crumbs([("Home", "/"), ("FAQ", "/pages/faq/")])])
    open(os.path.join(D, "pages", "faq", "index.html"), "w", encoding="utf-8").write(out)
    for s, t, n in cc:
        its = by[s]; desc0 = meta[s][2]
        body = (f'<section class="section" style="padding-top:24px"><div class="wrap stack" style="gap:22px">'
                f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/pages/faq/">FAQ</a> / <span aria-current="page">{html.escape(t)}</span></nav>'
                f'<div class="stack"><p class="eyebrow">{n} answers · Just 7 FAQ</p><h1>{html.escape(t)}</h1><p class="lead">{html.escape(desc0)}</p></div>'
                f'<div class="faqlay2">{nav(cc, s)}<div class="stack" style="gap:12px">'
                + SEARCH.format(id="faq-search", label=f"Filter {t} questions", ph=f"Filter these {n} answers…") +
                f'<section class="faqgrp" id="{s}-q"><h2 class="sr">{html.escape(t)} questions</h2>{"".join(qa_html(i) for i in its)}</section>'
                f'<p id="faq-none" hidden class="lead">Nothing here matches. <a href="/pages/faq/">Search all {total} answers</a> or <button class="btn sm" type="button" data-ask="">Ask Just</button></p>'
                f'<p class="mute">Didn\'t find it? <a href="/pages/faq/">Search all {total} answers</a> or <a href="/pages/contact/">contact us</a>.</p></div></div>'
                f'</div></section>')
        title = f"{t} FAQ: {n} Answers | Just 7 Laundry Tabs"
        desc = f"{n} answers on {t.lower()} for Just 7 Laundry Tabs. {desc0}"[:300]
        path = f"/pages/faq/{s}/"
        os.makedirs(os.path.join(D, "pages", "faq", s), exist_ok=True)
        out = page(shell, title, desc, path, body, [faq_ld(its), crumbs([("Home", "/"), ("FAQ", "/pages/faq/"), (t, path)])])
        out = out.replace("wl-pages-faq", f"wl-pages-faq-{s}").replace("-pages-faq\"", f"-pages-faq-{s}\"")
        open(os.path.join(D, "pages", "faq", s, "index.html"), "w", encoding="utf-8").write(out)
    for s, t, n in cc: print(f"{n:4d}  {s}")
    print(len(items), "items,", len(cc), "categories")

if __name__ == "__main__":
    if "--check" in sys.argv:
        cats, items, errs, dups = build_items()
        print("\n".join(errs)); [print("DUP:", d) for d in dups]
        ns = [(norm(i["q"]), i["q"]) for i in items]
        for k, (a, qa) in enumerate(ns):
            for b2, qb in ns[k+1:]:
                if difflib.SequenceMatcher(None, a, b2).ratio() > 0.9: print("NEAR:", qa, "|", qb)
        from collections import Counter; c = Counter(i["c"] for i in items); print(c); print(len(items))
    else: run()
