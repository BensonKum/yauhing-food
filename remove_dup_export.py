# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the dynamic export button code block
start_str = 'function addExportButtons(){'
end_str = '// --- Mobile Cart ---'

start_idx = c.find(start_str)
end_idx = c.find(end_str)

if start_idx >= 0 and end_idx > start_idx:
    # Remove from start of function to just before Mobile Cart comment
    removed = c[start_idx:end_idx]
    c = c[:start_idx].rstrip() + '\n\n' + c[end_idx:]
    print(f'Removed {len(removed)} chars of dynamic export button code')
else:
    print(f'ERROR: start={start_idx}, end={end_idx}')
    sys.exit(1)

with open('inventory.html', 'w', encoding='utf-8') as f:
    f.write(c)

# Verify
btn_count = c.count('btn-export')
addexp_count = c.count('addExportButtons')
print(f'Remaining btn-export: {btn_count} (expect 3: CSS x2 + HTML button x1)')
print(f'Remaining addExportButtons: {addexp_count} (expect 0)')
