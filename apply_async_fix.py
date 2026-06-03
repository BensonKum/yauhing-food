import re
import subprocess
import sys

# 1. 讀取 inventory.html
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2. 檢查並加 async 到 pinLogin()
if 'async function pinLogin' in html:
    print("[OK] pinLogin() already has async")
    result = "already_fixed"
elif 'function pinLogin()' in html:
    html = html.replace('function pinLogin(){', 'async function pinLogin(){', 1)
    print("[OK] Added async to pinLogin()")
    result = "fixed"
else:
    print("[ERROR] function pinLogin(){ not found!")
    sys.exit(1)

# 3. 儲存
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("[OK] Saved inventory.html")

# 4. 抽取 JS (block 4)
pattern = r'<script(?:\s+[^>]*)?>([\s\S]*?)</script>'
matches = re.findall(pattern, html, re.IGNORECASE)
if len(matches) > 4:
    js = matches[4].strip()
    js = re.sub(r'//\s*<!\[CDATA\[', '', js)
    js = re.sub(r'//\s*\]\]>', '', js)
    js = js.strip()
    with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\temp_check2.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"[OK] Extracted JS: {len(js)} chars")
    
    # 5. 執行 node --check
    r = subprocess.run(
        ['node', '--check', r'C:\Users\admin\.qclaw\workspace\yauhing-food\temp_check2.js'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    if r.returncode == 0:
        print("[OK] node --check: PASSED")
        print("\n=== READY TO COMMIT ===")
    else:
        print(f"[ERROR] node --check: FAILED (return code {r.returncode})")
        if r.stderr:
            print(f"STDERR: {r.stderr[:500]}")
        sys.exit(1)
else:
    print(f"[ERROR] Only {len(matches)} script blocks found")
    sys.exit(1)
