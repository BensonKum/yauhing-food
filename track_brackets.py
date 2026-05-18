# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('function loadReportData')
next_func = re.search(r'\nfunction\s+\w+\s*\(', content[start+20:])
if not next_func:
    end = content.find('</script>', start)
else:
    end = start + 20 + next_func.start()
block = content[start:end]

depth = 0
lines = block.split('\n')
for i, line in enumerate(lines):
    for ch in line:
        if ch == '{': depth += 1
        if ch == '}': depth -= 1
    # show lines where depth changes to interesting values
    if i > 3:
        print(f'L{i:4d} d={depth:2d} | {line.strip()[:120]}')
