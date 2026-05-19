c = open('inventory.html', 'r', encoding='utf-8-sig').read()
import re

script_pattern = r'<script[^>]*>(.*?)</script>'
scripts = list(re.finditer(script_pattern, c, re.DOTALL))
main_script = scripts[3].group(1)

lines = main_script.split('\n')
print(f'Total lines: {len(lines)}')
print(f'\n=== Line 560-570 ===')
for i in range(558, min(570, len(lines))):
    marker = '>>>' if i == 562 else '   '
    print(f'{marker} {i+1}: {lines[i]}')
