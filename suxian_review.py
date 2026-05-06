# -*- coding: utf-8 -*-
import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

suxian = u'素纖麵'.encode('utf-8')

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\suxian_review.txt', 'wb') as f:
    # Count 素纖麵
    count = data.count(suxian)
    f.write(('素纖麵 found %d times\n' % count).encode('utf-8'))
    
    # Find all p-card with 素纖麵
    f.write(('\n=== All p-card with 素纖麵 ===\n').encode('utf-8'))
    for m in re.finditer(b'data-cat="[^"]*' + suxian, data):
        pos = m.start()
        seg = data[max(0,pos-50):pos+300]
        cls_m = re.search(b'class="p-card ([^"]+)"', seg)
        grad = re.search(b'grad-ch">([^<]+)', seg)
        pn = re.search(b'p-name">([^<]+)', seg)
        cls = (cls_m.group(1).decode('utf-8', errors='replace') if cls_m else '?')
        g = (grad.group(1).decode('utf-8', errors='replace') if grad else '?')
        p = (pn.group(1).decode('utf-8', errors='replace') if pn else '?')
        f.write(('pos %d: cls=%s grad="%s" pname="%s"\n' % (pos, cls, g, p)).encode('utf-8'))
    
    # All data-cat values
    f.write(('\n=== All data-cat values ===\n').encode('utf-8'))
    cats = re.findall(b'data-cat="([^"]+)"', data)
    cat_counts = {}
    for c in cats:
        s = c.decode('utf-8', errors='replace')
        cat_counts[s] = cat_counts.get(s, 0) + 1
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        f.write(('  "%s": %d\n' % (cat, cnt)).encode('utf-8'))
    
    f.write(('\nTotal p-card: %d\n' % data.count(b'<div class="p-card ')).encode('utf-8'))
    f.write(('no-image: %d\n' % data.count(b'p-card no-image')).encode('utf-8'))