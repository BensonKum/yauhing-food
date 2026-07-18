"""
為 Samsung 手機生成 maskable 圖標
關鍵：內容縮到中間 60%，周圍留 20% 安全邊距
Samsung 會把整個 512x512 切成圓形，內容只在中間才會被保留
"""
from PIL import Image, ImageDraw
import os

icons_dir = r'C:\Users\user\.qclaw\workspace\yauhing-food\icons'
os.makedirs(icons_dir, exist_ok=True)

# 品牌顏色
BG_RED = (200, 70, 43)      # #C8462B 品牌紅
WHITE = (255, 255, 255)
CREAM = (250, 250, 248)     # #FAFAF8 米白

sizes = [72, 96, 128, 144, 152, 192, 384, 512]

for size in sizes:
    # 完全填滿品牌紅（Samsung 切圓角時會保留所有紅色）
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, size, size], fill=BG_RED)
    
    # 安全區域計算
    # Samsung 圓形遮罩會保留中間約 80-90%
    # 內容做喺中間 65%，周圍留 17.5% 邊距
    safe_size = size * 0.65
    margin = (size - safe_size) / 2
    center = size / 2
    
    # ===== 繪製「祐」字風格圖標 =====
    # 1) 外圈白色圓環
    outer_r = safe_size * 0.48
    line_w = max(2, int(size * 0.06))
    draw.ellipse(
        [center - outer_r, center - outer_r, center + outer_r, center + outer_r],
        outline=WHITE, width=line_w
    )
    
    # 2) 內圈白色實心圓
    inner_r = safe_size * 0.32
    draw.ellipse(
        [center - inner_r, center - inner_r, center + inner_r, center + inner_r],
        fill=WHITE
    )
    
    # 3) 中心品牌紅圓點
    dot_r = safe_size * 0.14
    draw.ellipse(
        [center - dot_r, center - dot_r, center + dot_r, center + dot_r],
        fill=BG_RED
    )
    
    # 4) 底部白色橫線（代表麵條/麵線）
    line_y_start = center + inner_r * 0.55
    line_y_end = center + outer_r * 0.85
    line_x_left = center - outer_r * 0.75
    line_x_right = center + outer_r * 0.75
    line_w_thin = max(2, int(size * 0.035))
    draw.line(
        [(line_x_left, line_y_start), (line_x_right, line_y_start)],
        fill=WHITE, width=line_w_thin
    )
    draw.line(
        [(line_x_left, line_y_end), (line_x_right, line_y_end)],
        fill=WHITE, width=line_w_thin
    )
    
    # 保存為 maskable 版本
    out_path = os.path.join(icons_dir, f'icon-maskable-{size}x{size}.png')
    img.save(out_path, 'PNG')
    print(f'[OK] {out_path}')

print('\n[Done] maskable icons generated')
