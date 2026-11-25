# Карусель отзывов учеников (promptica), 1080×1440 (3:4)

Слайды собираются из `cases.json`: `python3 build.py && npm run export -- promptica-reviews-carousel` (из корня проекта).

Каждый кейс — запись в `cases.json`:
- `layout`: `chat` — 2 фото + заголовок + скрин переписки; `photo` — 1–2 фото + заголовок + текст отзыва (`quote`); `quote` — чистый отзыв (`quote`, `name`, `note`).
- `title`, `name`, `note` — заголовок кейса, ученик, короткая пометка («пришла, ранее не работая с ИИ»).
- `photos`: `[{"file": "имя.jpg", "pos": "50% 40%"}]` — файлы в `img/`; `chat` — скрин переписки (лишнюю строку ввода сообщения обрезать).
Обложка — `img/01-a.jpg`. Последний слайд (призыв) и номера «NN / TT» создаются сами.
Пометки (`note`) писать только по фактам: из отзыва или со слов автора курса.

## Видео-кейс (layout `video`)
Видео ученика (9:16) → кадры: `ffmpeg -i видео.mp4 -vf scale=432:768 -q:v 3 img/04-frames/f%04d.jpg`, постер для PNG — отдельный кадр `img/04-poster.jpg`. В `cases.json`: `"video": {"poster", "frames", "count", "fps"}`, `"stats"` (крупные цифры из отзыва — только факты из самого отзыва), `"chat"`.
Сборка слайда-видео: `node scripts/render-video.js carousels/promptica-reviews-carousel/04.html output/promptica-reviews-carousel/04-video-silent.mp4 <сек> <fps>`, звук из исходника добавить `ffmpeg -i silent.mp4 -i исходник.mp4 -map 0:v -map 1:a -c:v copy -c:a aac -shortest 04-video.mp4`. Кадры и исходное видео не хранятся в git (`.gitignore`).
