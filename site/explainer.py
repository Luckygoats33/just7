"""'The seven, in a minute.' on the Ingredients page: replaces the empty video slot with a
one-minute animated explainer (intro, seven ingredients, outro). Plays when scrolled into view."""

ICONS = {
    'film': '<rect x="10" y="14" width="44" height="34" rx="6"/><path d="M18 24h28M18 32h28M18 40h18"/>',
    'grease': '<path d="M32 10c8 12 14 19 14 27a14 14 0 0 1-28 0c0-8 6-15 14-27z"/><path d="M26 40a7 7 0 0 0 7 6"/>',
    'gentle': '<path d="M32 12l4 12 12 4-12 4-4 12-4-12-12-4 12-4z"/><circle cx="48" cy="46" r="3"/><circle cx="16" cy="48" r="2"/>',
    'soda': '<path d="M14 50h36"/><path d="M20 50l4-26h16l4 26"/><path d="M27 24v-8h10v8"/><path d="M26 36h12"/>',
    'flex': '<path d="M12 44c10-24 30-24 40 0"/><path d="M12 44c10-10 30-10 40 0"/><circle cx="32" cy="22" r="3"/>',
    'citrus': '<circle cx="32" cy="34" r="16"/><path d="M32 18v32M16 34h32M21 23l22 22M43 23L21 45"/>',
    'water': '<path d="M32 10c10 14 16 22 16 30a16 16 0 0 1-32 0c0-8 6-16 16-30z"/><path d="M22 44h20"/>',
}
SCENES = [
    ('film', 'Pullulan film', 'The sheet itself', 'A film made from fermented starch holds everything together, then dissolves in the wash. No PVA.', 35, '#3A9BDC', '#1F6FA8'),
    ('grease', 'Lauryl glucoside', 'The grease lifter', 'A sugar-based cleaner that pulls body oils and grease out of fabric.', 17, '#5FB389', '#2F7D57'),
    ('gentle', 'Decyl glucoside', 'The gentle cleaner', 'Our main everyday cleaner. Mild, sugar-based, no sulfates.', 17, '#2F7D57', '#1E5A3D'),
    ('soda', 'Washing soda', 'The grime loosener', 'Softens the water and raises the pH so everyday dirt lets go.', 10, '#5B2A5E', '#3E1C40'),
    ('flex', 'Plant glycerin', 'The flex', 'Keeps the sheet soft and bendy in the pouch. Nothing from animals.', 10, '#9E6AA1', '#6E4571'),
    ('citrus', 'Sodium citrate', 'The water softener', 'Grabs the minerals in hard water so the cleaners can work.', 7, '#D9A21B', '#9A720F'),
    ('water', 'Water', 'The carrier', 'Carries it all while the sheet is made. Most of it dries off.', 4, '#6D9FC4', '#3F6E93'),
]
SECS = 6.5


def build():
    slides = ['<div class="xv-s xv-intro" style="--a:#5B2A5E;--b:#3E1C40"><div class="xv-big">7</div><div><p class="xv-k">The whole label</p><h3>Seven ingredients.<br>One minute.</h3><p>What each one does, in the order it sits in the sheet.</p></div></div>']
    for i, (ic, name, role, job, pc, a, b) in enumerate(SCENES):
        slides.append(
            f'<div class="xv-s" style="--a:{a};--b:{b};--p:{pc}">'
            f'<div class="xv-ring"><svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[ic]}</svg></div>'
            f'<div class="xv-t"><p class="xv-k">No. {i+1} &middot; {role}</p><h3>{name}</h3><p>{job}</p><b class="xv-pc"><span data-pc="{pc}">{pc}</span>% of a sheet</b></div>'
            f'<div class="xv-num" aria-hidden="true">{i+1}</div></div>')
    slides.append('<div class="xv-s xv-outro" style="--a:#22302B;--b:#111816"><div><p class="xv-k">That\'s it</p><h3>7 names. 100%.</h3><p>No fragrance, no dyes, no PVA, nothing from animals.</p></div><div class="xv-bar" aria-hidden="true">'
                  + ''.join(f'<span style="width:{s[4]}%;background:{s[5]}"></span>' for s in SCENES) + '</div></div>')
    n = len(slides)
    dots = ''.join(f'<button type="button" class="xv-seg" data-i="{i}" aria-label="Go to part {i+1} of {n}"><i></i></button>' for i in range(n))
    return f'''<style id="xv-css">
.xv{{position:relative;aspect-ratio:16/9;max-width:100%;border-radius:24px;overflow:hidden;color:#fff;font-family:var(--f-display);box-shadow:0 18px 40px rgba(0,0,0,.18);background:#22302B}}
@media (max-width:620px){{.xv{{aspect-ratio:4/5}}}}
.xv-s{{position:absolute;inset:0;display:grid;grid-template-columns:auto 1fr;gap:clamp(16px,4vw,48px);align-items:center;padding:clamp(22px,5vw,56px) clamp(22px,5vw,64px) 64px;background:radial-gradient(120% 120% at 15% 10%,var(--a),var(--b));opacity:0;visibility:hidden;transition:opacity .5s ease,visibility .5s}}
@media (max-width:620px){{.xv-s{{grid-template-columns:1fr;align-content:center;text-align:left}}}}
.xv-s.on{{opacity:1;visibility:visible}}
.xv-s h3{{font:900 clamp(1.9rem,5.6vw,3.6rem)/1 var(--f-display);letter-spacing:-.02em;color:#fff;margin:6px 0 10px}}
.xv-s p{{font:700 clamp(.95rem,2vw,1.2rem)/1.4 var(--f-display);color:rgba(255,255,255,.88);max-width:42ch}}
.xv-k{{font:900 .8rem/1 var(--f-display)!important;letter-spacing:.14em;text-transform:uppercase;color:#FFC94A!important}}
.xv-ring{{width:clamp(120px,22vw,220px);aspect-ratio:1;border-radius:50%;display:grid;place-items:center;position:relative;background:conic-gradient(#FFC94A calc(var(--fill,0)*1%),rgba(255,255,255,.18) 0);transition:--fill 1.6s}}
.xv-ring::before{{content:"";position:absolute;inset:12px;border-radius:50%;background:var(--b)}}
.xv-ring svg{{width:52%;height:52%;position:relative;color:#fff}}
.xv-s.on .xv-ring svg{{animation:xvpop .9s cubic-bezier(.3,1.6,.5,1) both}}
.xv-s.on .xv-t>*{{animation:xvup .6s cubic-bezier(.2,1.2,.4,1) both}}
.xv-s.on .xv-t>*:nth-child(2){{animation-delay:.08s}}.xv-s.on .xv-t>*:nth-child(3){{animation-delay:.16s}}.xv-s.on .xv-t>*:nth-child(4){{animation-delay:.24s}}
.xv-pc{{display:inline-block;margin-top:14px;background:#FFC94A;color:#2A2205;font:900 1.1rem var(--f-display);padding:8px 14px;border-radius:999px}}
.xv-num{{position:absolute;right:-.06em;bottom:-.18em;font:900 clamp(10rem,32vw,22rem)/1 var(--f-display);color:rgba(255,255,255,.08);pointer-events:none}}
.xv-intro,.xv-outro{{grid-template-columns:auto 1fr}}
.xv-big{{font:900 clamp(8rem,22vw,15rem)/.8 var(--f-display);color:#FFC94A;transform:rotate(-6deg)}}
.xv-s.on .xv-big{{animation:xvpop 1s cubic-bezier(.3,1.6,.5,1) both}}
.xv-outro{{grid-template-columns:1fr}}
.xv-bar{{display:flex;height:22px;border-radius:999px;overflow:hidden;width:100%}}
.xv-bar span{{display:block;height:100%;transform-origin:left;}}
.xv-s.on .xv-bar span{{animation:xvgrow .8s ease both}}
@keyframes xvpop{{from{{transform:scale(.4) rotate(-14deg);opacity:0}}}}
@keyframes xvup{{from{{transform:translateY(18px);opacity:0}}}}
@keyframes xvgrow{{from{{transform:scaleX(0)}}}}
.xv-ctl{{position:absolute;left:0;right:0;bottom:0;display:flex;gap:10px;align-items:center;padding:14px clamp(14px,3vw,24px);background:linear-gradient(transparent,rgba(0,0,0,.35));z-index:3}}
.xv-play{{flex:none;width:40px;height:40px;border-radius:50%;border:0;background:#FFC94A;color:#2A2205;cursor:pointer;display:grid;place-items:center;font:900 1rem var(--f-display)}}
.xv-segs{{flex:1;display:flex;gap:5px}}
.xv-seg{{flex:1;height:22px;border:0;padding:9px 0;background:none;cursor:pointer}}
.xv-seg i{{display:block;height:4px;border-radius:4px;background:rgba(255,255,255,.35);overflow:hidden;position:relative}}
.xv-seg i::after{{content:"";position:absolute;inset:0;background:#fff;transform:scaleX(var(--g,0));transform-origin:left}}
.xv-time{{flex:none;font:800 .85rem var(--f-display);font-variant-numeric:tabular-nums;color:#fff;min-width:74px;text-align:right}}
@media (prefers-reduced-motion:reduce){{.xv-s,.xv-s *{{animation:none!important;transition:none!important}}}}
</style>
<figure class="xv" style="margin:0" aria-label="The seven ingredients, explained in one minute" data-xv>
{''.join(slides)}
<div class="xv-ctl"><button type="button" class="xv-play" aria-label="Play">&#9654;</button><div class="xv-segs">{dots}</div><span class="xv-time">0:00 / 1:05</span></div>
</figure>
<script id="xv-js">(function(){{
  var root=document.querySelector("[data-xv]");if(!root)return;
  var S=root.querySelectorAll(".xv-s"),segs=root.querySelectorAll(".xv-seg i"),btn=root.querySelector(".xv-play"),tm=root.querySelector(".xv-time");
  var D={SECS}*1000,N=S.length,total=N*D,t=0,playing=false,last=0,raf=0,cur=-1;
  var still=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
  function fmt(ms){{var s=Math.floor(ms/1000);return Math.floor(s/60)+":"+("0"+s%60).slice(-2)}}
  function show(i){{if(i===cur)return;cur=i;S.forEach(function(s,k){{s.classList.toggle("on",k===i)}});
    var r=S[i].querySelector(".xv-ring");if(r){{var p=+getComputedStyle(S[i]).getPropertyValue("--p")||0;r.style.setProperty("--fill",0);
      var st=performance.now();(function grow(n){{var k=Math.min(1,(n-st)/1200);r.style.setProperty("--fill",(p*k).toFixed(1));if(k<1)requestAnimationFrame(grow)}})(st)}}}}
  function paint(){{var i=Math.min(N-1,Math.floor(t/D));show(i);segs.forEach(function(g,k){{g.style.setProperty("--g",k<i?1:k>i?0:((t-i*D)/D).toFixed(3))}});tm.textContent=fmt(t)+" / "+fmt(total)}}
  function tick(n){{if(!playing)return;t+=n-last;last=n;if(t>=total){{t=total-1;paint();pause();return}}paint();raf=requestAnimationFrame(tick)}}
  function play(){{if(t>=total-1)t=0;playing=true;btn.innerHTML="&#10074;&#10074;";btn.setAttribute("aria-label","Pause");last=performance.now();raf=requestAnimationFrame(tick)}}
  function pause(){{playing=false;cancelAnimationFrame(raf);btn.innerHTML="&#9654;";btn.setAttribute("aria-label","Play")}}
  btn.addEventListener("click",function(){{playing?pause():play()}});
  root.querySelectorAll(".xv-seg").forEach(function(b){{b.addEventListener("click",function(){{t=+b.dataset.i*D;cur=-1;paint();if(!playing)play()}})}});
  paint();
  if(!still&&"IntersectionObserver" in window){{var started=false;new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting&&!started){{started=true;play()}}else if(!e.isIntersecting&&playing){{pause()}}}})}},{{threshold:.5}}).observe(root)}}
}})();</script>'''


def apply(rel, s):
    if rel != 'pages/ingredients/index.html' or 'data-xv' in s:
        return s
    i = s.find('<figure class="vslot"')
    if i < 0:
        return s
    j = s.find('</figure>', i) + len('</figure>')
    s = s[:i] + build() + s[j:]
    return s.replace('<h2>The seven, in a minute.</h2>', '<h2>The seven, in a minute.</h2><p class="lead">Press play, or tap a segment to jump to any ingredient.</p>', 1)
