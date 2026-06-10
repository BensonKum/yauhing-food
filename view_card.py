with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8') as f:
    c = f.read()

idx = c.find('十年陳皮鴨湯麵')
start = c.rfind('<div class="p-card', 0, idx)
end = c.find('</div></div>', idx) + len('</div></div>')

card = c[start:end]
print('Current 十年陳皮 card:')
print(card)