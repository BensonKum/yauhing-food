# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the logType select's closing tag in the Log tab
old = '''        <option value="purchase">進貨</option>
        </select>
        <span class="filter-label">日期：</span>'''

new = '''        <option value="purchase">進貨</option>
        </select>
        <button class="btn-export" onclick="exportLogToExcel()">📊 匯出 Excel</button>
        <span class="filter-label">日期：</span>'''

if old in c:
    c = c.replace(old, new, 1)
    print('✅ Added export button to Log tab')
else:
    print('❌ Target string not found!')
    sys.exit(1)

with open('inventory.html', 'w', encoding='utf-8') as f:
    f.write(c)

# Verify
count = c.count('exportLogToExcel()')
print(f'exportLogToExcel occurrences: {count} (should be 2: button + function)')
