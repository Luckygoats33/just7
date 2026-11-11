p = 'home-template.html'
s = open(p, encoding='utf-8').read()


def R(a, b, n=1):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, n)


css = r'''
/* mobile menu that pops */
.mmenu{display:block;margin-left:6px}
.mmenu summary{list-style:none;cursor:pointer;width:48px;height:48px;border-radius:14px;background:var(--sky-deep);display:grid;place-items:center;box-shadow:0 4px 0 #144C74}
.mmenu summary::-webkit-details-marker{display:none}
.mmenu summary i,.mmenu summary i::before,.mmenu summary i::after{display:block;width:20px;height:3px;border-radius:3px;background:#fff;position:relative;transition:.25s}
.mmenu summary i::before,.mmenu summary i::after{content:"";position:absolute;left:0}
.mmenu summary i::before{top:-7px}.mmenu summary i::after{top:7px}
.mmenu[open] summary{background:var(--sun);box-shadow:0 4px 0 #B98A12}
.mmenu[open] summary i{background:transparent}
.mmenu[open] summary i::before,.mmenu[open] summary i::after{background:#2A2205;top:0}
.mmenu[open] summary i::before{transform:rotate(45deg)}.mmenu[open] summary i::after{transform:rotate(-45deg)}
.mpanel{position:fixed;left:0;right:0;bottom:0;top:calc(66px + env(safe-area-inset-top,0px));background:var(--sky);overflow-y:auto;padding:22px max(16px,env(safe-area-inset-left,0px)) calc(28px + env(safe-area-inset-bottom,0px));display:grid;gap:6px;align-content:start;animation:drop .35s cubic-bezier(.2,1.3,.4,1)}
@keyframes drop{from{transform:translateY(-16px);opacity:0}}
.mpanel a.big{font:900 2.4rem/1.05 var(--f-display);color:#fff;text-decoration:none;padding:6px 0;letter-spacing:-.02em;display:flex;justify-content:space-between;align-items:center}
.mpanel a.big span{font-size:1.4rem;color:var(--sun)}
.mpanel a.big:nth-child(2){color:var(--sun)}
.mpanel .mrow{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}
.mpanel .mrow a{background:#fff;color:#22302B;text-decoration:none;border-radius:16px;padding:14px;font:900 1.05rem var(--f-display);box-shadow:0 4px 0 rgba(0,0,0,.15)}
.mpanel .mrow a:nth-child(2){background:var(--mint);color:#10291D}
.mpanel .mrow a:nth-child(3){background:var(--plum);color:#fff}
.mpanel .mrow a:nth-child(4){background:var(--sun);color:#2A2205}
.mpanel .mfoot{margin-top:18px;color:#EAF5FD;font-size:.95rem}
nav.site-nav{z-index:70}
@media (max-width:899px){.logo svg{width:112px}}
@media (min-width:900px){.mmenu{display:none}}
/* background graphics */
.hero{isolation:isolate}
.hero canvas.fx{position:absolute;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none}
.wave{display:block;width:100%;height:clamp(40px,7vw,90px)}
.why{position:relative;overflow:hidden;isolation:isolate}
.why::before{content:"7";position:absolute;right:-4vw;top:-8vw;font:900 clamp(22rem,60vw,48rem)/1 var(--f-display);color:rgba(42,34,5,.06);z-index:-1;transform:rotate(12deg)}
.mission{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 24 24'%3E%3Cg fill='%23ffffff' fill-opacity='.06' transform='translate(3 3) scale(.6) rotate(-15 12 12)'%3E%3Cellipse cx='7' cy='7.5' rx='2' ry='2.6'/%3E%3Cellipse cx='12' cy='5.5' rx='2' ry='2.6'/%3E%3Cellipse cx='17' cy='7.5' rx='2' ry='2.6'/%3E%3Cpath d='M12 10.5c-3 0-6 4.2-6 6.6 0 1.8 1.4 2.9 3 2.9 1.3 0 2-.7 3-.7s1.7.7 3 .7c1.6 0 3-1.1 3-2.9 0-2.4-3-6.6-6-6.6z'/%3E%3C/g%3E%3C/svg%3E")}
.lineup{background-image:radial-gradient(circle at 12% 20%,rgba(58,155,220,.28) 0,transparent 32%),radial-gradient(circle at 88% 85%,rgba(95,179,137,.25) 0,transparent 30%),radial-gradient(circle at 70% 10%,rgba(91,42,94,.35) 0,transparent 26%)}
.out{background-image:radial-gradient(circle,rgba(255,255,255,.22) 2px,transparent 2.5px);background-size:26px 26px}
.wl{position:relative;overflow:hidden;isolation:isolate}
.wl::before,.wl::after{content:"";position:absolute;border-radius:50%;z-index:-1}
.wl::before{width:520px;height:520px;right:-160px;top:-200px;background:var(--sky);opacity:.55}
.wl::after{width:300px;height:300px;left:-90px;bottom:-120px;background:var(--plum);opacity:.6}
'''
R('/* footer */', css + '\n/* footer */')

menu = '''<details class="mmenu"><summary aria-label="Menu"><i></i></summary><div class="mpanel">
    <a class="big" href="products/just-7/index.html">Shop Just 7 <span>&rarr;</span></a>
    <a class="big" href="#waitlist">Join the waitlist <span>&rarr;</span></a>
    <a class="big" href="pages/ingredients/index.html">Ingredients <span>&rarr;</span></a>
    <a class="big" href="pages/why-just-7/index.html">Why Just 7 <span>&rarr;</span></a>
    <div class="mrow"><a href="pages/learn/index.html">Learn</a><a href="#laundry-day">Laundry day</a><a href="#mission">7% to animals</a><a href="pages/faq/index.html">FAQ</a></div>
    <p class="mfoot">Seven ingredients. Zero compromise.</p>
  </div></details>
  <a class="btn nav-cta" href="#waitlist">Join the waitlist</a>'''
R('<a class="btn nav-cta" href="#waitlist">Join the waitlist</a>', menu)

R('<section class="hero"><div class="w">', '<section class="hero"><canvas class="fx" aria-hidden="true"></canvas><div class="w">')
# wave from hero into band area: put a wave after mission and before price
wave_plum = '<svg class="wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true" style="background:var(--plum)"><path d="M0 40 C 240 90 480 0 720 40 S 1200 90 1440 30 V90 H0Z" fill="var(--paper)"/></svg>'
R('<section class="sec price-sec">', wave_plum + '\n<section class="sec price-sec">')
wave_sun = '<svg class="wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true" style="background:var(--ink)"><path d="M0 50 C 300 0 520 90 760 50 S 1180 0 1440 60 V90 H0Z" fill="var(--sun)"/></svg>'
R('<section class="sec why">', wave_sun + '\n<section class="sec why">')

js = r'''<script>(function(){
  var c=document.querySelector(".hero canvas.fx");if(!c||!c.getContext)return;
  var x=c.getContext("2d"),dpr=Math.min(2,window.devicePixelRatio||1),W,H,items=[];
  var still=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;
  function size(){var r=c.getBoundingClientRect();W=r.width;H=r.height;c.width=W*dpr;c.height=H*dpr;x.setTransform(dpr,0,0,dpr,0,0)}
  function seed(){items=[];var n=Math.round(Math.min(34,Math.max(16,W/40)));for(var i=0;i<n;i++){var sheet=i%3===0;items.push({sheet:sheet,x:Math.random()*W,y:Math.random()*H,r:sheet?14+Math.random()*16:4+Math.random()*22,a:Math.random()*6.28,va:(Math.random()-.5)*.01,vy:-(.15+Math.random()*.45),vx:(Math.random()-.5)*.2,ph:Math.random()*6.28})}}
  function rr(w,h,r){x.beginPath();x.moveTo(-w/2+r,-h/2);x.arcTo(w/2,-h/2,w/2,h/2,r);x.arcTo(w/2,h/2,-w/2,h/2,r);x.arcTo(-w/2,h/2,-w/2,-h/2,r);x.arcTo(-w/2,-h/2,w/2,-h/2,r);x.closePath()}
  function draw(t){x.clearRect(0,0,W,H);items.forEach(function(o){x.save();x.translate(o.x,o.y);
    if(o.sheet){x.rotate(o.a);x.fillStyle="rgba(255,255,255,.16)";rr(o.r*2.2,o.r*1.7,5);x.fill();x.strokeStyle="rgba(255,255,255,.28)";x.lineWidth=1.5;x.stroke()}
    else{x.beginPath();x.arc(0,0,o.r,0,6.283);x.strokeStyle="rgba(255,255,255,.45)";x.lineWidth=1.6;x.stroke();x.fillStyle="rgba(255,255,255,.07)";x.fill();x.beginPath();x.arc(-o.r*.35,-o.r*.35,o.r*.22,0,6.283);x.fillStyle="rgba(255,255,255,.55)";x.fill()}
    x.restore()})}
  function step(){items.forEach(function(o){o.y+=o.vy;o.x+=o.vx+Math.sin(o.ph+=.01)*.25;o.a+=o.va;if(o.y<-40){o.y=H+40;o.x=Math.random()*W}});draw();if(!still)requestAnimationFrame(step)}
  size();seed();draw();if(!still)requestAnimationFrame(step);
  window.addEventListener("resize",function(){size();seed();draw()});
})();</script>'''
R('{{SCRIPTS}}', '{{SCRIPTS}}\n' + js)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
