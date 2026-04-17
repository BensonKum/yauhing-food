import re

f = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8-sig')
c = f.read()
f.close()

# Find all image src references
imgs = re.findall(r'images/([^"\']+\.jpg)', c)
print('Images used in index.html:', len(imgs))
for i, img in enumerate(imgs):
    print(i + 1, img)
