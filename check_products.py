import json

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', encoding='utf-8') as f:
    products = json.load(f)

print(f'Total: {len(products)} products\n')
for i, p in enumerate(products, 1):
    name = p.get('name', '')
    local_img = p.get('local_img', None)
    img1 = p.get('img1', None)
    img2 = p.get('img2', None)
    label1 = p.get('label1', None)
    label2 = p.get('label2', None)
    print(f'{i:2}. {name[:22]:22} | local_img={str(local_img)[:40]:40} | img1={str(img1)[:20]:20} | label1={label1}')
