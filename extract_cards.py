import re

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8-sig') as f:
    content = f.read()

# Find p-card divs
cards = re.findall(r'<div class="p-card".*?</div>\s*</div>', content, re.DOTALL)
print(f'Found {len(cards)} p-cards')
for i, c in enumerate(cards, 1):
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', c)
    nm = re.search(r'class="p-name">([^<]+)', c)
    img = m.group(1) if m else 'NO_IMG'
    name = nm.group(1).strip()[:25] if nm else 'NO_NAME'
    print(f'{i:2}. {name:25} | {img}')
