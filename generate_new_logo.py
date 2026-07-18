"""
將新 logo（購物袋 + 心形）重畫成 PWA 圖標
- any 版：白底（用戶原設計）
- maskable 版：紅底填滿（Samsung 用呢個先唔會縮細）
"""
from PIL import Image, ImageDraw
import math, os

ICONS_DIR = r'C:\Users\user\.qclaw\workspace\yauhing-food\icons'
os.makedirs(ICONS_DIR, exist_ok=True)

WHITE = (255, 255, 255)
RED = (200, 70, 43)       # #C8462B 品牌紅
BAG_DARK = (51, 51, 51)   # #333333 深灰
CREAM = (250, 250, 248)

SIZES = [72, 96, 128, 144, 152, 192, 384, 512]


def heart_points(cx, cy, scale):
    """返回心形多邊形點（中心 cx,cy，scale 控制大小）"""
    pts = []
    for i in range(0, 630):
        t = i * 0.01
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * scale, cy - y * scale))
    return pts


def draw_logo(size, bg_color, bag_color, heart_color):
    img = Image.new('RGBA', (size, size), bg_color)
    d = ImageDraw.Draw(img)
    cx = size / 2

    # 購物袋本體（圓角矩形）
    bag_w = size * 0.46
    bag_h = size * 0.50
    bx0 = cx - bag_w / 2
    bx1 = cx + bag_w / 2
    by0 = size * 0.30
    by1 = by0 + bag_h
    radius = size * 0.06
    lw = max(2, int(size * 0.035))
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=radius, outline=bag_color, width=lw)

    # 提手（向上拱形）
    hw = bag_w * 0.55
    hh = bag_h * 0.42
    hx0 = cx - hw / 2
    hx1 = cx + hw / 2
    hy0 = by0 - hh
    hy1 = by0 + hh * 0.35
    d.arc([hx0, hy0, hx1, hy1], start=180, end=360, fill=bag_color, width=lw)

    # 心形（袋中央）
    heart_scale = bag_w * 0.018
    hcy = by0 + bag_h * 0.52
    d.polygon(heart_points(cx, hcy, heart_scale), fill=heart_color)

    return img


for s in SIZES:
    # any 版：白底
    any_img = draw_logo(s, WHITE, BAG_DARK, RED)
    any_path = os.path.join(ICONS_DIR, f'icon-{s}x{s}.png')
    any_img.save(any_path, 'PNG')

    # maskable 版：紅底填滿 + 內容縮到中間 60%（Samsung 安全區）
    full = draw_logo(s, RED, WHITE, WHITE)          # 紅底白袋白心，填滿整張
    small = full.resize((int(s * 0.62), int(s * 0.62)))
    canvas = Image.new('RGBA', (s, s), RED)         # 紅底填滿（Samsung 裁切後為實心紅圓）
    canvas.paste(small, (int(s * 0.19), int(s * 0.19)))
    canvas.save(os.path.join(ICONS_DIR, f'icon-maskable-{s}x{s}.png'), 'PNG')

    print(f'[OK] {s}x{s} (any + maskable)')

print('[Done]')
