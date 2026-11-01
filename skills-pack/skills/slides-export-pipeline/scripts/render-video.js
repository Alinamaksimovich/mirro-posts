// Рендер анимированного слайда в MP4 (H.264, 30 fps).
//   node scripts/render-video.js <слайд.html> <выход.mp4> [длительность_с=6] [fps=30]
// Слайд должен определять window.setT(секунды, номер_кадра) — он рисует кадр для момента t.

const path = require('path');
const { spawn } = require('child_process');
const { chromium } = require('playwright');

const [srcArg, out, dur = '6', fps = '30'] = process.argv.slice(2);
const [src, query = ''] = (srcArg || '').split('?'); // слайд.html?set=bad — параметры страницы
if (!src || !out) { console.error('Использование: node scripts/render-video.js слайд.html выход.mp4 [сек] [fps]'); process.exit(1); }

(async () => {
  const html = require('fs').readFileSync(src, 'utf8');
  const m = html.match(/data-size="(\d+)x(\d+)"/);
  const W = m ? +m[1] : 1080, H = m ? +m[2] : 1350;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(src) + (query ? '?' + query : ''), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', fps, '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '16', '-preset', 'slow', '-movflags', '+faststart', out]);
  ff.stderr.pipe(process.stderr);

  const total = Math.round(+dur * +fps);
  for (let i = 0; i < total; i++) {
    await page.evaluate(([t, f]) => window.setT(t, f), [i / +fps, i]);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log(`✓ ${out} (${W}×${H}, ${dur} с, ${fps} fps, ${total} кадров)`);
})().catch(e => { console.error(e); process.exit(1); });
