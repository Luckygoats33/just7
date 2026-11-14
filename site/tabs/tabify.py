"""Sheet -> tab language helpers for the v2 (tabs) site. Text-level only; callers decide where to apply."""
import re

PROTECT = re.compile(r'(https?://[^\s"<>)]+|(?<![\w])/(?:[\w.#-]+/)*[\w.#-]*|just7sheets(?:\.com|@gmail\.com)?|@just7sheets|\[[^\]]*\]\([^)]*\))')
KEEP = [  # non-product "sheet" senses: bedding, dryer sheets, documents
    r"bed ?sheets?", r"fitted sheets?", r"flat sheets?", r"dryer sheets?", r"cheat sheets?", r"sheet sets?", r"data sheets?",
    r"crib sheets?", r"bamboo sheets?", r"color-catcher sheets?", r"spreadsheets?", r"stylesheets?", r"baking sheets?", r"cookie sheets?",
    r"(?:cotton|linen|silk|flannel|sateen|percale|jersey|satin|microfiber|hotel|clean|dirty|fresh|kids'|guest) sheets", r"sheet masks?",
    r"(?:wash|washing|change|changing|strip|stripping|launder|laundering|drying|folding|iron|ironing) (?:your |the |bed |)sheets(?! (?:in|into|per|for each|for a|pouch))", r"lint on sheets", r"planned a (?:laundry )?sheet", r"from sheets to tabs", r"the sheet you showed", r"pre-ordered the sheets", r"Sheets can be torn", r"sheets can be torn", r"tabs and sheets", r"[Tt]abs vs (?:laundry )?sheets", r"than sheets", r"Tabs, sheets", r"[Bb]ig sheets can tangle", r"sheets with clothes", r"wash sheets alone",
    r"(?:your|my|our bed|new|their bed|the bed) sheets(?! (?:in|per))", r"sheets and (?:towels|pillowcases|duvet)", r"(?:towels|pillowcases),? (?:and )?sheets",
    r"sheets, towels", r"how often should you wash your sheets", r"blood out of sheets", r"Sheets? weekly", r"Thursday: sheets", r"the sheets on (?:the|your) bed",
]
KEEP_RE = re.compile(r"\b(?:" + "|".join(KEEP) + r")", re.I)
BRANDS = r"(?:Earth Breeze|Tru Earth|Kind Laundry|Clean People|Sheets Laundry Club|ECOS|Ecos|Arm & Hammer|Arm and Hammer|Tide|Grove|Blueland|HeySunday|Dropps|Biokleen|Seventh Generation|Method|Mrs\. Meyer's|Puracy|Ecoegg|Kind|Smol|Cleancult|Unscented|eco|Eco|big-brand|big brand|other|most|many|some|PVA|PVA-free|competitor|leading|typical|cheap|scented|fresh scent|free and clear)"
BRAND_RE = re.compile(r"\b" + BRANDS + r"(?:'s)?(?: [A-Za-z-]+)?(?: laundry| detergent)? sheets?\b|\blaundry sheet brands?|\bsheet brands?|sheet makers?|sheet companies|sheet market|the sheet category|sheets as a category", re.I)

def _mask(s, rx, store, tag):
    def f(m):
        store.append(m.group(0)); return f"\x00{tag}{len(store)-1}\x00"
    return rx.sub(f, s)

def _unmask(s, store, tag):
    return re.sub(f"\x00{tag}(\\d+)\x00", lambda m: store[int(m.group(1))], s)

def case(src, rep):
    if src.isupper(): return rep.upper()
    if src[:1].isupper(): return rep[:1].upper() + rep[1:]
    return rep

PHRASES = [  # product-specific phrasing first (order matters)
    (r"half a sheet or one", "one tab"), (r"half a sheet", "one tab"), (r"half of a sheet", "one tab"), (r"½ sheet", "1 tab"), (r"a half sheet", "one tab"),
    (r"half sheets?", "one tab"), (r"quarter sheet", "one tab"), (r"tear (?:it|the sheet|a sheet|one|them) in half", "use one tab"),
    (r"tears? cleanly in half", "is one full dose"), (r"torn in half", "one per load"), (r"tear-off", "pre-measured"), (r"tearable", "pre-measured"),
    (r"a dissolved sheet", "a dissolved tab"), (r"dissolved sheet", "dissolved tab"),
    (r"30 sheets", "60 tabs"), (r"thirty sheets", "60 tabs"),
    (r"laundry detergent sheets", "laundry detergent tabs"), (r"laundry detergent sheet", "laundry detergent tab"),
    (r"detergent sheets", "detergent tabs"), (r"detergent sheet", "detergent tab"),
    (r"laundry sheets", "laundry tabs"), (r"laundry sheet", "laundry tab"),
    (r"sheets", "tabs"), (r"sheet", "tab"),
]
PHRASE_RE = [(re.compile(r"\b" + p + r"\b", re.I), r) for p, r in PHRASES]

def tabify(text, keep_brands=True):
    """Full mode: every product 'sheet' becomes 'tab'. Bedding/dryer/cheat sheets and brand-category mentions are kept."""
    st1, st2, st3 = [], [], []
    s = _mask(text, PROTECT, st1, "P")
    s = re.sub(r"\b([Hh]ow many) (?:laundry )?sheets\b", r"\1 tabs", s)
    s = _mask(s, KEEP_RE, st2, "K")
    if keep_brands: s = _mask(s, BRAND_RE, st3, "B")
    for rx, rep in PHRASE_RE:
        s = rx.sub(lambda m: case(m.group(0), rep), s)
    s = _unmask(s, st3, "B"); s = _unmask(s, st2, "K"); s = _unmask(s, st1, "P")
    return s

PRODUCT_CTX = re.compile(r"\b(?:(?:Just 7|our|Our|one|One|two|Two|a|A|the|The|each|Each|every|per|this|that|your|half a|½|1|2|3|30|extra|single|whole|first|dry|damp|dissolved|finished|fragrance-free|seven-ingredient|everyday)\s+(?:laundry\s+|detergent\s+)?)sheets?\b")

def tabify_product(text):
    """Light mode for general articles: only product-context 'sheet' mentions become 'tab'; category talk about laundry sheets stays."""
    st1, st2, st3 = [], [], []
    s = _mask(text, PROTECT, st1, "P"); s = _mask(s, KEEP_RE, st2, "K"); s = _mask(s, BRAND_RE, st3, "B")
    s = re.sub(r"\bJust 7(?:'s)? (laundry |detergent |laundry detergent )?sheets?\b", lambda m: m.group(0).replace("sheets", "tabs").replace("sheet", "tab"), s)
    for p, r in PHRASES[:13]:
        s = re.sub(r"\b" + p + r"\b", lambda m: case(m.group(0), r), s, flags=re.I)
    s = PRODUCT_CTX.sub(lambda m: m.group(0).replace("sheets", "tabs").replace("sheet", "tab"), s)
    s = _unmask(s, st3, "B"); s = _unmask(s, st2, "K"); s = _unmask(s, st1, "P")
    return s
