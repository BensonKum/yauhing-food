# -*- coding: utf-8 -*-
"""
Scrape all categories from noodlesx.com using xbrowser.
Strategy: use direct URL with category filter, then snapshot to get products.
"""
import subprocess, json, re, time

NODE = r"C:\Program Files\nodejs\node.exe"
XB = r"C:\Users\admin\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs"

# Categories from the website filter (name -> checkbox ref mapping)
# We'll navigate to shop page and use the filter UI

def run_xb(args, timeout=30):
    """Run xbrowser command and return parsed JSON result"""
    cmd = f'"{NODE}" "{XB}" run --browser cft ' + ' '.join(args)
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=timeout,
        encoding='utf-8'
    )
    if result.stdout.strip():
        return json.loads(result.stdout.strip())
    return None

def parse_products_from_text(text):
    """Parse product name + HKD price pairs from page text"""
    lines = text.split('\n')
    products = []
    skip_words = {'首頁','商店','所有分類','關於我們','聯絡我們','文章',
                  '推介貨品','每頁顯示','價錢','產品類型','願望清單','我的帳號',
                  '購物車','隱私權政策','條款及細則','Previous page','Next page',
                  '更多','缺貨中','Copyright','Powered by','keyboard_arrow_down',
                  'keyboard_arrow_up','chevron_left','chevron_right','shopping_cart',
                  'check_box','check_box_outline_blank','關於祐興粉麵廠',
                  '網站資源'}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line in skip_words:
            i += 1
            continue
        # Skip lines that are just UI elements
        if i + 1 < len(lines):
            nxt = lines[i+1].strip()
            if re.match(r'^HKD\s*\d+', nxt, re.IGNORECASE):
                price_match = re.search(r'HKD\s*(\d+)', nxt)
                if price_match:
                    products.append({
                        'name': line.replace('缺貨中 ', ''),
                        'price': int(price_match.group(1)),
                        'out_of_stock': '缺貨中' in line
                    })
                    i += 2
                    continue
        i += 1
    return products

# Main scraping loop
categories_to_scrape = ['特式麵', '醬料']
total_all = []

for cat in categories_to_scrape:
    print(f'\n=== Scraping: {cat} ===')

    # Step 1: Open shop page fresh
    result = run_xb([f'open "https://www.noodlesx.com/zh-hk/shop/"'])
    if not result or not result.get('ok'):
        print(f'  Failed to open shop page')
        continue
    time.sleep(1)

    # Step 2: Get snapshot to find current refs
    result = run_xb(['snapshot -i'])
    if not result or not result.get('ok'):
        print(f'  Failed to get snapshot')
        continue

    snapshot_data = result['data']['result']
    refs = snapshot_data.get('refs', {})
    snapshot_text = snapshot_data.get('snapshot', '')

    # Find the product type filter button
    filter_btn_ref = None
    for ref_id, ref_info in refs.items():
        if ref_info.get('name') == '產品類型' and ref_info.get('role') == 'button':
            filter_btn_ref = ref_id
            break

    if not filter_btn_ref:
        print(f'  Product type filter not found')
        continue

    print(f'  Filter button ref: {filter_btn_ref}')

    # Step 3: Click filter to open dropdown
    result = run_xb([f'click @{filter_btn_ref}', 'wait --load 1000', 'snapshot -i'])
    if not result or not result.get('ok'):
        print(f'  Failed to open filter')
        continue

    # Parse the new snapshot to find checkboxes
    new_refs = result['data']['result'][2].get('refs', {})

    # First uncheck all currently checked items
    for ref_id, ref_info in new_refs.items():
        if ref_info.get('role') == 'checkbox' and ref_info.get('checked') == True:
            run_xb([f'click @{ref_id}', 'wait --load 500'])
            time.sleep(0.5)

    # Get fresh snapshot after unchecking
    result = run_xb([f'click @{filter_btn_ref}', 'wait --load 1000', 'snapshot -i'])
    if not result or not result.get('ok'):
        print(f'  Failed to reopen filter')
        continue

    final_refs = result['data']['result'][2].get('refs', {})

    # Find and click target category checkbox
    target_ref = None
    for ref_id, ref_info in final_refs.items():
        if ref_info.get('role') == 'checkbox' and ref_info.get('name') == cat:
            target_ref = ref_id
            break

    if not target_ref:
        print(f'  Category {cat} not found in filter')
        # Try "更多" button first
        for ref_id, ref_info in final_refs.items():
            if ref_info.get('name') == '更多' and ref_info.get('role') == 'button':
                print(f'  Trying "更多" button: {ref_id}')
                run_xb([f'click @{ref_id}', 'wait --load 1000', 'snapshot -i'])
                time.sleep(1)
                # Re-check for target
                break
        continue

    print(f'  Found {cat} checkbox: {target_ref}')

    # Click the target category
    result = run_xb([f'click @{target_ref}', 'wait --load networkidle', 'get text body'])
    if not result or not result.get('ok'):
        print(f'  Failed to get products')
        continue

    # Extract text from batch result
    text = None
    batch_results = result['data']['result']
    for item in batch_results:
        if isinstance(item, dict) and item.get('command') == ['get', 'text', 'body']:
            r = item['result']
            text = r.get('text')
            break

    if not text:
        print(f'  No text extracted')
        continue

    products = parse_products_from_text(text)
    for p in products:
        p['category'] = cat

    print(f'  Found {len(products)} products')
    for p in products:
        stock_status = ' [OUT OF STOCK]' if p.get('out_of_stock') else ''
        print(f'    {p["name"]}: HKD {p["price"]}{stock_status}')

    total_all.extend(products)

# Load existing products
try:
    with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_products.json', 'r', encoding='utf-8') as f:
        existing = json.load(f)
except:
    existing = []

existing_names = set(p['name'] for p in existing)
new_count = 0
for p in total_all:
    if p['name'] not in existing_names:
        existing.append(p)
        existing_names.add(p['name'])
        new_count += 1

# Save
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_products.json', 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f'\n=== DONE ===')
print(f'New products added: {new_count}')
print(f'Total products: {len(existing)}')
