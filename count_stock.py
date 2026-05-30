#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""統計 products.json 嘅庫存數量"""

import json
import sys

# 讀取 products.json
try:
    with open('products.json', 'r', encoding='utf-8-sig') as f:
        products = json.load(f)
except Exception as e:
    print(f"讀取失敗：{e}")
    sys.exit(1)

# 統計
total = len(products)
in_stock = sum(1 for p in products if p.get('stock', 0) > 0)
out_of_stock = total - in_stock

print(f"總產品數：{total}")
print(f"有庫存：{in_stock}")
print(f"缺貨：{out_of_stock}")
print()
print(f"HTML 需要更新嘅數字：")
print(f"  款產品：{total}")
print(f"  款有貨：{in_stock}")
print(f"  款缺貨：{out_of_stock}")
