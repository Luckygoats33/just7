"""Will (Nov 11): remove the dagger explainer and 'Preview, not on sale yet' lines from the footer."""
import re


def apply(rel, s):
    s = re.sub(r'<p class="fine"[^>]*><sup class="p">.{0,400}?A dagger means.*?</p>', '', s, count=1, flags=re.S)
    s = s.replace('<p class="fine">© 2026 Just Seven. Just 7 is not on sale yet.</p>', '<p class="fine">© 2026 Just Seven.</p>')
    s = s.replace('<p class="fine">&copy; 2026 Just Seven. Just 7 is not on sale yet.</p>', '<p class="fine">&copy; 2026 Just Seven.</p>')
    s = s.replace('<span>Preview. Not on sale yet.</span>', '')
    return s
