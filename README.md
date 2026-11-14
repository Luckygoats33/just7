# Just 7

Website for Just 7 laundry detergent sheets (Just Seven). Seven ingredients, every one named. 7% of every sale goes to animal sanctuaries.

- `docs/` the built site (static HTML, ready for GitHub Pages)
- `site/` build scripts and homepage source (`home-template.html`, `skin.html`, `motion.html`, `prices.py`, `topbar.py`, `footnote.py`, `build_all.py`)
- `product-images/` the 5 product page images (HTML sources and PNGs)

Pre-order now. Coming soon. Prices: $15 subscribe, $14 each on 3+, $19 one-time. 90-day keep-the-pouch promise.

## After any rebuild

`docs/` has post-build passes that the old `site/build_all.py` does not know about. After regenerating pages, run:

```
python3 site/seo_pass.py        # links, fonts, schema, a11y, brand-claim wording (idempotent)
python3 site/sitemap_robots.py  # sitemap.xml, robots.txt (AI crawlers allowed), llms.txt
```

Google Search Console HTML-tag verification: put the `content="..."` token in `site/gsc-token.txt` and rerun `seo_pass.py`.
