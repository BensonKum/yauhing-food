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
    return result.returncode == 0

# Between 3400 and 3500
for s in range(3400, 3510, 10):
    ok = test_prefix(s)
    status = "OK" if ok else "FAIL"
    print(f'Prefix {s}: {status}')

# Fine grain
print('\n--- Fine grain ---')
for s in range(3440, 3510, 5):
    ok = test_prefix(s)
    status = "OK" if ok else "FAIL"
    print(f'Prefix {s}: {status}')
