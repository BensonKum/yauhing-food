# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Strategy: Add export button INSIDE the log-sidebar area (below the 4 summary cards, above date picker)
# Find the "自訂日期範圍" label area in the sidebar
target = '<div class="log-sidebar" id="logSidebar"></div>'

if target in c:
    # Replace with: same div + a visible export button after it
    new_target = '''<div class="log-sidebar" id="logSidebar">
        <button class="btn-export" onclick="exportLogToExcel()" style="display:inline-flex!important;visibility:visible!important;opacity:1!important;margin-top:.5rem;width:100%;justify-content:center;padding:.6rem;font-size:.85rem;border-radius:10px;box-shadow:0 2px 8px rgba(0,200,100,0.3);">📊 匯出 Excel</button>
      </div>'''
    c = c.replace(target, new_target, 1)
    print('Added export button inside log-sidebar')
else:
    print('WARNING: logSidebar not found')
    # Try alternate
    idx = c.find('id="logSidebar"')
    if idx >= 0:
        print('Found at', idx, ':', c[idx-30:idx+50])

with open('inventory.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done')
