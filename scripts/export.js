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
    const outDir = path.join(OUTPUT, name);
    fs.rmSync(outDir, { recursive: true, force: true });
    fs.mkdirSync(outDir, { recursive: true });

    // Панорама: один файл panorama.html шириной N×1080 режется на N слайдов
    const pano = path.join(dir, 'panorama.html');
    if (fs.existsSync(pano)) {
      const count = Number((fs.readFileSync(pano, 'utf8').match(/data-slides="(\d+)"/) || [])[1] || 5);
      const panoPage = await browser.newPage({ viewport: { width: WIDTH * count, height: HEIGHT }, deviceScaleFactor: 1 });
      await panoPage.goto('file://' + pano, { waitUntil: 'networkidle' });
      await panoPage.evaluate(() => document.fonts.ready);
      await panoPage.waitForTimeout(500); // даём дорисоваться маркерным линиям
      console.log(`\n▸ ${name} (панорама, ${count} слайдов)`);
      for (let i = 0; i < count; i++) {
        const out = path.join(outDir, String(i + 1).padStart(2, '0') + '.png');
        await panoPage.screenshot({ path: out, clip: { x: i * WIDTH, y: 0, width: WIDTH, height: HEIGHT } });
        console.log(`  ✓ output/${name}/${path.basename(out)}`);
        total++;
      }
      await panoPage.screenshot({ path: path.join(outDir, 'panorama-preview.png') });
      await panoPage.close();
      continue;
    }

    const slides = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();

    console.log(`\n▸ ${name} (${slides.length} слайдов)`);
    for (const file of slides) {
      // размер по умолчанию 1080×1350; для сторис в разметке: data-size="1080x1920"
      const m = fs.readFileSync(path.join(dir, file), 'utf8').match(/data-size="(\d+)x(\d+)"/);
      const w = m ? +m[1] : WIDTH, h = m ? +m[2] : HEIGHT;
      await page.setViewportSize({ width: w, height: h });
      await page.goto('file://' + path.join(dir, file), { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready); // ждём загрузку шрифтов
      const out = path.join(outDir, file.replace(/\.html$/, '.png'));
      await page.screenshot({ path: out, clip: { x: 0, y: 0, width: w, height: h } });
      console.log(`  ✓ output/${name}/${path.basename(out)}  (${w}×${h})`);
      total++;
    }
  }

  await browser.close();
  console.log(`\nГотово: ${total} PNG в папке output/`);
})().catch(err => {
  console.error(err);
  process.exit(1);
});
