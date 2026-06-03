# -*- coding: utf-8 -*-
"""
Scrape all pages from noodlesx.com shop (no category filter, all products).
"""
import subprocess, json, re

NODE = r"C:\Program Files\nodejs\node.exe"
XB = r"C:\Users\admin\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs"

def run_xb(args, timeout=30):
    cmd = f'"{NODE}" "{XB}" run --browser cft ' + ' '.join(args)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, encoding='utf-8')
    if result.stdout.strip():
        return json.loads(result.stdout.strip())
    return None

def parse_products(text):
    lines = text.split('\n')
    products = []
    skip = {'首頁','商店','所有分類','關於我們','聯絡我們','文章','推介貨品',
            '每頁顯示','價錢','產品類型','願望清單','我的帳號','購物車','隱私權政策',
            '條款及細則','更多','Copyright','Powered by','keyboard_arrow_down',
            'chevron_left','chevron_right','shopping_cart','關於祐興粉麵廠',
            '網站資源','check_box','check_box_outline_blank'}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line in skip or line.isdigit():
            i += 1
            continue
        if i + 1 < len(lines):
            nxt = lines[i+1].strip()
            m = re.match(r'^HKD\s*(\d+)', nxt)
            if m:
                oos = '缺貨中' in line
                name = line.replace('缺貨中 ', '').strip()
                if name:
                    products.append({'name': name, 'price': int(m.group(1)), 'out_of_stock': oos})
                i += 2
                continue
        i += 1
    return products

all_products = []

for page in range(1, 4):
    url = f'https://www.noodlesx.com/zh-hk/shop/?query=%7B%22page%22:{page},%22rowsPerPage%22:24,%22sortBy%22:[%22order%22,%22date%22],%22sortDesc%22:[false,true]%7D'
    print(f'=== Page {page} ===')
    
    result = run_xb([f'open "{url}"', 'wait --load networkidle', 'get text body'], timeout=30)
    if not result or not result.get('ok'):
        print(f'  Failed')
        continue
    
    r = result['data']['result']
    txt = r[-1]['result']['text'] if isinstance(r, list) else r['data']['text']
    
    products = parse_products(txt)
    print(f'  Found {len(products)} products')
    for p in products:
        status = ' [OOS]' if p.get('out_of_stock') else ''
        print(f'    {p["name"]}: HKD {p["price"]}{status}')
    
    all_products.extend(products)

# Deduplicate by name
seen = {}
for p in all_products:
    if p['name'] not in seen:
        seen[p['name']] = p

unique = list(seen.values())
print(f'\n=== Summary ===')
print(f'Total products: {len(unique)}')
oos = [p for p in unique if p.get('out_of_stock')]
print(f'Out of stock: {len(oos)}')
in_stock = [p for p in unique if not p.get('out_of_stock')]
print(f'In stock: {len(in_stock)}')

# Save
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_all_products.json', 'w', encoding='utf-8') as f:
    json.dump(unique, f, ensure_ascii=False, indent=2)
print(f'Saved to noodlesx_all_products.json')
