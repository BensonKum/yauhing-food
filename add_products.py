import json

# Read products.json with UTF-8 BOM
with open('products.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Find insert position (after YH501A)
insert_idx = None
for i, p in enumerate(data):
    if p.get('sku') == 'YH501A':
        insert_idx = i + 1
        break

if insert_idx is None:
    print("Error: YH501A not found!")
    exit(1)

# New products
yh502 = {
    "cat": "罐頭/零售裝",
    "name": "醬油套裝 (稻米油，豉油，雞精)",
    "price": "HKD 20",
    "note": "稻米油 + 豉油 + 雞精 + 鹽",
    "stock": 0,
    "image": None,
    "local_img": "product_sauce_set.jpg",
    "sku": "YH502"
}

yh503 = {
    "cat": "罐頭/零售裝",
    "name": "稻米油 150ml",
    "price": "HKD 10",
    "note": "",
    "stock": 0,
    "image": None,
    "local_img": "product_rice_oil_150ml.jpg",
    "sku": "YH503"
}

# Insert (YH503 first, then YH502 - reverse order to preserve indices)
data.insert(insert_idx, yh502)
data.insert(insert_idx + 1, yh503)

# Write back with UTF-8 BOM
with open('products.json', 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Added YH502 and YH503 after YH501A (position {insert_idx})")
print(f"Total products: {len(data)}")
