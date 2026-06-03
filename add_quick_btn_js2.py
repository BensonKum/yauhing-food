c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# Find where to add quick button click handler
# Add before </script> that contains renderLog

js_to_add = '''
// Quick button click handler for log date card
document.getElementById('logSidebar').addEventListener('click', function(e){
  if(e.target.classList.contains('quick-btn')){
    const days = parseInt(e.target.dataset.days);
    quickDays = days;
    document.getElementById('logDateInput').value = '';
    renderLog();
  }
});

'''

# Find renderLog function and insert after its closing brace
import re

# Find the renderLog function definition
idx = c.find('async function renderLog()')
if idx >= 0:
    # Find the matching closing brace for the function
    # Count braces from the function start
    brace_count = 0
    pos = idx
    started = False
    while pos < len(c):
        if c[pos] == '{':
            brace_count += 1
            started = True
        elif c[pos] == '}':
            brace_count -= 1
            if started and brace_count == 0:
                # Found function end
                insert_pos = pos + 1
                c = c[:insert_pos] + js_to_add + c[insert_pos:]
                print(f'OK: Handler added after renderLog (pos {insert_pos})')
                break
        pos += 1
    else:
        print('FAIL: Could not find function end')
else:
    print('FAIL: renderLog not found')

open('inventory.html', 'w', encoding='utf-8-sig').write(c)
