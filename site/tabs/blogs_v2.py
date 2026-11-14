"""v2 tabs: convert blog/page copy from sheets to tabs, rename/drop posts, write redirect stubs, relink the whole site.
Idempotent. Run from repo root: python3 site/tabs/blogs_v2.py"""
import os, re, shutil, sys, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DOCS = os.path.join(ROOT, "docs"); sys.path.insert(0, HERE)
from tabify import tabify, tabify_product
from blogmap import RENAME, DROP, OTHER, relink
SITE = "https://just7sheets.com"

LIGHT_PAGES = ("blogs/compare/", "blogs/planet/", "blogs/ingredients/whats-in-laundry-detergent-sheets", "blogs/life/a-quick-history",
               "blogs/how-to/how-often-should-you-wash-your-sheets", "blogs/stains/how-to-get-blood-out-of-sheets-and-clothes",
               "blogs/how-to/how-to-wash-a-down-comforter", "blogs/stains/pet-accidents-on-bedding", "blogs/vegan/", "blogs/home/why-fewer")
FULL_ANYWAY = ("blogs/compare/just-7-faq-everything-people-ask-about-our-tabs", "blogs/compare/laundry-tabs-vs-laundry-sheets",
               "blogs/vegan/why-our-tabs-are-musk-free")
SKIP = ("pages/faq/", "assets/", "index.html", "products/just-7/", "pages/ingredients/", "pages/how-to-use/", "pages/compare/",
        "pages/planet/", "pages/why-just-7/")  # built by faq_build / core.py

POST = [
    (r"\b[Hh]alf a tab\b", "one tab"), (r"\bhalf to one (?:extra )?tabs?\b", "one more tab"), (r"\bAdd half to one\b", "Add one"),
    (r"\b(?:a )?quarter (?:of a )?tab\b", "one tab"), (r"\bhalf or one tab\b", "one tab"), (r"\ba tab or half\b", "one tab"),
    (r"\b[Tt]ear (?:the|a|your) tab in half(?: and|,)? ?", ""), (r"\b[Tt]ear(?:ing)? (?:it|the tab) (?:up )?(?:into|in) (?:half|pieces|strips)(?: and|,)? ?", ""),
    (r"(?:rub |work )?a (?:wet|damp|small) piece of (?:a )?tab", "a tab dissolved in a spoonful of warm water"),
    (r"a small piece of dissolved tab", "a little dissolved tab"), (r"\bwith a small piece of tab\b", "with a little dissolved tab"),
    (r"\bJust sheet\b", "Just formula"), (r"\bthin tab\b", "small tab"), (r"\bflat tab\b", "small tab"),
]

ATTR_RE = re.compile(r'(<(?:meta)\b[^>]*?\b(?:name|property)="(?:description|og:title|og:description|twitter:title|twitter:description)"[^>]*?\bcontent=")([^"]*)(")'
                     r'|(\b(?:alt|aria-label|title)=")([^"]*)(")')

def convert_html(s, fn):
    def conv_text(t):
        if not re.search(r"(?i)sheet|half|tear|piece", t): return t
        u = fn(H.unescape(t)) if "&" in t else fn(t)
        if fn is tabify:
            for p, r in POST: u = re.sub(p, r, u)
        if "&" in t: u = H.escape(u, quote=False).replace("'", "&#x27;")
        return u
    out, pos = [], 0
    # tokenise: tags, style/script blocks, ld+json bodies, text
    tok = re.compile(r"<style\b.*?</style>|<script\b[^>]*ld\+json[^>]*>.*?</script>|<script\b.*?</script>|<!--.*?-->|<[^>]+>", re.S)
    for m in tok.finditer(s):
        out.append(conv_text(s[pos:m.start()])); t = m.group(0)
        if t.startswith("<script") and "ld+json" in t[:80]:
            i = t.index(">") + 1; t = t[:i] + conv_text(t[i:-9]) + "</script>"
        elif t.startswith("<meta") or re.search(r'\b(?:alt|aria-label|title)="', t) and not t.startswith(("<style", "<script")):
            t = ATTR_RE.sub(lambda a: (a.group(1) + conv_text(a.group(2)) + a.group(3)) if a.group(1) else (a.group(4) + conv_text(a.group(5)) + a.group(6)), t)
        out.append(t); pos = m.end()
    out.append(conv_text(s[pos:]))
    return "".join(out)

def stub(new_url):
    full = new_url if new_url.startswith("http") else SITE + new_url
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved | Just 7</title>
<meta name="robots" content="noindex, follow"><link rel="canonical" href="{full}"><meta http-equiv="refresh" content="0; url={new_url}">
<meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="font-family:system-ui,sans-serif;padding:40px;text-align:center"><p>This page moved. <a href="{new_url}">Continue to the new page</a>.</p></body></html>
"""

def run():
    moved = 0
    for o, n in RENAME.items():
        src, dst = os.path.join(DOCS, "blogs", o), os.path.join(DOCS, "blogs", n)
        if os.path.isdir(src) and not os.path.isfile(os.path.join(src, ".stub")):
            if not os.path.exists(dst): shutil.copytree(src, dst)
            shutil.rmtree(src); os.makedirs(src)
            open(os.path.join(src, "index.html"), "w").write(stub(f"/blogs/{n}/")); open(os.path.join(src, ".stub"), "w").write(n)
            moved += 1
    for o, t in list(DROP.items()) + [(k, v) for k, v in OTHER.items()]:
        d = os.path.join(DOCS, "blogs", o) if not o.startswith("pages/") else os.path.join(DOCS, o)
        if not os.path.isfile(os.path.join(d, ".stub")):
            if os.path.isdir(d): shutil.rmtree(d)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "w").write(stub(t)); open(os.path.join(d, ".stub"), "w").write(t)
    changed = 0
    for dp, dn, fns in os.walk(DOCS):
        for f in fns:
            if not f.endswith(".html"): continue
            p = os.path.join(dp, f); rel = os.path.relpath(p, DOCS).replace(os.sep, "/")
            if os.path.isfile(os.path.join(dp, ".stub")): continue
            s0 = open(p, encoding="utf-8").read(); s = relink(s0)
            if rel.startswith(("blogs/", "pages/", "collections/")) and not any(rel.startswith(x) for x in SKIP):
                post = rel.startswith("blogs/") and rel.count("/") == 3
                light = (not post) or any(rel.startswith(x) for x in LIGHT_PAGES) and not any(rel.startswith(x) for x in FULL_ANYWAY)
                s = convert_html(s, tabify_product if light else tabify)
            # self-references of renamed posts
            if s != s0: open(p, "w", encoding="utf-8").write(s); changed += 1
    print("moved", moved, "changed", changed)
    sync_cards()

def h1_of(url):
    p = os.path.join(DOCS, url.strip("/"), "index.html")
    if not os.path.isfile(p): return None
    m = re.search(r"<h1[^>]*>(.*?)</h1>", open(p, encoding="utf-8").read(), re.S)
    return m.group(1).strip() if m else None

def sync_cards():
    """Post cards everywhere show the target post's own H1, so renamed titles follow."""
    cache, n = {}, 0
    card = re.compile(r'(<a class="post" href="(/blogs/[^"]+)"[^>]*>.*?<h3>)(.*?)(</h3>)', re.S)
    for dp, dn, fns in os.walk(DOCS):
        for f in fns:
            if not f.endswith(".html"): continue
            p = os.path.join(dp, f); s0 = open(p, encoding="utf-8").read()
            def rep(m):
                u = m.group(2)
                if u not in cache: cache[u] = h1_of(u)
                return m.group(1) + (cache[u] or m.group(3)) + m.group(4)
            s = card.sub(rep, s0)
            if s != s0: open(p, "w", encoding="utf-8").write(s); n += 1
    print("cards synced in", n, "files")

if __name__ == "__main__":
    run()
