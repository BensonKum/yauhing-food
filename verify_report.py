import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

checks = [
    ('tabReport button', 'id="tabReport"'),
    ('tabContentReport', 'id="tabContentReport"'),
    ('report-filter', 'class="report-filter"'),
    ('repList', 'id="repList"'),
    ('loadReportData', 'function loadReportData'),
    ('setRepQuick', 'function setRepQuick'),
    ('report wrap CSS', '.report-wrap{'),
    ('log-entry CSS', '.log-entry{'),
    ('quick-btn CSS', '.quick-btn{'),
]

print('=== 驗證結果 ===')
all_ok = True
for name, pattern in checks:
    found = pattern in c
    status = '✅' if found else '❌'
    print('%s %s: %s' % (status, name, 'OK' if found else 'MISSING'))
    if not found:
        all_ok = False

if all_ok:
    print('\n🎉 所有檢查通過！可以 commit + push')
else:
    print('\n⚠️ 有項目缺失，請檢查')

# 另外檢查 tab-bar 有冇 Report 按鈕
idx = c.find('tabReport')
if idx >= 0:
    print('\n tab-bar 附近的內容：')
    print(repr(c[idx-50:idx+200]))
