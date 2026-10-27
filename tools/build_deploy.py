"""Build the GitHub Pages copy of the Energy Gazette page from the artifact source.
usage: python3 -I build_deploy.py <source index.html> <repo dir>"""
import sys, os, shutil
src_path, repo = sys.argv[1:3]
src = open(src_path).read()
lines = src.split('\n')
assert lines[0].startswith('<meta charset') and lines[1].startswith('<title>')
drop = ('<meta charset', '<title>', '<meta name="claude:', '<meta name="description"')
body = '\n'.join(l for l in lines[:6] if not l.startswith(drop)) + '\n' + '\n'.join(lines[6:])
B = "https://abaxgrid.com/energygazette/"
head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>The Energy Gazette: Venezuela Edition</title>
<meta name="description" content="Venezuela's energy reopening, read from primary sources: biweekly issues, a living timeline, a sector map and a fiscal take calculator. By Danny Peña.">
<link rel="canonical" href="{B}">
<link rel="alternate" hreflang="en" href="{B}?lang=en">
<link rel="alternate" hreflang="es" href="{B}?lang=es">
<link rel="alternate" hreflang="pt-BR" href="{B}?lang=pt">
<link rel="alternate" hreflang="x-default" href="{B}">
<meta property="og:site_name" content="The Energy Gazette">
<meta property="og:title" content="The Energy Gazette: Venezuela Edition">
<meta property="og:description" content="Venezuela's energy reopening, read from primary sources: biweekly issues, a living timeline, a sector map and a fiscal take calculator.">
<meta property="og:url" content="{B}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="es_LA">
<meta property="og:locale:alternate" content="pt_BR">
<meta property="og:image" content="{B}assets/share-eg-en.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The Energy Gazette: Venezuela Edition. Venezuela's energy reopening, read from primary sources.">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
'''
open(os.path.join(repo, 'index.html'), 'w').write(head + body.lstrip('\n') + '\n</body>\n</html>\n')
P = {'en': dict(lang='en', loc='en_US', t='The Energy Gazette: Venezuela Edition', d="Venezuela's energy reopening, read from primary sources: biweekly issues, a living timeline, a sector map and a fiscal take calculator.", a='The Energy Gazette in English →'),
     'es': dict(lang='es', loc='es_LA', t='The Energy Gazette: Edición Venezuela', d='La reapertura energética de Venezuela, leída desde las fuentes primarias: ediciones quincenales, cronología viva, mapa del sector y calculadora de participación fiscal.', a='The Energy Gazette en español →'),
     'pt': dict(lang='pt-BR', loc='pt_BR', t='The Energy Gazette: Edição Venezuela', d='A reabertura energética da Venezuela, lida a partir das fontes primárias: edições quinzenais, linha do tempo viva, mapa do setor e calculadora da participação fiscal.', a='The Energy Gazette em português →')}
for k, v in P.items():
    os.makedirs(os.path.join(repo, k), exist_ok=True)
    open(os.path.join(repo, k, 'index.html'), 'w').write(f'''<!doctype html>
<html lang="{v["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{v["t"]}</title>
<meta name="description" content="{v["d"]}">
<meta property="og:site_name" content="The Energy Gazette">
<meta property="og:title" content="{v["t"]}">
<meta property="og:description" content="{v["d"]}">
<meta property="og:url" content="{B}{k}/">
<meta property="og:type" content="website">
<meta property="og:locale" content="{v["loc"]}">
<meta property="og:image" content="{B}assets/share-eg-{k}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{B}?lang={k}">
<meta http-equiv="refresh" content="0; url=/energygazette/?lang={k}">
<script>location.replace('/energygazette/?lang={k}'+location.hash);</script>
<style>body{{margin:0;background:#0F2A43;color:#fff;font:16px system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}}a{{color:#7FB6D3}}</style>
</head>
<body><a href="/energygazette/?lang={k}">{v["a"]}</a></body>
</html>
''')
print('built', repo)
