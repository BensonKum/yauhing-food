# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add export button to Report tab (after repStatus select)
old_rep = '''      <select class="filter-select" id="repStatus" onchange="renderReport()">
        <option value="all">全部</option>
        <option value="alert">⚠️ 低庫存</option>
        <option value="zero">🔴 缺貨</option>
        <option value="discontinued">❌ 停售</option>
      </select>'''

new_rep = '''      <select class="filter-select" id="repStatus" onchange="renderReport()">
        <option value="all">全部</option>
        <option value="alert">⚠️ 低庫存</option>
        <option value="zero">🔴 缺貨</option>
        <option value="discontinued">❌ 停售</option>
      </select>
      <button class="btn-export" onclick="exportReportToExcel()">📊 匯出 Excel</button>'''

if old_rep in c:
    c = c.replace(old_rep, new_rep, 1)
    print('OK - Report tab export button added')
else:
    print('WARN - Report tab pattern not found (may already exist)')

# 2. Add export button to Log tab (find logStore select)
old_log = '''<select class="filter-select" id="logStore" onchange="renderLog()">'''
# Check if logStore exists
if 'logStore' in c and 'btnExportLog' not in c:
    # Find the logStore select and add button after its closing </select>
    import re
    # Pattern: logStore select with options, then closing </select>
    log_pattern = r'(<select class="filter-select" id="logStore" onchange="renderLog\(\)">.*?</select>)'
    match = re.search(log_pattern, c, re.DOTALL)
    if match:
        log_select = match.group(1)
        new_log_select = log_select + '\n      <button class="btn-export" onclick="exportLogToExcel()">📊 匯出 Excel</button>'
        c = c.replace(log_select, new_log_select, 1)
        print('OK - Log tab export button added')
    else:
        print('WARN - Log tab select pattern not found')
elif 'btnExportLog' in c:
    print('OK - Log tab export button already exists')
else:
    print('WARN - logStore not found in file')

with open('inventory.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done!')
