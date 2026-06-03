c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# Add CSS for quick buttons after .log-card .num
css_to_add = '''.quick-btns{display:flex;gap:.4rem;margin-bottom:.5rem;flex-wrap:wrap;justify-content:center}
.quick-btn{background:#f5f5f5;border:1px solid #ddd;border-radius:12px;padding:.3rem .6rem;font-size:.75rem;cursor:pointer;transition:all .2s}
.quick-btn:hover{background:#e0e0e0}
.quick-btn.active{background:var(--red);color:white;border-color:var(--red)}
.log-date-card input[type="date"]{width:100%;padding:.3rem;border:1px solid #ddd;border-radius:8px;font-size:.85rem;text-align:center}
'''

# Find .log-card .num CSS
idx = c.find('.log-card .num{')
if idx >= 0:
    # Find closing brace
    brace_start = idx + len('.log-card .num{')
    brace_count = 1
    pos = brace_start
    while brace_count > 0 and pos < len(c):
        if c[pos] == '{':
            brace_count += 1
        elif c[pos] == '}':
            brace_count -= 1
        pos += 1
    # Insert new CSS after closing brace
    insert_pos = pos
    c = c[:insert_pos] + '\n' + css_to_add + c[insert_pos:]
    print('OK: CSS added')
else:
    print('FAIL: .log-card .num not found')

open('inventory.html', 'w', encoding='utf-8-sig').write(c)
