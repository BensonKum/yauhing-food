c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# Check if window.editTransaction and window.deleteTransaction are complete
import re

for fn in ['window.editTransaction', 'window.deleteTransaction']:
    idx = c.find(fn)
    if idx >= 0:
        # Get the full function
        start = idx
        # Find the closing brace
        brace_count = 0
        in_fn = False
        pos = idx
        
        # Skip to the opening brace
        while pos < len(c) and c[pos] != '{':
            pos += 1
        
        # Now count braces
        brace_count = 1
        pos += 1
        while pos < len(c) and brace_count > 0:
            if c[pos] == '{':
                brace_count += 1
            elif c[pos] == '}':
                brace_count -= 1
            pos += 1
        
        full_fn = c[start:pos]
        print(f'=== {fn} (length: {len(full_fn)}) ===')
        print(full_fn[:300])
        print('...' if len(full_fn) > 300 else '')
        print()
