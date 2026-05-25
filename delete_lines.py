#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Delete '今日' button lines 1928-1931 (1-indexed)"""

with open('inventory.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines to delete: 1928-1931 (1-indexed) = indices 1927-1930
# Let's verify these are the correct lines
print("Checking lines to delete:")
for i in range(1927, 1931):
    if i < len(lines):
        print(f"  Line {i+1}: {lines[i].rstrip()}")

# Delete the 4 lines (in reverse order to preserve indices)
for i in sorted(range(1927, 1931), reverse=True):
    if i < len(lines):
        del lines[i]

with open('inventory.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Deleted 4 lines (1928-1931)")
print("'今日' button removed from sidebar!")
