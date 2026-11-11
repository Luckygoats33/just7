import re
src = r'C:\Users\willw\.claude\projects\C--Users-willw-Projects-just7\275108eb-5c48-4af4-b45a-03fa3ae9be1c\tool-results\artifact-92ae9c9c-1794383490-d928.html'
lines = open(src, encoding='utf-8').read().split('\n')
nav = lines[270]
logo = re.search(r'<svg role="img".*?</svg>', nav).group(0)
scripts = '\n'.join(lines[467:472])
t = open('home-template.html', encoding='utf-8').read()
t = t.replace('{{LOGO}}', logo).replace('{{SCRIPTS}}', scripts)
open('index.html', 'w', encoding='utf-8', newline='').write(t)
print(len(t), t.count('<script'), t.count('{{'))
