"""Карусель «Нейросети с нуля — что вы получите» (promptica). Тексты — в этом файле; python3 build.py && npm run export -- promptica-course"""
import os
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
TOTAL = 8
FIT = '''<script>
Promise.all([document.fonts.load("100px 'HN Black Ext'"), document.fonts.load("20px 'Helios Ext'"), document.fonts.ready]).then(() => {
  document.querySelectorAll('[data-fit]').forEach(el => { el.style.fontSize = '100px'; el.style.fontSize = (100 * parseFloat(el.dataset.fit) / el.getBoundingClientRect().width) + 'px'; });
});
</script>'''
def grain(n): return f'<svg class="grain"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="{n}" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg>'
def page(n, body, cls='', logo='logo_black.png', col=''):
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
    <div class="mt"{col}>курс «нейросети с нуля»<br>{n:02d} / {TOTAL:02d}</div>
    {grain(n)}
  </div>
{FIT}
</body>
</html>
''')
def ph(x, y, w, h, hint, fn, pos='50% 35%'):
    return f'    <div class="ph" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><div class="hn">{hint}</div><img src="img/{fn}" alt="" style="object-position:{pos}" onerror="this.remove()"></div>'
def fit(text, w=908, top=200, color='', lh='.9'):
    c = f';color:{color}' if color else ''
    return f'    <div class="abs" style="left:86px;top:{top}px;width:908px"><div class="fit" data-fit="{w}" style="line-height:{lh}{c}">{text}</div></div>'
def mrow(left, right, top, color=''):
    c = f';color:{color}' if color else ''
    return f'    <div class="abs mrow" style="left:86px;top:{top}px;width:908px{c}"><span class="br">{left}</span><span>{right}</span></div>'
cb = '<i class="cb" style="display:inline-block;margin-right:22px;vertical-align:middle"></i>'

# 1 хук
page(1, f'''{mrow('[курс]','листай →',190)}
{fit('Нейросети<br>с нуля',908,240)}
    <div class="abs" style="left:86px;top:540px;width:820px;font-size:36px;line-height:1.3">бренд-фотосессия без студии: от идеи до готовой серии кадров</div>
{ph(0,700,1080,650,'лучшая работа ученика','01-a.jpg','50% 45%')}''')
# 2 формат
parts = ''.join(f'<div style="flex:{f};height:120px;background:#fff7e6;border:1px solid rgba(13,13,13,.15);padding:10px 12px"><span class="br" style="font-size:16px">[{i:02d}]</span></div>' for i, f in enumerate([3, 2, 4, 2, 3], start=1))
page(2, f'''{fit('Видеоуроки',908,200)}
{mrow('[формат]','короткие модули · своё расписание',340)}
    <div class="abs" style="left:86px;top:480px;width:840px;font-size:40px;line-height:1.38">Смотрите уроки в удобное время и идите в своём темпе. Каждый урок разбит на небольшие части, поэтому не нужно выделять на него целый день.</div>
    <div class="abs lbl br" style="left:86px;top:900px">[один урок = несколько небольших частей]</div>
    <div class="abs" style="left:86px;top:944px;width:908px;display:flex;gap:8px">{parts}</div>''')
# 3 кураторы
page(3, f'''    <div class="abs name" style="left:86px;top:190px;font-size:52px;white-space:nowrap">Кто ведёт курс</div>
{ph(0,300,538,640,'фото Алины','03-a.jpg','50% 25%')}
{ph(542,300,538,640,'фото Ани','03-b.jpg','50% 25%')}
    <div class="abs" style="left:86px;top:980px;width:420px"><div class="name" style="font-size:62px">Алина</div>
      <div class="lbl br" style="margin-top:16px">[куратор курса]</div>
      <div style="font-size:24px;line-height:1.4;margin-top:12px">креативный директор promptica<br>AI-креатор</div></div>
    <div class="abs" style="left:582px;top:980px;width:420px"><div class="name" style="font-size:62px">Аня</div>
      <div class="lbl br" style="margin-top:16px">[8 лет в дизайне]</div>
      <div style="font-size:24px;line-height:1.4;margin-top:12px">брендинг и визуал для соцсетей<br>ведущий креатор</div></div>''')
# 4 срок
items = ['разбор работ участников на курсе', 'сборка портфолио', 'проверка домашних заданий с комментариями', 'ответы кураторов на вопросы по ходу курса', 'закрытый чат участников']
rows = ''.join(f'<div class="row" style="padding:30px 0;font-size:34px">{cb}<span class="t">{t}</span></div>' for t in items)
page(4, f'''{fit('2 месяца',650,200)}
{mrow('[срок курса]','с обратной связью',340)}
    <div class="abs lbl br" style="left:86px;top:470px">[что входит]</div>
    <div class="abs" style="left:86px;top:510px;width:908px">{rows}</div>''')
# 5 модули
mods = [('01', 'Инструменты и основы', '', False),
        ('02', 'Идея и первые кадры', 'поиск своего стиля: от референса до готовой фотосессии', False),
        ('03', 'Исправляем недочёты', 'Убираем артефакты, «пластиковую» кожу и другое. Кадр выглядит как настоящая фотография.', False),
        ('04', 'Вся фотосессия целиком', 'Планируем съёмку по кадрам, меняем локации и образы, отбираем лучшее и собираем серию.', False),
        ('05', 'Как монетизировать навык и получать заказы', 'Упаковываем навык в услугу', True)]
mr = ''.join(f'<div class="row" style="padding:26px 0"><span class="n">[{n}]</span><span class="t" style="font-size:32px{";color:#930400" if red else ""}"><b style="font-weight:400">{t}</b>{f"<small style='font-size:22px;margin-top:8px'>{d}</small>" if d else ""}</span></div>' for n, t, d, red in mods)
page(5, f'''{fit('5 модулей',908,200)}
{mrow('[программа]','видеоуроки + домашние задания',340)}
    <div class="abs" style="left:86px;top:430px;width:908px">{mr}</div>''')
# 6 коммерческий модуль
pts = ['как упаковать фотосессию в услугу', 'пакеты и цены', 'портфолио, которое продаёт']
pr = ''.join(f'<div class="row" style="padding:26px 0;font-size:34px"><span class="n">[{i:02d}]</span><span class="t">{t}</span></div>' for i, t in enumerate(pts, start=1))
page(6, f'''{fit('Из навыка<br>в заказы',908,200)}
{mrow('[коммерческий модуль]','модуль 05',500)}
    <div class="abs" style="left:86px;top:600px;width:908px">{pr}</div>''')
# 7 что останется
page(7, f'''{fit('Гайды — навсегда',908,200)}
{mrow('[что останется с вами]','после курса',300)}
    <div class="abs" style="left:86px;top:420px;width:908px">
      <div class="row" style="padding:26px 0;font-size:32px"><span class="t">Забираете гайды и пользуетесь ими после курса.</span></div>
      <div class="row" style="padding:26px 0;font-size:32px"><span class="t">После каждого урока: домашнее задание.</span></div>
    </div>
    <div class="abs" style="left:86px;top:800px;width:908px;background:#fff7e6;padding:54px 54px 58px">
      <div class="lbl br">[бонус]</div>
      <div class="name" style="font-size:52px;line-height:1.08;margin-top:20px">Урок по оформлению дизайна постов и рилс</div>
    </div>''')
# 8 CTA
page(8, f'''{fit('Запись<br>на курс',908,240,'#fff7e6')}
{mrow('курс [нейросети с нуля]','2 месяца',560,'#fff7e6')}
    <div class="abs hair" style="left:86px;top:640px;width:908px;color:#fff7e6;opacity:.4"></div>
    <div class="abs" style="left:86px;top:690px;width:780px;font-size:32px;line-height:1.4;color:#fff7e6">[как записаться: слово в комментариях / ссылка в шапке профиля / анкета]</div>''', 'red', 'logo_cream.png', ' style="color:#fff7e6"')
print('слайдов:', TOTAL)
