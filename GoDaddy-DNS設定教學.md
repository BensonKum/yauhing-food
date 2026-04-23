# GoDaddy DNS 設定教學（yauhingfood.com）

## 步驟一：登入 GoDaddy

1. 前往 https://account.godaddy.com
2. 登入你的帳戶

---

## 步驟二：進入 DNS 管理

1. 登入後進入「**我的產品**」頁面
2. 找到 `yauhingfood.com`，點擊「**DNS**」按鈕

---

## 步驟三：設定 A 記錄（4個）

點擊「**添加**」→ 選擇「**A**」

| 主機 | 指向 | TTL |
|------|------|-----|
| @ | 185.199.108.153 | 1 小時 |
| @ | 185.199.109.153 | 1 小時 |
| @ | 185.199.110.153 | 1 小時 |
| @ | 185.199.111.153 | 1 小時 |

> ⚠️ 主機留空不填（不要填 www），指向 IP 照填

---

## 步驟四：設定 CNAME（www）

點擊「**添加**」→ 選擇「**CNAME**」

| 主機 | 指向 |
|------|------|
| www | bensonkum.github.io |

---

## 步驟五：GitHub Pages 設定

1. 前往：https://github.com/BensonKum/yauhing-food/settings/pages
2. 在「Custom domain」輸入 `yauhingfood.com`
3. 點擊「Save」
4. 等待 DNS 生效（通常 5 分鐘 ~ 48 小時）

---

## 驗證 DNS

設定完成後可以到以下網站驗證：
https://dnschecker.org/#A/yauhingfood.com

看到 4 個 IP 都出現「✓」就代表成功。

---

## 常見問題

**Q: 為什麼要 4 個 A 記錄？**
A: GitHub Pages 用負載平衡，4 個 IP 都要設定才能確保隨時可訪問。

**Q: 要等多長時間？**
A: 通常 5-30 分鐘內生效，有時最長 48 小時。

**Q: SSL 證書？**
A: GitHub Pages 會自動免費提供 HTTPS，勾選"Enforce HTTPS"即可。

---

## 完成後測試

打開瀏覽器，輸入：`https://yauhingfood.com`

如果顯示祐興食品網站，代表設定成功！