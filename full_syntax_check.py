c = open('inventory.html', 'r', encoding='utf-8-sig').read()

import re

# Check ALL script blocks for syntax errors
script_pattern = r'<script[^>]*>(.*?)</script>'
scripts = list(re.finditer(script_pattern, c, re.DOTALL))

print(f'Found {len(scripts)} <script> blocks\n')

for i, s in enumerate(scripts):
    content = s.group(1)
    ob = content.count('{')
    cb = content.count('}')
    op = content.count('(')
    cp = content.count(')')
    osq = content.count('[')
    csq = content.count(']')
    
    issues = []
    if ob != cb: issues.append(f'braces {ob}/{cb}')
    if op != cp: issues.append(f'parens {op}/{cp}')
    if osq != csq: issues.append(f'brackets {osq}/{csq}')
    
    status = 'ISSUE: ' + ', '.join(issues) if issues else 'OK'
    print(f'Script #{i} (pos {s.start()}-{s.end()}, len={len(content)}): {status}')

# Also check for common JS syntax errors in the main script
print('\n=== Checking for common issues ===')
# Check for incomplete statements near the removed area
idx = c.find('// OLD editTransaction removed')
if idx >= 0:
    print(f'\nAround removed functions (pos {idx}):')
    print(repr(c[idx-50:idx+150]))
