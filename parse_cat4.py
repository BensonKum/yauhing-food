# -*- coding: utf-8 -*-
import json, re

def extract_products(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    result = data['data']['result']
    if isinstance(result, dict):
        text = result['data']['text']
    elif isinstance(result, list):
        # Find get text body command
        for item in result:
            if isinstance(item, dict) and item.get('command') == ['get', 'text', 'body']:
                r = item['result']
                text = r.get('data', r).get('text') if isinstance(r, dict) else r['text']
                break
        else:
            text = result[-1]['result']['data']['text']
    else:
        return []
    lines = text.split('\n')
    products = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if i + 1 < len(lines):
            nxt = lines[i+1].strip()
            if re.match(r'HKD\s*\d+', nxt, re.IGNORECASE):
                products.append({'name': line, 'price': nxt})
                i += 2
                continue
        i += 1
    return products

# Parse cat4 (素纖麵+蝦籽麵 combined)
cat4 = extract_products('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_cat4.txt')
print(f'cat4 products: {len(cat4)}')
for p in cat4:
    print(f'  {p["name"]}: {p["price"]}')

# Load existing
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_products.json', 'r', encoding='utf-8') as f:
    all_products = json.load(f)

# cat4 has combined categories, we already have 蝦籽麵 from cat3
# So we need to find products in cat4 that are NOT in existing list
existing_names = set(p['name'] for p in all_products)
new_products = []
for p in cat4:
    if p['name'] not in existing_names:
        p['category'] = '素纖麵'
        new_products.append(p)
        existing_names.add(p['name'])
    else:
        # Already exists, just mark category
        pass

print(f'\nNew from cat4: {len(new_products)}')
for p in new_products:
    print(f'  [NEW] {p["name"]}: {p["price"]}')

all_products.extend(new_products)

# Save
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)
print(f'\nTotal: {len(all_products)} products')
