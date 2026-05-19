c = open('inventory.html', 'r', encoding='utf-8-sig').read()
import re

# 1. Check all script blocks balance
script_pattern = r'<script[^>]*>(.*?)</script>'
scripts = list(re.finditer(script_pattern, c, re.DOTALL))

print('=== Script Block Balance Check ===')
for i, s in enumerate(scripts):
    content = s.group(1)
    ob = content.count('{')
    cb = content.count('}')
    op = content.count('(')
    cp = content.count(')')
    issues = []
    if ob != cb: issues.append(f'{{}}= {ob}-{cb} = {ob-cb}')
    if op != cp: issues.append(f'()= {op}-{cp} = {op-cp}')
    status = 'ISSUE: ' + ', '.join(issues) if issues else 'OK'
    print(f'Script #{i}: {status}')

# 2. Verify window.editTransaction and window.deleteTransaction exist
print('\n=== Checking window.editTransaction ===')
idx1 = c.find('window.editTransaction')
if idx1 >= 0:
    chunk = c[idx1:idx1+200]
    print(f'Found at {idx1}: {repr(chunk)}')
else:
    print('NOT FOUND!')

print('\n=== Checking window.deleteTransaction ===')
idx2 = c.find('window.deleteTransaction')
if idx2 >= 0:
    chunk = c[idx2:idx2+200]
    print(f'Found at {idx2}: {repr(chunk)}')
else:
    print('NOT FOUND!')

# 3. Verify no duplicate function definitions
print('\n=== Checking for duplicate definitions ===')
for fn_name in ['function editTransaction', 'function deleteTransaction']:
    positions = []
    start = 0
    while True:
        pos = c.find(fn_name, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    print(f'{fn_name}: {len(positions)} definitions at positions {positions}')

# 4. Run Node.js syntax check
print('\n=== Node.js Syntax Check ===')
main_script = scripts[3].group(1)
with open('tmp_check2.js', 'w', encoding='utf-8') as f:
    f.write(main_script)
print(f'Extracted script to tmp_check2.js ({len(main_script)} chars)')
