"""Approved launch prices (Will, Nov 10): $19 one-time, $15 subscribe (21% off), $14 each on 3+,
free shipping on subscriptions and on 2+ pouches, 90-day keep-the-pouch promise on every order."""

PRICE_HELPERS = ('<script id="j7-prices">window.j7unit=function(l){return l.sub?(l.qty>=3?14:15):19};'
                 'window.j7tot=function(c){return c.reduce(function(t,l){return t+l.qty*window.j7unit(l)},0)};'
                 'window.j7ship=function(c){var subs=c.some(function(l){return l.sub});'
                 'var n=c.reduce(function(t,l){return t+l.qty},0);return subs||n>=2?"Free":"Free on 2+ pouches"};</script>')

SWAPS = [
    # cart line, readable and minified script variants
    ("""(l.sub ? 'Subscribe and save, <span class="ph">[X]% off</span>' : "One-time purchase") + ' · Price set at launch</div>'""",
     """(l.sub ? 'Subscribe and save, $' + window.j7unit(l) + ' each' : "One-time, $19 each") + '</div>'"""),
    ("""(l.sub?'Subscribe and save, <span class="ph">[X]% off</span>':"One-time purchase")+" · Price set at launch</div>\"""",
     """(l.sub?'Subscribe and save, $'+window.j7unit(l)+' each':"One-time, $19 each")+"</div>\""""),
    ("""'<div class="sumrow"><span>Subtotal</span><b>Set at launch</b></div>'""",
     """'<div class="sumrow"><span>Subtotal</span><b>$'+window.j7tot(c).toFixed(2)+'</b></div>'"""),
    ("""'<div class="sumrow"><span>Subscribe and save</span><b><span class="ph">[X]% off</span></b></div>'""",
     """'<div class="sumrow"><span>Subscribe and save</span><b>21% off</b></div>'"""),
    ("""'<div class="sumrow"><span>Shipping</span><b>Set at launch</b></div>'""",
     """'<div class="sumrow"><span>Shipping</span><b>'+window.j7ship(c)+'</b></div>'"""),
    ("This is a preview cart. Nothing is charged or sent. Prices, the subscription discount and shipping are set at launch. ",
     "This is a preview cart. Nothing is charged or sent. "),
    ('qty + (qty === 1 ? " box" : " boxes") + " added"', 'qty + (qty === 1 ? " pouch" : " pouches") + " added"'),
    ('qty+(qty===1?" box":" boxes")+" added"', 'qty+(qty===1?" pouch":" pouches")+" added"'),
    # answers (Ask Just knowledge base, FAQ page, FAQ schema)
    ("We'll share prices when sales open. Waitlist members hear first.",
     "$15 a pouch with subscribe and save ($0.25 a load), $14 each on a 3-pouch subscription, or $19 for one pouch. Same price on every delivery."),
    ("Yes, that's the plan: choose how often a pouch shows up and save on every delivery. We'll share the details when sales open.",
     "Yes. Pick every 4, 8 or 12 weeks and pay $15 a pouch, 21% off, on every delivery, not just the first. Free shipping. Skip or cancel anytime before it ships."),
    ("We'll publish our return and satisfaction policy before we sell a single pouch.",
     "The 7 Promise: 90 days to love it. If you don't, email us and we'll refund the order. Keep the pouch, no return needed. It covers every order, one refund per household."),
    ("Prices and the subscribe and save discount are set at launch.",
     "Just 7 is $15 a pouch on subscribe and save, or $19 one-time."),
    # shop page and old homepage blocks
    ('<p class="price">Price set at launch</p>', '<p class="price">$15 subscribe &middot; $19 one-time</p>'),
    ('<span class="ph">[X]%</span> off every subscription pouch.</b> The discount is set at launch.',
     '21% off every subscription pouch.</b> $15 instead of $19, on every delivery.'),
    ('Every 4, 8 or 12 weeks for now, final options set at launch.', 'Every 4, 8 or 12 weeks.'),
    ('Subscribe and save <span class="ph">[X]% off</span>', 'Subscribe and save 21%: $15'),
    ('<legend>Deliver every <span class="ph">placeholder</span></legend>', '<legend>Deliver every</legend>'),
    ('<div class="save"><b>Price set at launch</b>', '<div class="save"><b>$15</b>'),
]

REFUND = ('<div class="ednote"><b>Draft.</b> Needs a legal read before launch.</div>'
          '<h2 style="font-size:1.6rem">The 7 Promise</h2><p>You have 90 days from delivery to love Just 7. If you don\'t, email us and we\'ll refund that order in full. Keep the pouch. No return needed.</p>'
          '<ul class="pol"><li>Covers every order, one-time or subscription, not just your first.</li><li>One refund per household.</li>'
          '<li>Refunds go back to your original payment method, usually within 5 to 10 business days.</li>'
          '<li>Damaged or wrong order? Send a photo and we\'ll replace it.</li>'
          '<li>Subscriptions: skip, change or cancel anytime before your next pouch ships.</li></ul>')
SHIP = ('<div class="ednote"><b>Draft.</b> Shipping areas and times get confirmed with our fulfillment partner before launch.</div>'
        '<ul class="pol"><li>Free shipping on every subscription order.</li><li>Free shipping on one-time orders of 2 or more pouches.</li>'
        '<li>Pouches ship flat in a mailer, no plastic jug.</li><li>Subscriptions ship every 4, 8 or 12 weeks, your pick.</li>'
        '<li>Lost or damaged pouch? Email us and we\'ll send a new one.</li></ul>')


def apply(rel, s):
    for a, b in SWAPS:
        s = s.replace(a, b)
    if 'id="j7-prices"' not in s and 'window.J7_PRODUCTS' in s:
        s = s.replace('<script>window.J7ROOT', PRICE_HELPERS + '<script>window.J7ROOT', 1)
    if rel in ('policies/refund-policy/index.html', 'policies/shipping-policy/index.html'):
        i = s.find('<div class="ednote"><b>Not written yet.</b>')
        if i > -1:
            j = s.find('</ul>', i) + 5
            s = s[:i] + (REFUND if 'refund' in rel else SHIP) + s[j:]
    return s
