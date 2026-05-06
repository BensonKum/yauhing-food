# -*- coding: utf-8 -*-
import subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

dst = r'C:\Users\admin\.qclaw\workspace\yauhing-food'

# Commit
r = subprocess.run(['git', 'add', 'index.html', 'products.json'], cwd=dst, capture_output=True)
r2 = subprocess.run(['git', 'commit', '-m', 'Fix 素纖麵 character (U+7E4B 纂)'], cwd=dst, capture_output=True, text=True)
msg = (r2.stdout or '') + (r2.stderr or '')
msg = msg.decode('utf-8', errors='replace').strip()
print('Commit:', msg if msg else '(no output)')

# Push
r3 = subprocess.run(['git', 'push'], cwd=dst, capture_output=True, text=True)
out = (r3.stdout or '') + (r3.stderr or '')
out = out.decode('utf-8', errors='replace').strip()
print('Push:', out if out else 'done')

# Verify final state
data = open(dst + '\\index.html', 'rb').read()
import re
cats = re.findall(b'data-cat="([^"]+)"', data)
from collections import Counter
cc = Counter(c.decode('utf-8','replace') for c in cats)
print('\nFinal data-cat values:')
for k, v in sorted(cc.items(), key=lambda x: x[0]):
    print(' ', k, '->', v)
print('\nFile size:', len(data))