# Заготовка проекта

1. `npm install` и `npx playwright install chromium` (нужен Node.js; для видео — ffmpeg; для вырезки — `python3 -m pip install pillow`).
2. Положи в папку `carousels/<тема>/` слайды `01.html…` и фото в `img/`. Образцы — в `carousels/_ref-*/` (без фото, только вёрстка).
3. Экспорт: `npm run export -- <тема>` → `output/<тема>/`.
4. Подробности — в скиллах `slides-export-pipeline`, `mirro-carousels`, `promptica-carousels` и в `PLAYBOOK.md`.
