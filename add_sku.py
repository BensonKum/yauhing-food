import json

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', encoding='utf-8') as f:
    products = json.load(f)

# Add SKU based on index position (YH001, YH002, ...)
for i, p in enumerate(products, 1):
    if 'sku' not in p:
        p['sku'] = f'YH{str(i).zfill(3)}'

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f'Added SKU to {len(products)} products')
