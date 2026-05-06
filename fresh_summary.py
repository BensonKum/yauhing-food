# -*- coding: utf-8 -*-
import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\fresh_summary.txt', 'wb') as f:
    # Count all p-card
    all_cards = list(re.finditer(b'<div class="p-card ', data))
    no_img_cards = list(re.finditer(b'<div class="p-card no-image"', data))
    f.write(('Total p-card: %d\n' % len(all_cards)).encode('utf-8'))
    f.write(('Total p-card no-image: %d\n' % len(no_img_cards)).encode('utf-8'))
    
    # Fresh powder section cards (>=58689)
    f.write(('\nFresh powder section cards (pos >= 58689):\n').encode('utf-8'))
    count = 0
    for m in no_img_cards:
        pos = m.start()
        if pos >= 58689:
            seg = data[pos:pos+600]
            grad = re.search(b'grad-ch">([^<]+)', seg)
            name = (grad.group(1).decode('utf-8', errors='replace') if grad else '?')
            f.write(('  pos %d: %s\n' % (pos, name)).encode('utf-8'))
            count += 1
    f.write(('Total in fresh section: %d\n' % count).encode('utf-8'))
    
    # All grad-ch values >=58689
    f.write(('\nAll grad-ch >= 58689:\n').encode('utf-8'))
    for m in re.finditer(b'grad-ch">([^<]+)', data):
        if m.start() >= 58689:
            name = m.group(1).decode('utf-8', errors='replace')
            f.write(('  pos %d: %s\n' % (m.start(), name)).encode('utf-8'))