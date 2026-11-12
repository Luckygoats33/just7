"""Higgsfield product video on the homepage hero and the product page gallery.

Homepage: the hero art becomes one muted, looping video. Wide (16:9) on desktop,
vertical (9:16) on phones. The source is picked at load so only one file downloads.
Paused with its poster frame when the visitor prefers reduced motion.

Product page: a video thumbnail goes second in the gallery. Clicking it swaps the
main image for the wide video; clicking any photo thumb swaps back.
"""
import re

ALT = 'A Just 7 pouch rises out of a bowl of water'

HERO_CSS = ('<style id="j7-hvid">'
            '.hvid{position:relative;width:100%;max-width:640px;justify-self:center}'
            '.hvid video{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:22px;'
            'box-shadow:0 30px 60px rgba(15,50,80,.35),0 0 0 4px rgba(255,255,255,.9);background:#9cc9e8}'
            '.hvid .sticker{position:absolute;left:-14px;bottom:-18px}'
            '@media (max-width:899px){.hvid{max-width:340px}.hvid video{aspect-ratio:9/16;max-height:72vh}}'
            '</style>')

HERO = ('<div class="hvid">'
        '<video data-hvid muted loop playsinline preload="none" '
        'poster="assets/just7-product-16x9-poster.jpg" aria-label="' + ALT + '"></video>'
        '<span class="sticker price"><span><b>$0.25</b><small>a load</small></span></span>'
        '</div>'
        '<script>(function(){var v=document.querySelector("[data-hvid]");if(!v)return;'
        'var tall=matchMedia("(max-width:899px)").matches;var k=tall?"9x16":"16x9";'
        'v.poster="assets/just7-product-"+k+"-poster.jpg";v.src="assets/just7-product-"+k+".mp4";'
        'if(!matchMedia("(prefers-reduced-motion: reduce)").matches){v.autoplay=true;v.play().catch(function(){})}'
        '})();</script>')

PDP_CSS = ('<style id="j7-pvid">'
           '.pg-v{position:relative;padding:0;border:2px solid var(--line);border-radius:12px;overflow:hidden;'
           'background:var(--card);cursor:pointer;aspect-ratio:1;transition:border-color .15s,transform .15s}'
           '.pg-v img{width:100%;height:100%;object-fit:cover;display:block}.pg-v:hover{transform:translateY(-2px)}'
           '.pg-v[aria-current=true]{border-color:var(--sky)}'
           '.pg-v .play{position:absolute;inset:0;display:grid;place-items:center}'
           '.pg-v .play span{width:38%;aspect-ratio:1;border-radius:50%;background:rgba(255,255,255,.92);'
           'display:grid;place-items:center;box-shadow:0 4px 12px rgba(0,0,0,.25)}'
           '.pg-main video{width:100%;height:100%;object-fit:cover;display:block}'
           '.pg-main.is-video picture{display:none}'
           '</style>')

PDP_THUMB = ('<button type="button" class="pg-v" aria-label="Play video: ' + ALT + '">'
             '<img src="../../assets/just7-product-16x9-poster.jpg" alt="" width="1920" height="1080" loading="lazy">'
             '<span class="play"><span><svg viewBox="0 0 24 24" width="55%" fill="#1E6FB0" aria-hidden="true">'
             '<path d="M8 5v14l11-7z"/></svg></span></span></button>')

PDP_JS = ('<script>(function(){var b=document.querySelector(".pg-v"),main=document.querySelector(".pg-main");'
          'if(!b||!main)return;var v;'
          'b.addEventListener("click",function(){if(!v){v=document.createElement("video");'
          'v.src="../../assets/just7-product-16x9.mp4";v.poster="../../assets/just7-product-16x9-poster.jpg";'
          'v.muted=true;v.loop=true;v.playsInline=true;v.controls=true;v.setAttribute("aria-label","' + ALT + '");'
          'main.appendChild(v)}main.classList.add("is-video");v.hidden=false;v.play().catch(function(){});'
          'document.querySelectorAll(".pg-t").forEach(function(x){x.removeAttribute("aria-current")});'
          'b.setAttribute("aria-current","true")});'
          'document.querySelectorAll(".pg-t").forEach(function(t){t.addEventListener("click",function(){'
          'main.classList.remove("is-video");b.removeAttribute("aria-current");if(v){v.pause();v.hidden=true}})})'
          '})();</script>')


def apply(rel, s):
    if rel == 'index.html' and 'data-hvid' not in s:
        a = s.index('<div class="stage" aria-hidden="true">')
        z = s.index('</div>', s.index('<span class="sticker loads">', a)) + len('</div>')
        s = s[:a] + HERO + s[z:]
        s = s.replace('</head>', HERO_CSS + '</head>', 1)
    elif rel == 'products/just-7/index.html' and 'class="pg-v"' not in s:
        s = s.replace('grid-template-columns:repeat(5,1fr)', 'grid-template-columns:repeat(6,1fr)', 1)
        i = s.index('<button type="button" class="pg-t" data-pg="2"')
        s = s[:i] + PDP_THUMB + s[i:]
        # after the gallery's own script so its thumb handlers exist first
        j = s.index('</script></div>', i) + len('</script>')
        s = s[:j] + PDP_JS + s[j:]
        s = s.replace('</head>', PDP_CSS + '</head>', 1)
    return s


if __name__ == '__main__':
    import sys, pathlib
    docs = pathlib.Path(sys.argv[1])
    for rel in ('index.html', 'products/just-7/index.html'):
        p = docs / rel
        t = p.read_text(encoding='utf-8')
        n = apply(rel, t)
        if n != t:
            p.write_text(n, encoding='utf-8', newline='')
            print('updated', rel)
        else:
            print('unchanged', rel)
