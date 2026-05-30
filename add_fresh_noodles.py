"""Add 新鮮粉麵 products to index.html"""
import json

# Read products.json
with open('products.json', 'r', encoding='utf-8-sig') as f:
    products = json.load(f)

# Filter 新鮮粉麵 products
fresh = [p for p in products if p.get('cat') == '新鮮粉麵']
print(f"Found {len(fresh)} 新鮮粉麵 products")

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Generate HTML for each product
new_cards = []
for p in fresh:
    name = p['name']
    price = p['price']
    sku = p['sku']
    img = p.get('local_img') or p.get('image') or ''
    if img:
        img_tag = f'<img src="images/{img}" alt="{name}" loading="lazy">'
    else:
        img_tag = f'<img src="images/placeholder.jpg" alt="{name}" loading="lazy">'
    
    card = f'''<!-- 新鮮粉麵：{name} ({sku}) -->
<div class="p-card has-image" data-cat="新鮮粉麵" data-stock="in">
  <div class="p-img">
    <span class="s-badge in">有庫存</span>
    {img_tag}
  </div>
  <div class="p-info">
    <div class="p-cat">新鮮粉麵</div>
    <h3 class="p-name">{name}</h3>
    <div class="p-price">{price}</div>
  </div>
</div>'''
    new_cards.append(card)

new_html = '\n'.join(new_cards)
print(f"Generated {len(new_cards)} product cards")

# Find insertion point: before </div></div></section><section class="ab"
# This is after the last product card
marker = '</div></div></section><section class="ab"'
idx = html.find(marker)
if idx == -1:
    print("ERROR: Could not find insertion point")
    exit(1)

print(f"Insertion point found at position {idx}")

# Insert new cards
new_html_content = html[:idx] + new_html + '\n' + html[idx:]

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html_content)

print("Done! 新鮮粉麵 products added to index.html")
