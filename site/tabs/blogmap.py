"""v2 tabs: blog posts renamed to tab slugs, and sheet-only posts dropped (old URLs become noindex redirect stubs)."""
RENAME = {
    "how-to/how-many-laundry-sheets-per-load": "how-to/how-many-laundry-tabs-per-load",
    "how-to/do-laundry-sheets-dissolve-in-cold-water": "how-to/do-laundry-tabs-dissolve-in-cold-water",
    "how-to/can-you-use-laundry-sheets-in-a-high-efficiency-washer": "how-to/can-you-use-laundry-tabs-in-a-high-efficiency-washer",
    "how-to/how-to-use-laundry-detergent-sheets-in-any-washer": "how-to/how-to-use-laundry-detergent-tabs-in-any-washer",
    "how-to/how-to-store-laundry-sheets-so-they-last": "how-to/how-to-store-laundry-tabs-so-they-last",
    "how-to/laundry-sheets-for-travel-and-camping": "how-to/laundry-tabs-for-travel-and-camping",
    "how-to/how-to-hand-wash-clothes-with-a-laundry-sheet": "how-to/how-to-hand-wash-clothes-with-a-laundry-tab",
    "ingredients/why-our-sheets-have-no-dyes": "ingredients/why-our-tabs-have-no-dyes",
    "vegan/why-our-sheets-are-musk-free": "vegan/why-our-tabs-are-musk-free",
    "pets/what-to-do-if-your-pet-chews-a-laundry-sheet-or-pod": "pets/what-to-do-if-your-pet-chews-a-laundry-tab-or-pod",
    "compare/just-7-faq-everything-people-ask-about-our-sheets": "compare/just-7-faq-everything-people-ask-about-our-tabs",
    "compare/laundry-sheets-vs-detergent-tablets": "compare/laundry-tabs-vs-laundry-sheets",
}
DROP = {
    "ingredients/what-is-pullulan-the-film-in-our-sheets": "/pages/ingredients/",
    "ingredients/what-is-pullulan-the-plant-based-film-in-our-sheets": "/pages/ingredients/",
    "ingredients/plant-glycerin-in-laundry-sheets-what-it-does-and-why-the": "/pages/ingredients/",
    "planet/pva-free-laundry-sheets-why-the-film-matters": "/blogs/planet/are-laundry-sheets-plastic/",
    "compare/our-gentle-sheet-vs-just-7-vs-just-9-which-should-you-choose": "/collections/all/",
}
OTHER = {"pages/faq/laundry-sheets": "/pages/faq/laundry-tabs/"}

def url_map():
    m = {f"/blogs/{o}/": f"/blogs/{n}/" for o, n in RENAME.items()}
    m.update({f"/blogs/{o}/": t for o, t in DROP.items()})
    m.update({f"/{o}/": t for o, t in OTHER.items()})
    return m

def relink(s):
    """Point every internal link at the new URL (relative and absolute forms)."""
    for o, n in url_map().items():
        s = s.replace(o, n)
    return s
