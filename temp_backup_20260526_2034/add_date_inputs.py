#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add date inputs back to renderLog() sidebar generation"""

with open('inventory.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The innerHTML assignment ends with the 淨額 card
# We need to ADD the date inputs AFTER the 淨額 card and BEFORE the closing ';
old_ending = "'</div></div>';\n\n  // Right side: summary + list"
new_ending = """'</div></div>' +\n    '<div style=\"margin-top:1rem;\">' +
      '<input type=\"date\" id=\"logFromDate\" class=\"filter-select\" style=\"width:130px\">' +
      '<span style=\"margin:0 .5rem;color:var(--muted)\">至</span>' +
      '<input type=\"date\" id=\"logToDate\" class=\"filter-select\" style=\"width:130px\">' +
    '</div>';\n\n  // Right side: summary + list"""

if old_ending in content:
    content = content.replace(old_ending, new_ending)
    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.write(content)
    with open('fix_status.txt', 'w') as f:
        f.write('FIXED')
    print('Fixed! Added date inputs back to renderLog() sidebar.')
else:
    with open('fix_status.txt', 'w') as f:
        f.write('NOT_FOUND')
    print('Pattern not found! Checking...')
    # Find what's there
    idx = content.find('淨額')
    if idx >= 0:
        print(repr(content[idx:idx+200]))
