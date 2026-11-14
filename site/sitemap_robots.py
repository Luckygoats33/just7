"""Writes docs/sitemap.xml, docs/robots.txt and docs/llms.txt from the built pages."""
import os, re, subprocess, html
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs"); D = os.path.normpath(D)
SITE = "https://just7sheets.com"
pages = []
for r, _, fs in os.walk(D):
    for f in fs:
        if not f.endswith(".html") or f == "404.html": continue
        p = os.path.join(r, f); rel = "/" + os.path.relpath(p, D).replace(os.sep, "/")
        s = open(p, encoding="utf-8").read()
        if 'content="noindex' in s: continue
        url = rel[:-10] if rel.endswith("/index.html") else rel
        t = re.search(r"<title>(.*?)</title>", s, re.S); d = re.search(r'<meta name="description" content="([^"]*)"', s)
        lm = subprocess.run(["git", "log", "-1", "--format=%cs", "--", p], cwd=D, capture_output=True, text=True).stdout.strip() or "2026-11-11"
        pages.append((url, html.unescape(t.group(1)) if t else url, html.unescape(d.group(1)) if d else "", lm))
def pri(u):
    if u == "/": return "1.0"
    if u.startswith("/products/"): return "0.9"
    if u.startswith("/pages/") or u.startswith("/collections/"): return "0.7"
    if u.count("/") == 3 and u.startswith("/blogs/"): return "0.6"
    return "0.5"
pages.sort(key=lambda x: (x[0] != "/", not x[0].startswith("/products"), x[0]))
with open(os.path.join(D, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u, _, _, lm in pages:
        f.write(f"  <url><loc>{SITE}{u}</loc><lastmod>{lm}</lastmod><priority>{pri(u)}</priority></url>\n")
    f.write("</urlset>\n")
bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai", "PerplexityBot", "Perplexity-User",
        "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended", "CCBot", "Meta-ExternalAgent", "Amazonbot", "DuckAssistBot", "cohere-ai", "MistralAI-User", "YouBot"]
with open(os.path.join(D, "robots.txt"), "w") as f:
    f.write("# Just 7 welcomes search engines and AI assistants.\n")
    for b in bots: f.write(f"User-agent: {b}\nAllow: /\n\n")
    f.write("User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: https://just7sheets.com/sitemap.xml\n")
def sec(prefix): return [p for p in pages if p[0].startswith(prefix)]
L = ["# Just 7 Laundry Tabs (Just Seven)", "",
     "> Fragrance-free pressed laundry detergent tabs with seven ingredients, every one named: sodium carbonate (washing soda), citric acid, sodium citrate, microcrystalline cellulose, lauryl glucoside, decyl glucoside and water. No film, no PVA, no plastic jug. Nothing from animals. 7% of every sale goes to animal sanctuaries and nonprofits. Pre-order now. Coming soon.", "",
     "Prices: $19 one-time, $15 each with subscribe and save, $14 each on 3 or more. 60 tabs (4 g each), up to 60 loads per pouch: one tab per regular load, two for large. 90-day keep-the-pouch promise.", "",
     "## Shop", ""]
L += [f"- [{t}]({SITE}{u}): {d}" for u, t, d, _ in pages if u in ("/", "/products/just-7/", "/collections/all/", "/cart/")]
L += ["", "## About the product", ""]
L += [f"- [{t}]({SITE}{u}): {d}" for u, t, d, _ in sec("/pages/")]
L += ["", "## Policies", ""] + [f"- [{t}]({SITE}{u}): {d}" for u, t, d, _ in sec("/policies/")]
cats = sorted({u.split("/")[2] for u, *_ in sec("/blogs/")})
for c in cats:
    L += ["", f"## Learn: {c.replace('-', ' ').title()}", ""] + [f"- [{t}]({SITE}{u}): {d}" for u, t, d, _ in sec(f"/blogs/{c}/")]
open(os.path.join(D, "llms.txt"), "w").write("\n".join(L) + "\n")
print(len(pages), "urls")
