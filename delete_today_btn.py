#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Delete '今日' quick button from sidebar in inventory.html"""

import re

with open('inventory.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to delete: the entire 4-line "今日" button block
# The button starts with '<div class="log-card date-btn"' and ends with "'</div>';"
old_pattern = """    '<div class="log-card date-btn" onclick="setDateRange(&#39;today&#39;)">' +
      '<div class="num" style="font-size:1.1rem">今日</div>' +
      '<div class="label">快速按鈕</div>' +
    '</div>' +"""

# Replace with empty string (delete it)
new_content = content.replace(old_pattern, '')

if new_content == content:
    print("ERROR: Pattern not found! Trying alternate match...")
    # Try with slightly different whitespace
    if "'</div>' +" in content:
        print("Found '</div>' + pattern, checking context...")
else:
    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Deleted '今日' button from sidebar!")
    print(f"Lines removed: 4")
