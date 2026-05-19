c = open('inventory.html', 'r', encoding='utf-8-sig').read()

script_start = c.rfind('<script>')
script_end = c.rfind('</script>')
main_script = c[script_start+8:script_end]

# Binary search for the syntax error
# Test progressively larger prefixes
import subprocess, sys

def test_prefix(length):
    prefix = main_script[:length]
    with open('tmp_prefix.js', 'w', encoding='utf-8', newline='\n') as f:
        f.write(prefix)
    result = subprocess.run(['node', '--check', 'tmp_prefix.js'], 
                          capture_output=True, text=True)
    ok = result.returncode == 0
    return ok

# Find approximate location by testing increasing sizes
# Start from where we know it fails (23832) and go down
sizes = [5000, 10000, 15000, 20000, 22000, 23000, 23500, 23700, 23800]
for s in sizes:
    ok = test_prefix(s)
    status = "OK" if ok else "FAIL"
    print(f'Prefix {s}: {status}')
