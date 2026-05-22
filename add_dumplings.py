import json

# 讀取 products.json
with open('products.json', 'r', encoding='utf-8-sig') as f:
    products = json.load(f)

print(f'当前产品数量: {len(products)}')
print(f'最后一个 SKU: {products[-1]["sku"]}')
print(f'最后一个产品: {products[-1]["name"]}')

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
        "sku": "YH063"  # 待確認
    },
    {
        "cat": "餃子系列",
        "name": "麻辣餃",
        "price": "HKD 25",
        "note": "",
        "stock": True,
        "image": None,
        "local_img": "product_spicy_dumpling.jpg",  # placeholder
        "sku": "YH064"  # 待確認
    }
]

# 加到 products.json
products.extend(new_products)

# 寫回檔案（保留 UTF-8 BOM）
with open('products.json', 'w', encoding='utf-8-sig') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f'\n✅ 已新增 2 款餃子產品')
print(f'新的产品数量: {len(products)}')
print('\n新增產品:')
for p in new_products:
    print(f'  - {p["sku"]}: {p["name"]} ({p["price"]})')
