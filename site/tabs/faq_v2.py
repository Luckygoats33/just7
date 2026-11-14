"""v2 tabs FAQ rewrite. Reads the sheets-era modules from git master, rewrites them for Just 7 Laundry Tabs and writes
site/faq/c*.py. Re-runnable (always starts from master). Run from repo root: python3 site/tabs/faq_v2.py"""
import os, re, subprocess, sys, types
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from tabify import tabify, tabify_product
from blogmap import relink, url_map
from faq_fixes import FIX, NEW_C17, NEW_C22, ADD, LIGHT, CATS

def master(path):
    return subprocess.run(["git", "show", "master:" + path], cwd=ROOT, capture_output=True, text=True, check=True).stdout

POST = [  # sentence-level tidy-ups after sheet -> tab
    (r"\bUse one tab or one tab\b", "Use one tab"), (r"\bone tab or one\b", "one"), (r"\bone tab, one or two tabs\b", "one or two tabs"),
    (r"half, one or two tabs", "one or two tabs"), (r"one tab to one tab", "one tab"), (r"\bhalf to one tab\b", "one tab"),
    (r"\ba quarter or one tab\b", "one tab"), (r"\bone tab is the dose for a small load\b", "one tab is the dose for a small load"),
    (r"Damp hands soften the film\.", "Water starts the fizz."), (r"Moisture softens the film and makes tabs stick\.", "Moisture starts the fizz and can make tabs crumble or stick."),
    (r"(?:rub |work )?a (?:wet|damp|small wet) piece of tab(?: in(?=,| and))?", "a tab dissolved in a spoonful of warm water"),
    (r"a paste of a damp tab piece", "a tab dissolved in a spoonful of warm water"),
    (r"a small piece of dissolved tab", "a little dissolved tab"), (r"with a small piece of tab", "with a little dissolved tab"),
    (r"a dissolved one tab", "one dissolved tab"), (r"\bhalf to one tab", "one tab"),
    (r"roughly 2 g each", "4 g each"), (r"[Rr]oughly 2 g", "4 g"), (r"5\.5 x 4\.25 in", "about 30 mm (1.2 in) across"),
]

NEW_URLS = set(url_map().values())
def fix_links(a):
    a = relink(a)
    # link text of renamed posts follows the product: [Use sheets in any washer](new-tab-url) -> tabs
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f"[{tabify(m.group(1)) if m.group(2) in NEW_URLS and 'tabs' in m.group(2) or 'tab-' in m.group(2) else m.group(1)}]({m.group(2)})", a)

def esc(s): return s.replace("\\", "\\\\").replace('"', '\\"')

def write(fname, cat, qa):
    lines = [f'CAT = ("{esc(cat[0])}", "{esc(cat[1])}", "{esc(cat[2])}")', 'P = "†"', "QA = ["]
    for q, a in qa: lines.append(f'("{esc(q)}", "{esc(a)}"),')
    lines.append("]")
    open(os.path.join(ROOT, "site", "faq", fname), "w", encoding="utf-8").write("\n".join(lines) + "\n")

def run():
    total = 0
    for fname in sorted(os.listdir(os.path.join(ROOT, "site", "faq"))):
        if not re.match(r"c\d\d_.*\.py$", fname): continue
        key = fname[:3]
        m = types.ModuleType(key); exec(master("site/faq/" + fname), m.__dict__)
        cat = CATS.get(key, m.CAT)
        if key == "c17": qa = list(NEW_C17)
        elif key == "c22": qa = list(NEW_C22); fname_out = fname
        else:
            fn = tabify_product if key in LIGHT else tabify
            qa = []
            for k, (q, a) in enumerate(m.QA):
                fk = f"{key}#{k}"
                if fk in FIX:
                    if FIX[fk] is None: continue
                    q, a = FIX[fk]
                else:
                    q, a = fn(q), fn(a)
                    for p, r in POST: q = re.sub(p, r, q); a = re.sub(p, r, a)
                qa.append((q, a))
        qa += ADD.get(key, [])
        qa = [(q, fix_links(a)) for q, a in qa]
        write(fname, cat, qa); total += len(qa)
    print("FAQ items:", total)
    return total

if __name__ == "__main__":
    run()
