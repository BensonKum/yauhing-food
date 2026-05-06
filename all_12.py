# -*- coding: utf-8 -*-
import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\all_12.txt', 'wb') as f:
    f.write(('All 14 p-card no-image:\n').encode('utf-8'))
    for m in re.finditer(b'<div class="p-card no-image"', data):
        pos = m.start()
        seg = data[pos:pos+600]
        grad = re.search(b'grad-ch">([^<]+)', seg)
        pn = re.search(b'p-name">([^<]+)', seg)
        cat = re.search(b'data-cat="([^"]+)"', seg)
        name_g = (grad.group(1).decode('utf-8', errors='replace') if grad else '?')
        name_p = (pn.group(1).decode('utf-8', errors='replace') if pn else '?')
        cat_s = (cat.group(1).decode('utf-8', errors='replace') if cat else '?')
        f.write(('  pos %d: grad="%s" p-name="%s" cat="%s"\n' % (pos, name_g, name_p, cat_s)).encode('utf-8'))