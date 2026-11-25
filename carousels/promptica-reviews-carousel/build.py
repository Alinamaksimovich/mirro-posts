"""Собирает слайды карусели отзывов из cases.json. Запуск: python3 build.py (из этой папки или откуда угодно).
Раскладки (layout): chat — 2 фото + заголовок + скрин переписки; photo — 1–2 фото + заголовок + текст отзыва; quote — чистый отзыв.
Слайды: 01 обложка, 02… кейсы по порядку, последний — призыв. Номера «NN / TT» считаются сами."""
import json, os, glob, sys
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'cases.json', encoding='utf-8'))
cases = data['cases']; TOTAL = len(cases) + 2
for f in glob.glob('[0-9][0-9].html'): os.remove(f)

FIT = '''<script>
Promise.all([document.fonts.load("100px 'HN Black Ext'"), document.fonts.load("30px 'Playfair'"), document.fonts.load("20px 'Helios Ext'"), document.fonts.ready]).then(() => {
  document.querySelectorAll('[data-fit]').forEach(el => { el.style.fontSize = '100px'; el.style.fontSize = (100 * parseFloat(el.dataset.fit) / el.getBoundingClientRect().width) + 'px'; });
  document.querySelectorAll('[data-box]').forEach(el => { const max = parseFloat(el.dataset.max || 46), h = parseFloat(el.dataset.box); let fs = max; el.style.fontSize = fs + 'px'; while (el.scrollHeight > h && fs > 22) { fs -= 1; el.style.fontSize = fs + 'px'; } });
});
</script>'''
def grain(n): return f'<svg class="grain"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="{n}" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg>'
def head(n, logo='logo_black.png', col=''):
    return f'<div class="hd"><img src="../../assets/{logo}" alt="promptica"></div>\n    <div class="mt"{col}>отзывы учеников<br>{n:02d} / {TOTAL:02d}</div>'
def page(n, body, cls=''):
    open(f'{n:02d}.html', 'w', encoding='utf-8').write(f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Отзывы учеников — {n:02d}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body data-size="1080x1440">
  <div class="slide {cls}">
{body}
    {grain(n)}
  </div>
{FIT}
</body>
</html>
''')
def ph(x, y, w, h, p, k=0):
    return f'    <div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="hn">{p.get("hint","фото")}</div><img src="img/{p["file"]}" alt="" style="object-position:{p.get("pos","50% 40%")}" onerror="this.remove()"></div>'

def chat_w(fn, top, bottom=1385, maxw=908):
    """ширина скрина переписки: целиком в 908 px, а если не помещается по высоте — уже"""
    w, h = Image.open('img/' + fn).size
    return min(maxw, int((bottom - top) * w / h))
def photos(ps, y, h):
    if len(ps) == 1: return ph(0, y, 1080, h, ps[0])
    return ph(0, y, 538, h, ps[0]) + '\n' + ph(542, y, 538, h, ps[1])
def meta(i, c):  # заголовок + имя + пометка
    return f'''    <div class="abs lbl br" style="left:86px;top:{c['y']}px">[{i:02d}] кейс</div>
    <div class="abs name" style="left:86px;top:{c['y']+40}px;width:908px;font-size:40px;line-height:1.05">{c['title']}</div>
    <div class="abs mrow" style="left:86px;top:{c['y']+162}px;width:908px"><span class="br">[{c['name']}]</span><span style="opacity:.7">{c.get('note','')}</span></div>'''
# обложка
page(1, f'''    <div class="ph" style="left:0;top:0;width:1080px;height:900px"><div class="hn">обложка: крупный план</div><img src="img/01-a.jpg" alt="" style="object-position:50% 30%" onerror="this.remove()"></div>
    <div class="vert" style="right:44px;top:560px">promptica.digital agency</div>
    <div class="abs" style="left:86px;top:960px;width:908px"><div class="fit" data-fit="908">Отзывы<br>учеников</div></div>
    <div class="abs mrow" style="left:86px;top:1232px;width:908px"><span>курс <b class="br" style="font-weight:400">[{data['course']}]</b></span><span>01 / {TOTAL:02d} · листай →</span></div>''')
# кейсы
for i, c in enumerate(cases, start=1):
    n = i + 1; L = c.get('layout', 'chat')
    if L == 'chat':
        c['y'] = 812
        page(n, f'''{photos(c['photos'], 170, 600)}
{meta(i, c)}
    <div class="abs" style="left:86px;top:1040px;width:908px"><img src="img/{c['chat']}" alt="" style="width:{chat_w(c['chat'],1040)}px;display:block"></div>
    {head(n)}''')
    elif L == 'photo':
        c['y'] = 812
        page(n, f'''{photos(c['photos'], 170, 600)}
{meta(i, c)}
    <div class="abs quote" data-box="230" data-max="40" style="left:86px;top:1064px;width:908px;height:230px;overflow:hidden">«{c['quote']}»</div>
    {head(n)}''')
    elif L == 'video':
        v = c['video']; st = ''.join(f'''<div style="padding:18px 0;border-top:1px solid rgba(13,13,13,.25)"><div style="font-family:'HN Black Ext',sans-serif;font-size:96px;line-height:.9;letter-spacing:-0.03em">{x['big']}</div><div class="lbl" style="margin-top:12px;opacity:.7">{x['label']}</div></div>''' for x in c.get('stats', []))
        page(n, f'''    <div class="ph" style="left:0;top:170px;width:416px;height:740px"><div class="hn">видео ученика</div><img id="vid" src="img/{v['poster']}" alt="" style="object-position:50% 40%" onerror="this.remove()"></div>
    <div class="abs lbl br" style="left:470px;top:176px">[{i:02d}] кейс</div>
    <div class="abs name" style="left:470px;top:216px;width:524px;font-size:40px;line-height:1.05">{c['title']}</div>
    <div class="abs" style="left:470px;top:332px;width:524px"><div class="br lbl" style="font-size:17px">[{c['name']}]</div><div class="res" style="margin-top:8px;opacity:.75">{c.get('note','')}</div></div>
    <div class="abs" style="left:470px;top:470px;width:524px">{st}</div>
    <div class="abs" style="left:86px;top:950px;width:908px"><img src="img/{c['chat']}" alt="" style="width:{chat_w(c['chat'],1040)}px;display:block"></div>
    {head(n)}
    <script>
    // покадровая подмена кадров видео (для render-video.js); в обычном экспорте остаётся постер
    const FR = {v['frames']!r}, N = {v['count']}, FPS = {v['fps']}, vid = document.getElementById('vid');
    window.setT = async function (t) {{ const k = Math.min(N, Math.floor(t * FPS + 1e-6) + 1); vid.src = 'img/' + FR + '/f' + String(k).padStart(4, '0') + '.jpg'; await vid.decode().catch(() => {{}}); }};
    </script>''')
    else:  # quote
        page(n, f'''    <div class="abs" style="left:78px;top:250px;font-family:'HN Black Ext',sans-serif;font-size:300px;line-height:.8;color:var(--red)">“</div>
    <div class="abs quote" data-box="640" data-max="58" style="left:86px;top:480px;width:908px;height:640px;overflow:hidden">{c['quote']}</div>
    <div class="abs hair" style="left:86px;top:1170px;width:908px"></div>
    <div class="abs" style="left:86px;top:1206px;width:908px;display:flex;justify-content:space-between;align-items:flex-end"><div><div class="name">{c['name']}</div><div class="res" style="margin-top:12px"><span class="br">[</span>{c.get('note','результат ученика')}<span class="br">]</span></div></div><div class="lbl" style="opacity:.65;text-align:right">курс {data['course']}</div></div>
    {head(n)}''')
# призыв
n = TOTAL
page(n, f'''    <div class="abs" style="left:86px;top:300px;width:908px"><div class="fit" data-fit="908" style="color:var(--cream)">Хочешь<br>так же?</div></div>
    <div class="abs mrow" style="left:86px;top:600px;width:908px;color:var(--cream)"><span>курс [{data['course']}]</span><span>{data.get('cta_note','запись открыта')}</span></div>
    <div class="abs hair" style="left:86px;top:690px;width:908px;color:var(--cream)"></div>
    <div class="abs" style="left:86px;top:730px;width:760px;font-size:34px;line-height:1.38;color:var(--cream)">{data.get('cta','Напиши слово «КУРС» в комментариях, и мы пришлём программу.')}</div>
    {head(n,'logo_cream.png',' style="color:#fff7e6"')}''', 'red')
print('слайдов:', TOTAL)
