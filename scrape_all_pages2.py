# -*- coding: utf-8 -*-
import subprocess, json, re, time

NODE = r"C:\Program Files\nodejs\node.exe"
XB = r"C:\Users\admin\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs"

def get_page_text(page):
    url = f'https://www.noodlesx.com/zh-hk/shop/?query=%7B%22page%22:{page},%22rowsPerPage%22:24,%22sortBy%22:[%22order%22,%22date%22],%22sortDesc%22:[false,true]%7D'
    # Step 1: open
    cmd = f'"{NODE}" "{XB}" run --browser cft open "{url}"'
    subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20, encoding='utf-8')
    time.sleep(2)
    # Step 2: get text body (single command)
    cmd = f'"{NODE}" "{XB}" run --browser cft get text body'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20, encoding='utf-8')
    d = json.loads(result.stdout.strip())
    return d['data']['result']['data']['text']

def parse_products(text):
    lines = text.split('\n')
    products = []
    skip = {'首頁','商店','所有分類','關於我們','聯絡我們','文章','推介貨品',
            '每頁顯示','價錢','產品類型','願望清單','我的帳號','購物車','隱私權政策',
            '條款及細則','更多','Copyright','Powered by','keyboard_arrow_down','keyboard_arrow_up',
            'chevron_left','chevron_right','shopping_cart','關於祐興粉麵廠','網站資源',
            'check_box','check_box_outline_blank','keyboard_arrow_left','keyboard_arrow_right',
            '1','2','3'}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line in skip or (len(line) <= 2 and not re.match(r'HKD', line)):
            i += 1
            continue
        if i + 1 < len(lines):
            nxt = lines[i+1].strip()
            m = re.match(r'^HKD\s*(\d+)', nxt)
            if m:
                oos = '缺貨中' in line
                name = line.replace('缺貨中 ', '').strip()
                if name and len(name) > 1:
                    products.append({'name': name, 'price': int(m.group(1)), 'out_of_stock': oos})
                i += 2
                continue
        i += 1
    return products

all_products = []

for page in range(1, 4):
    print(f'=== Page {page} ===', flush=True)
    try:
        text = get_page_text(page)
    except Exception as e:
        print(f'  Error: {e}', flush=True)
        continue
    products = parse_products(text)
    print(f'  Found {len(products)} products', flush=True)
    all_products.extend(products)

# Deduplicate
seen = {}
for p in all_products:
    if p['name'] not in seen:
        seen[p['name']] = p
unique = list(seen.values())

print(f'\n=== Total unique: {len(unique)} ===', flush=True)
oos = [p for p in unique if p.get('out_of_stock')]
print(f'Out of stock: {len(oos)}', flush=True)
print(f'In stock: {len(unique) - len(oos)}', flush=True)

with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_all_products.json', 'w', encoding='utf-8') as f:
    json.dump(unique, f, ensure_ascii=False, indent=2)
print('Saved!', flush=True)
