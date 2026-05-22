import sys, json, subprocess, re, time
sys.stdout.reconfigure(encoding='utf-8')

NODE = r"C:\Program Files\nodejs\node.exe"
XB = r"C:\Users\admin\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs"

def run_xb(args):
    """Run xbrowser command and return JSON result"""
    cmd = f'"{NODE}" "{XB}" run --browser cft ' + args
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
    return result.stdout

# Category refs to click
categories = [
    ('e16', '手工麵'),
    ('e17', '蝦籽麵'),
    ('e18', '素纖麵'),
    ('e19', '零售裝'),
    ('e20', '禮盒套裝'),
    ('e21', '罐頭'),
    ('e22', '養生麵'),
    ('e23', '醬汁配料'),
    ('e24', '特式麵')
]

all_products = []

print('=== 開始抓取 noodlesx.com 產品 ===\n')

for ref, cat_name in categories:
    print(f'📁 處理分類：{cat_name} ({ref})')
    
    # Click on category
    result = run_xb(f'click @{ref}')
    time.sleep(2)
    
    # Wait for load
    run_xb('wait --load networkidle')
    
    # Get page text
    text_result = run_xb('get text body')
    
    # Parse products from text
    # Look for pattern: product name line, then HKD xxx line
    lines = text_result.split('\n')
    i = 0
    cat_products = []
    while i < len(lines):
        line = lines[i].strip()
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            # Check if next line is HKD price
            if re.match(r'HKD?\s*\d+', next_line, re.IGNORECASE):
                name = line
                price = next_line
                cat_products.append({'name': name, 'price': price, 'category': cat_name})
                i += 2
            else:
                i += 1
        else:
            i += 1
    
    print(f'  找到 {len(cat_products)} 款產品')
    all_products.extend(cat_products)
    
    # Go back to all categories
    run_xb('click @e28')  # 所有分類 link
    time.sleep(1)
    run_xb('wait --load networkidle')
    
    print()

print(f'\n=== 總計：{len(all_products)} 款產品 ===\n')
for p in all_products:
    print(f'{p["category"]} | {p["name"]} | {p["price"]}')

# Save to JSON
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_all_products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)
print('\n✓ 已保存到 noodlesx_all_products.json')
