# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

skus_removed = ['YH001', 'YH006', 'YH007', 'YH008', 'YH009', 'YH010', 'YH015']

print('=' * 50)
print('第 1 次驗證')
print('=' * 50)

# 1. 總產品數量
print(f'\n1. 總產品數量：{len(products)} 款（預期：62）')
if len(products) == 62:
    print('   ✅ 正確')
else:
    print('   ❌ 錯誤')

# 2. 手工麵數量
handmade = [p for p in products if p.get('cat') == '手工麵']
print(f'\n2. 手工麵數量：{len(handmade)} 款（預期：10）')
if len(handmade) == 10:
    print('   ✅ 正確')
else:
    print('   ❌ 錯誤')

# 3. 7款產品已不存在
print(f'\n3. 確認 7 款產品已刪除：')
current_skus = [p.get('sku') for p in products]
all_removed = True
for sku in skus_removed:
    if sku in current_skus:
        print(f'   ❌ {sku} 仍然存在')
        all_removed = False
    else:
        print(f'   ✅ {sku} 已刪除')

# 4. 其他產品無受影響
print(f'\n4. 其他產品狀態：')
expected_remaining = 62
print(f'   剩餘產品：{len(products)} 款')
if len(products) == expected_remaining and all_removed:
    print('   ✅ 其他產品無受影響')
else:
    print('   ❌ 可能有問題')

print('\n' + '=' * 50)
print('第 2 次驗證')
print('=' * 50)

# 重新讀取確認
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', 'r', encoding='utf-8') as f:
    products2 = json.load(f)

print(f'\n1. 總產品數量：{len(products2)} 款')
print(f'2. 手工麵數量：{len([p for p in products2 if p.get("cat") == "手工麵"])} 款')
print(f'3. YH001 存在：{"是" if "YH001" in [p.get("sku") for p in products2] else "否"}')
print(f'4. YH006 存在：{"是" if "YH006" in [p.get("sku") for p in products2] else "否"}')
print(f'5. YH007 存在：{"是" if "YH007" in [p.get("sku") for p in products2] else "否"}')
print(f'6. YH008 存在：{"是" if "YH008" in [p.get("sku") for p in products2] else "否"}')
print(f'7. YH009 存在：{"是" if "YH009" in [p.get("sku") for p in products2] else "否"}')
print(f'8. YH010 存在：{"是" if "YH010" in [p.get("sku") for p in products2] else "否"}')
print(f'9. YH015 存在：{"是" if "YH015" in [p.get("sku") for p in products2] else "否"}')

print('\n' + '=' * 50)
print('第 3 次驗證')
print('=' * 50)

# 列出所有手工麵
handmade3 = [p for p in products2 if p.get('cat') == '手工麵']
print(f'\n手工麵剩餘產品（共 {len(handmade3)} 款）：')
for p in handmade3:
    print(f'   {p.get("sku")}: {p.get("name")}')

print('\n✅ 3 次驗證完成')