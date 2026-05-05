import re, json

html = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
products = json.load(open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json','r',encoding='utf-8-sig'))
pickup = [p for p in products if p.get('pickup_only')]

# How many cards per category (by hex)?
simplified_cat = bytes.fromhex('e696b0e9b29ce9bab5')  # simplified 新鲜麵
card_area = html[30000:]
cats_in_cards = re.findall(rb'data-cat="([^"]+)"', card_area)
print(f'Cards in 新鲜麵 category: {cats_in_cards.count(simplified_cat)}')

# Total cards: 50
print(f'Total cards: 50')

# 12 products missing from HTML
print(f'\n=== ROOT CAUSE: 12 pickup products NOT in HTML at all ===')
print(f'These products exist in products.json but have NO hard-coded HTML card:')

# Find which ones ARE in HTML by name
in_html = []
out_html = []
for p in pickup:
    name_utf8 = p['name'].encode('utf-8')
    if name_utf8 in html:
        in_html.append(p)
    else:
        out_html.append(p)

print(f'\nIN HTML (5 products with cards):')
for p in in_html:
    print(f'  {p["name"]}')

print(f'\nOUT HTML (12 products MISSING cards):')
for p in out_html:
    print(f'  {p["name"]}')

# Check: how many products are in products.json total?
print(f'\nproducts.json total products: {len(products)}')
print(f'HTML total cards: 50')
print(f'Missing from HTML: {len(products) - 50} products')

# The issue is: HTML has HARD-CODED cards, only 50 cards exist
# We need to add cards for the 12 missing pickup_only products
print(f'\nSOLUTION: Add HTML cards for the 12 missing pickup_only products')
print(f'Plus: Fix products.json cat from 新鮮麵(traditional) to 新鲜麵(simplified) to match HTML')