# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 加 group header CSS
css = '''
.rep-group-header{ font-size:15px; font-weight:bold; margin:1rem 0 0.5rem; padding:0.4rem 0.8rem; background:linear-gradient(90deg,#f0f0f0,transparent); border-left:4px solid #4CAF50; color:#333; }
'''

style_end = content.find('</style>')
if style_end > 0 and 'rep-group-header' not in content:
    content = content[:style_end] + css + content[style_end:]
    print('OK - added .rep-group-header CSS')
else:
    if 'rep-group-header' in content:
        print('OK - already exists')
    else:
        print('WARNING - failed')

with open('inventory.html', 'w', encoding='utf-8') as f:
    f.write(content)
