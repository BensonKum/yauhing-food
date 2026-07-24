import json

with open('products_v2.json', 'r', encoding='utf-8-sig') as f:
    products = json.load(f)

print(f'總產品數: {len(products)}')

skus = ['YH501', 'YH501A', 'YH502', 'YH502A']
found = [p for p in products if p.get('sku') in skus]

print(f'\nYH501/YH501A/YH502/YH502A 是否存在: {len(found)} 項')

if found:
    for p in found:
        print(f"  {p['sku']}: {p['name']}")
else:
    print('  ✅ 已全部刪除')
