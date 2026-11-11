p = 'home-template.html'
s = open(p, encoding='utf-8').read()


def R(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# color stripe becomes a teaser of what's coming
R('<div class="band" aria-hidden="true"><span></span><span></span><span></span></div>',
  '<div class="band" role="list" aria-label="The Just lineup">'
  '<button type="button" role="listitem" data-tip="Just 5 &middot; Gentle &middot; Coming in time"><span class="sr">Just 5, gentle, coming in time</span></button>'
  '<button type="button" role="listitem" data-tip="Just 7 &middot; Everyday &middot; Here first"><span class="sr">Just 7, everyday, here first</span></button>'
  '<button type="button" role="listitem" data-tip="Just 9 &middot; Gritty &middot; Coming in time"><span class="sr">Just 9, gritty, coming in time</span></button></div>')
css = '''
/* teaser stripe */
.band{height:28px;position:relative;z-index:5}
.band button{border:0;padding:0;margin:0;cursor:help;position:relative;transition:transform .2s,filter .2s}
.band button:nth-child(1){background:var(--mint)}
.band button:nth-child(2){background:var(--sun)}
.band button:nth-child(3){background:var(--plum)}
.band button:hover,.band button:focus-visible{filter:brightness(1.08);transform:scaleY(1.35)}
.band button::after{content:attr(data-tip);position:absolute;left:50%;bottom:calc(100% + 14px);transform:translateX(-50%) translateY(6px) scaleY(.75);white-space:nowrap;background:var(--ink);color:var(--paper);font:900 .95rem var(--f-display);padding:10px 16px;border-radius:999px;box-shadow:0 10px 24px rgba(0,0,0,.25);opacity:0;pointer-events:none;transition:opacity .2s,transform .25s cubic-bezier(.3,1.5,.5,1)}
.band button:hover::after,.band button:focus-visible::after,.band button.on::after{opacity:1;transform:translateX(-50%) scaleY(.75)}
.band button:first-child::after{left:16px;transform:translateY(6px) scaleY(.75)}
.band button:first-child:hover::after,.band button:first-child:focus-visible::after,.band button:first-child.on::after{transform:scaleY(.75)}
.band button:last-child::after{left:auto;right:16px;transform:translateY(6px) scaleY(.75)}
.band button:last-child:hover::after,.band button:last-child:focus-visible::after,.band button:last-child.on::after{transform:scaleY(.75)}
'''
R('/* footer */', css + '\n/* footer */')
# tap support on phones
R('{{SCRIPTS}}', '{{SCRIPTS}}\n<script>document.querySelectorAll(".band button").forEach(function(b){b.addEventListener("click",function(){var on=!b.classList.contains("on");document.querySelectorAll(".band button").forEach(function(x){x.classList.remove("on")});b.classList.toggle("on",on)})});</script>')
# every menu item goes to its own page
R('<a class="big" href="#waitlist">Join the waitlist <span>&rarr;</span></a>', '<a class="big" href="pages/waitlist/index.html">Join the waitlist <span>&rarr;</span></a>')
R('<a href="#laundry-day">Laundry day</a>', '<a href="pages/how-to-use/index.html">How to use</a>')
R('<a href="#mission">7% to animals</a>', '<a href="pages/about/index.html#mission">7% to animals</a>')
R('<a class="btn ghost" href="#ingredients">What\'s inside</a>', '<a class="btn ghost" href="pages/ingredients/index.html">What\'s inside</a>')
R('<a class="btn nav-cta" href="#waitlist">Join the waitlist</a>', '<a class="btn nav-cta" href="pages/waitlist/index.html">Join the waitlist</a>')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
