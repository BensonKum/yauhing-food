import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# Find the first card in the fresh powder section (at 58689)
segment = data[58689:59189]
grad = re.search(b'grad-ch">([^<]+)', segment)
pname = re.search(b'p-name">([^<]+)', segment)
print('First fresh card (58689):')
print('  grad:', grad.group(1).decode('utf-8', errors='replace') if grad else '?')
print('  p-name:', pname.group(1).decode('utf-8', errors='replace') if pname else '?')

# Count ALL no-image cards in #pg (pos >= 58689)
cards = []
for m in re.finditer(b'<div class="p-card no-image"', data):
    pos = m.start()
    if pos >= 58689:
        seg = data[pos:pos+500]
        grad2 = re.search(b'grad-ch">([^<]+)', seg)
        pn = re.search(b'p-name">([^<]+)', seg)
        grad_name = (grad2.group(1).decode('utf-8', errors='replace') if grad2 else '?')
        pname2 = (pn.group(1).decode('utf-8', errors='replace') if pn else '?')
        cards.append((pos, grad_name, pname2))

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\all_fresh.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total fresh powder cards: {len(cards)}\n\n')
    for i, (pos, grad, pn) in enumerate(cards):
        f.write(f'{i+1}. pos {pos}: grad="{grad}" p-name="{pn}"\n')