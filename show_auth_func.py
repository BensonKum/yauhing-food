import re

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\temp_check.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 抽取 authLogin 函數
m = re.search(r'function\s+authLogin\s*\([^)]*\)\s*\{', js)
if m:
    start = m.start()
    # 搵匹配嘅結束大括號
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
        if c in ('\'', '"'):
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
    print("=== authLogin() function ===")
    print(func_code[:2000])  # 首 2000 字符
    if len(func_code) > 2000:
        print(f"\n... (truncated, total {len(func_code)} chars)")
else:
    print("authLogin() function not found")
