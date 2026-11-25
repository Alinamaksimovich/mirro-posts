// HTML → PDF (A4) через Chromium. Использование: node scripts/render-pdf.js <файл.html> <выход.pdf>
const path = require('path');
const { chromium } = require('playwright');
const [src, out] = process.argv.slice(2);
if (!src || !out) { console.error('Использование: node scripts/render-pdf.js файл.html выход.pdf'); process.exit(1); }
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('✓ ' + out);
})().catch(e => { console.error(e); process.exit(1); });
