# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Strategy: Add export button RIGHT AFTER the "暫無交易記錄" message in log-main
# Find the log-main div and add button at the top
target = '<div class="log-main">'

if target in c:
    new_target = '''<div class="log-main">
        <button class="btn-export" onclick="exportLogToExcel()" style="display:inline-flex!important;visibility:visible!important;opacity:1!important;margin-bottom:.8rem;padding:.6rem 1.2rem;font-size:.85rem;border-radius:10px;box-shadow:0 2px 8px rgba(0,200,100,0.3);z-index:999;position:relative;">📊 匯出 Excel</button>'''
    c = c.replace(target, new_target, 1)
    print('Added export button at TOP of log-main')
else:
    print('WARNING: .log-main not found')

with open('inventory.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done')
