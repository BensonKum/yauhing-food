#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""統計 index.html 入面產品卡嘅庫存狀態"""

import re

# 讀取 index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 找出所有產品卡嘅 data-stock 值
stock_matches = re.findall(r'data-stock="(.*?)"', html)

# 統計
total = len(stock_matches)
in_stock = sum(1 for s in stock_matches if s == 'in')
out_of_stock = sum(1 for s in stock_matches if s == 'out')

print(f"總產品卡數：{total}")
print(f"有庫存：{in_stock}")
print(f"缺貨：{out_of_stock}")
print()
print("需要在 index.html 更新的統計數字：")
print(f"  - 款產品：{total}")
print(f"  - 款有貨：{in_stock}")
print(f"  - 款缺貨：{out_of_stock}")
