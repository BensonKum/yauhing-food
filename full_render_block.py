# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 搵從 snap.forEach 到 repList.innerHTML 的完整區塊
start = content.find('snap.forEach(doc => {')
end = content.find("document.getElementById('repList').innerHTML", start)

print(content[start:end+120])
