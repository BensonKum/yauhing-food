import re

with open('index.html', encoding='utf-8-sig') as f:
    content = f.read()

# Find insertion point
search = '</div></div></div></section><section class="ab" id="about">'
idx = content.find(search)
print(f'Found at position: {idx}')

# New product cards - 新鮮粉麵 category
new_cards = '''<div class="p-card has-image" data-cat="新鮮粉麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/product_shanghai_fine_noodle.jpg" alt="上海麵 (幼) 盒裝" loading="lazy"></div><div class="p-info"><div class="p-cat">新鮮粉麵</div><h3 class="p-name">上海麵 (幼) 盒裝</h3><div class="p-price">HKD 10</div></div></div>
<div class="p-card has-image" data-cat="新鮮粉麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/product_shanghai_thick_noodle.jpg" alt="上海麵(粗)盒裝" loading="lazy"></div><div class="p-info"><div class="p-cat">新鮮粉麵</div><h3 class="p-name">上海麵(粗)盒裝</h3><div class="p-price">HKD 10</div></div></div>
'''

# Insert before the closing section
new_content = content.replace(search, new_cards + search)

with open('index.html', 'w', encoding='utf-8-sig') as f:
    f.write(new_content)

print('Done! Cards inserted.')
