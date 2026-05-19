c = open('inventory.html', 'r', encoding='utf-8-sig').read()

script_start = c.rfind('<script>')
script_end = c.rfind('</script>')
before_script = c[:script_start+8]
after_script = c[script_end:]
main_script = c[script_start+8:script_end]

# Remove the window.xxx assignment block for old edit functions
old_block = 'window.openEditModal=openEditModal;window.closeEditModal=closeEditModal;window.buildEditItemRow=buildEditItemRow;window.addEditItemRow=addEditItemRow;window.saveEditTransaction=saveEditTransaction;'

if old_block in main_script:
    new_main = main_script.replace(old_block, '')
    print(f'Removed window assignment block ({len(old_block)} chars)')
else:
    print('WARNING: window block not found as exact string')
    # Try finding it
    idx = main_script.find('window.openEditModal')
    if idx >= 0:
        print(f'Found at {idx}: {repr(main_script[idx:idx+150])}')
    new_main = main_script

new_c = before_script + new_main + after_script

with open('inventory.html', 'w', encoding='utf-8-sig', newline='\n') as f:
    f.write(new_c)

# Verify
import subprocess
ss2 = new_c.rfind('<script>')+8
se2 = new_c.rfind('</script>')
new_script_content = new_c[ss2:se2]
with open('tmp_verify3.js','w',encoding='utf-8',newline='\n') as f:
    f.write(new_script_content)
r = subprocess.run(['node','--check','tmp_verify3.js'],capture_output=True,text=True)
print(f'node --check: {"PASSED!" if r.returncode==0 else "FAILED - " + r.stderr[-200:]}')

# Double check no remaining references to deleted functions
for term in ['openEditModal','closeEditModal','buildEditItemRow','addEditItemRow','saveEditTransaction']:
    idx = new_script_content.find(term)
    print(f'{term}: {"STILL PRESENT at " + str(idx) if idx >= 0 else "OK - removed"}')
