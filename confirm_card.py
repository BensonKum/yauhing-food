# -*- coding: utf-8 -*-
import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\confirm.txt', 'wb') as f:
    # Verify: find the 上海麵 card and check it has 新鮮粉麵 category
    for m in re.finditer(b'grad-ch">([^<]+)', data):
        name = m.group(1).decode('utf-8', errors='replace')
        if '上海麵' in name:
            pos = m.start()
            seg = data[max(0,pos-200):pos+200]
            cat = re.search(b'data-cat="([^"]+)"', seg)
            cls = re.search(b'class="p-card ([^"]+)"', seg)
            f.write(('上海麵 card at grad-ch pos %d:\n' % pos).encode('utf-8'))
            f.write(('  name: %s\n' % name).encode('utf-8'))
            f.write(('  cat: %s\n' % cat.group(1).decode('utf-8', errors='replace')).encode('utf-8') if cat else '  cat: NOT FOUND\n'.encode('utf-8'))
            f.write(('  cls: %s\n' % cls.group(1).decode('utf-8', errors='replace')).encode('utf-8') if cls else '  cls: NOT FOUND\n'.encode('utf-8'))
    
    # Count all cards with 新鮮粉麵
    count = 0
    for m in re.finditer(b'data-cat="\u65b0\u9aeav\u7d30\u98df"', data):  # 新鮮粉麵 in UTF-8
        seg = data[m.start():m.start()+200]
        if b'p-card' in seg:
            count += 1
    f.write(('\nTotal 新鮮粉麵 cards: %d\n' % count).encode('utf-8'))
    
    # Check filter button
    ct_html = data[data.find(b'<div class="ct"'):data.find(b'</div>', data.find(b'<div class="ct"'))+6]
    ct_decoded = ct_html.decode('utf-8', errors='replace')
    f.write(('\nFilter buttons:\n').encode('utf-8'))
    for btn in re.finditer(b'data-cat="([^"]+)"', ct_html):
        f.write(('  - %s\n' % btn.group(1).decode('utf-8', errors='replace')).encode('utf-8'))