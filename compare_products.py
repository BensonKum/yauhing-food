import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

# Read products.json
f = open('C:/Users/admin/.qclaw/workspace/yauhing-food/products.json', 'r', encoding='utf-8-sig')
data = json.load(f)
f.close()

# Read index.html
f2 = open('C:/Users/admin/.qclaw/workspace/yauhing-food/index.html', 'r', encoding='utf-8')
html = f2.read()
f2.close()

print('=== 比對結果 ===\n')

# Group by category
cat_products = {}
for p in data:
    cat = p.get('cat', '未分類')
    name = p.get('name', '')
    # Search in HTML
    found_in_html = name in html
    if cat not in cat_products:
        cat_products[cat] = []
    cat_products[cat].append((name, found_in_html))

# Print by category
for cat in sorted(cat_products.keys()):
    print(f'【{cat}】')
    for name, found in cat_products[cat]:
        status = '✓ 網站有' if found else '✗ 網站無'
        print(f'  {status}  {name}')
    print()

# Summary
total = len(data)
in_website = sum(1 for cat in cat_products.values() for _, found in cat if found)
not_in_website = total - in_website
print(f'=== 統計 ===')
print(f'總產品數：{total}')
print(f'網站有：{in_website}')
print(f'網站無：{not_in_website}')
