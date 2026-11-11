p = 'home-template.html'
s = open(p, encoding='utf-8').read()


def R(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)


# text-color tokens per theme
R('--on-color:#FFFFFF;', '--on-color:#FFFFFF; --t-mint:#2F7D57; --t-sky:#1F6FA8; --t-plum:#5B2A5E;')
R('--plum:#5B2A5E; --plum-tint:#2A1A2C; --sun:#FFC94A;\n  --shadow:0 2px 0 rgba(0,0,0,.3),0 14px 34px rgba(0,0,0,.35);\n  color-scheme:dark}}',
  '--plum:#5B2A5E; --plum-tint:#2A1A2C; --sun:#FFC94A; --t-mint:#7FD3A6; --t-sky:#86C5F0; --t-plum:#E7B8EA;\n  --shadow:0 2px 0 rgba(0,0,0,.3),0 14px 34px rgba(0,0,0,.35);\n  color-scheme:dark}}')
R('--plum:#5B2A5E; --plum-tint:#2A1A2C; --sun:#FFC94A;\n  --shadow:0 2px 0 rgba(0,0,0,.3),0 14px 34px rgba(0,0,0,.35);\n  color-scheme:dark}\n',
  '--plum:#5B2A5E; --plum-tint:#2A1A2C; --sun:#FFC94A; --t-mint:#7FD3A6; --t-sky:#86C5F0; --t-plum:#E7B8EA;\n  --shadow:0 2px 0 rgba(0,0,0,.3),0 14px 34px rgba(0,0,0,.35);\n  color-scheme:dark}\n')
R('a{color:var(--sky-deep);text-underline-offset:3px}\n:root:not([data-theme="light"]) a{color:inherit}', 'a{color:var(--t-sky);text-underline-offset:3px}')
R('.links a:hover{background:var(--mint-tint);color:var(--mint-deep)}\n:root:not([data-theme="light"]) .links a:hover{color:var(--ink)}', '.links a:hover{background:var(--mint-tint);color:var(--t-mint)}')
R('.ing-head .eyebrow{color:var(--mint-deep)}\n:root:not([data-theme="light"]) .ing-head .eyebrow{color:var(--mint)}', '.ing-head .eyebrow{color:var(--t-mint)}')
R('.how .eyebrow{color:var(--sky-deep)}\n:root:not([data-theme="light"]) .how .eyebrow{color:var(--sky)}', '.how .eyebrow{color:var(--t-sky)}')
R('.learn .eyebrow{color:var(--plum)}\n:root:not([data-theme="light"]) .learn .eyebrow{color:#E7B8EA}', '.learn .eyebrow{color:var(--t-plum)}')
R('.reviews .eyebrow{color:var(--plum)}\n:root:not([data-theme="light"]) .reviews .eyebrow{color:#E7B8EA}', '.reviews .eyebrow{color:var(--t-plum)}')
R('<p class="eyebrow" style="color:var(--sky-deep)">Launch pricing</p>', '<p class="eyebrow" style="color:var(--t-sky)">Launch pricing</p>')
R('.done .big{font:900 1.9rem var(--f-display);color:var(--mint-deep)}', '.done .big{font:900 1.9rem var(--f-display);color:var(--t-mint)}')
# hero headline size
R('.hero h1{font-size:clamp(3.4rem,11vw,7.4rem);', '.hero h1{font-size:clamp(3rem,8.4vw,6rem);')
R('.hero-copy{display:grid;gap:24px;min-width:0}', '.hero-copy{display:grid;gap:24px;min-width:0;position:relative;z-index:1}')
# band: mint / sun / plum so it reads under the sky hero
R('.band span:nth-child(2){background:var(--sky)}', '.band span:nth-child(2){background:var(--sun)}')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
