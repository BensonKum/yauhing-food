import os

img_dir = r'C:\Users\admin\.qclaw\workspace\yauhing-food\images'
files = sorted(os.listdir(img_dir))
print(f'Total images: {len(files)}')
for f in files:
    print(f)
