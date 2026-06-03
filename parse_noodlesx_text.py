import json, re

# Read the JSON file saved by xbrowser
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_raw.txt', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Extract the text field
text = data['data']['result']['data']['text']
lines = text.split('\n')

# Parse product name + price pairs
products = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if i + 1 < len(lines):
        next_line = lines[i+1].strip()
        # Check if next line is HKD price
        if re.match(r'HKD?\s*\d+', next_line, re.IGNORECASE):
            name = line
            price = next_line
            products.append({'name': name, 'price': price, 'category': '禮盒/套裝'})
            i += 2
        else:
            i += 1
    else:
        i += 1

print(f'=== 提取到 {len(products)} 款產品 ===\n')
for p in products:
    print(f'{p["name"]}: {p["price"]}')

# Save to JSON
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
print('\n✓ 已保存到 noodlesx_products.json')
