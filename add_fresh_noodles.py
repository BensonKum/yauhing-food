# -*- coding: utf-8 -*-
import json, shutil, os, sys, io, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

workspace = r'C:\Users\admin\.qclaw\workspace\yauhing-food'
backup_dir = r'C:\Users\admin\Desktop\QClaw\備份\祐興網站'
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup_path = os.path.join(backup_dir, f'products_backup_{timestamp}')
os.makedirs(backup_path, exist_ok=True)

# Step 1: Backup
print('=== Step 1: 備份 ===')
shutil.copy(os.path.join(workspace, 'products.json'), os.path.join(backup_path, 'products.json'))
print(f'備份已建立: {backup_path}')

# Step 2: Read current products
print('\n=== Step 2: 讀取現有產品 ===')
with open(os.path.join(workspace, 'products.json'), 'r', encoding='utf-8') as f:
    products = json.load(f)
print(f'現有產品數量: {len(products)}')

# Step 3: Define 12 new products
new_products = [
    {"cat": "新鮮粉麵", "name": "豆卜 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "河粉 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "瀨粉 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "銀針粉 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "上海麵 (幼) 盒裝", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "生幼麵 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "生粗麵 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "油麵 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "水餃皮 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "雲吞皮 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "齋腸粉 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
    {"cat": "新鮮粉麵", "name": "蝦米腸粉 (盒裝)", "price": "HKD 10", "note": "", "stock": True, "image": None, "local_img": None, "sku": None},
]

print(f'新增產品數量: {len(new_products)}')

# Step 4: Add new products
print('\n=== Step 4: 新增產品 ===')
products.extend(new_products)
print(f'新增後產品數量: {len(products)}')

# Step 5: Save
print('\n=== Step 5: 儲存 ===')
with open(os.path.join(workspace, 'products.json'), 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
print('products.json 已更新')

# Step 6: Verification 1 - Count
print('\n=== 驗證 1: 產品數量 ===')
with open(os.path.join(workspace, 'products.json'), 'r', encoding='utf-8') as f:
    verify_products = json.load(f)
print(f'總產品數量: {len(verify_products)}')
expected = 57 + 12
print(f'預期數量: {expected}')
print(f'結果: {"✅ 正確" if len(verify_products) == expected else "❌ 錯誤"}')

# Step 7: Verification 2 - 新鮮粉麵 count
print('\n=== 驗證 2: 新鮮粉麵產品 ===')
fresh_noodles = [p for p in verify_products if p.get('cat') == '新鮮粉麵']
print(f'新鮮粉麵產品數量: {len(fresh_noodles)}')
print('新鮮粉麵產品清單:')
for i, p in enumerate(fresh_noodles, 1):
    print(f'  {i}. {p["name"]}')
print(f'結果: {"✅ 正確 (13款含placeholder)" if len(fresh_noodles) == 13 else "❌ 錯誤"}')

# Step 8: Verification 3 - Check each product
print('\n=== 驗證 3: 逐一檢查 ===')
expected_names = [
    "豆卜 (盒裝)", "河粉 (盒裝)", "瀨粉 (盒裝)", "銀針粉 (盒裝)",
    "上海麵 (幼) 盒裝", "生幼麵 (盒裝)", "生粗麵 (盒裝)", "油麵 (盒裝)",
    "水餃皮 (盒裝)", "雲吞皮 (盒裝)", "齋腸粉 (盒裝)", "蝦米腸粉 (盒裝)"
]
all_found = True
for name in expected_names:
    found = any(p['name'] == name for p in verify_products)
    status = '✅' if found else '❌'
    print(f'  {status} {name}')
    if not found:
        all_found = False

print(f'\n結果: {"✅ 全部正確" if all_found else "❌ 有缺漏"}')

# Final summary
print('\n' + '='*50)
print('=== 最終結果 ===')
print(f'總產品: {len(verify_products)} (預期 {expected})')
print(f'新鮮粉麵: {len(fresh_noodles)} 款 (含placeholder)')
print(f'12款新增產品: {"✅ 全部存在" if all_found else "❌ 有缺漏"}')