"""Карусель «Нейросети с нуля — что вы получите» (promptica). Тексты — здесь; python3 build.py && npm run export -- promptica-course"""
import os
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
TOTAL = 7
FIT = '''<script>
Promise.all([document.fonts.load("200 100px 'Vela'"), document.fonts.load("20px 'Helios Ext'"), document.fonts.load("italic 30px 'Playfair'"), document.fonts.ready]).then(() => {
  document.querySelectorAll('[data-fit]').forEach(el => { el.style.fontSize = '100px'; el.style.fontSize = (100 * parseFloat(el.dataset.fit) / el.getBoundingClientRect().width) + 'px'; });
  const ctx = document.createElement('canvas').getContext('2d');
  document.querySelectorAll('[data-fit],.thin,.light').forEach(el => { if (el.dataset.opt === '0') return; const cs = getComputedStyle(el); ctx.font = cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily; const m = ctx.measureText((el.textContent.trim()[0] || 'A')); el.style.marginLeft = m.actualBoundingBoxLeft + 'px'; });
});
</script>'''
def grain(n): return f'<svg class="grain"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="{n}" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg>'
def page(n, body, cls='', logo='logo_black.png', meta_style='', meta_text='нейросети с нуля'):
    open(f'{n:02d}.html', 'w', encoding='utf-8').write(f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Нейросети с нуля — {n:02d}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="slide {cls}">
{body}
    <div class="hd"><img src="../../assets/{logo}" alt="promptica"></div>
    <div class="mt"{meta_style}>{meta_text}<br>{n:02d} / {TOTAL:02d}</div>
    {grain(n)}
  </div>
{FIT}
</body>
</html>
''')
def ph(x, y, w, h, hint, fn, pos='50% 35%', style=''):
    return f'    <div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px{style}"><div class="hn">{hint}</div><img src="img/{fn}" alt="" style="object-position:{pos}" onerror="this.remove()"></div>'
def fit(text, w, top, left=86, cls='thin', extra=''):
    return f'    <div class="abs" style="left:{left}px;top:{top}px"><div class="{cls}" data-fit="{w}" style="{extra}">{text}</div></div>'

# 1 — одно фото на весь пост, текст в свободной белой колонке слева
page(1, '''    <div class="ph" style="left:72px;top:0;width:1008px;height:1350px;background:#fff;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 70px);mask-image:linear-gradient(90deg,transparent 0,#000 70px)"><div class="hn">фото на весь пост</div><img src="img/01-a.jpg" alt="" onerror="this.remove()"></div>
    <div class="abs light" style="left:86px;top:170px;font-size:60px;line-height:1.04;width:300px">Нейросети<br>с нуля</div>
    <div class="abs" style="left:86px;top:330px;width:250px;font-size:22px;line-height:1.4">бренд-фотосессия без студии: от идеи до готовой серии кадров</div>
    <div class="abs micro" style="left:86px;top:1262px">курс · 2 месяца</div>
    <div class="abs micro" style="right:86px;top:1262px">листай →</div>''', meta_text='курс promptica')
# 2 — красный верх + фото снизу на половину кадра
page(2, f'''    <div class="abs" style="left:0;top:0;width:1080px;height:675px;background:#930400"></div>
{ph(0,675,1080,675,'фото на половину кадра','02-a.jpg','50% 45%')}
{fit('Видеоуроки',908,150,86,'thin','color:#fff7e6')}
    <div class="abs it" style="left:86px;top:330px;width:880px;font-size:48px;line-height:1.1;color:#fff7e6">Смотрите уроки в удобное время и идите в своём темпе.</div>
    <div class="abs" style="left:86px;top:470px;width:760px;font-size:25px;line-height:1.42;color:#fff7e6">Каждый урок разбит на небольшие части, поэтому не нужно выделять на него целый день.</div>
    <div class="abs mrow" style="left:86px;top:615px;width:908px;color:#fff7e6"><span>короткие модули</span><span>своё расписание</span><span>в удобное время</span></div>''', '', 'logo_cream.png', ' style="color:#fff7e6"')
# 3 — кураторы, минимализм
page(3, '''    <div class="abs micro" style="left:86px;top:150px">кто ведёт курс</div>
''' + ph(0,200,538,720,'фото Алины','03-a.jpg','50% 25%') + '\n' + ph(542,200,538,720,'фото Ани','03-b.jpg','50% 25%') + '''
    <div class="abs" style="left:86px;top:960px;width:420px"><div class="light" style="font-size:58px;line-height:1">Алина</div>
      <div style="font-size:22px;line-height:1.45;margin-top:18px">куратор курса<br>креативный директор promptica<br>AI-креатор</div></div>
    <div class="abs" style="right:86px;top:960px;width:420px;text-align:right"><div class="light" data-opt="0" style="font-size:58px;line-height:1">Аня</div>
      <div style="font-size:22px;line-height:1.45;margin-top:18px">8 лет в дизайне<br>брендинг и визуал для соцсетей<br>ведущий креатор</div></div>''')
# 4 — карточка поверх фото (референс Borcelle)
items = ['разбор работ участников на курсе', 'сборка портфолио', 'проверка домашних заданий с комментариями', 'ответы кураторов на вопросы по ходу курса', 'закрытый чат участников']
li = ''.join(f'<div>{t}</div>' for t in items)
page(4, f'''{ph(0,0,1080,1350,'фото на весь слайд','04-a.jpg','50% 50%',';background:#2a0000')}
    <div class="abs" style="left:240px;top:250px;width:600px;height:860px;background:#fff7e6;border-radius:14px;box-shadow:0 24px 70px rgba(0,0,0,.3)">
      <div style="text-align:center;padding-top:46px"><img src="../../assets/logo_black.png" alt="promptica" style="height:26px"></div>
      <div style="position:absolute;left:0;right:0;top:230px;text-align:center">
        <div class="thin" data-opt="0" style="font-size:104px">2 месяца</div>
        <div class="it" style="font-size:38px;margin-top:12px">с обратной связью</div>
      </div>
      <div style="position:absolute;left:0;right:0;bottom:48px;padding:0 20px;text-align:center;font-size:20px;line-height:1.6;white-space:nowrap">
        <div style="font-size:17px;letter-spacing:.03em;color:#930400;margin-bottom:12px">что входит</div>{li}
      </div>
    </div>''', '', 'logo_cream.png', ' style="color:#fff7e6"')
# 5 — модули как оглавление
mods = [('01', 'Инструменты и основы', '', False),
        ('02', 'Идея и первые кадры', 'поиск своего стиля: от референса до готовой фотосессии', False),
        ('03', 'Исправляем недочёты', 'Убираем артефакты, «пластиковую» кожу и другое. Кадр выглядит как настоящая фотография.', False),
        ('04', 'Вся фотосессия целиком', 'Планируем съёмку по кадрам, меняем локации и образы, отбираем лучшее и собираем серию.', False),
        ('05', 'Как монетизировать навык и получать заказы', 'Упаковываем навык в услугу', True)]
rows = ''.join(f'<div style="display:flex;gap:30px;align-items:baseline;padding:26px 0;border-top:1px solid rgba(13,13,13,.22)"><div class="thin{" rd" if r else ""}" style="font-size:64px;width:110px;flex:none">{n}</div><div style="flex:1"><div style="font-size:31px;line-height:1.22{";color:#930400" if r else ""}">{t}</div>{f"<div style=\'font-size:21px;line-height:1.4;opacity:.7;margin-top:8px\'>{d}</div>" if d else ""}</div></div>' for n, t, d, r in mods)
page(5, f'''{fit('5 модулей',620,170)}
    <div class="abs" style="left:86px;top:400px;width:908px">{rows}</div>''')
# 6 — блок цвета + фото снизу (Pretend)
page(6, '''    <div class="abs" style="left:0;top:0;width:1080px;height:900px;background:#930400"></div>
''' + ph(0,900,1080,450,'фото или видео для слайда','06-a.jpg','50% 50%') + '''
    <div class="abs light" style="left:86px;top:190px;font-size:92px;line-height:1;color:#fff7e6">Гайды —<br>навсегда</div>
    <div class="abs" style="left:86px;top:440px;width:860px;font-size:30px;line-height:1.4;color:#fff7e6">Забираете гайды и пользуетесь ими после курса.<br>После каждого урока: домашнее задание.</div>
    <div class="abs" style="left:86px;top:660px;width:908px;background:#fff;border-radius:14px;padding:34px 40px 38px"><div class="it" style="font-size:44px;line-height:1.14;color:#930400">Бонус: урок по оформлению дизайна постов и рилс</div></div>
    <div class="abs mrow" style="left:86px;top:858px;width:908px;color:#fff7e6"><span>гайды</span><span>домашнее задание</span><span>бонус-урок</span></div>''', '', 'logo_cream.png', ' style="color:#fff7e6"')
# 7 — запись: текст сверху, фото вылетом снизу (белый фон — фото переходит без шва)
page(7, f'''{fit('Запись на курс',908,150,86,'thin')}
    <div class="abs it" style="left:86px;top:325px;width:908px;font-size:41px;line-height:1.14">Пишите слово <span class="rd">«курс»</span> в комментариях, и мы пришлём подробную программу курса.</div>
    <div class="abs mrow" style="left:86px;top:470px;width:908px"><span>курс «нейросети с нуля»</span><span>2 месяца</span></div>
{ph(0,540,1080,810,'фото на нижнюю часть слайда','07-a.jpg','50% 50%',';background:#fff;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 50px);mask-image:linear-gradient(180deg,transparent 0,#000 50px)')}''')
print('слайдов:', TOTAL)
