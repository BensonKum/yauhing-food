import re

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== Checking login functions ===\n")

# 1. 檢查 authLogin() 函數
auth_pattern = r'function\s+authLogin\s*\([^)]*\)\s*\{'
auth_match = re.search(auth_pattern, html)
if auth_match:
    start = auth_match.start()
    brace_count = 0
    in_string = False
    string_char = None
    end = start
    
    for i in range(start + len(auth_match.group()) - 1, len(html)):
        c = html[i]
        if in_string:
            if c == string_char and html[i-1] != '\\':
                in_string = False
            i += 1
            continue
        if c in ("'", '"'):
            in_string = True
            string_char = c
            i += 1
            continue
        if c == '{':
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    
    auth_func = html[start:end]
    print(f"[OK] authLogin() found: {len(auth_func)} chars")
    print(f"Content (first 1000 chars):\n{auth_func[:1000]}\n")
    
    # 檢查是否有明顯問題
    if 'auth.signInWithEmailAndPassword' in auth_func:
        print("[OK] auth.signInWithEmailAndPassword call found")
    else:
        print("[WARN] auth.signInWithEmailAndPassword call NOT found")
        
    if 'firebase.auth()' in html or 'const auth' in html:
        print("[OK] Firebase auth object initialization found")
    else:
        print("[WARN] Firebase auth object initialization NOT found")
else:
    print("[ERROR] authLogin() function NOT FOUND!\n")

# 2. 檢查 pinLogin() 函數
pin_pattern = r'async\s+function\s+pinLogin\s*\([^)]*\)\s*\{'
pin_match = re.search(pin_pattern, html)
if not pin_match:
    pin_pattern = r'function\s+pinLogin\s*\([^)]*\)\s*\{'
    pin_match = re.search(pin_pattern, html)

if pin_match:
    start = pin_match.start()
    brace_count = 0
    in_string = False
    string_char = None
    end = start
    
    for i in range(start + len(pin_match.group()) - 1, len(html)):
        c = html[i]
        if in_string:
            if c == string_char and html[i-1] != '\\':
                in_string = False
            i += 1
            continue
        if c in ("'", '"'):
            in_string = True
            string_char = c
            i += 1
            continue
        if c == '{':
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break
    
    pin_func = html[start:end]
    print(f"\n[OK] pinLogin() found: {len(pin_func)} chars")
    print(f"Has 'async': {'async' in pin_func[:20]}")
    print(f"Content (first 1000 chars):\n{pin_func[:1000]}\n")
    
    # 檢查是否有明顯問題
    if 'await db.collection' in pin_func:
        print("[OK] 'await db.collection' found (async function)")
    else:
        print("[WARN] 'await db.collection' NOT found")
        
    if 'db.collection' in pin_func:
        print("[OK] db.collection call found")
    else:
        print("[WARN] db.collection call NOT found")
else:
    print("\n[ERROR] pinLogin() function NOT FOUND!\n")

# 3. 檢查 Firebase 初始化
print("\n=== Firebase Initialization ===")
if 'firebase.initializeApp' in html:
    print("[OK] firebase.initializeApp found")
    # 擷取配置
    config_match = re.search(r'const\s+firebaseConfig\s*=\s*\{[^}]+\};', html, re.DOTALL)
    if config_match:
        print(f"[OK] firebaseConfig found")
    else:
        print("[WARN] firebaseConfig NOT found")
else:
    print("[ERROR] firebase.initializeApp NOT FOUND!")

if 'const auth = firebase.auth()' in html or 'let auth = firebase.auth()' in html or 'var auth = firebase.auth()' in html:
    print("[OK] 'const auth = firebase.auth()' found")
else:
    print("[WARN] 'auth = firebase.auth()' NOT found - may cause auth.signInWithEmailAndPassword to fail")

if 'const db = firebase.firestore()' in html or 'let db = firebase.firestore()' in html or 'var db = firebase.firestore()' in html:
    print("[OK] 'const db = firebase.firestore()' found")
else:
    print("[WARN] 'db = firebase.firestore()' NOT found - may cause db.collection to fail")

# 4. 檢查 window.* 賦值
print("\n=== window.* Assignments ===")
for fn in ['authLogin', 'pinLogin', 'showPinLogin', 'showEmailLogin', 'showApp']:
    if re.search(rf'\bwindow\.{fn}\s*=\s*{fn}', html) or re.search(rf'\bwindow\.{fn}\s*=\s*function', html):
        print(f"  [OK] window.{fn} assigned")
    elif fn in html:
        print(f"  [WARN] {fn} defined but window.{fn} NOT assigned (HTML onclick may fail)")
    else:
        print(f"  [MISSING] {fn} NOT found")
