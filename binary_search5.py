c = open('inventory.html', 'r', encoding='utf-8-sig').read()

script_start = c.rfind('<script>')
script_end = c.rfind('</script>')
main_script = c[script_start+8:script_end]

import subprocess

def test_prefix(length):
    prefix = main_script[:length]
    with open('tmp_prefix.js', 'w', encoding='utf-8', newline='\n') as f:
        f.write(prefix)
    result = subprocess.run(['node', '--check', 'tmp_prefix.js'], 
                          capture_output=True, text=True)
    ok = result.returncode == 0
    if not ok:
        print(f'Prefix {length}: FAIL - {result.stderr.strip()[-100:]}')
    else:
        print(f'Prefix {length}: OK')

# Character by character around 3420-3435
for s in range(3420, 3436):
    test_prefix(s)

# Show the exact area
print('\n=== Chars 3400-3450 ===')
chunk = main_script[3400:3450]
with open('tmp_problem_area.txt', 'w', encoding='utf-8') as f:
    f.write(chunk)
print('Written to tmp_problem_area.txt')
