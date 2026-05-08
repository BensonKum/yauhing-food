# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Check 素纖麵 in restored files
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
text = data.decode('utf-8', errors='replace')
import re
matches = re.findall(r'素.{1}麵', text)
print('素?麵 in index.html:')
for m in matches[:3]:
    print('  "%s" hex=%s' % (m, m.encode('utf-8').hex()))

pdata = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\products.json', 'rb').read()
pmatches = re.findall(r'素.{1}麵', pdata.decode('utf-8', errors='replace'))
print('\n素?麵 in products.json:')
for m in pmatches[:3]:
    print('  "%s" hex=%s' % (m, m.encode('utf-8').hex()))

from collections import Counter
cats = re.findall(b'data-cat="([^"]+)"', data)
cc = Counter(c.decode('utf-8','replace') for c in cats)
print('\ndata-cat values:')
for k, v in sorted(cc.items(), key=lambda x: x[0]):
    print('  %s -> %d' % (k, v))