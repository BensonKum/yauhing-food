import re
import json

# Read files
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8-sig') as f:
    html = f.read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', encoding='utf-8') as f:
    products = json.load(f)

# Extract img src + alt from index.html
# Pattern: <img src="images/XXX.jpg" alt="產品名"
img_pattern = r'<img src="images/([^"]+\.jpg)" alt="([^"]+)"'
matches = re.findall(img_pattern, html)
print(f'Found {len(matches)} img tags with alt in index.html')

# Build alt -> img map
alt_to_img = {}
for img, alt in matches:
    alt_to_img[alt] = img

print(f'\nAlt to img mappings: {len(alt_to_img)}')

# Match products by alt text (exact match first)
fixed_count = 0
null_count = 0
for i, p in enumerate(products):
    alt_key = p['name']
    if alt_key in alt_to_img:
        products[i]['local_img'] = alt_to_img[alt_key]
        fixed_count += 1
    else:
        # Try to find partial match
        found = False
        for alt, img in alt_to_img.items():
            if p['name'] in alt or alt in p['name']:
                products[i]['local_img'] = img
                fixed_count += 1
                found = True
                break
        if not found:
            products[i]['local_img'] = None
            null_count += 1

print(f'\nFixed (matched by alt): {fixed_count}')
print(f'Set to null (no match): {null_count}')

# Save
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print('\nDone!')
