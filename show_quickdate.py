# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('function setQuickDate')
if idx >= 0:
    print(c[idx:idx+400])
else:
    print('NOT FOUND')
