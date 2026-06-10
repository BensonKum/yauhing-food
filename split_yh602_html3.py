with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8') as f:
    html = f.read()

# Find exact position
idx = html.find('十年陳皮鴨湯麵')
if idx < 0:
    print('Not found')
    exit()

# Go back to find start of card
start = html.rfind('<div class="p-card', 0, idx)
# Find end (after the closing </div></div>)
end = html.find('</div></div>', idx) + len('</div></div>')

old_card = html[start:end]
print(f'Found card from {start} to {end}')
print('Old card:')
print(repr(old_card[:200]) + '...')

# New cards
card_602a = '<div class="p-card has-image" data-cat="蝦籽麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/十年陳皮鴨湯麵.jpg" alt="十年陳皮鴨湯麵" loading="lazy"></div><div class="p-info"><div class="p-cat">蝦籽麵</div><h3 class="p-name">十年陳皮鴨湯麵</h3><div class="p-note">單包</div><div class="p-price">HKD 15 (單包)</div></div></div>'

card_602 = '<div class="p-card has-image" data-cat="蝦籽麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/十年陳皮鴨湯麵6個裝.jpg" alt="十年陳皮鴨湯麵" loading="lazy"></div><div class="p-info"><div class="p-cat">蝦籽麵</div><h3 class="p-name">十年陳皮鴨湯麵</h3><div class="p-note">6個裝</div><div class="p-price">HKD 80 (6個裝)</div></div></div>'

new_cards = card_602a + '\n' + card_602

# Replace
html = html[:start] + new_cards + html[end:]

with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done! 十年陳皮鴨湯麵 split into 2 cards ✅')
