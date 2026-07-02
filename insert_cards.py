# Insert YH502, YH503 cards after line 309 in index.html
import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 309 (0-indexed: 308)
target_line = 308  # 0-indexed
print(f"Line 309 content (first 80 chars): {lines[target_line][:80]}...")

# New cards HTML (strictly follow Ben's data - no extra content)
new_cards = '''<div class="p-card has-image" data-cat="罐頭/零售裝" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/product_sauce_set.jpg" alt="醬油套裝 (稻米油，豉油，雞精)" loading="lazy"></div><div class="p-info"><div class="p-cat">罐頭/零售裝</div><h3 class="p-name">醬油套裝 (稻米油，豉油，雞精)</h3><div class="p-price">HKD 20</div></div></div>
<div class="p-card has-image" data-cat="罐頭/零售裝" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><img src="images/product_rice_oil_150ml.jpg" alt="稻米油 150ml" loading="lazy"></div><div class="p-info"><div class="p-cat">罐頭/零售裝</div><h3 class="p-name">稻米油 150ml</h3><div class="p-price">HKD 10</div></div></div>
'''

# Insert after target_line
lines.insert(target_line + 1, new_cards)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Inserted YH502, YH503 cards after line 309")
print(f"Total lines: {len(lines)}")
