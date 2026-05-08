# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

workspace = r'C:\Users\admin\.qclaw\workspace\yauhing-food'

# Verification run
def verify(run_num):
    print(f'\n{"="*50}')
    print(f'=== 第 {run_num} 次驗證 ===')
    print('='*50)

    with open(workspace + '\\products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    # Check 1: Total count
    total = len(products)
    print(f'\n1. 總產品數量: {total} (預期 69)')
    print(f'   結果: {"✅ 正確" if total == 69 else "❌ 錯誤"}')

    # Check 2: 新鮮粉麵 count
    fresh = [p for p in products if p.get('cat') == '新鮮粉麵']
    print(f'\n2. 新鮮粉麵數量: {len(fresh)} (預期 13)')
    print(f'   結果: {"✅ 正確" if len(fresh) == 13 else "❌ 錯誤"}')

    # Check 3: All 12 products exist
    expected = [
        "豆卜 (盒裝)", "河粉 (盒裝)", "瀨粉 (盒裝)", "銀針粉 (盒裝)",
        "上海麵 (幼) 盒裝", "生幼麵 (盒裝)", "生粗麵 (盒裝)", "油麵 (盒裝)",
        "水餃皮 (盒裝)", "雲吞皮 (盒裝)", "齋腸粉 (盒裝)", "蝦米腸粉 (盒裝)"
    ]

    print(f'\n3. 逐一檢查12款產品:')
    all_ok = True
    for name in expected:
        found = any(p['name'] == name for p in products)
        status = '✅' if found else '❌'
        print(f'   {status} {name}')
        if not found:
            all_ok = False

    print(f'\n   結果: {"✅ 全部存在" if all_ok else "❌ 有缺漏"}')

    # Check 4: All have correct price
    correct_price = all(p.get('price') == 'HKD 10' for p in fresh if p['name'] != '新鮮粉麵')
    print(f'\n4. 價格檢查 (HKD 10): {"✅ 正確" if correct_price else "❌ 錯誤"}')

    # Check 5: All have correct stock
    correct_stock = all(p.get('stock') == True for p in fresh if p['name'] != '新鮮粉麵')
    print(f'5. 庫存檢查 (true): {"✅ 正確" if correct_stock else "❌ 錯誤"}')

    return total == 69 and len(fresh) == 13 and all_ok and correct_price and correct_stock

# Run 3 times
results = []
for i in range(1, 4):
    results.append(verify(i))

print(f'\n{"="*50}')
print('=== 最終結果 ===')
print('='*50)
print(f'第1次驗證: {"✅ 通過" if results[0] else "❌ 失敗"}')
print(f'第2次驗證: {"✅ 通過" if results[1] else "❌ 失敗"}')
print(f'第3次驗證: {"✅ 通過" if results[2] else "❌ 失敗"}')
print(f'\n總結: {"✅ 3次全部通過" if all(results) else "❌ 有驗證失敗"}')