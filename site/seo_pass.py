"""Nov 11 site pass (Will's 20-point SEO list + cart bug + Lighthouse mobile).
Idempotent: run `python3 site/seo_pass.py` from the repo root; it rewrites docs/*.html in place."""
import os, re, json, html, subprocess
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
D = os.path.normpath(D)
SITE = "https://just7sheets.com"
SKIP = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:", "#", "/", "'", "@", "{")

def page_path(f):
    rel = os.path.relpath(f, D).replace(os.sep, "/")
    return "/" + rel

def pretty(path):
    if path.endswith("/index.html"): return path[:-10]
    if path == "index.html": return "/"
    return path

def absolutize(s, fpath):
    """Every relative href/src/poster/srcset -> root-absolute, pretty for pages."""
    base = "http://x" + fpath
    def fix(u):
        if not u or u.startswith(SKIP): 
            if u.startswith("/") and not u.startswith("//"): 
                p = urlparse(u); return pretty(p.path) + (("#" + p.fragment) if p.fragment else "")
            return u
        t = urlparse(urljoin(base, u))
        return pretty(t.path) + (("#" + t.fragment) if t.fragment else "")
    def attr(m):
        return m.group(1) + '"' + fix(m.group(2)) + '"'
    s = re.sub(r'(\s(?:href|src|poster)=)"([^"]*)"', attr, s)
    def sset(m):
        parts = [p.strip() for p in m.group(2).split(",")]
        out = []
        for p in parts:
            bits = p.split()
            if bits: bits[0] = fix(bits[0])
            out.append(" ".join(bits))
        return m.group(1) + '"' + ", ".join(out) + '"'
    s = re.sub(r'(\ssrcset=)"([^"]*)"', sset, s)
    # relative paths inside inline JS strings ("../../assets/x", v.src="../../assets/..")
    s = re.sub(r'(["\'])(?:\.\./)+((?:assets|pages|blogs|products|cart|collections|policies)/[^"\']*)\1', lambda m: m.group(1) + "/" + m.group(2) + m.group(1), s)
    s = re.sub(r'"img": "assets/', '"img": "/assets/', s)
    s = re.sub(r'window\.J7ROOT="[^"]*";window\.J7PRETTY=(?:false|true);', 'window.J7ROOT="/";window.J7PRETTY=true;', s)
    s = re.sub(r'window\.J7ROOT="[^"]*"', 'window.J7ROOT="/"', s)
    s = re.sub(r'window\.J7PRETTY=false', 'window.J7PRETTY=true', s)
    return s

FONT_CSS = ('<link rel="preload" href="/assets/fonts/nunito-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
  '<style id="j7-fonts">@font-face{font-family:"Nunito";font-style:normal;font-weight:500 900;font-display:swap;'
  'src:url(/assets/fonts/nunito-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}'
  '@font-face{font-family:"Nunito Fallback";src:local("Arial");ascent-override:99.71%;descent-override:34.82%;line-gap-override:0%;size-adjust:101.39%}'
  '%PLAYFAIR%</style>')
PLAYFAIR = ('@font-face{font-family:"Playfair Display";font-style:italic;font-weight:600 700;font-display:swap;'
  'src:url(/assets/fonts/playfair-italic-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+2000-206F}')

A11Y_CSS = """<style id="j7-a11y">
.band .eyebrow,.band.sage .eyebrow{color:#fff!important}
.hero-pdp .crumbs,.hero-pdp .crumbs a,.hero-pdp .crumbs span{color:#0E2A3F!important}
.lbl li span{color:#5E6A65!important}
.mline span > a{color:#17557F!important}
.count{background:var(--sky-deep)!important}
.ing2 .pc{color:color-mix(in srgb,var(--c) 65%,#000)!important}
footer .fh{font-size:.95rem;line-height:1.3;margin:0}
a,button,summary{-webkit-tap-highlight-color:rgba(91,42,94,.15)}
.crumbs a{display:inline-block;padding:10px 2px;margin:-10px 0}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
.pbar a{display:inline-block;padding:6px 0}
.pill.ok{color:#22603F!important}
.pill.wait{color:#6E470C!important}
.feat .eyebrow,.band .eyebrow[style]{color:#fff!important}
.filters button small{opacity:1!important;color:inherit!important;font-weight:600}
.build .bar span em{text-shadow:none!important;background:rgba(14,42,63,.55);padding:0 5px;border-radius:5px}
.ph a{color:#17557F!important}
</style>"""

def fonts(s, is_home):
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com"><link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n?', '', s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">\n?', '', s)
    if 'id="j7-fonts"' not in s:
        css = FONT_CSS.replace("%PLAYFAIR%", PLAYFAIR if is_home else "")
        s = s.replace("</head>", css + "\n</head>", 1)
    # metric-matched fallback so the swap doesn't shift text (CLS)
    s = s.replace('"Nunito",ui-rounded', '"Nunito","Nunito Fallback",ui-rounded')
    s = s.replace('"Nunito","Nunito Fallback","Nunito Fallback"', '"Nunito","Nunito Fallback"')
    s = s.replace('font:900 clamp(5rem,18vw,9rem)/1 "Nunito",', 'font:900 clamp(5rem,18vw,9rem)/1 "Nunito","Nunito Fallback",')
    return s

def fix_home_head(s):
    # the homepage closed </head> right after its first <style>, so <title>, description,
    # canonical and icons sat in <body>. Move the head end to just before the skip link.
    m = re.search(r'</head>\n<body>\n(?=<link rel="canonical"|<title>)', s)
    if m:
        s = s[:m.start()] + s[m.end():]
        s = s.replace('\n<a class="sr" href="#main">Skip to content</a>', '\n</head>\n<body>\n<a class="sr" href="#main">Skip to content</a>', 1)
    return s

PLACEHOLDER_RES = [
    (r'<div class="ednote"[^>]*>.*?</div>', ''),
    (r'<span class="?draftpill"?>Draft</span>', ''),
    (r' \[(?:Cite|Needs proof|no medical claims)[^\]<]*\]', ''),
    (r'\[(?:Cite|Needs proof)[^\]<]*\] ?', ''),
    (r'<p>\[Founder story here, in their own words\.\]</p>\n?', ''),
    (r' ?\[Founder story here, in their own words\.\]', ''),
    (r' ?\[Add our price per load\]', ''),
    (r'\[Source: ([^\]<]+)\]', r'(Source: \1)'),
    (r'class="post draft"', 'class="post"'),
]

CLAIM_SUBS = [
    # brand rule: no Pet-safe / Plant-based claims (education about the words themselves stays)
    ("Pet-Safe Laundry Detergent: What to Look For and What to Avoid", "Pet-Friendly Laundry Detergent: What to Look For and What to Avoid"),
    ("Pet-Safe Laundry Detergent: What to Look For", "Pet-Friendly Laundry Detergent: What to Look For"),
    ("Pet-Safe Laundry Detergent", "Pet-Friendly Laundry Detergent"),
    ("Clear pet-safety choices", "Clear pet-friendly choices"),
    ("What Is Pullulan? The Plant-Based Film in Our Sheets", "What Is Pullulan? The Starch-Based Film in Our Sheets"),
    ("What Is Pullulan? The Plant-Based Laundry Sheet Film", "What Is Pullulan? The Starch-Based Laundry Sheet Film"),
    ("PVA or a plant-based film?", "PVA or a starch-based film?"),
    ("PVA or a plant-based film like pullulan?", "PVA or a starch-based film like pullulan?"),
    ("A short-list sheet with a plant-based film.", "A short-list sheet with a pullulan film."),
    ("Why ours is plant-based", "Why ours comes from plants"),
    ("Two plant-based building blocks", "Two plant-derived building blocks"),
    ("Plant-based, with nothing from animals.", "Plant-derived, with nothing from animals."),
    ("Yes (plant-based)", "Yes (plant-derived)"),
    ("Laundry: plant-based sheets,", "Laundry: vegan sheets with a short label,"),
    ("One with only plant-based and mineral ingredients, like Just 7.", "One with only plant-derived and mineral ingredients, like Just 7."),
    ("Every ingredient is plant-based or mineral.", "Every ingredient is plant-derived or mineral."),
    ("Is Just 7 plant-based?", "What is Just 7 made from?"),
    ("Is the glycerin really plant-based?", "Is the glycerin really from plants?"),
    ("A plant-based sheet like Just 7 sidesteps it.", "A pullulan-film sheet like Just 7 sidesteps it."),
    ("Plant-based avoids the PVA question.", "A pullulan film avoids the PVA question."),
    ("with plant-derived ingredients and a plant-based film.", "with plant-derived ingredients and a starch-based pullulan film."),
    ("Sulfates, because plant-based glucosides", "Sulfates, because plant-derived glucosides"),
    ("Pick a plant-based film to skip PVA", "Pick a pullulan or starch film to skip PVA"),
    ("Look for cardboard packaging and a plant-based film.", "Look for cardboard packaging and a pullulan film."),
    ("Are plant-based sheets safe if eaten? No detergent is safe to eat, plant-based or not.", "Are laundry sheets safe if eaten? No detergent is safe to eat."),
    ("Is every ingredient plant-based or synthetic?", "Is every ingredient plant-derived, mineral or synthetic?"),
    ("<td>Pet-safe</td>", "<td>Pet-friendly</td>"),
    ("[contact email, set at launch]", '<a href="mailto:just7sheets@gmail.com">just7sheets@gmail.com</a>'),
]

BLOG_MAP = {
    "earth-breeze-ingredients": "/blogs/compare/earth-breeze-ingredients-vs-just-7/",
    "fragrance-free-vs-unscented": "/blogs/home/fragrance-free-vs-unscented-whats-the-difference/",
    "essential-oils-laundry-detergent-pets": "/blogs/pets/why-we-never-use-essential-oils-not-even-lavender/",
    "are-laundry-sheets-worth-it": "/blogs/compare/cost-per-load-how-to-compare-any-detergent/",
    "tru-earth-vs-earth-breeze": "/blogs/compare/tru-earth-vs-earth-breeze-vs-just-7/",
    "pva-free-laundry-sheets": "/blogs/planet/pva-free-laundry-sheets-why-the-film-matters/",
    "pet-safe-laundry-detergent": "/blogs/pets/pet-safe-laundry-detergent/",
}
def content_fixes(s):
    # draft "→ /blog/slug" pointers become real links
    s = re.sub(r"\(→ /blog/([a-z0-9-]+)\)", lambda m: '(<a href="%s">read it</a>)' % BLOG_MAP[m.group(1)], s)
    s = re.sub(r"<li>([^<]+?) → /blog/([a-z0-9-]+)</li>", lambda m: '<li><a href="%s">%s</a></li>' % (BLOG_MAP[m.group(2)], m.group(1)), s)
    s = re.sub(r'<h2 id="other-options">Other options</h2>\n<p>\[Add a fair one-line summary[^<]*\]</p>\n', '', s)
    s = re.sub(r'<li><a href="#other-options">Other options</a></li>', '', s)
    s = s.replace("<p>[Add each brand&#x27;s price per load from its own site, with read date.]</p>",
        "<p>Just 7 works out to about $0.25 a load with subscribe and save: $15 for 30 sheets, up to 60 loads. Prices change, so check each brand&#x27;s own site and compare per load, not per box (<a href=\"/blogs/compare/cost-per-load-how-to-compare-any-detergent/\">here&#x27;s how</a>).</p>")
    s = s.replace("<strong>Laundry:</strong> plant-based sheets", "<strong>Laundry:</strong> vegan sheets with a short label")
    s = s.replace("Laundry: plant-based sheets", "Laundry: vegan sheets with a short label")
    s = s.replace("Are plant-based sheets safe if eaten?", "Are laundry sheets safe if eaten?").replace("No detergent is safe to eat, plant-based or not.", "No detergent is safe to eat.")
    s = s.replace("because plant-based glucosides", "because plant-derived glucosides")
    s = s.replace("<h3>Pet-safe</h3>", "<h3>Pet-friendly</h3>")
    s = s.replace("nothing from animals. Subscribe and save is coming. 7% of every sale goes to animal sanctuaries.",
                  "nothing from animals. $19, or $15 with subscribe and save. Pre-order now. Orders ship Jan 11th.")
    s = s.replace("<strong>Plant-based,</strong> with nothing from animals.", "<strong>Plant-derived,</strong> with nothing from animals.")
    if 'id="waitlist"' not in s:
        s = s.replace('href="#waitlist"', 'href="/pages/waitlist/"')
    return s

def placeholders(s):
    s = content_fixes(s)
    for pat, rep in PLACEHOLDER_RES:
        s = re.sub(pat, rep, s, flags=re.S)
    for a, b in CLAIM_SUBS:
        s = s.replace(a, b)
        s = s.replace(html.escape(a, quote=False), html.escape(b, quote=False)) if "&" in html.escape(a, quote=False) else s
    return s

def scripts(s):
    # CART BUG: the cart icon's click was swallowed (preventDefault -> drawer) while the
    # capture-phase "Loading" overlay had already gone up, so the page sat on the same URL.
    s = s.replace('$$(".cartbtn").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); openDrawer(); }); });', '')
    s = re.sub(r'\$\$\("\.cartbtn"\)\.forEach\(function\(b\)\{b\.addEventListener\("click",function\(e\)\{e\.preventDefault\(\);openDrawer\(\)\}\)\}\);', '', s)
    # drop the full-screen "7 Loading" overlay (it could stick on any intercepted click)
    s = re.sub(r'<style id="j7-go-css">.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="j7-go-js">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('var o=document.querySelector(".j7-go");if(o)o.classList.remove("on");', '')
    return s

def headings(s):
    s = re.sub(r'<h4>([^<]*)</h4>', r'<h2 class="fh">\1</h2>', s)
    s = s.replace("footer h4", "footer .fh")
    if '<div class="acc">' in s and 'id="pd-h"' not in s:
        s = s.replace('<div class="acc">', '<div class="acc"><h2 class="sr" id="pd-h">Product details</h2>', 1)
    if '<ol class="alist"' in s and 'id="al-h"' not in s:
        s = s.replace('<ol class="alist"', '<h2 class="sr" id="al-h">All articles</h2><ol class="alist"', 1)
    return s

def first_heading_fix(s):
    # first heading after the H1 must not skip a level (Lighthouse heading-order)
    m = re.search(r"</h1>", s)
    if not m: return s
    n = re.compile(r"<h([2-6])[\s>]").search(s, m.end())
    if n and int(n.group(1)) > 2 and 'id="ov-h"' not in s:
        s = s[:n.start()] + '<h2 class="sr" id="ov-h">Overview</h2>' + s[n.start():]
    return s

def cta(s):
    s = s.replace('Orders ship Jan 11th. <a href="/pages/waitlist/"><b>Pre-order now &rarr;</b></a>',
                  '<a href="/pages/waitlist/"><b>Pre-order now.</b></a> Orders ship Jan 11th.')
    s = s.replace('<span>Orders ship Jan 11th.</span><a href="/pages/waitlist/"><b>Pre-order now &rarr;</b></a>',
                  '<a href="/pages/waitlist/"><b>Pre-order now.</b></a><span>Orders ship Jan 11th.</span>')
    return s

def images(s):
    def pic(m):
        n = m.group(1)
        return (f'<source type="image/webp" srcset="/assets/just-7-product-{n}-300.webp 300w, /assets/just-7-product-{n}-600.webp 600w, /assets/just-7-product-{n}.webp 1200w" sizes="(max-width: 700px) 92vw, 560px">')
    s = re.sub(r'<source srcset="/assets/just-7-product-(\d)\.webp" type="image/webp">', pic, s)
    # thumbnails in the product gallery are ~70px
    s = re.sub(r'(<button[^>]*class="pg-t[^"]*"[^>]*>)<picture><source type="image/webp" srcset="/assets/just-7-product-(\d)-300\.webp[^"]*" sizes="[^"]*">',
               lambda m: m.group(1) + f'<picture><source type="image/webp" srcset="/assets/just-7-product-{m.group(2)}-300.webp" sizes="80px">', s)
    s = s.replace('<source srcset="/assets/just-7-pouch.webp" type="image/webp">',
                  '<source type="image/webp" srcset="/assets/just-7-pouch-336.webp 336w, /assets/just-7-pouch.webp 672w" sizes="(max-width: 700px) 80vw, 336px">')
    return s

HERO_JS = ('<script id="j7-hvid-js">(function(){var v=document.querySelector("[data-hvid]");if(!v)return;'
  'function go(){if(navigator.connection&&navigator.connection.saveData)return;v.src="/assets/just7-hero-16x9.mp4";'
  'if(!matchMedia("(prefers-reduced-motion: reduce)").matches){v.autoplay=true;v.play().catch(function(){})}}'
  'if(document.readyState==="complete")setTimeout(go,400);else addEventListener("load",function(){setTimeout(go,400)})})();</script>')
def video(s):
    # 3.2 MB HEVC mobile video (it also showed the old Pet-safe / Plant-based pouch icons)
    # -> one 235 KB H.264 960x540 clip, loaded after the page is done, cropped 4:3 on phones.
    s = s.replace('<video data-hvid muted loop playsinline preload="none" poster="/assets/just7-product-16x9-poster.jpg"',
                  '<video data-hvid muted loop playsinline preload="none" width="960" height="540" poster="/assets/just7-hero-16x9-poster.webp"')
    s = re.sub(r'<script>\(function\(\)\{var v=document\.querySelector\("\[data-hvid\]"\);if\(!v\)return;var tall=.*?</script>', HERO_JS, s, flags=re.S)
    s = s.replace('@media (max-width:899px){.hvid{max-width:340px}.hvid video{aspect-ratio:9/16;max-height:72vh}}', '@media (max-width:899px){.hvid{max-width:420px}.hvid video{aspect-ratio:4/3;max-height:none}}')
    s = s.replace('v.src="/assets/just7-product-16x9.mp4"', 'v.src="/assets/just7-hero-16x9.mp4"')
    s = s.replace('src.srcset="/assets/just-7-product-"+i+".webp"', 'src.srcset="/assets/just-7-product-"+i+"-300.webp 300w, /assets/just-7-product-"+i+"-600.webp 600w, /assets/just-7-product-"+i+".webp 1200w"')
    s = s.replace('v.poster="/assets/just7-product-16x9-poster.jpg"', 'v.poster="/assets/just7-hero-16x9-poster.webp"')
    s = s.replace('<img src="/assets/just7-product-16x9-poster.jpg" alt="" width="1920" height="1080" loading="lazy">', '<img src="/assets/just7-hero-16x9-poster.webp" alt="" width="960" height="540" loading="lazy">')
    return s

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": SITE + "/#org", "name": "Just Seven", "alternateName": "Just 7",
       "url": SITE + "/", "logo": SITE + "/icon-512.png", "email": "just7sheets@gmail.com",
       "slogan": "Seven ingredients. Zero compromise.",
       "description": "Laundry detergent sheets with seven ingredients, every one named. Fragrance-free, nothing from animals. 7% of every sale goes to animal sanctuaries.",
       "sameAs": ["https://www.facebook.com/just7sheets", "https://www.instagram.com/just7sheets/", "https://x.com/just7sheets", "https://www.linkedin.com/company/just7sheets/", "https://www.youtube.com/@just7sheets"]}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "name": "Just 7 Laundry Sheets", "url": SITE + "/", "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US"}

def offer(price, name, extra=None):
    o = {"@type": "Offer", "name": name, "price": f"{price}.00", "priceCurrency": "USD", "availability": "https://schema.org/PreOrder",
         "availabilityStarts": "2027-01-11", "url": SITE + "/products/just-7/", "seller": {"@id": SITE + "/#org"},
         "itemCondition": "https://schema.org/NewCondition"}
    if extra: o.update(extra)
    return o
PRODUCT = {"@context": "https://schema.org", "@type": "Product", "@id": SITE + "/products/just-7/#product",
    "name": "Just 7 Laundry Detergent Sheets", "sku": "JUST7-30", "brand": {"@type": "Brand", "name": "Just Seven"},
    "description": "Fragrance-free laundry detergent sheets with seven ingredients: pullulan film, lauryl glucoside, decyl glucoside, sodium carbonate, plant glycerin, sodium citrate and water. 30 sheets, up to 60 loads. Pre-order now. Orders ship Jan 11th.",
    "category": "Laundry detergent", "image": [SITE + f"/assets/just-7-product-{i}.jpg" for i in range(1, 6)], "url": SITE + "/products/just-7/",
    "offers": [offer(19, "One-time purchase"),
               offer(15, "Subscribe and save", {"priceSpecification": {"@type": "UnitPriceSpecification", "price": "15.00", "priceCurrency": "USD", "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "C62"}}}),
               offer(14, "Subscribe, 3 or more pouches", {"eligibleQuantity": {"@type": "QuantitativeValue", "minValue": 3, "unitCode": "C62"}})]}

def git_date(f):
    try:
        out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%cs", "--", f], cwd=D, capture_output=True, text=True).stdout.split()
        return out[-1] if out else "2026-11-11"
    except Exception:
        return "2026-11-11"

def schema(s, fpath, f):
    url = SITE + pretty(fpath)
    # absolute breadcrumb item URLs
    s = re.sub(r'("item": ")(/[^"]*)"', lambda m: m.group(1) + SITE + m.group(2) + '"', s)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    types = []
    for b in blocks:
        try: types.append(json.loads(b).get("@type"))
        except Exception: pass
    add = []
    if fpath == "/index.html":
        if "Organization" not in types: add += [ORG, WEBSITE]
    if fpath == "/products/just-7/index.html":
        s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "Product".*?</script>', ld(PRODUCT), s, count=1, flags=re.S)
    if "BlogPosting" in types:
        def enrich(m):
            d = json.loads(m.group(1))
            if d.get("@type") != "BlogPosting" or "mainEntityOfPage" in d: return m.group(0)
            d["@type"] = "BlogPosting"
            d["url"] = url; d["mainEntityOfPage"] = {"@type": "WebPage", "@id": url}
            d["datePublished"] = d.get("datePublished") or git_date(f); d["dateModified"] = "2026-11-11"
            d["image"] = SITE + "/assets/just-7-product-1.jpg"
            d["author"] = {"@type": "Organization", "name": "Just Seven", "url": SITE + "/"}
            d["publisher"] = {"@type": "Organization", "name": "Just Seven", "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png"}}
            d["inLanguage"] = "en-US"
            return ld(d)
        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', enrich, s, flags=re.S)
    if "FAQPage" not in types and '<h2 id="faq">FAQ</h2>' in s:
        soup = BeautifulSoup(s.split('<h2 id="faq">FAQ</h2>', 1)[1].split('<div class="cta">', 1)[0], "lxml")
        qs = []
        for p in soup.find_all("p"):
            st = p.find("strong")
            if not st: continue
            q = st.get_text(" ", strip=True); st.extract()
            for sup in p.find_all("sup"): sup.decompose()
            a = re.sub(r"\s+", " ", p.get_text(" ", strip=True)).replace(" .", ".").replace(" ,", ",")
            if q.endswith("?") and a: qs.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        if qs: add.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qs})
    elif "FAQPage" not in types and 'class="qa"' in s and fpath != "/404.html":
        soup = BeautifulSoup(s, "lxml"); qs = []
        for d in soup.select("details.qa"):
            sm = d.find("summary")
            if not sm: continue
            q = sm.get_text(" ", strip=True)
            if not q.endswith("?"): continue
            sm.extract()
            for sup in d.find_all("sup"): sup.decompose()
            a = re.sub(r"\s+", " ", d.get_text(" ", strip=True)).replace(" .", ".").replace(" ,", ",")
            if a: qs.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        if qs: add.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qs})
    if not blocks and fpath != "/404.html":
        name = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        name = re.sub("<[^>]+>", "", name.group(1)).strip() if name else "Just 7"
        add.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": html.unescape(name)}]})
    if add:
        s = s.replace("</head>", "".join(ld(a) for a in add) + "\n</head>", 1)
    return s

GSC_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc-token.txt")
def gsc(s, fpath):
    """Google Search Console HTML-tag verification: paste the content="..." token into
    site/gsc-token.txt and rerun; it lands on the homepage head."""
    if fpath != "/index.html" or not os.path.exists(GSC_FILE): return s
    tok = open(GSC_FILE).read().strip()
    m = re.search(r'content="([^"]+)"', tok); tok = m.group(1) if m else tok
    if not tok: return s
    s = re.sub(r'<meta name="google-site-verification"[^>]*>\n?', '', s)
    return s.replace("<title>", f'<meta name="google-site-verification" content="{tok}">\n<title>', 1)

GA_ID = "G-WMDPS6GT3J"
GA_JS = ('<script id="j7-ga">window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}'
  'gtag("js",new Date());gtag("config","' + GA_ID + '",{allow_google_signals:false,allow_ad_personalization_signals:false});'
  # gtag.js loads 3.5 s after window load at the next idle moment, or on first interaction, whichever is first
  '(function(){var d=0;function l(){if(d)return;d=1;var s=document.createElement("script");s.async=true;'
  's.src="https://www.googletagmanager.com/gtag/js?id=' + GA_ID + '";document.head.appendChild(s)}'
  'function idle(){setTimeout(function(){(window.requestIdleCallback||function(f){setTimeout(f,1)})(l,{timeout:3000})},3500)}'
  'if(document.readyState==="complete")idle();else addEventListener("load",idle);'
  '["pointerdown","keydown","touchstart","scroll"].forEach(function(e){addEventListener(e,l,{once:true,passive:true})});'
  # generate_lead on a valid waitlist / pre-order submit (capture phase, before the form is replaced)
  'document.addEventListener("submit",function(e){var f=e.target;if(!f||!f.matches||!f.matches("[data-waitlist]"))return;'
  'var m=f.querySelector("input[type=email]");if(!m||!m.value||!m.checkValidity())return;'
  'gtag("event","generate_lead",{form_id:f.id||"waitlist",form_location:location.pathname,method:"waitlist_form"});'
  'if(typeof window.j7OnLead==="function")try{window.j7OnLead(m.value,f)}catch(err){}},true)})();</script>')
def ga(s):
    s = re.sub(r'<script id="j7-ga">.*?</script>\n?', '', s, flags=re.S)
    return s.replace("</head>", GA_JS + "\n</head>", 1)

def head_fixes(s, fpath):
    s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '').replace('<meta name="claude:viewport-fit-sides" content="cover">', '')
    url = SITE + pretty(fpath)
    if fpath == "/404.html":
        s = re.sub(r'<link rel="canonical"[^>]*>\n?', '', s)
        if 'name="robots"' not in s:
            s = s.replace("<title>", '<meta name="robots" content="noindex">\n<title>', 1)
    elif 'rel="canonical"' not in s:
        s = s.replace("<title>", f'<link rel="canonical" href="{url}">\n<title>', 1)
    if 'property="og:url"' not in s and fpath != "/404.html":
        s = s.replace('<meta property="og:site_name"', f'<meta property="og:url" content="{url}"><meta property="og:type" content="{"article" if fpath.count("/") >= 4 and fpath.startswith("/blogs/") else "website"}"><meta property="og:site_name"', 1)
    if 'property="og:image"' not in s:
        s = s.replace('<meta name="twitter:card"', f'<meta property="og:image" content="{SITE}/assets/just-7-product-1.jpg"><meta name="twitter:card"', 1)
        if 'property="og:image"' not in s:
            s = s.replace("</head>", f'<meta property="og:image" content="{SITE}/assets/just-7-product-1.jpg"><meta name="twitter:card" content="summary_large_image">\n</head>', 1)
    s = re.sub(r'<style id="j7-a11y">.*?</style>\n?', '', s, flags=re.S)
    s = s.replace("</head>", A11Y_CSS + "\n</head>", 1)
    if fpath == "/index.html":
        s = s.replace("<title>Just 7 Laundry Sheets</title>", "<title>Just 7 Laundry Sheets: Seven Ingredients, Fragrance-Free</title>")
    # body-level duplicate Google font link (already removed in fonts()); keep head tidy
    return s

def run():
    for r, _, fs in os.walk(D):
        for n in fs:
            if not n.endswith(".html"): continue
            f = os.path.join(r, n); fpath = page_path(f)
            s = open(f, encoding="utf-8").read(); o = s
            s = fix_home_head(s)
            s = absolutize(s, fpath)
            s = fonts(s, fpath == "/index.html")
            s = placeholders(s)
            s = scripts(s)
            s = headings(s)
            s = first_heading_fix(s)
            s = cta(s)
            s = images(s)
            s = video(s)
            s = head_fixes(s, fpath)
            s = gsc(s, fpath)
            s = ga(s)
            s = schema(s, fpath, f)
            if s != o: open(f, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    run()
