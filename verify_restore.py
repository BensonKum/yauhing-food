# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
print('Size:', len(data))
print('<div>:', data.count(b'<div'))
print('</div>:', data.count(b'</div>'))

cats = re.findall(b'data-cat="([^"]+)"', data)
from collections import Counter
cc = Counter(c.decode('utf-8', errors='replace') for c in cats)
for k, v in sorted(cc.items(), key=lambda x: -x[1]):
    print('  cat:', k, '->', v)
print('Total p-card:', data.count(b'<div class="p-card '))
print('no-image:', data.count(b'p-card no-image'))