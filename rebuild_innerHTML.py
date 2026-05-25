#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix logSidebar.innerHTML - force rebuild assignment"""

with open('inventory.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start of logSidebar assignment
start = -1
for i, line in enumerate(lines):
    if "document.getElementById('logSidebar').innerHTML =" in line:
        start = i
        break

if start >= 0:
    print(f"Found assignment at line {start+1}")
    # Find the end (next non-empty line that is NOT a string continuation)
    end = start + 1
    while end < len(lines):
        line = lines[end]
        stripped = line.strip()
        # String continuation starts with '  (with leading spaces)
        if stripped.startswith("'") and stripped.endswith("' +") or (stripped.startswith("'") and not stripped.endswith("';")):
            end += 1
        else:
            break
    
    print(f"Block ends at line {end}")
    print("Current block:")
    for i in range(start, min(end+2, len(lines))):
        print(f"  {i+1}: {lines[i].rstrip()}")
    
    # Now FIX: ensure all lines except last end with ' +
    # and last line ends with ';
    new_block = []
    new_block.append("  // Left sidebar cards\n")
    new_block.append("  document.getElementById('logSidebar').innerHTML =\n")
    new_block.append("    '<div style=\"height:70px;flex-shrink:0\"></div>' +\n")
    new_block.append("    '<div class=\"log-card\" style=\"background:#e8f5e9;border-left:4px solid #4caf50\"><div class=\"label\">銷售</div><div class=\"num\" style=\"color:#2e7d32;font-weight:700\">HK$'+sales.toLocaleString()+'</div></div>' +\n")
    new_block.append("    '<div class=\"log-card\" style=\"background:#fff3e0;border-left:4px solid #ff9800\"><div class=\"label\">進貨</div><div class=\"num\" style=\"color:#e65100;font-weight:700\">HK$'+purchase.toLocaleString()+'</div></div>' +\n")
    new_block.append("    '<div class=\"log-card\" style=\"background:#e3f2fd;border-left:4px solid #2196f3\"><div class=\"label\">淨額</div><div class=\"num\" style=\"color:#1565c0;font-weight:700\">'+(net>=0?'+':'')+'HK$'+net.toLocaleString()+'</div></div>';\n")
    
    # Replace
    lines[start:end] = new_block
    
    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    with open('fix_status.txt', 'w') as f:
        f.write('FIXED')
    print("\nDone! Rebuilt innerHTML assignment.")
else:
    with open('fix_status.txt', 'w') as f:
        f.write('NOT_FOUND')
    print("Assignment not found!")
