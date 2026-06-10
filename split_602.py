with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8') as f:
    c = f.read()

# Find the multi-pack card
idx = c.find('十年陳皮鴨湯麵')
start = c.rfind('<div class="p-card', 0, idx)
end = c.find('</div></div>', idx) + len('</div></div>')

old_card = c[start:end]
print('Old card:')
print(old_card)
print()

# New cards
card_602a = '<div class="p-card has-image" data-cat="蝦籽麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/十年陳皮鴨湯麵.jpg" alt="十年陳皮鴨湯麵" loading="lazy"></div><div class="p-info"><div class="p-cat">蝦籽麵</div><h3 class="p-name">十年陳皮鴨湯麵</h3><div class="p-note">單包</div><div class="p-price">HKD 15 (單包)</div></div></div>'

card_602 = '<div class="p-card has-image" data-cat="蝦籽麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/十年陳皮鴨湯麵6個裝.jpg" alt="十年陳皮鴨湯麵" loading="lazy"></div><div class="p-info"><div class="p-cat">蝦籽麵</div><h3 class="p-name">十年陳皮鴨湯麵</h3><div class="p-note">6個裝</div><div class="p-price">HKD 80 (6個裝)</div></div></div>'

new_cards = card_602a + '\n' + card_602

c = c[:start] + new_cards + c[end:]

with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('✅ Split into 2 cards:')
print('Card 1 (單包):', card_602a)
print('Card 2 (6個裝):', card_602)