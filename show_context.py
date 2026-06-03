c = open('inventory.html', 'r', encoding='utf-8-sig').read()
import re

script_pattern = r'<script[^>]*>(.*?)</script>'
scripts = list(re.finditer(script_pattern, c, re.DOTALL))
main_script = scripts[3].group(1)

lines = main_script.split('\n')
# Show more context around line 563
print('=== Lines 555-568 ===')
for i in range(554, min(568, len(lines))):
    marker = '>>>' if i in [558, 562] else '   '
    print(f'{marker} {i+1}: {lines[i]}')
