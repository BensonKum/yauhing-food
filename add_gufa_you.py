# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The new card for 古法大地魚蝦籽麵 (幼) - same structure as (粗) version
new_card = '''<div class="p-card has-image multi-pack" data-cat="蝦籽麵" data-stock="in"><div class="p-img"><span class="s-badge in">有庫存</span><div class="pk-sw"><button class="pk-btn active" data-pk="1">單包</button><button class="pk-btn" data-pk="2">6個裝</button></div><img src="images/古法大地魚蝦籽麵(幼).jpg" alt="古法大地魚蝦籽麵 (幼)" loading="lazy"><img src="images/古法大地魚蝦籽麵(幼)6個裝.jpg" alt="古法大地魚蝦籽麵 (幼)" loading="lazy" style="display:none;"></div><div class="p-info"><div class="p-cat">蝦籽麵</div><h3 class="p-name">古法大地魚蝦籽麵 (幼)</h3><div class="p-note">單包 / 6個裝 HKD 80</div><div class="p-price multi">HKD 15 (單包) / HKD 80 (6個裝)</div></div></div>'''

# Insert after the 古法大地魚蝦籽麵 (粗) card
target = '<div class="p-note">單包 / 6個裝 HKD 80</div><div class="p-price multi">HKD 15 (單包) / HKD 80 (6個裝)</div></div></div>'
# Find the (粗) version's closing tags and insert after it
idx = html.find('古法大地魚蝦籽麵 (粗)')
if idx < 0:
    print("ERROR: cannot find 古法大地魚蝦籽麵 (粗)")
else:
    # Find the end of this card - look for the closing </div></div> after price
    search_from = idx
    end_pattern = 'HKD 15 (單包) / HKD 80 (6個裝)</div></div>'
    end_idx = html.find(end_pattern, search_from)
    if end_idx >= 0:
        insert_pos = end_idx + len(end_pattern)
        new_html = html[:insert_pos] + '\n' + new_card + html[insert_pos:]
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        # Verify
        verify = '古法大地魚蝦籽麵 (幼)' in new_html
        print(f"Card inserted at position {insert_pos}")
        print(f"Verification (幼 exists): {verify}")
        
        # Count cards
        cards = re.findall(r'<div class="p-cat">蝦籽麵</div>', new_html)
        print(f"Total 蝦籽麵 cards: {len(cards)}")
    else:
        print("ERROR: cannot find end pattern for (粗) card")
