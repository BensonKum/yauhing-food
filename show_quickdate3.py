# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the full setQuickDate function and replace it
old_start = 'function setQuickDate(days){'
idx = c.find(old_start)
if idx >= 0:
    # Find the end of the function (next function or closing brace at top level)
    # We'll replace from start to the closing } of this function
    chunk = c[idx:idx+800]
    print('Current function:')
    print(chunk)
