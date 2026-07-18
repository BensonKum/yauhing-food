"""
還原 PWA icon 做舊版「I Love 麵子」logo
- any 版：直接縮放原 logo.png（用於一般 launcher / browser）
- maskable 版：加 18% 安全區 padding（防止 Samsung 圓形 mask 切到內容）
"""
from PIL import Image
import os

ICONS_DIR = r'C:\Users\user\.qclaw\workspace\yauhing-food\icons'
LOGO_PATH = os.path.join(ICONS_DIR, 'logo.png')

SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

logo = Image.open(LOGO_PATH).convert('RGBA')
print(f'原 logo 尺寸：{logo.size}  模式：{logo.mode}')

# 統計原 logo 白色邊框比例（用嚟決定 maskable padding 比例）
# 原 logo 嘅 I ❤ 麵子 內容大約佔 75% 中心區，留返 12% 邊距
# 為咗 Samsung maskable 安全，我哋額外加 padding 確保 safe zone

for s in SIZES:
    # any 版：直接縮放原圖
    any_img = logo.resize((s, s), Image.LANCZOS)
    any_img.save(os.path.join(ICONS_DIR, f'icon-{s}x{s}.png'), 'PNG')

    # maskable 版：縮到 64% 大小 + 白底 canvas
    inner = int(s * 0.64)
    small = logo.resize((inner, inner), Image.LANCZOS)
    canvas = Image.new('RGBA', (s, s), (255, 255, 255, 255))
    offset = (s - inner) // 2
    canvas.paste(small, (offset, offset), small)
    canvas.save(os.path.join(ICONS_DIR, f'icon-maskable-{s}x{s}.png'), 'PNG')

    print(f'[OK] {s}x{s}  (any + maskable)')

print('\n[Done] 16 個 icon 已用「I Love 麵子」logo 重新生成')
