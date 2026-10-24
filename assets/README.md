# assets/ — материалы для карусели promptica «AI SMM-система»

- `fonts/` — Vela Sans (текст), Old Soviet (заголовки, «печатная машинка»). Лицензии рядом. Pangolin берётся из Google Fonts.
- `logo_black.png` — на светлом фоне; `logo_cream.png` (#fff7e6) — на красном и чёрном. Сделаны из логотипов promptica.
- `sticker-02.png` … `sticker-07.png` — стикеры-вырезки (номер = слайд), фон убран `scripts/cutout.py`.

Сборка: `npm run export -- promptica-ai-smm` (PNG) и
`node scripts/render-video.js carousels/promptica-ai-smm/01.html output/promptica-ai-smm/01.mp4 6 30` (слайд 1 в MP4).
