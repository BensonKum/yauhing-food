import re
import subprocess

# 1. 抽取 JS from inventory.html
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'<script(?:\s+[^>]*)?>([\s\S]*?)</script>'
matches = re.findall(pattern, html, re.IGNORECASE)

if len(matches) > 4:
    js = matches[4].strip()
    js = re.sub(r'//\s*<!\[CDATA\[', '', js)
    js = re.sub(r'//\s*\]\]>', '', js)
    js = js.strip()
    with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\temp_check.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"Extracted JS: {len(js)} chars")
else:
    print(f"ERROR: Only {len(matches)} script blocks found")
    exit(1)

# 2. 驗證 pinLogin 有 async
if 'async function pinLogin' in js:
    print("[OK] pinLogin() has 'async' keyword")
else:
    print("[ERROR] pinLogin() is MISSING 'async' keyword!")

# 3. 執行 node --check
result = subprocess.run(
    ['node', '--check', r'C:\Users\admin\.qclaw\workspace\yauhing-food\temp_check.js'],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='replace'
)

if result.returncode == 0:
    print("[OK] node --check: PASSED (no syntax errors)")
    print("\nReady to commit and push!")
else:
    print(f"[ERROR] node --check: FAILED (return code {result.returncode})")
    if result.stderr:
        print(f"STDERR: {result.stderr[:500]}")
