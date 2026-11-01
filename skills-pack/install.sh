#!/usr/bin/env bash
# Установка пакета скиллов и рабочей заготовки.
# Запуск из папки skills-pack:
#   ./install.sh                         скиллы → ~/.claude/skills (работают во всех проектах Claude Code)
#   ./install.sh --project ~/studio      + рабочая заготовка в папку проекта; скиллы кладутся в <проект>/.claude/skills
#   ./install.sh --with-third-party      + сторонние скиллы из GitHub (необязательно, см. third-party-skills.md)
# Переменная SKILLS_DEST переопределяет папку скиллов (для проверки установки).
set -euo pipefail
export GIT_LFS_SKIP_SMUDGE=1   # не тянуть большие LFS-файлы чужих репозиториев

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT=""
THIRD=0
while [ $# -gt 0 ]; do
  case "$1" in
    --project) PROJECT="${2:?укажите папку проекта}"; shift 2 ;;
    --with-third-party) THIRD=1; shift ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "Неизвестный параметр: $1"; exit 1 ;;
  esac
done

if [ -n "${SKILLS_DEST:-}" ]; then DEST="$SKILLS_DEST"
elif [ -n "$PROJECT" ]; then DEST="$PROJECT/.claude/skills"
else DEST="${CLAUDE_HOME:-$HOME/.claude}/skills"; fi
mkdir -p "$DEST"

echo "▸ Скиллы → $DEST"
for d in "$HERE"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "$DEST/$name"
  cp -r "$d" "$DEST/$name"
  echo "  ✓ $name"
done

if [ -n "$PROJECT" ]; then
  echo "▸ Рабочая заготовка → $PROJECT"
  mkdir -p "$PROJECT"
  # копируем только отсутствующие файлы — уже существующие файлы проекта не перезаписываются
  (cd "$HERE/starter-project" && find . -type f | while IFS= read -r f; do
    if [ ! -e "$PROJECT/$f" ]; then mkdir -p "$PROJECT/$(dirname "$f")"; cp "$f" "$PROJECT/$f"; fi
  done)
  if command -v npm >/dev/null 2>&1; then
    (cd "$PROJECT" && npm install --no-audit --no-fund >/dev/null 2>&1 && echo "  ✓ npm install (playwright)") || echo "  ! npm install не удался — выполните вручную в $PROJECT"
  else
    echo "  ! Не найден npm — установите Node.js (nodejs.org, кнопка LTS) и выполните в $PROJECT: npm install"
  fi
  echo "  Далее: npx playwright install chromium   (если Chromium ещё нет), нужен ffmpeg для видео и python3 + pillow для вырезки"
fi

if [ "$THIRD" = 1 ]; then
  echo "▸ Сторонние скиллы (GitHub)"
  T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
  clone_at() { # url sha dir
    git clone -q --depth 1 "$1" "$3"
    ( cd "$3" && git fetch -q --depth 1 origin "$2" 2>/dev/null && git checkout -q FETCH_HEAD ) || echo "  (для $1 взят последний коммит)"
  }
  clone_at https://github.com/pbakaus/impeccable d631a8827f99414d2b6daba4ef08b7f8701751d7 "$T/imp"
  rm -rf "$DEST/impeccable"; cp -r "$T/imp/.claude/skills/impeccable" "$DEST/impeccable"; echo "  ✓ impeccable"
  clone_at https://github.com/emilkowalski/skills e8a175de22ae1e49370fc144c1f3bb9aeedf988d "$T/emil"
  for d in "$T"/emil/skills/*/; do rm -rf "$DEST/$(basename "$d")"; cp -r "$d" "$DEST/$(basename "$d")"; done; echo "  ✓ emilkowalski/skills"
  clone_at https://github.com/latent-spaces/brag 8531ccb9f471ef5099abf930079e47b55c55bb21 "$T/brag"
  for n in brag brag-slim; do rm -rf "$DEST/$n"; cp -r "$T/brag/skills/$n" "$DEST/$n"; done; echo "  ✓ brag, brag-slim"
  clone_at https://github.com/heygen-com/hyperframes 6f3f86a9c9824c8ad5b7bf760375e243466e5ee0 "$T/hf"
  for d in "$T"/hf/skills/*/; do [ -f "$d/SKILL.md" ] && { rm -rf "$DEST/$(basename "$d")"; cp -r "$d" "$DEST/$(basename "$d")"; }; done; echo "  ✓ hyperframes (скиллы)"
  git clone -q --depth 1 --filter=blob:none --no-checkout https://github.com/microsoft/playwright "$T/pw"
  git -C "$T/pw" checkout -q HEAD -- packages/playwright-core/src/tools/skills/playwright-cli
  rm -rf "$DEST/playwright-cli"; cp -r "$T/pw/packages/playwright-core/src/tools/skills/playwright-cli" "$DEST/playwright-cli"; echo "  ✓ playwright-cli"
fi

echo "Готово. Перезапустите Claude Code (или начните новую сессию), чтобы скиллы подхватились."
