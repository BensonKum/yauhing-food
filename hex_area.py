# -*- coding: utf-8 -*-
# Check bytes 58689-58750 from data
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# The grad-ch at 58689+ contains 上海麵 (幼) 盒裝
# Show hex of first 100 bytes from insert area
chunk = data[58689:58789]
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\hex_area.txt', 'wb') as f:
    f.write(chunk.hex().encode('utf-8'))
    f.write(u'\n\n'.encode('utf-8'))
    # Also count cards
    f.write(u'total p-card: %d\n' % data.count(b'<div class="p-card '))
    f.write(u'no-image: %d\n' % data.count(b'p-card no-image'))
    # Count fresh powder no-image cards
    count_fresh = 0
    for m in re.finditer(b'<div class="p-card no-image"', data):
        if m.start() >= 58689:
            count_fresh += 1
    f.write(u'fresh powder cards: %d\n' % count_fresh)

import re