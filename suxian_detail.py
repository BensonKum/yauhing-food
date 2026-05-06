# -*- coding: utf-8 -*-
import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# Use unicode escapes to avoid encoding issues
suxian = b'\xe7\xb4\xa0\xe7\xb4\xab\xe9\xba\xb5'  # 素纖麵

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\suxian_detail.txt', 'wb') as f:
    f.write(('File size: %d\n' % len(data)).encode('utf-8'))
    f.write(('素纖麵 total occurrences: %d\n\n' % data.count(suxian)).encode('utf-8'))
    
    f.write('=== All 素纖麵 p-cards ===\n'.encode('utf-8'))
    cards = []
    pat = b'data-cat="'
    pat += suxian
    pat += b'"'
    for m in re.finditer(pat, data):
        pos = m.start()
        seg = data[max(0,pos-50):pos+400]
        cls_m = re.search(b'class="p-card ([^"]+)"', seg)
        grad = re.search(b'grad-ch">([^<]+)', seg)
        pn_m = re.search(b'p-name">([^<]+)', seg)
        cls = (cls_m.group(1).decode('utf-8', errors='replace') if cls_m else '?')
        g = (grad.group(1).decode('utf-8', errors='replace') if grad else '?')
        pname = (pn_m.group(1).decode('utf-8', errors='replace') if pn_m else '?')
        f.write(('pos %d: cls="%s" grad="%s" pname="%s"\n' % (pos, cls, g, pname)).encode('utf-8'))
        cards.append((pos, cls, g, pname))
    
    f.write('\n=== Div balance for each card ===\n'.encode('utf-8'))
    for pos, cls, grad, pname in cards:
        card_start = data.rfind(b'<div', 0, pos)
        card_end = data.find(b'</div>', pos) + 6
        card_data = data[card_start:card_end]
        opens = card_data.count(b'<div')
        closes = card_data.count(b'</div>')
        status = 'OK' if opens == closes else 'MISMATCH'
        f.write(('  byte %d (%s): opens=%d closes=%d => %s\n' % (
            pos, g, opens, closes, status)).encode('utf-8'))
    
    if cards:
        last_end = max(data.find(b'</div>', p) + 6 for p, _, _, _ in cards)
        f.write(('\nLast suxian card ends at byte %d\n' % last_end).encode('utf-8'))
        f.write('First fresh powder at 58689\n'.encode('utf-8'))
        if last_end < 58689:
            gap = data[last_end:58689]
            f.write(('Gap of %d bytes: %s\n' % (len(gap), gap.decode('utf-8', errors='replace')[:200])).encode('utf-8'))
    
    f.write(('\nOverall: <div=%d </div>=%d\n' % (data.count(b'<div'), data.count(b'</div>'))).encode('utf-8'))