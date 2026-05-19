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
    return result.returncode == 0, result.stderr

# Narrow down
sizes = [1000, 2000, 3000, 4000]
for s in sizes:
    ok, err = test_prefix(s)
    status = "OK" if ok else "FAIL"
    print(f'Prefix {s}: {status}')
    if not ok:
        # Show last 200 chars
        print(f'  Last 200 chars: {repr(main_script[max(0,s-200):s])}')
