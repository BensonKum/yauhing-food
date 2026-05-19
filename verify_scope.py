c = open('inventory.html', 'r', encoding='utf-8-sig').read()

import re

# Check for window.editTransaction and window.deleteTransaction
print('=== Global exposure check ===')
for fn in ['window.editTransaction', 'window.deleteTransaction']:
    count = c.count(fn)
    print(f'{fn}: {count} occurrences')
    if count > 0:
        idx = c.find(fn)
        print(f'  First at {idx}: ...{repr(c[idx:idx+80])}...')
    print()

# Check for function definitions
print('=== Function definition check ===')
for fn in ['editTransaction', 'deleteTransaction']:
    positions = [m.start() for m in re.finditer(rf'function\s+{fn}\s*\(' , c)]
    print(f'{fn}: {len(positions)} definitions')
    for p in positions:
        print(f'  @{p}')
    print()

print('Done')
