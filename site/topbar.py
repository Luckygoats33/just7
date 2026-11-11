"""Top bar on every page: sign up for pre-launch updates."""
import re

MSG = 'Just 7 is almost here. <a href="{href}"><b>Sign up for pre-launch updates &rarr;</b></a>'


def inner(rel):
    depth = rel.count('/')
    return MSG.format(href='../' * depth + 'pages/waitlist/index.html')


def apply(rel, s):
    return re.sub(r'(<div class="pbar"><div class="wrap">).*?(</div></div>)',
                  lambda m: m.group(1) + inner(rel) + m.group(2), s, count=1, flags=re.S)
