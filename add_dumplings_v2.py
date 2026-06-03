import json
import re

# 讀取 products.json
with open('products.json', 'r', encoding='utf-8-sig') as f:
    products = json.load(f)

print('当前产品数量:', len(products))

# 搵最後一個 YH SKU 編號
max_num = 0
for p in products:
    sku = p.get('sku', '')
    if sku and sku.startswith('YH'):
        try:
            num = int(sku[2:])
            if num > max_num:
                max_num = num
        except:
            pass

print('最後 SKU 編號: YH' + str(max_num).zfill(3))

# 新增餃子系列產品
new_products = [
    {
        "cat": "餃子系列",
        "name": "白菜餃",
        "price": "HKD 25",
        "note": "",
        "stock": True,
        "image": None,
        "local_img": "product_cabbage_dumpling.jpg",  # placeholder
        "sku": "YH" + str(max_num + 1).zfill(3)
    },
    {
        "cat": "餃子系列",
        "name": "麻辣餃",
        "price": "HKD 25",
        "note": "",
        "stock": True,
        "image": None,
        "local_img": "product_spicy_dumpling.jpg",  # placeholder
        "sku": "YH" + str(max_num + 2).zfill(3)
    }
]

# 加到 products.json
products.extend(new_products)

# 寫回檔案（保留 UTF-8 BOM）
with open('products.json', 'w', encoding='utf-8-sig') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print('\n✅ 已新增 2 款餃子產品')
print('新的产品数量:', len(products))
print('\n新增產品:')
for p in new_products:
    print(f'  - {p["sku"]}: {p["name"]} ({p["price"]})')
