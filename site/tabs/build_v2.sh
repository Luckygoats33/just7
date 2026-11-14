#!/usr/bin/env bash
# v2 tabs full rebuild, from repo root: bash site/tabs/build_v2.sh
set -euo pipefail
python3 site/tabs/faq_v2.py
python3 site/tabs/blogs_v2.py
python3 site/tabs/posts_v2.py
python3 site/tabs/polish_v2.py
python3 site/creators.py
python3 site/seo_pass.py
python3 site/faq_build.py
python3 site/ask_just.py
python3 site/sitemap_robots.py
