c = open('inventory.html','r',encoding='utf-8-sig').read()
ss = c.rfind('<script>')+8
se = c.rfind('</script>')
main_script = c[ss:se]
print(f'Script size: {len(main_script)} chars')

with open('tmp_final_check.js','w',encoding='utf-8',newline='\n') as f:
    f.write(main_script)

import subprocess, json

# 1. node --check
r = subprocess.run(['node','--check','tmp_final_check.js'],capture_output=True,text=True)
print(f'node --check: {"PASSED" if r.returncode==0 else "FAILED: " + r.stderr[-300:]}')

# 2. Try parsing as Function body (how browsers do it)
# Use a small node script to test
test_js = '''
try {
    new Function(require("fs").readFileSync("tmp_final_check.js","utf8"));
    console.log("Function() parse: PASSED");
} catch(e) {
    console.log("Function() parse: FAILED - " + e.message);
}
'''
with open('tmp_fn_test.js','w',encoding='utf-8',newline='\n') as f:
    f.write(test_js)
r2 = subprocess.run(['node','tmp_fn_test.js'],capture_output=True,text=True)
print(r2.stdout.strip())
if r2.stderr:
    print('STDERR:', r2.stderr[-200:])
