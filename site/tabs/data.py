"""Just 7 Laundry Tabs: single source of truth for the v2 site copy (Formula A, working formula)."""
PRE = "Pre-order now. Coming soon."
NAME = "Just 7 Laundry Tabs"
DAG = '<sup class="p"><a href="/pages/claims/" title="Pending proof: see our claims page" aria-label="Pending proof: see our claims page">†</a></sup>'

# label order: most to least by weight. pct = share of a 4 g tab (glucosides counted as active)
ING = [
    dict(id="sodium-carbonate", name="Washing soda", inci="Sodium carbonate", pct="45%", p=45, c="#1F6FA8", quip="The grease lifter", pill="Mineral",
         does="Lifts grease and softens water, so everyday grime lets go. It's also the solid base of the tab.",
         src="A mineral, made from salt and limestone or mined from trona ore.",
         why="A cleaner your great-grandparents used, still earning its spot.",
         short="Lifts grease and softens water.", icon="soda"),
    dict(id="citric-acid", name="Citric acid", inci="Citric acid", pct="18%", p=18, c="#D9A21B", quip="The fizz", pill="Fermentation",
         does="Meets the washing soda in water and makes a light fizz that helps break the tab apart. It helps with hard water too.",
         src="Made by fermenting sugar.",
         why="It gets the tab apart without a film or a wrapper, and it's the same citric acid used in food.",
         short="A light fizz that breaks the tab apart.", icon="fizz"),
    dict(id="sodium-citrate", name="Sodium citrate", inci="Sodium citrate", pct="10%", p=10, c="#8CC4EA", quip="The water softener", pill="Fermentation",
         does="Ties up the minerals in hard water so the cleaners can do their job, and keeps the pH steady.",
         src="Citric acid from fermented sugar, paired with sodium.",
         why="Food-grade, simple, and a classic swap for the phosphates detergents used to use.",
         short="Ties up hard-water minerals.", icon="citrus"),
    dict(id="cellulose", name="Microcrystalline cellulose", inci="Microcrystalline cellulose", pct="10%", p=10, c="#9E6AA1", quip="The binder", pill="Binder",
         does="Holds the powder together when it's pressed into a tab, then swells in water to pop the tab apart.",
         src="Purified cellulose, the same kind of binder used in many pressed vitamin tablets. We'll share the supplier spec when it's confirmed.",
         why="It's what lets us press a tab with no film, no wrapper and no PVA.",
         short="Holds the tab together, then pops it apart.", icon="tab"),
    dict(id="lauryl-glucoside", name="Lauryl glucoside", inci="Lauryl glucoside", pct="7.5%", p=7.5, c="#5E9C6B", quip="The main cleaner", pill="Sugar-based",
         does="Our main cleaner. It goes after body oils and grease, with a little lather.",
         src="It's a sugar-based cleaner. We'll share the supplier source when it's confirmed.",
         why="Same gentle sugar-based family as decyl glucoside, with a bit more muscle. No sulfates.",
         short="The main cleaner, for oils and grease.", icon="grease"),
    dict(id="decyl-glucoside", name="Decyl glucoside", inci="Decyl glucoside", pct="7.5%", p=7.5, c="#7DB88A", quip="The cold-water cleaner", pill="Sugar-based",
         does="A mild cleaner picked for cold washes. It grabs oil and dirt and lets the water carry them away.",
         src="It's a sugar-based cleaner. We'll share the supplier source when it's confirmed.",
         why="Known as one of the milder cleaners used in personal care, and it isn't ethoxylated.",
         short="The cold-water cleaner.", icon="gentle"),
    dict(id="water", name="Water", inci="Water", pct="about 2%", p=2, c="#C9D3D9", quip="Left over", pill="Water",
         does="Comes in with the two liquid cleaners. Only about 2% is left in the finished tab.",
         src="Purified water.",
         why="It's in the recipe, so it's on the list. We count everything.",
         short="Left over from the cleaners.", icon="water"),
]
ING_LIST_TXT = "sodium carbonate (washing soda), citric acid, sodium citrate, microcrystalline cellulose, lauryl glucoside, decyl glucoside and water"
PCT_NOTE = "Share of a 4 g tab in our working formula, with the two cleaners counted as active ingredient. We'll match it to the final manufacturer documents before launch."

ICON64 = {  # stroke icons, viewBox 0 0 64 64
    "soda": '<path d="M14 50h36"/><path d="M20 50l4-26h16l4 26"/><path d="M27 24v-8h10v8"/><path d="M26 36h12"/>',
    "fizz": '<circle cx="24" cy="42" r="8"/><circle cx="40" cy="28" r="6"/><circle cx="44" cy="46" r="4"/><circle cx="26" cy="20" r="3"/>',
    "citrus": '<circle cx="32" cy="34" r="16"/><path d="M32 18v32M16 34h32M21 23l22 22M43 23L21 45"/>',
    "tab": '<ellipse cx="32" cy="26" rx="20" ry="8"/><path d="M12 26v10c0 4.4 9 8 20 8s20-3.6 20-8V26"/><path d="M20 52l-4 4M44 52l4 4M32 50v6"/>',
    "grease": '<path d="M32 10c8 12 14 19 14 27a14 14 0 0 1-28 0c0-8 6-15 14-27z"/><path d="M26 40a7 7 0 0 0 7 6"/>',
    "gentle": '<path d="M32 12l4 12 12 4-12 4-4 12-4-12-12-4 12-4z"/><circle cx="48" cy="46" r="3"/><circle cx="16" cy="48" r="2"/>',
    "water": '<path d="M32 10c10 14 16 22 16 30a16 16 0 0 1-32 0c0-8 6-16 16-30z"/><path d="M22 44h20"/>',
}
def svg64(k): return f'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON64[k]}</svg>'

SCENE100 = {  # animated scene art on the ingredients page, viewBox 0 0 100 100
    "soda": '<path class="s s-pulse" d="M30 34l10 12-10 12-10-12z" fill="currentColor"/><path class="s s-pulse d2" d="M60 26l13 16-13 16-13-16z" fill="currentColor" opacity=".8"/><path class="s s-pulse d3" d="M52 58l9 11-9 11-9-11z" fill="currentColor" opacity=".6"/>',
    "fizz": '<ellipse cx="50" cy="76" rx="20" ry="6" fill="currentColor" opacity=".85"/><circle class="s s-rise" cx="34" cy="60" r="6" fill="none" stroke="currentColor" stroke-width="3"/><circle class="s s-rise d2" cx="62" cy="56" r="5" fill="none" stroke="currentColor" stroke-width="3"/><circle class="s s-rise d3" cx="48" cy="44" r="8" fill="none" stroke="currentColor" stroke-width="3"/><circle class="s s-rise" cx="66" cy="34" r="3" fill="none" stroke="currentColor" stroke-width="3"/>',
    "citrus": '<path d="M50 18s20 22 20 36a20 20 0 0 1-40 0c0-14 20-36 20-36z" fill="currentColor" opacity=".35"/><circle class="s s-fade" cx="42" cy="56" r="4" fill="#4F6575"/><circle class="s s-fade d2" cx="56" cy="62" r="4" fill="#4F6575"/><circle class="s s-fade d3" cx="50" cy="46" r="4" fill="#4F6575"/>',
    "tab": '<g class="s s-pulse"><path d="M24 46v12c0 5.5 11.6 10 26 10s26-4.5 26-10V46z" fill="currentColor" opacity=".7"/><ellipse cx="50" cy="46" rx="26" ry="10" fill="currentColor"/></g>',
    "grease": '<ellipse class="s s-lift" cx="50" cy="66" rx="16" ry="9" fill="#2B2F2E" opacity=".75"/><circle class="s s-rise" cx="30" cy="60" r="7" fill="none" stroke="currentColor" stroke-width="3"/><circle class="s s-rise d2" cx="70" cy="58" r="5" fill="none" stroke="currentColor" stroke-width="3"/><circle class="s s-rise d3" cx="52" cy="50" r="9" fill="none" stroke="currentColor" stroke-width="3"/><path d="M14 80h72" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>',
    "gentle": '<circle class="s s-lift" cx="48" cy="68" r="6" fill="#8B6B4A"/><circle class="s s-rise" cx="28" cy="62" r="8" fill="none" stroke="currentColor" stroke-width="3"/><circle class="s s-rise d2" cx="66" cy="64" r="6" fill="none" stroke="currentColor" stroke-width="3"/><circle class="s s-rise d3" cx="46" cy="56" r="5" fill="none" stroke="currentColor" stroke-width="3"/><path d="M14 80h72" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>',
    "water": '<path class="s s-evap" d="M50 26s16 18 16 30a16 16 0 0 1-32 0c0-12 16-30 16-30z" fill="currentColor"/><path d="M28 82h44" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".5"/>',
}

# product image gallery (alt text is the single source for page markup and the gallery script)
GALLERY = [
    (1, "Pouch", "Just 7 Laundry Tabs pouch with white pressed tabs: 60 tabs, up to 60 loads, fragrance-free, no film"),
    (8, "The tab", "Close-up of plain white pressed Just 7 tabs, about 30 mm across"),
    (6, "Fizz", "A Just 7 tab fizzing apart in a glass of cold water"),
    (2, "Ingredients", "The seven Just 7 ingredients, what each one does and how much is in a tab"),
    (7, "Flat lay", "The seven Just 7 ingredients in small dishes, with three pressed tabs"),
    (3, "How to use", "How to use: one tab for a regular load, two for a big or extra-dirty load"),
    (4, "Size and value", "One flat pouch next to a plastic jug: 60 tabs, up to 60 loads, $0.25 a load"),
    (5, "Giveback", "7% of every sale goes to animal sanctuaries"),
]
