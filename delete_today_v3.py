#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Delete '今日' button and fix trailing + (correct version)"""

with open('inventory.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the "今日" button block
# Lines 1928-1931 (1-indexed) = indices 1927-1930
# But let's find it dynamically
start_del = -1
for i, line in enumerate(lines):
    if '今日</div>' in line:
        start_del = i - 1  # Line before "今日" (starts with '<div class="log-card date-btn"')
        break

if start_del >= 0:
    # The button spans 4 lines: start_del, start_del+1, start_del+2, start_del+3
    # But the FIRST line ends with ' +' (continuation)
    # And the LAST line (start_del+3) ends with "' +" (continuation)
    # After deletion, we need to remove the trailing ' +' from line start_del-1
    
    print(f"Found '今日' button at lines {start_del+1}-{start_del+4}")
    
    # Fix the line BEFORE the button (remove trailing ' +')
    prev_line = lines[start_del - 1]
    if prev_line.rstrip().endswith("' +"):
        lines[start_del - 1] = prev_line.rstrip().rstrip('+').rstrip() + "';\n"
        print(f"Fixed line {start_del} (removed trailing +)")
    
    # Now delete the 4 button lines
    del lines[start_del:start_del+4]
    print(f"Deleted lines {start_del+1}-{start_del+4}")
    
    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    with open('fix_status.txt', 'w') as f:
        f.write('FIXED')
    print("\nDone!")
else:
    with open('fix_status.txt', 'w') as f:
        f.write('NOT_FOUND')
    print("'今日' button not found!")
