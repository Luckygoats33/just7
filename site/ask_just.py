"""Sitewide Ask Just: empties the old inline window.JUST_KB (so the legacy widget never binds)
and injects <script id="j7-ask"> (site/ask_just.js), which lazy-loads /assets/faq.json on open.
Idempotent. Run after seo_pass.py and faq_build.py."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.normpath(os.path.join(HERE, "..", "docs"))
JS = open(os.path.join(HERE, "ask_just.js"), encoding="utf-8").read().strip()
TAG = '<script id="j7-ask">' + JS + "</script>"
FIXES = [  # legacy on-page copies of the old KB answers
    (' We\'ll only say "pet-safe" once a vet or toxicologist signs off.', ' A vet or toxicologist review is pending on our <a href="/pages/claims/">claims page</a>.'),
    (' We&#x27;ll only say &quot;pet-safe&quot; once a vet or toxicologist signs off.', ' A vet or toxicologist review is pending on our <a href="/pages/claims/">claims page</a>.'),
    (" We'll only say \\\"pet-safe\\\" once a vet or toxicologist signs off.", " A vet or toxicologist review is pending on our claims page."),
    (' We\'ll only say "pet-safe" once a vet or toxicologist signs off', ' A vet or toxicologist review is pending on our claims page'),
]
def kb_empty(s):
    k = "window.JUST_KB="; i = s.find(k)
    if i < 0: return s
    j = i + len(k)
    if s.startswith("[]", j): return s
    _, end = json.JSONDecoder().raw_decode(s, j)
    return s[:j] + "[]" + s[end:]
n = 0
for r, _, fs in os.walk(D):
    for f in fs:
        if not f.endswith(".html"): continue
        p = os.path.join(r, f); s = open(p, encoding="utf-8").read(); o = s
        s = kb_empty(s)
        for a, b in FIXES: s = s.replace(a, b)
        s = re.sub(r'<script id="j7-ask">.*?</script>', "", s, flags=re.S)
        if 'class="ask-fab' in s or "ask-fab" in s:
            i = s.rfind("</body>"); s = s[:i] + TAG + s[i:] if i > -1 else s + TAG
        if s != o: open(p, "w", encoding="utf-8").write(s); n += 1
print(n, "pages updated")
