"""Top bar on every page: Pre-order now. Orders ship Jan 11th."""
import re

MSG = 'Orders ship Jan 11th. <a href="{href}"><b>Pre-order now &rarr;</b></a>'


def inner(rel):
    depth = rel.count('/')
    return MSG.format(href='../' * depth + 'pages/waitlist/index.html')


def apply(rel, s):
    return re.sub(r'(<div class="pbar"><div class="wrap">).*?(</div></div>)',
                  lambda m: m.group(1) + inner(rel) + m.group(2), s, count=1, flags=re.S)
