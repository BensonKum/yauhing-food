# -*- coding: utf-8 -*-
with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\inventory.js', encoding='utf-8') as f:
    c = f.read()

# Add debug log after products load
old = "fetch('products.json').then(r=>r.json()).then(data=>{\n  products = data;\n  renderCatBar();\n  renderGrid();"
new = "fetch('products.json').then(r=>r.json()).then(data=>{\n  products = data;\n  console.log('[DEBUG] Loaded products:', products.length, 'items');\n  console.log('[DEBUG] YH603:', products.find(p=>p.sku==='YH603'));\n  console.log('[DEBUG] YH603A:', products.find(p=>p.sku==='YH603A'));\n  renderCatBar();\n  renderGrid();"

c = c.replace(old, new)

with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\inventory.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('OK - added debug logs')
