c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# check tabContentLog
idx = c.find('id="tabContentLog"')
print('tabContentLog HTML (first 500 chars):')
print(c[idx:idx+500])
print('...\n')

# check CSS
print('CSS .report-wrap flex:', c.find('.report-wrap{display:flex'))
print('CSS .log-sidebar:', c.find('.log-sidebar{width:180px'))
print('CSS .log-main:', c.find('.log-main{flex:1'))
print()

# check JS renderLog
idx2 = c.find('async function renderLog')
print('renderLog starts at line:', c[:idx2].count('\n')+1)
print()

# check div balance
opens = c.count('<div')
closes = c.count('</div>')
print('div balance:', opens, 'open,', closes, 'close, diff=', opens-closes)
print()

# check functions
for fn in ['renderReport', 'renderLog', 'switchTab', 'pinLogin']:
    i = c.find('function '+fn)
    print(fn, ':', 'FOUND' if i>=0 else 'MISSING')
