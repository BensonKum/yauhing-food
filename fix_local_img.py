import json
import re

# Load products
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', encoding='utf-8') as f:
    products = json.load(f)

# Load index.html to get real mappings
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8-sig') as f:
    html = f.read()

# Extract p-card HTML blocks
# Pattern: <div class="p-card"...>...<img src="images/XXX.jpg"...>...</div>
pattern = r'<div class="p-card"[^>]*>.*?<img[^>]+src="images/([^"]+\.jpg)"[^>]*>.*?</div>'
raw_matches = re.findall(pattern, html, re.DOTALL)
print(f'Real index.html images found: {len(raw_matches)}')

# Build map of HTML order -> image filename
html_img_map = {}
for i, img in enumerate(raw_matches):
    html_img_map[i + 1] = img

# Compare with products.json local_img
print('\n=== MISMATCH CHECK ===')
problems = []
for i, p in enumerate(products):
    idx = i + 1
    expected_img = p.get('local_img', None)
    actual_img = html_img_map.get(idx, None)
    
    if expected_img != actual_img:
        # Check if actual file exists
        import os
        img_path = os.path.join(r'C:\Users\admin\.qclaw\workspace\yauhing-food\images', actual_img or '')
        file_exists = os.path.exists(img_path) if actual_img else False
        problems.append({
            'idx': idx,
            'name': p['name'],
            'current_local_img': expected_img,
            'correct_img': actual_img,
            'file_exists': file_exists
        })

print(f'\nTotal problems: {len(problems)}')
for prob in problems:
    status = 'EXISTS' if prob['file_exists'] else 'MISSING'
    print(f"  [{prob['idx']:2}] {prob['name']}")
    print(f"       current: {prob['current_local_img']}")
    print(f"       correct: {prob['correct_img']} [{status}]")

# Fix products.json
for prob in problems:
    idx = prob['idx'] - 1
    if prob['file_exists']:
        products[idx]['local_img'] = prob['correct_img']
    else:
        products[idx]['local_img'] = None

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f'\nFixed {len([p for p in problems if p['file_exists']])} local_img entries')
print(f'Set {len([p for p in problems if not p['file_exists']])} to null (image file missing)')
