with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8') as f:
    c = f.read()

# Check if we have multi-pack card for 十年陳皮
if '<div class="pk-sw">' in c and '十年陳皮' in c:
    print('✅ index.html 已還原到多包裝設計（帶 pk-sw 按鈕）')
    # Find the card
    idx = c.find('十年陳皮')
    start = c.rfind('<div class="p-card', 0, idx)
    print(c[start:start+500])
else:
    print('❌ 可能仲有問題')
