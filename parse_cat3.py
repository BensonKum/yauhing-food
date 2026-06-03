import json, re

# Read cat3 text (蝦籽麵 category)
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_cat3.txt', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Extract the text field from batch result (index 3 = get text body)
# Structure: result[3]['result']['text'] (not ['result']['data']['text'])
text = data['data']['result'][3]['result']['text']
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
            products.append({'name': name, 'price': price, 'category': '蝦籽麵'})
            i += 2
        else:
            i += 1
    else:
        i += 1

print(f'=== 提取到 {len(products)} 款產品 (蝦籽麵) ===\n')
for p in products:
    print(f'{p["name"]}: {p["price"]}')

# Append to main JSON file
try:
    with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_products.json', 'r', encoding='utf-8') as f:
        all_products = json.load(f)
except:
    all_products = []

all_products.extend(products)

with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)
print(f'\nOK 已追加到 noodlesx_products.json (總計 {len(all_products)} 款)')
