# -*- coding: utf-8 -*-
with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\inventory.js', encoding='utf-8') as f:
    c = f.read()

# Replace with detailed debug
old = """console.log('[DEBUG] YH603:', products.find(p=>p.sku==='YH603'));
  console.log('[DEBUG] YH603A:', products.find(p=>p.sku==='YH603A'));"""

new = """const yh603 = products.find(p=>p.sku==='YH603');
  const yh603a = products.find(p=>p.sku==='YH603A');
  console.log('[DEBUG] YH603 price:', yh603 ? yh603.price : 'NOT FOUND');
  console.log('[DEBUG] YH603A price:', yh603a ? yh603a.price : 'NOT FOUND');
  console.log('[DEBUG] All 大地魚 products:', products.filter(p=>p.name.includes('大地魚')).map(p=>({sku:p.sku, name:p.name, price:p.price})));"""

c = c.replace(old, new)

with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\inventory.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('OK - added detailed debug')
