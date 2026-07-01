import pandas as pd
import json

# Read Ben's Excel
BEN_FILE = r'C:\Users\admin\.qclaw\media\inbound\罐頭_零售裝---1acc1ee2-716b-4f5c-8fdb-f6f0874e6066.xls'
PRODUCTS_FILE = r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json'

df = pd.read_excel(BEN_FILE)
print("Ben's Excel columns:", df.columns.tolist())
print("\nBen's Excel data:")
print(df.to_string(index=False))
print(f"\nTotal rows: {len(df)}")

# Load products.json
with open(PRODUCTS_FILE, 'r', encoding='utf-8-sig') as f:
    products = json.load(f)

# Find products in cat "罐頭/零售裝"
cat_products = [p for p in products if p.get('cat') == '罐頭/零售裝']
print(f"\n\nProducts in '罐頭/零售裝' category ({len(cat_products)} items):")
for p in cat_products:
    print(f"  {p.get('sku')} | {p.get('name')} | {p.get('price')}")
