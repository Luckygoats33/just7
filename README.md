# Just 7

Website for Just 7 Laundry Tabs (Just Seven): pressed laundry detergent tabs, 4 g each, 60 per pouch. Seven ingredients, every one named. No film, no PVA, no plastic jug. 7% of every sale goes to animal sanctuaries.

The domain stays just7sheets.com.

- `docs/` the built site (static HTML, ready for GitHub Pages)
- `site/` build scripts and homepage source (`home-template.html`, `skin.html`, `motion.html`, `prices.py`, `topbar.py`, `footnote.py`, `build_all.py`)
- `product-images/` the 8 product page images (HTML sources and PNGs; tab photos in `product-images/src/tabs/`)
- `site/tabs/` the v2 tabs rewrite (FAQ, blogs, posts, polish passes, image build)

Pre-order now. Coming soon. Prices: $15 subscribe, $14 each on 3+, $19 one-time. 90-day keep-the-pouch promise.

## v2 tabs rebuild

From the repo root:

```
python3 site/img/build_tabs_assets.py   # product images -> docs/assets (only when photos change)
bash site/tabs/build_v2.sh              # FAQ rewrite, blog renames/stubs, copy fixes, then the full post-build chain
```

`site/home-template.html`, `site/index.html`, `site/home-extra.html` and `site/build_all.py` are sheets-era legacy sources and are not used; `docs/` is the source of truth.

## After any rebuild

`docs/` has post-build passes that the old `site/build_all.py` does not know about. After regenerating pages, run:

```
python3 site/seo_pass.py        # links, fonts, schema, a11y, brand-claim wording (idempotent)
python3 site/sitemap_robots.py  # sitemap.xml, robots.txt (AI crawlers allowed), llms.txt
```

Google Search Console HTML-tag verification: put the `content="..."` token in `site/gsc-token.txt` and rerun `seo_pass.py`.
