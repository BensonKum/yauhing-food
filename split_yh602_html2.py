with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8') as f:
    html = f.read()

# Extract the exact string from file
start_marker = '<div class="p-card has-image" data-cat="蝦籽麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><div class="pk-sw"><button class="pk-btn active" data-pk="1">單包</button><button class="pk-btn" data-pk="2">6個裝</button></div><img src="images/十年陳皮鴨湯麵.jpg" alt="十年陳皮鴨湯麵" loading="lazy"><img src="images/十年陳皮鴨湯麵6個裝.jpg" alt="十年陳皮鴨湯麵" loading="lazy" style="display:none;"></div><div class="p-info"><div class="p-cat">蝦籽麵</div><h3 class="p-name">十年陳皮鴨湯麵</h3><div class="p-note">單包 / 6個裝 HKD 80</div><div class="p-price multi">HKD 15 (單包) / HKD 80 (6個裝)</div></div></div>'

card_602a = '<div class="p-card has-image" data-cat="蝦籽麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/十年陳皮鴨湯麵.jpg" alt="十年陳皮鴨湯麵" loading="lazy"></div><div class="p-info"><div class="p-cat">蝦籽麵</div><h3 class="p-name">十年陳皮鴨湯麵</h3><div class="p-note">單包</div><div class="p-price">HKD 15 (單包)</div></div></div>'

card_602 = '<div class="p-card has-image" data-cat="蝦籽麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/十年陳皮鴨湯麵6個裝.jpg" alt="十年陳皮鴨湯麵" loading="lazy"></div><div class="p-info"><div class="p-cat">蝦籽麵</div><h3 class="p-name">十年陳皮鴨湯麵</h3><div class="p-note">6個裝</div><div class="p-price">HKD 80 (6個裝)</div></div></div>'

if start_marker in html:
    html = html.replace(start_marker, card_602a + card_602)
    print('Replaced ✅')
else:
    # Try to find with different quote style
    idx = html.find('十年陳皮鴨湯麵')
    if idx > 0:
        # Get surrounding context
        context = html[idx-200:idx+600]
        print('Context found:')
        print(repr(context))
    else:
        print('Not found at all')

with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
