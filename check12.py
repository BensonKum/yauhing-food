data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# Check for all 12 fresh powder items
items = ['上海麵', '河粉', '油麵', '生幼麵', '生粗麵', '豆卜', '瀨粉', '銀針粉', '水餃皮', '雲吞皮', '齋腸粉', '蝦米腸粉']
for item in items:
    count = data.count(item.encode('utf-8'))
    print(f'{item}: {count}')

print(f'\nTotal p-card no-image: {data.count(b"p-card no-image")}')
print(f'Total p-card: {data.count(b"p-card ")}')
print(f'File size: {len(data)}')