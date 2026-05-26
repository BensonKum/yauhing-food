#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Force rebuild logSidebar innerHTML assignment (correct version)"""

with open('inventory.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the START of the assignment (line with "document.getElementById('logSidebar').innerHTML =")
start_idx = -1
for i, line in enumerate(lines):
    if "document.getElementById('logSidebar').innerHTML =" in line:
        start_idx = i
        break

if start_idx < 0:
    print("ERROR: Could not find assignment!")
    with open('fix_status.txt', 'w') as f:
        f.write('NOT_FOUND')
else:
    print(f"Found assignment at line {start_idx+1}")
    
    # The block to replace is lines start_idx to start_idx+4 (5 lines total)
    # (assignment + 4 string lines)
    # Actually, let's find the REAL end: last line ending with ";
    end_idx = start_idx + 1
    while end_idx < len(lines):
        if lines[end_idx].strip().endswith("';'"):
            break
        end_idx += 1
    
    print(f"Block ends at line {end_idx+1}")
    print("Current block:")
    for i in range(start_idx, end_idx+1):
        print(f"  {i+1}: {lines[i].rstrip()}")
    
    # Now REPLACE lines[start_idx:end_idx+1] with correct block
    new_block = [
        "  // Left sidebar cards\n",
        "  document.getElementById('logSidebar').innerHTML =\n",
        "    '<div style=\"height:70px;flex-shrink:0\"></div>' +\n",
        "    '<div class=\"log-card\" style=\"background:#e8f5e9;border-left:4px solid #4caf50\"><div class=\"label\">銷售</div><div class=\"num\" style=\"color:#2e7d32;font-weight:700\">HK$'+sales.toLocaleString()+'</div></div>' +\n",
        "    '<div class=\"log-card\" style=\"background:#fff3e0;border-left:4px solid #ff9800\"><div class=\"label\">進貨</div><div class=\"num\" style=\"color:#e65100;font-weight:700\">HK$'+purchase.toLocaleString()+'</div></div>' +\n",
        "    '<div class=\"log-card\" style=\"background:#e3f2fd;border-left:4px solid #2196f3\"><div class=\"label\">淨額</div><div class=\"num\" style=\"color:#1565c0;font-weight:700\">'+(net>=0?'+':'')+'HK$'+net.toLocaleString()+'</div></div>';\n"
    ]
    
    # Replace
    lines[start_idx:end_idx+1] = new_block
    
    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    with open('fix_status.txt', 'w') as f:
        f.write('FIXED')
    print("\nDone! Rebuilt innerHTML assignment.")
