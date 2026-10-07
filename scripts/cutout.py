"""Вырезает вещь со светлого однотонного фона: python3 scripts/cutout.py вход.jpg выход.png"""
import sys, collections
from PIL import Image, ImageFilter

def cutout(src, dst, tol=26):
    im = Image.open(src).convert('RGB'); W, H = im.size; px = im.load()
    corners = [px[2, 2], px[W - 3, 2], px[2, H - 3], px[W - 3, H - 3]]
    bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))
    def is_bg(p): return max(abs(p[i] - bg[i]) for i in range(3)) < tol and max(p) - min(p) < 30
    mask = Image.new('L', (W, H), 255); m = mask.load(); seen = bytearray(W * H)
    q = collections.deque([(x, 0) for x in range(W)] + [(x, H - 1) for x in range(W)] + [(0, y) for y in range(H)] + [(W - 1, y) for y in range(H)])
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= W or y >= H or seen[y * W + x]: continue
        seen[y * W + x] = 1
        if not is_bg(px[x, y]): continue
        m[x, y] = 0
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    # замкнутые участки фона (например, внутри ручки сумки) — тоже убираем, если они крупные
    for y0 in range(0, H, 3):
        for x0 in range(0, W, 3):
            if seen[y0 * W + x0] or not is_bg(px[x0, y0]): continue
            comp = []; q = collections.deque([(x0, y0)])
            while q:
                x, y = q.popleft()
                if x < 0 or y < 0 or x >= W or y >= H or seen[y * W + x]: continue
                seen[y * W + x] = 1
                if not is_bg(px[x, y]): continue
                comp.append((x, y)); q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
            if len(comp) > W * H * 0.004:
                for x, y in comp: m[x, y] = 0
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
    im.putalpha(mask); im.crop(mask.getbbox()).save(dst)

if __name__ == '__main__':
    cutout(sys.argv[1], sys.argv[2])
