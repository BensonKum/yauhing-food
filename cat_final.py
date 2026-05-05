import json

products = json.load(open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json','r',encoding='utf-8-sig'))

# Raw hex of ALL unique categories in products.json
cats = {}
for p in products:
    cat = p.get('cat','')
    h = cat.encode('utf-8').hex()
    if h not in cats:
        cats[h] = cat

print('=== All categories in products.json (raw hex) ===')
for h, c in sorted(cats.items()):
    print(f'  hex={h} -> {c!r}')

# Check pickup_only specific cats
pickup = [p for p in products if p.get('pickup_only')]
pickup_cats = set(p.get('cat','') for p in pickup)
print(f'\n=== Pickup_only categories ===')
for c in pickup_cats:
    h = c.encode('utf-8').hex()
    print(f'  hex={h} -> {c!r}')

# The key question: what cat does each missing product have vs what HTML shows?
# HTML shows: e696b0e9b29ce9bab5 = 新鲜麵 (simplified)
# Let's see what cat each OUT product has vs the IN products
html = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
name_utf8_in_html = [p['name'].encode('utf-8') for p in pickup if p['name'].encode('utf-8') in html]
name_utf8_out = [p['name'].encode('utf-8') for p in pickup if p['name'].encode('utf-8') not in html]

print(f'\n=== Products WITH cards (IN): {len(name_utf8_in_html)} ===')
for n in name_utf8_in_html:
    p = next(x for x in pickup if x['name'].encode('utf-8') == n)
    cat = p.get('cat','')
    print(f'  {p["name"]} -> cat hex={cat.encode("utf-8").hex()}')

print(f'\n=== Products WITHOUT cards (OUT): {len(name_utf8_out)} ===')
for n in name_utf8_out:
    p = next(x for x in pickup if x['name'].encode('utf-8') == n)
    cat = p.get('cat','')
    cat_hex = cat.encode('utf-8').hex()
    in_nav = cat.encode('utf-8') in html[:35000]
    in_card = cat.encode('utf-8') in html[30000:]
    print(f'  {p["name"]} -> cat hex={cat_hex} nav={in_nav} card_area={in_card}')