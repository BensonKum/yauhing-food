import json

with open('products.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data:
    print(p.get('sku'), p.get('name'), p.get('image'))

print("---")
for p in data:
    if '上海' in p.get('name', ''):
        p['image'] = 'images/product_31.jpg'
        p['local_img'] = 'product_31.jpg'
        print(f'Updated: {p["sku"]} - {p["name"]}')

with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved.')