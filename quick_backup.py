# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\backup_index.html', 'rb').read()
print('File size:', len(data))
print('div:', data.count(b'<div'), 'close:', data.count(b'</div>'))

wrong = b'\xe7\xb4\xa0\xe7\xba\x96\xe9\xba\xb5'
correct = b'\xe7\xb4\xa0\xe7\xb4\xab\xe9\xba\xb5'
print('素纖麵 wrong:', data.count(wrong), 'correct:', data.count(correct))

print('Total p-card:', data.count(b'<div class="p-card '))
print('no-image:', data.count(b'p-card no-image'))

cats = re.findall(b'data-cat="([^"]+)"', data)
from collections import Counter
cc = Counter(c.decode('utf-8', errors='replace') for c in cats)
for k, v in sorted(cc.items(), key=lambda x: -x[1]):
    print('  cat:', k, '->', v)