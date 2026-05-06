data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# Check 新鮮粉麵 count (button + card cats)
s1 = '新鮮粉麵'.encode('utf-8')
count = data.count(s1)
print(f'新鮮粉麵 occurrences: {count}')

# Check 12 new p-card no-image elements
no_img = data.count(b'p-card no-image')
print(f'p-card no-image count: {no_img}')

# Count total p-card
total = data.count(b'p-card ')
print(f'Total p-card count: {total}')

# Check the insert area
insert_area = data[58680:58850]
print('\nAround insert:')
print(insert_area.decode('utf-8', errors='replace')[:200])