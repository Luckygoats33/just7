"""Creators program (Nov 11): homepage 'Try it free' section, /pages/creators/ page,
footer link sitewide, and illustrated 'Learn more' tiles on /pages/waitlist/.
Idempotent. Run from repo root BEFORE seo_pass.py and sitemap_robots.py:
  python3 site/creators.py && python3 site/seo_pass.py && python3 site/sitemap_robots.py
"""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, "..", "docs"))
SITE = "https://just7sheets.com"
STAR = "&#9733;" * 5

def home_section(link):
    return f'''<section class="sec reviews" id="try-free"><div class="w">
  <p class="eyebrow">Creators and reviewers</p>
  <h2 class="big-letters" style="margin-top:12px">Try it free. <span class="script">Tell the truth.</span></h2>
  <p style="color:var(--mute);margin-top:14px">We're sending free pouches to creators, reviewers and everyday laundry people before launch. All we ask is an honest review or post. Love it or not, say so.</p>
  <div class="rv-grid">
    <div class="rv"><span class="stars" aria-hidden="true">{STAR}</span><b>Creators of any size</b><p>TikTok, Instagram, YouTube, a blog or a group chat that trusts you. Follower count isn't the point.</p></div>
    <div class="rv"><span class="stars" aria-hidden="true">{STAR}</span><b>Everyday laundry people</b><p>Big families, pet homes, sensitive skin, gym bags. Run a few loads and tell us how it went.</p></div>
    <div class="rv cta"><b>Get a free pouch</b><p>Apply in two minutes. We're picking testers now.</p><a class="btn sun" href="{link}" style="justify-self:start">Apply to try it free</a></div>
  </div>
</div></section>'''

HOME_RE = re.compile(r'<section class="sec reviews" id="(?:reviews|try-free)">.*?</div></section>', re.S)

def homepage():
    for rel, link in (("docs/index.html", "/pages/creators/"), ("site/index.html", "pages/creators/index.html"),
                      ("site/home-template.html", "pages/creators/index.html"), ("site/home-extra.html", "pages/creators/index.html")):
        p = os.path.join(HERE, "..", rel)
        s = open(p, encoding="utf-8").read()
        n = HOME_RE.sub(lambda m: home_section(link), s, count=1)
        if n != s: open(p, "w", encoding="utf-8", newline="").write(n)

# ---------- footer link ----------
FOOT_OLD = '<a href="/pages/business/">For business</a>'
FOOT_NEW = FOOT_OLD + '<a href="/pages/creators/">Creators: try it free</a>'
def footer(s):
    if 'href="/pages/creators/">Creators: try it free</a>' in s: return s
    return s.replace(FOOT_OLD, FOOT_NEW)
def footer_src(s):
    old = '<a href="pages/business/index.html">For business</a>'
    if 'Creators: try it free' in s or old not in s: return s
    return s.replace(old, old + '<a href="pages/creators/index.html">Creators: try it free</a>')

# ---------- waitlist tiles ----------
SV = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
IC_ING = f'<svg {SV}><path d="M9 3h6"/><path d="M10 3v5.5L5.3 17a2.5 2.5 0 0 0 2.2 3.7h9a2.5 2.5 0 0 0 2.2-3.7L14 8.5V3"/><path d="M7.5 14h9"/></svg>'
IC_LEARN = f'<svg {SV}><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/><path d="M9 8h7M9 11.5h5"/></svg>'
IC_PAW = f'<svg {SV}><circle cx="7" cy="9" r="1.8"/><circle cx="11" cy="5.5" r="1.8"/><circle cx="15.5" cy="6" r="1.8"/><circle cx="18.5" cy="10" r="1.8"/><path d="M8.5 16.5c0-2.6 2-4.8 4.3-4.8s4.2 2.2 4.2 4.8c0 2-1.5 3-3 2.5-.8-.3-1.5-.3-2.3 0-1.6.5-3.2-.5-3.2-2.5z"/></svg>'
TILE_CSS = ('<style id="j7-tiles">.tile.art{align-content:start;gap:12px}'
            '.tile .tart{position:relative;display:block;margin:-6px -6px 4px}'
            '.tile .tart img{display:block;width:100%;height:auto;aspect-ratio:8/5;object-fit:cover;border-radius:18px;'
            'background:rgba(255,255,255,.15);box-shadow:0 6px 18px rgba(0,0,0,.18);transform:rotate(-1.2deg);transition:transform .25s}'
            '.tile:hover .tart img{transform:rotate(0)}'
            '.tile .tic{position:absolute;left:14px;bottom:-30px;width:48px;height:48px;border-radius:14px;display:grid;place-items:center;'
            'background:var(--sun,#FFC94A);color:#2A2205;box-shadow:0 4px 0 rgba(0,0,0,.18)}'
            '.tile .tic svg{width:26px;height:26px}.tile.art h3{margin-top:24px}</style>')
def tile(href, bg, img, alt, icon, h, p):
    return (f'<a class="tile art" href="{href}" style="background:{bg}"><span class="tart">'
            f'<img src="/assets/{img}" width="560" height="350" alt="{alt}" loading="lazy" decoding="async">'
            f'<span class="tic">{icon}</span></span><h3>{h}</h3><p>{p}</p></a>')
TILES = ('<div class="tiles">'
         + tile("/pages/ingredients/", "#1F6FA8", "tile-ingredients.webp", "The Just 7 label listing all seven ingredients", IC_ING, "Meet all 7", "Every ingredient, explained.")
         + tile("/pages/learn/", "#3F7A4C", "tile-learn.webp", "How to dose: half, one or two sheets", IC_LEARN, "Learn", "144 articles on labels, pets and stains.")
         + tile("/pages/about/#mission", "#5B2A5E", "tile-mission.webp", "7% of every sale goes to animal sanctuaries", IC_PAW, "Our mission", "7% of every sale to the animals.")
         + '</div>')
TILES_RE = re.compile(r'<div class="tiles"><a class="tile[^"]*" href="/pages/ingredients/".*?</a></div>', re.S)
def waitlist_tiles():
    p = os.path.join(D, "pages", "waitlist", "index.html")
    s = open(p, encoding="utf-8").read(); o = s
    s = TILES_RE.sub(lambda m: TILES, s, count=1)
    s = re.sub(r'<style id="j7-tiles">.*?</style>', '', s, flags=re.S)
    s = s.replace("</head>", TILE_CSS + "\n</head>", 1)
    if s != o: open(p, "w", encoding="utf-8").write(s)

# ---------- /pages/creators/ ----------
TITLE = "Try Just 7 Free: Creator and Reviewer Program"
DESC = "Creators, reviewers and everyday laundry people: apply for a free pouch of Just 7 laundry sheets before launch. All we ask is an honest review or post."
URL = SITE + "/pages/creators/"
PLATFORMS = ["TikTok", "Instagram", "YouTube", "Facebook", "Pinterest", "Bluesky", "X", "Blog", "Other"]
FOLLOWERS = ["Under 1,000", "1,000 to 10,000", "10,000 to 50,000", "50,000 to 250,000", "250,000+", "I don't post, I just do laundry"]
NICHES = ["Laundry and cleaning", "Home and organizing", "Pets", "Eco and low-waste", "Parenting and family", "Vegan living", "Sensitive skin", "Reviews and unboxing", "Other"]
def opts(xs, ph):
    return f'<option value="">{ph}</option>' + "".join(f"<option>{x}</option>" for x in xs)
FAQ = [
    ("Do I need a big following?", "No. Small creators, reviewers and people who just do a lot of laundry are all welcome. An honest take from a real home is what we're after."),
    ("Is this paid?", "No. You get a free pouch to keep. There's no payment and no affiliate commission in this program."),
    ("When will my pouch arrive?", "Pouches go out as our first batch is ready, around when orders ship Jan 11th. We'll email you before yours ships."),
    ("Do I have to post a good review?", "No. We want your honest opinion, good or bad. We'd rather hear it now than after launch."),
    ("How do I disclose it?", "Say you got it free. Use #gifted or #ad, or say so in the post or video itself. The FTC asks for this, and it's simply fair to your audience."),
    ("Will you share my details?", "No. We use your application to pick testers and send your pouch. Questions? Visit just7sheets.com/contact."),
]
def faq_html():
    return "".join(f'<details class="qa"><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in FAQ)

MAIN = f'''<main id="main">
<section class="section" style="padding-top:24px"><div class="wrap stack" style="gap:18px">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span aria-current="page">Creators</span></nav>
<p class="eyebrow">Creators and reviewers</p><h1>Try it free. Tell the truth.</h1>
<p class="lead">We're sending free pouches of Just 7 to creators, reviewers and everyday laundry people before launch. All we ask is that you try it for a few loads and share an honest review or post.</p>
<p><a class="btn" href="#apply">Apply for a free pouch</a></p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="grid">
<div class="card"><h2 style="font-size:1.35rem">Who it's for</h2><p>Creators of any size: pets, home, eco, cleaning, parenting and laundry niches. Reviewers and unboxers. And everyday folks who just do a lot of laundry.</p></div>
<div class="card"><h2 style="font-size:1.35rem">What you get</h2><p>A free pouch of Just 7: 30 sheets, up to 60 loads. Pouches go out as our first batch is ready, around when orders ship Jan 11th. It's yours to keep.</p></div>
<div class="card"><h2 style="font-size:1.35rem">What we ask</h2><p>Try it for a few loads. Share an honest review or post and tag <b>@just7sheets</b>. Please say you got it free, with #gifted or #ad.</p></div>
</div></div></section>
<section class="section" id="apply" style="padding-top:0;scroll-margin-top:96px"><div class="wrap" style="display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));align-items:start">
<div class="stack"><h2>Apply in two minutes.</h2><p class="mute">Tell us a bit about you and where you share. We read every application and pick testers in batches.</p>
<p class="fine">This program doesn't include payment or affiliate commission. Under FTC rules, please disclose that you got the product free, for example with #gifted or #ad.</p>
<h2 style="margin-top:12px">Good questions.</h2>
<div class="stack" style="gap:10px">{faq_html()}</div></div>
<form class="formcard" id="creators" data-waitlist data-creators style="scroll-margin-top:110px">
<div class="field"><label for="cr-name">Name</label><input id="cr-name" name="name" type="text" required autocomplete="name"></div>
<div class="field"><label for="cr-email">Email</label><input id="cr-email" name="email" type="email" required autocomplete="email" placeholder="you@example.com"></div>
<div class="field"><label for="cr-platform">Main platform</label><select id="cr-platform" name="platform" required>{opts(PLATFORMS, "Choose one")}</select></div>
<div class="field"><label for="cr-handle">Handle or URL</label><input id="cr-handle" name="handle" type="text" required autocomplete="off" placeholder="@yourname or a link" maxlength="200"></div>
<div class="field"><label for="cr-followers">Followers</label><select id="cr-followers" name="followers" required>{opts(FOLLOWERS, "Choose a range")}</select></div>
<div class="field"><label for="cr-niche">Niche</label><select id="cr-niche" name="niche" required>{opts(NICHES, "Choose one")}</select></div>
<div class="field"><label for="cr-why">Why do you want to try Just 7?</label><textarea id="cr-why" name="why" required maxlength="600" rows="4"></textarea></div>
<label class="ck" style="display:flex;gap:10px;align-items:flex-start;font-size:.95rem"><input type="checkbox" name="consent" required style="width:22px;height:22px;min-height:0;flex:none;margin-top:2px;accent-color:var(--sky-ink)"><span>I'll share an honest review or post and disclose that I got it free. Just 7 can email me about this program.</span></label>
<p class="fine j7-consent">By applying, you agree to get emails from Just 7. Unsubscribe anytime. <a href="/policies/privacy-policy/">Privacy policy</a>.</p>
<button class="btn" type="submit">Send my application</button>
<p class="fine">We'll email you at the address you enter. No spam, no sharing your address.</p>
</form>
<script id="j7-creators">(function(){{var f=document.getElementById("creators");if(!f)return;f.__j7lead=1;
f.addEventListener("submit",function(e){{e.preventDefault();if(!f.checkValidity()){{f.reportValidity&&f.reportValidity();return}}
var email=f.querySelector("input[type=email]");var btn=f.querySelector("[type=submit]");
if(btn){{btn.disabled=true;btn.setAttribute("aria-busy","true")}}
var prev=f.querySelector(".j7-lead-err");if(prev)prev.textContent="";
var go=(typeof window.j7OnLead==="function")?window.j7OnLead(email&&email.value,f):Promise.reject();
Promise.resolve(go).then(function(){{var box=document.createElement("div");box.className="done";box.setAttribute("role","status");box.setAttribute("tabindex","-1");
box.innerHTML='<div class="big">Thanks. We got it.</div><p>We\\'ll email you when we pick the next batch of testers.</p>';
f.innerHTML="";f.appendChild(box);box.focus({{preventScroll:true}});f.scrollIntoView({{block:"start"}})}}).catch(function(){{
if(btn){{btn.disabled=false;btn.removeAttribute("aria-busy")}}
var err=f.querySelector(".j7-lead-err");
if(!err){{err=document.createElement("p");err.className="fine j7-lead-err";err.setAttribute("role","alert");err.style.color="#8B2E2E";if(btn&&btn.parentNode)btn.parentNode.insertBefore(err,btn.nextSibling);else f.appendChild(err)}}
err.textContent="We couldn't send your application just now. Please try again in a moment.";}})}})}})();</script>
</div></section>
</main>'''

def creators_page():
    src = open(os.path.join(D, "pages", "contact", "index.html"), encoding="utf-8").read()
    head, rest = src.split("<main id=\"main\">", 1)
    tail = rest.split("</main>", 1)[1]
    head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, count=1)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{URL}">', head, count=1)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{URL}">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{TITLE}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', head)
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Creators", "item": URL}]}
    head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>',
                  lambda m: '<script type="application/ld+json">' + json.dumps(bc) + "</script>", head, count=1, flags=re.S)
    # drop any FAQPage/other JSON-LD inherited from contact (seo_pass regenerates FAQPage from details.qa)
    head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>', '', head, flags=re.S)
    tail = tail.replace("wl-pages-contact", "wl-pages-creators")
    out = head + MAIN + tail
    os.makedirs(os.path.join(D, "pages", "creators"), exist_ok=True)
    open(os.path.join(D, "pages", "creators", "index.html"), "w", encoding="utf-8").write(out)

def run():
    homepage()
    creators_page()
    waitlist_tiles()
    for r, _, fs in os.walk(D):
        for n in fs:
            if n.endswith(".html"):
                p = os.path.join(r, n); s = open(p, encoding="utf-8").read(); t = footer(s)
                if t != s: open(p, "w", encoding="utf-8").write(t)
    for rel in ("index.html", "home-template.html", "home-extra.html"):
        p = os.path.join(HERE, rel); s = open(p, encoding="utf-8").read(); t = footer_src(s)
        if t != s: open(p, "w", encoding="utf-8", newline="").write(t)

if __name__ == "__main__":
    run()
