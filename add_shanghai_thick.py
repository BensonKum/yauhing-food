# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('products.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# 新增：上海麵(粗)盒裝
new_product = {
    "cat": "新鮮粉麵",
    "name": "上海麵(粗)盒裝",
    "price": "HKD 10",
    "note": "",
    "stock": True,
    "image": None,
    "local_img": "product_shanghai_thick_noodle.jpg",
    "sku": None
}

data.append(new_product)

with open('products.json', 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Done! Total products: {len(data)}')
print('Added: 上海麵(粗)盒裝 (local_img placeholder: product_shanghai_thick_noodle.jpg)')
print('Waiting for Ben to provide actual product photo...')
