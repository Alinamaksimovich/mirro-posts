// Графичные силуэты вещей — заглушки вместо фото для черновика (шаблон C «Хаос → порядок»).
// <i class="g" data-g="dress" data-c="#B9A8F0" style="left:..;top:..;width:..;--r:-8deg"></i>
const SHAPES = {
  tee:      'M30 12 L42 6 Q50 16 58 6 L70 12 L94 30 L83 45 L72 37 L72 114 L28 114 L28 37 L17 45 L6 30 Z',
  sweater:  'M30 12 L42 6 Q50 16 58 6 L70 12 L95 42 L92 104 L80 104 L74 50 L74 114 L26 114 L26 50 L20 104 L8 104 L5 42 Z',
  trousers: 'M26 6 L74 6 L80 116 L57 116 L50 42 L43 116 L20 116 Z',
  skirt:    'M30 22 L70 22 L86 104 L14 104 Z',
  dress:    'M37 4 L43 4 L50 14 L57 4 L63 4 L65 36 L86 116 L14 116 L35 36 Z',
  jacket:   'M31 8 L44 4 L50 34 L56 4 L69 8 L95 28 L91 104 L77 104 L75 46 L75 110 L25 110 L25 46 L23 104 L9 104 L5 28 Z',
  top:      'M35 14 L40 14 L42 34 L58 34 L60 14 L65 14 L69 44 L73 96 L27 96 L31 44 Z',
  bag:      'M18 48 L82 48 L88 112 L12 112 Z M34 48 Q34 16 50 16 Q66 16 66 48 L60 48 Q60 24 50 24 Q40 24 40 48 Z',
  shoe:     'M8 96 L8 64 L30 64 Q40 86 70 92 Q92 96 92 108 L8 108 Z',
  coat:     'M33 6 L44 4 L50 30 L56 4 L67 6 L90 24 L92 116 L76 116 L74 50 L74 118 L26 118 L26 50 L24 116 L8 116 L10 24 Z',
};
function renderGarment(el) {
  const fill = el.dataset.c || '#FAF8F6';
  const stroke = el.dataset.s || '#2C2C2A';
  const extra = el.dataset.g === 'jacket' || el.dataset.g === 'coat' ? `<path d="M50 34 L50 ${el.dataset.g === 'coat' ? 118 : 110}" stroke="${stroke}" stroke-width="2" fill="none"/>` : '';
  el.innerHTML = `<svg viewBox="0 0 100 120"><path d="${SHAPES[el.dataset.g]}" fill="${fill}" stroke="${stroke}" stroke-width="2.4" stroke-linejoin="round" fill-rule="evenodd"/>${extra}</svg>`;
}
// Куча вещей: <div class="pile" data-n="14" data-seed="3" data-tones="#555,#777" ...>
function pile(box) {
  let seed = +box.dataset.seed || 1;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const kinds = Object.keys(SHAPES), tones = box.dataset.tones.split(',');
  const W = box.clientWidth, H = box.clientHeight, n = +box.dataset.n, size = +(box.dataset.size || 200);
  for (let i = 0; i < n; i++) {
    const g = document.createElement('i'); g.className = 'g';
    g.dataset.g = kinds[Math.floor(rnd() * kinds.length)];
    g.dataset.c = tones[Math.floor(rnd() * tones.length)];
    g.dataset.s = box.dataset.stroke || '#2C2C2A';
    const w = size * (0.7 + rnd() * 0.6);
    g.style.cssText = `left:${rnd() * (W - w * .6) - w * .2}px; top:${rnd() * (H - w * .8) - w * .1}px; width:${w}px; --r:${(rnd() - .5) * 70}deg; opacity:${box.dataset.fade ? (0.25 + rnd() * 0.75).toFixed(2) : 1}`;
    box.appendChild(g);
  }
}
document.querySelectorAll('.pile').forEach(pile);
document.querySelectorAll('.g').forEach(renderGarment);
