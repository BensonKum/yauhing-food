c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# Find where to add quick button click handler
# Add after the renderLog function ends (before the next function or DOMContentLoaded)

# Find end of renderLog function
import re

# Add event delegation for quick buttons in logSidebar
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

# Find DOMContentLoaded and add before it
idx = c.find('document.addEventListener(\'DOMContentLoaded\'')
if idx >= 0:
    c = c[:idx] + js_to_add + c[idx:]
    print('OK: Quick button handler added')
else:
    print('FAIL: DOMContentLoaded not found')

open('inventory.html', 'w', encoding='utf-8-sig').write(c)
