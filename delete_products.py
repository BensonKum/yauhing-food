# -*- coding: utf-8 -*-
import json, shutil, sys, io, os
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 路徑
products_path = r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json'
backup_dir = r'C:\Users\admin\Desktop\QClaw\備份\祐興網站'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_path = os.path.join(backup_dir, f'products_backup_{timestamp}')

# 備份
os.makedirs(backup_path, exist_ok=True)
shutil.copy(products_path, backup_path)
print(f'✅ 備份已建立: {backup_path}')

# 讀取
with open(products_path, 'r', encoding='utf-8') as f:
    products = json.load(f)
print(f'✅ 讀取 products.json，原有 {len(products)} 款產品')

# 要刪除的 SKU
skus_to_remove = ['YH001', 'YH006', 'YH007', 'YH008', 'YH009', 'YH010', 'YH015']

# 刪除
products_new = [p for p in products if p.get('sku') not in skus_to_remove]
removed = [p for p in products if p.get('sku') in skus_to_remove]

print(f'\n已刪除 {len(removed)} 款產品：')
for p in removed:
    print(f'  - {p.get("sku")}: {p.get("name")}')

# 寫入
with open(products_path, 'w', encoding='utf-8') as f:
    json.dump(products_new, f, ensure_ascii=False, indent=2)
print(f'\n✅ 已寫入 products.json，現有 {len(products_new)} 款產品')
