# Сторонние скиллы (необязательно)

Для самих каруселей не нужны — мы их в работе не вызывали. Установились по просьбе, ставятся `install.sh --with-third-party`.

| Скилл | Источник | Коммит на момент установки | Зачем |
|---|---|---|---|
| `impeccable` | github.com/pbakaus/impeccable (`.claude/skills/impeccable`) | d631a88 | дизайн-критика, полировка, типографика |
| `emil-design-eng`, `apple-design`, `animate`, `animation-vocabulary`, `review-animations`, `improve-animations`, `find-animation-opportunities`, `break-ui`, `prototype`, `pick-ui-library`, `mobile-native`, `ask-sonner`, `animate-expo`, `write-swift` | github.com/emilkowalski/skills (`skills/*`) | e8a175d | вкус UI, анимации |
| `playwright-cli` | github.com/microsoft/playwright (`packages/playwright-core/src/tools/skills/playwright-cli`) | d9f2fd3 | управление браузером |
| `brag`, `brag-slim` | github.com/latent-spaces/brag (`skills/brag`, `skills/brag-slim`) | 8531ccb | промо-видео проекта (≈16 МБ из-за музыки) |
| `hyperframes*`, `slideshow`, `motion-graphics`, `product-launch-video`, … (21 скилл) | github.com/heygen-com/hyperframes (`skills/*`) | 6f3f86a | видео из HTML |

Движок Hyperframes: `npm i -D hyperframes@0.8.144`. Перед установкой чужих скиллов просматривай их `SKILL.md` — это инструкции для Claude.
