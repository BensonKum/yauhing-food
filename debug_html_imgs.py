import re
import json

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8-sig') as f:
    html = f.read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', encoding='utf-8') as f:
    products = json.load(f)

# Extract img src + alt
matches = re.findall(r'<img src="images/([^"]+\.jpg)" alt="([^"]+)"', html)
print(f'Total img tags with alt: {len(matches)}')

# Print all matches
print('\nHTML Image -> Alt mappings:')
for i, (img, alt) in enumerate(matches):
    print(f'{i+1:2}. {img[:45]:45} | alt: {alt}')

print(f'\n\nProducts local_img status:')
null_count = sum(1 for p in products if not p.get('local_img'))
print(f'  null: {null_count}')
print(f'  has img: {len(products) - null_count}')
