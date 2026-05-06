import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# NEW search: look for the actual string bytes in the new file
sh = '上海麵'.encode('utf-8')
print(f'Searching for: {sh.hex()} = "上海麵"')
print(f'File size: {len(data)} bytes')

positions = []
p = 0
while True:
    pos = data.find(sh, p)
    if pos < 0:
        break
    positions.append(pos)
    p = pos + 1

print(f'Found {len(positions)} times')
for pos in positions:
    seg = data[max(0,pos-100):pos+150]
    # Find p-card class
    pc = re.search(b'<div class="p-card ([^"]+)"', seg)
    cat = re.search(b'data-cat="([^"]+)"', seg)
    grad = re.search(b'grad-ch">([^<]+)', seg)
    print(f'  {pos}: cls={pc.group(1) if pc else "?"} cat={cat.group(1).decode("utf-8","replace") if cat else "?"} grad={grad.group(1).decode("utf-8","replace") if grad else "?"}')

# Also check if there are 2 "上海麵 (幼) 盒裝" in p-name fields
pnames = re.findall(b'p-name">([^<]+)', data)
for i, p in enumerate(pnames):
    if '上海麵' in p.decode('utf-8', errors='replace'):
        print(f'p-name #{i+1}: {p.decode("utf-8","replace")}')