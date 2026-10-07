// Экспорт слайдов в PNG 1080×1350.
//   npm run export              — все карусели из папки carousels/
//   npm run export -- <папка>   — только одна карусель, например: npm run export -- 01-trends
// Готовые картинки появляются в output/<имя-карусели>/

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.join(__dirname, '..');
const CAROUSELS = path.join(ROOT, 'carousels');
const OUTPUT = path.join(ROOT, 'output');
const WIDTH = 1080;
const HEIGHT = 1350;

function pickCarousels(names) {
  if (names.length) {
    for (const n of names) {
      if (!fs.existsSync(path.join(CAROUSELS, n))) {
        console.error(`✗ Нет такой папки: carousels/${n}`);
        process.exit(1);
      }
    }
    return names;
  }
  // По умолчанию — все папки, кроме служебных (начинаются с "_")
  return fs.readdirSync(CAROUSELS, { withFileTypes: true })
    .filter(d => d.isDirectory() && !d.name.startsWith('_'))
    .map(d => d.name)
    .sort();
}

(async () => {
  const carousels = pickCarousels(process.argv.slice(2));
  if (!carousels.length) {
    console.log('Пока нет каруселей в папке carousels/. Создайте папку со слайдами.');
    return;
  }

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1, // ровно 1080×1350 пикселей
  });

  let total = 0;
  for (const name of carousels) {
    const dir = path.join(CAROUSELS, name);
    const slides = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
    const outDir = path.join(OUTPUT, name);
    fs.rmSync(outDir, { recursive: true, force: true });
    fs.mkdirSync(outDir, { recursive: true });

    console.log(`\n▸ ${name} (${slides.length} слайдов)`);
    for (const file of slides) {
      await page.goto('file://' + path.join(dir, file), { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready); // ждём загрузку шрифтов
      const out = path.join(outDir, file.replace(/\.html$/, '.png'));
      await page.screenshot({ path: out, clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT } });
      console.log(`  ✓ output/${name}/${path.basename(out)}`);
      total++;
    }
  }

  await browser.close();
  console.log(`\nГотово: ${total} PNG (1080×1350) в папке output/`);
})().catch(err => {
  console.error(err);
  process.exit(1);
});
