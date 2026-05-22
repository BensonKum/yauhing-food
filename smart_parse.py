import json, re, sys

def extract_text_from_xb_output(file_path):
    """Extract text field from xbrowser output (handles both single and batch command)"""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    result = data['data']['result']
    
    # Case 1: Single command (result is dict)
    if isinstance(result, dict):
        return result['data']['text']
    
    # Case 2: Batch command (result is list)
    elif isinstance(result, list):
        # Find the 'get text body' command result
        for item in result:
            if isinstance(item, dict) and item.get('command') == ['get', 'text', 'body']:
                return item['result']['data']['text']
        # Fallback: return text from last item
        return result[-1]['result']['data']['text']
    
    else:
        raise ValueError(f'Unknown result type: {type(result)}')

# Parse cat4 (素麵 category)
text = extract_text_from_xb_output('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_cat4.txt')
lines = text.split('\n')

# Parse product name + price pairs
products = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if i + 1 < len(lines):
        next_line = lines[i+1].strip()
        if re.match(r'HKD?\s*\d+', next_line, re.IGNORECASE):
            name = line
            price = next_line
            products.append({'name': name, 'price': price, 'category': '素麵'})
            i += 2
        else:
            i += 1
    else:
        i += 1

print(f'=== 提取到 {len(products)} 款產品 (素麵) ===\n')
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
