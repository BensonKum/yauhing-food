#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Delete '今日' quick button from sidebar - v2 with regex"""

import re

with open('inventory.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to match the 4-line button block (flexible whitespace)
pattern = r"""    '<div class="log-card date-btn" onclick="setDateRange\(&#39;today&#39;\)">' \+\s+'<div class="num" style="font-size:1\.1rem">今日</div>' \+\s+'<div class="label">快速按鈕</div>' \+\s+'</div>' \+"""

match = re.search(pattern, content, re.MULTILINE)
if match:
    print(f"Found pattern at position {match.start()}")
    print(f"Matched: {repr(match.group()[:100])}")
    content = content[:match.start()] + content[match.end():]
    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Deleted '今日' button!")
else:
    print("Pattern not found with regex, trying line-by-line...")
    lines = content.split('\n')
    new_lines = []
    skip_until = -1
    for i, line in enumerate(lines):
        if '今日</div>' in line:
            print(f"Found '今日' at line {i+1}, removing block...")
            # Remove this line and previous 3 lines
            skip_until = i + 1
            # Also need to remove the 3 preceding lines
            # This is getting complex, let's just do string replace
            pass
    print("Please check manually.")
