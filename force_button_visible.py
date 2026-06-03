# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Add inline style to force visibility on the Log export button
old = '<button class="btn-export" onclick="exportLogToExcel()">📊 匯出 Excel</button>'
new = '<button class="btn-export" onclick="exportLogToExcel()" style="display:inline-flex!important;visibility:visible!important;opacity:1!important;position:relative!important;z-index:999!important;font-size:0.85rem!important;padding:.5rem 1rem!important;">📊 匯出 Excel</button>'

if old in c:
    c = c.replace(old, new, 1)
    print('Added inline style to Log export button')
else:
    print('WARNING: button not found')

# Also add to Report export button for consistency
old2 = '<button class="btn-export" onclick="exportReportToExcel()">📊 匯出 Excel</button>'
new2 = '<button class="btn-export" onclick="exportReportToExcel()" style="display:inline-flex!important;visibility:visible!important;opacity:1!important;position:relative!important;z-index:999!important;font-size:0.85rem!important;padding:.5rem 1rem!important;">📊 匯出 Excel</button>'

if old2 in c:
    c = c.replace(old2, new2, 1)
    print('Added inline style to Report export button')
else:
    print('WARNING: Report button not found')

with open('inventory.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done - both buttons now have forced inline styles')
