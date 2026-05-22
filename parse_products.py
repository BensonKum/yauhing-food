import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

# Read the text output from xbrowser
text = """首頁
商店
所有分類
關於我們
聯絡我們
文章
蝦籽麵
素纖麵
醬料
禮盒/套裝
特式麵
手工麵
零售裝
推介產品
keyboard_arrow_down
每頁顯示 24 個
keyboard_arrow_down
價錢
keyboard_arrow_down
產品類型
keyboard_arrow_down
陳皮鴨湯麵禮盒
HKD 108
香港手信系列-蝦子麵套裝
HKD 98
蝦子麵禮盒裝
HKD 108
鮑魚禮盒
HKD 168
鮑魚保溫壺收納套裝
HKD 88
素纖麵5個+保溫壺套裝
HKD 78
經典蝦籽麵禮盒
HKD 88
蝦籽麵雙重禮盒裝
HKD 198
蝦籽麵+素纖麵(套裝)
HKD 68
chevron_left
1
chevron_right
shopping_cart
關於祐興粉麵廠
首頁
關於我們
聯絡我們
文章
商店
網站資源
願望清單
我的帳號
購物車
隱私權政策
條款及細則
商店
手工麵
蝦籽麵
素纖麵
零售裝
禮盒套裝
罐頭
養生麵
醬汁配料
特式麵
Copyright © 2022 Yau hing Food Processing All Right Reserved.
Powered by BOXS Limited
條款及細則"""

# Extract product name + price pairs
# Pattern: product name line, then HKD xxx line
lines = text.split('\n')
products = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    # Check if next line is HKD price
    if i + 1 < len(lines) and re.match(r'HKD?\s*\d+', lines[i+1].strip()):
        name = line
        price = lines[i+1].strip()
        products.append({'name': name, 'price': price, 'category': '禮盒/套裝'})
        i += 2
    else:
        i += 1

print(f'=== 提取到 {len(products)} 款產品 ===\n')
for p in products:
    print(f'{p["name"]}: {p["price"]}')

# Save to JSON
with open('C:/Users/admin/.qclaw/workspace/yauhing-food/noodlesx_products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
print('\n✓ 已保存到 noodlesx_products.json')
