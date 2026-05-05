import re

html_raw = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# Count product cards by looking for .p-card class
cards = re.findall(rb'<div class="p-card"', html_raw)
print(f'Total p-card divs in index.html: {len(cards)}')

# Count img tags with src containing images/
imgs = re.findall(rb'src="images/[^"]+"', html_raw)
print(f'Product images (images/*): {len(imgs)}')

# Find all data-cat values in card sections (after byte 30000)
card_area = html_raw[30000:]
cats_in_cards = re.findall(rb'data-cat="([^"]+)"', card_area)
print(f'data-cat in card area: {len(cats_in_cards)}')

# Check what hex the cards use for 新鲜麵
simplified = '新鲜麵'.encode('utf-8')
print(f'\nSimplified 新鲜麵 (hex={simplified.hex()}) in card area: {cats_in_cards.count(simplified)}')

# Try different encodings
for enc in ['utf-8', 'big5', 'gbk']:
    try:
        c = '新鮮麵'.encode(enc)
        print(f'  Traditional 新鮮麵 ({enc}): hex={c.hex()}, count={cats_in_cards.count(c)}')
    except Exception as e:
        print(f'  Error: {e}')

# Find ALL distinct category strings used in card data-cat
unique_cats_in_cards = set(cats_in_cards)
print(f'\nUnique categories in card area: {len(unique_cats_in_cards)}')
for c in sorted(unique_cats_in_cards, key=lambda x: x.hex()):
    try:
        label = c.decode('utf-8')
    except:
        label = c.hex()
    count = cats_in_cards.count(c)
    print(f'  {label!r} (hex={c.hex()}) -> {count} cards')

# Also check the render function to see how cat is used
script = html_raw.decode('utf-8', errors='replace')
idx = script.find('currentCat')
if idx > 0:
    print(f'\n--- currentCat in script at {idx} ---')
    print(script[idx:idx+500])