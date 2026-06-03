import sys

html_path = r"C:\Users\admin\.qclaw\workspace\yauhing-food\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 在「特色麵」按鈕後面加「餃子系列」分類
old = '<button class="t-btn" data-cat="特色麵">特色麵</button><button class="t-btn" data-cat="禮盒套裝">禮盒套裝</button>'
new = '<button class="t-btn" data-cat="特色麵">特色麵</button><button class="t-btn" data-cat="餃子系列">餃子系列</button><button class="t-btn" data-cat="禮盒套裝">禮盒套裝</button>'

if old in content:
    content = content.replace(old, new, 1)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done! 餃子系列分類已加到 index.html")
else:
    print("ERROR: 搵唔到目標字串")
    sys.exit(1)
