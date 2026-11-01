# Пакет: скиллы + ключевые моменты + рабочая заготовка

Берёшь эту папку в новый аккаунт — Claude работает в той же системе: те же бренды MIRRO и promptica, те же шаблоны, те же правила и экспорт в PNG/MP4.

## Что внутри
| Что | Где | Зачем |
|---|---|---|
| **Ключевые моменты** | `PLAYBOOK.md` | договорённости, бренды, что нравится/нет, ловушки, чек-лист |
| Текст для «Preferences» | `PREFERENCES.txt` | вставить в настройки профиля нового аккаунта |
| **Скиллы** | `skills/` | `mirro-carousels`, `promptica-carousels`, `slides-export-pipeline`, `design-taste`, `instagram-posts-premium` |
| Скиллы по одному (для claude.ai) | `zips/*.zip` | загрузка через Settings → Skills |
| **Рабочая заготовка** | `starter-project/` | скрипты экспорта/видео/вырезки, `brand.css`, шрифты, логотипы, эталонные макеты `_ref-*` |
| Установщик | `install.sh` | ставит всё одной командой |
| Сторонние скиллы | `third-party-skills.md` | необязательно; Impeccable, Emil Kowalski, Hyperframes, brag, playwright-cli |

`design-taste` и `instagram-posts-premium` — это **ваши** скиллы из прежнего аккаунта: в новом их нет, поэтому они в пакете. В копиях уже внесены: актуальная айдентика promptica (чёрный/белый/#930400/кремовый вместо #B1202D) и заполненный «Анти-вкус» (что вам не нравится).

## Установка в Claude Code (рекомендуется — только там работает экспорт PNG/MP4)
**Командой (Терминал):**
```
cd skills-pack
./install.sh --project ~/studio            # скиллы + рабочая заготовка в папку ~/studio
./install.sh                                # или только скиллы, для всех проектов (~/.claude/skills)
./install.sh --with-third-party             # + необязательные сторонние скиллы
```
Дальше в папке проекта: `npx playwright install chromium` (если нет Chromium), для видео нужен `ffmpeg`, для вырезки — `python3 -m pip install pillow`. Нужен Node.js (nodejs.org, кнопка LTS).

**Без Терминала:** скопируй папки из `skills/` в `~/.claude/skills/` (или в `<проект>/.claude/skills/`), а содержимое `starter-project/` — в папку проекта.

Затем открой Claude Code в папке проекта — скиллы подхватятся сами (после перезапуска). Файл `CLAUDE.md` из заготовки подскажет правила.

## Установка в claude.ai (чат)
1. Settings → Capabilities → Skills → Upload skill → по очереди загрузи 5 файлов из `zips/`.
2. Settings → Profile → Preferences → вставь `PREFERENCES.txt`.
3. Скиллы дадут стиль, тексты и структуру. PNG/MP4 Claude соберёт сам, только если в аккаунте включено выполнение кода и доступны Node, Playwright и ffmpeg; иначе экспорт делай в Claude Code.

## Проверка, что всё переехало
Напиши в новой сессии: «Сделай сторис для MIRRO: вопрос "Как добавить одежду?"». Должно быть: русский язык; Claude называет `mirro-carousels`/`design-taste`; цвета лайм/лаванда/крем/тёмный; CTA «ссылка в шапке профиля» + @Mirro_wardrobe_bot; сначала концепция или черновик.
Для promptica: «Сделай слайд 02 "Слишком AI"» → только цвета #0D0D0D / #FFF / #930400 / #fff7e6, колонтитул, зерно, пара «✕ не ок / ✓ ок».

## Что НЕ входит
Фото, стикеры, исходные видео и готовые PNG/MP4 — они в репозитории `alinamaksimovich/mirro-posts` (ветка `claude/amazing-pascal-uuv6c7`: `carousels/*/img`, `assets/sticker-*.png`, `output/`). Эталоны `_ref-*` без фото — только вёрстка.

## Важно
В `starter-project/assets/fonts/` лежат шрифты Helvetica Neue и Helios (коммерческие, ваши файлы) и Vela Sans / Old Soviet (с лицензиями рядом). Не публикуй пакет и репозиторий открыто.
