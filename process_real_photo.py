from PIL import Image
import os

src = r'C:\Users\admin\.qclaw\media\inbound\af2ca01f-4023-4e11-9c7c-d8f8a592a1f9.jpg'
dst = r'C:\Users\admin\.qclaw\workspace\yauhing-food\images\product_sauce_set.jpg'

img = Image.open(src).convert('RGB')
w, h = img.size
s = min(w, h)
left = (w - s) // 2
top = (h - s) // 2
img = img.crop((left, top, left+s, top+s))
img = img.resize((800, 800), Image.LANCZOS)
img.save(dst, 'JPEG', quality=85, optimize=True)
print(f'Done: {os.path.getsize(dst)//1024}KB')
