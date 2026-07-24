from PIL import Image, ImageDraw, ImageFont
import os, sys

script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

files = [
    'product_cabbage_dumpling.jpg',
    'product_corn_dumpling.jpg',
]

for name in files:
    src = os.path.join(images_dir, name)
    if not os.path.exists(src):
        print(f'SKIP (not found): {name}')
        continue
    img = Image.open(src).convert('RGBA')
    w, h = img.size
    sz = int(min(w, h) * 0.25)
    sticker = Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(sticker)
    # white border circle
    d.ellipse([0, 0, sz-1, sz-1], fill=(255, 255, 255, 255))
    # red fill
    inset = max(3, sz // 18)
    d.ellipse([inset, inset, sz-1-inset, sz-1-inset], fill=(220, 30, 30, 255))
    # font
    try:
        font = ImageFont.truetype(os.path.join(os.environ['WINDIR'], 'Fonts', 'msyh.ttc'), int(sz * 0.38))
    except:
        font = ImageFont.load_default()
    text = '待售'
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (sz - tw) // 2 - bbox[0]
    ty = (sz - th) // 2 - bbox[1]
    d.text((tx, ty), text, fill=(255, 255, 255, 255), font=font)
    # center
    pos = ((w - sz) // 2, (h - sz) // 2)
    img.paste(sticker, pos, sticker)
    out = img.convert('RGB')
    out.save(src, 'JPEG', quality=92)
    print(f'OK: {name} ({w}x{h})')
print('Done.')
