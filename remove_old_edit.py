c = open('inventory.html', 'r', encoding='utf-8-sig').read()

script_start = c.rfind('<script>')
script_end = c.rfind('</script>')
before_script = c[:script_start+8]
after_script = c[script_end:]
main_script = c[script_start+8:script_end]

# Remove old edit functions (positions 298 to 3429)
new_main = main_script[:298] + main_script[3429:]

# Reassemble
new_c = before_script + new_main + after_script

with open('inventory.html', 'w', encoding='utf-8-sig', newline='\n') as f:
    f.write(new_c)

print(f'Removed 3131 chars of old edit functions')
print(f'New script size: {len(new_main)} (was {len(main_script)})')
print(f'New file size: {len(new_c)} (was {len(c)})')

# Verify with node --check
import subprocess
with open('tmp_verify.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_main)
r = subprocess.run(['node', '--check', 'tmp_verify.js'], capture_output=True, text=True)
if r.returncode == 0:
    print('node --check: PASSED!')
else:
    print(f'node --check: FAILED - {r.stderr[-200:]}')
