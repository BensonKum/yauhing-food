import re

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\temp_check.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 抽取 pinLogin 函數
m = re.search(r'function\s+pinLogin\s*\([^)]*\)\s*\{', js)
if m:
    start = m.start()
    brace_count = 0
    in_string = False
    string_char = None
    end = start + len(m.group())
    
    for i in range(start + len(m.group()) - 1, len(js)):
        c = js[i]
        if in_string:
            if c == string_char and js[i-1] != '\\':
                in_string = False
            continue
        if c in ("'", '"'):
            in_string = True
            string_char = c
            continue
        if c == '{':
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    
    func_code = js[start:end]
    print("=== pinLogin() function ===")
    print(func_code[:1500])
    if len(func_code) > 1500:
        print(f"\n... (truncated, total {len(func_code)} chars)")
else:
    print("pinLogin() function not found")

# 檢查 pinInput 嘅使用
print("\n=== pinInput references ===")
pin_refs = [(i, js[i:i+50]) for i in range(len(js)) if js[i:i+9] == 'pinInput']
print(f"Found {len(pin_refs)} references to 'pinInput'")
for pos, context in pin_refs[:5]:
    print(f"  At {pos}: {context!r}")
