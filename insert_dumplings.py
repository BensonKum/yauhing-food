#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert 2 dumpling product cards after last 素纖麵 card in index.html"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Dumpling cards HTML
dumpling_html = '''
<!-- 餃子系列：白菜餃 (YH509) -->
<div class="p-card has-image" data-cat="餃子系列" data-stock="in">
  <div class="p-img">
    <span class="s-badge in">有庫存</span>
    <img src="images/product_cabbage_dumpling.jpg" alt="白菜餃" loading="lazy">
  </div>
  <div class="p-info">
    <div class="p-cat">餃子系列</div>
    <h3 class="p-name">白菜餃</h3>
    <div class="p-price">HKD 25</div>
  </div>
</div>

<!-- 餃子系列：麻辣餃 (YH510) -->
<div class="p-card has-image" data-cat="餃子系列" data-stock="in">
  <div class="p-img">
    <span class="s-badge in">有庫存</span>
    <img src="images/product_spicy_dumpling.jpg" alt="麻辣餃" loading="lazy">
  </div>
  <div class="p-info">
    <div class="p-cat">餃子系列</div>
    <h3 class="p-name">麻辣餃</h3>
    <div class="p-price">HKD 25</div>
  </div>
</div>
'''

# Find last 素纖麵 card
# Pattern: <div class="p-card ... data-cat="素纖麵" ...> ... </div>
# We need to find the last </div> that closes a 素纖麵 card
# Strategy: Find all 素纖麵 cards, get the last one's closing position

pattern = r'<div class="p-card[^"]*" data-cat="素纖麵"[^>]*>.*?</div>\s*</div>\s*</div>'

# Use non-greedy match with DOTALL
matches = list(re.finditer(r'<div class="p-card[^"]*" data-cat="素纖麵"[^>]*>(?:.*?)</div>\s*</div>\s*</div>', content, re.DOTALL))

if not matches:
    print('ERROR: Cannot find any 素纖麵 card!')
    exit(1)

last_match = matches[-1]
insert_pos = last_match.end()

print(f'Found {len(matches)} 素纖麵 card(s)')
print(f'Inserting after position: {insert_pos}')
print(f'Context (50 chars): ...{content[insert_pos-50:insert_pos+50]}...')

# Insert dumpling HTML
new_content = content[:insert_pos] + dumpling_html + content[insert_pos:]

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('SUCCESS: Dumpling cards inserted!')
print(f'File size: {len(new_content)} bytes')
