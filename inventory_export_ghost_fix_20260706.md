# 交易記錄匯出 Excel — Ghost 空行 + SKU 錯誤 診斷與修復 (2026-07-06)

## 問題現象
Ben 重新匯出「交易記錄」Excel，發現：
1. **第 6 行（Excel row 6）係 ghost 空行**：時間/類型/分店/SKU/產品名稱全空，只得 數量=5、單價=$5.00、金額=$25.00
2. **SKU 欄顯示產品名**（「豆卜（盒裝）」）而非 YH 編號（YH101）
3. 數量整體 shift 一格（Ben row7 YH101 qty=1，但 Firestore YH101 qty=5；ghost 行 qty=5 正正係 YH101 嘅數量）

## 根因
**真正根因：Service Worker 緩存未失效，Ben 個 browser 食咗舊 cache 版本嘅 inventory.html。**

- 部署咗嘅 inventory.html **已經有 fix**（`rawSku = i.sku`，line 1717）同 Firestore `QKWp` 筆 transaction 係 **19 個乾淨 items（全部有正確 sku）**，無 ghost。
- 但 `service-worker.js` 用 `CACHE_NAME='yauhing-inventory-v2'` 且 fetch handler 係 **cache-first**：一旦 `/inventory.html` 入咗 v2 cache，之後永遠 serve 舊版本。`activate` 只刪「唔同名」cache，v2 同名所以舊 cache 一直留低。
- Ben 睇到嘅係 v2 cache 入面舊 code（用 `i.name` 做 SKU + 舊 shift 邏輯）→ 出現 ghost + SKU=產品名 + 數量錯位。

## 修復（commit 20dd942，已 deploy 上 yauhing-food.web.app）
1. **service-worker.js**：`CACHE_NAME` v2 → **v3**（強制刪舊 cache）；fetch handler 改為 **HTML network-first**（`.html` / navigate 請求永遠攞最新，static assets 仍 cache-first）。理由：admin 工具經常更新，唔可以食舊 cache。
2. **inventory.html exportLogToExcel**：加 defensive guard，skip 到 `sku` 同 `name` 都空嘅 line item（`cleanRows` filter），確保永遠唔會出 ghost 行。

## 驗證
- 部署後 curl 確認：`service-worker.js` 含 `CACHE_NAME='yauhing-inventory-v3'` + network-first；`inventory.html` 含 `Defensive: drop any line item`。
- Firestore `QKWp`（2026-07-04 始創進貨）19 items 全部有 `sku`（YH101...YHF01），無 ghost。

## Ben 需要做（清 cache）
Ben 個 browser 仲註冊緊舊 v2 SW。要令新版本生效：
- **關閉 PWA / tab 再重新開 `inventory.html`**，或 **Ctrl+Shift+R 硬刷新 1-2 次**。
- 新 v3 SW 安裝後會透過 SKIP_WAITING 自動啟用並刪 v2 cache；其後 HTML 永遠 network-first，唔會再食舊版。
- 重新匯出後應為：19 行、SKU=YH101...、無 ghost 空行。

## 教訓
- **Admin / 後台工具嘅 Service Worker 唔可以用 cache-first 緩存 HTML**，否則修復咗都睇唔到，極易誤判為「bug 未修」。應用 network-first（或每次 deploy bump cache 版本 + 加版本查詢參數）。
- 診斷此類「線上明明有 fix 但用家仲見舊行為」時，第一步應 curl 部署檔確認 fix 真係 live，再查 SW / 瀏覽器緩存。
