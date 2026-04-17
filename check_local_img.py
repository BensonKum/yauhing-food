import json

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', encoding='utf-8') as f:
    data = json.load(f)

print('Total products:', len(data))
print()
for i, p in enumerate(data):
    name = p.get('name', '')
    local_img = p.get('local_img', None)
    sku = p.get('sku', '')
    print(f'{i+1:2}. [{sku}] {name} -> {local_img}')
