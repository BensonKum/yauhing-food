data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
insert_at = 58689

cards = [
    ('上海麵 (幼) 盒裝', 'e67d59'),
    ('河粉 盒裝', 'e6a832'),
    ('油麵 盒裝', '4CAF50'),
    ('生幼麵 盒裝', '2196F3'),
    ('生粗麵 盒裝', '3F51B5'),
    ('豆卜 盒裝', '9C27B0'),
    ('瀨粉 盒裝', '00BCD4'),
    ('銀針粉 盒裝', '795548'),
    ('水餃皮 盒裝', 'f44336'),
    ('雲吞皮 盒裝', 'FF9800'),
    ('齋腸粉 盒裝', '9E9E9E'),
    ('蝦米腸粉 盒裝', '607D8B'),
]

html = ''
for name, color in cards:
    html += f'''<div class="p-card no-image" data-cat="新鮮粉麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><div class="grad-card" style="background:linear-gradient(135deg,#{color},#{color}88);"><span class="grad-ch">{name}</span></div></div><div class="p-info"><div class="p-cat">新鮮粉麵</div><h3 class="p-name">{name}</h3><div class="p-price">HKD --</div></div></div>
'''

new_data = data[:insert_at] + html.encode('utf-8') + data[insert_at:]
open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'wb').write(new_data)
print(f'Inserted {len(cards)} cards at byte {insert_at}')
print(f'New file size: {len(new_data)} (was {len(data)})')