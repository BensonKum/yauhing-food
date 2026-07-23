# 一卡兩 SKU 產品卡片做法（Multi-Pack Pattern）

## 適用場景
同一產品有兩個包裝規格，需要喺網店顯示為一張卡、用 Tab 切換：
- 8隻裝 / 8隻裝+麵
- 單包裝 / 5個裝
- 其他類似組合

---

## 三步做法

### Step 1: products_v2.json 設定

**必須用兩個獨立 SKU 條目，唔好用舊版 `packs` + `label1/label2` pattern**

```json
{
  "sku": "YH805",
  "name": "椰菜鮮肉餃 (8隻裝)",
  "cat": "餃子系列",
  "price": "HKD 25",
  "stock": 50,
  "image": "product_cabbage_dumpling.jpg",
  "local_img": "product_cabbage_dumpling.jpg"
},
{
  "sku": "YH805A",
  "name": "椰菜鮮肉餃+麵",
  "cat": "餃子系列",
  "price": "HKD 20",
  "stock": 30,
  "image": "product_dumpling_noodle.jpg",
  "local_img": "product_dumpling_noodle.jpg"
}
```

**關鍵規則：**
- SKU 結尾：`A` = 加配版（+麵 / 5個裝），無尾碼 = 基礎版
- 兩個條目必須**獨立存在**，唔好加 `packs` / `label1` / `label2` 欄位
- 圖片分開：`img1` / `img2` 係舊版，新版直接用各自 `image` + `local_img`

---

### Step 2: index.html（前台網店）

**手動插入合併卡 HTML**，位置喺對應分類區域：

```html
<div class="p-card" data-sku="YH805" data-cat="餃子系列">
  <div class="p-img-wrap">
    <img id="img-YH805" class="p-img" src="images/product_cabbage_dumpling.jpg" alt="椰菜鮮肉餃">
  </div>
  <div class="p-info">
    <div class="p-name">椰菜鮮肉餃</div>
    <div class="p-price-row">
      <span class="p-price" id="price-YH805">HKD 25</span>
      <span class="p-unit" id="unit-YH805">/ 8隻裝</span>
    </div>
    <!-- Tab 切換按鈕 -->
    <div class="pack-tabs" style="display:flex;gap:8px;margin:8px 0;">
      <button class="pack-tab active" data-pack="base" data-sku="YH805" 
              data-price="HKD 25" data-unit="/ 8隻裝" data-img="images/product_cabbage_dumpling.jpg"
              onclick="switchPack(this,'YH805')">8隻裝</button>
      <button class="pack-tab" data-pack="plus" data-sku="YH805A"
              data-price="HKD 20" data-unit="/ +麵" data-img="images/product_dumpling_noodle.jpg"
              onclick="switchPack(this,'YH805')">+麵</button>
    </div>
    <button class="add-btn" id="btn-YH805" onclick="addToCart('YH805')">加入購物車</button>
  </div>
</div>
```

**注意：**
- `data-sku` 用 base SKU（YH805）
- `switchPack()` 已內建喺 `index.html`，會自動更新價格、單位、圖片、按鈕 SKU
- BOGO 列表要更新（見 Step 3）

---

### Step 3: inventory.html（倉庫系統）

**自動合併邏輯**，唔使改 HTML，只係改 JSON：

`renderGrid()` 函數會自動偵測 SKU pair：
- 如果 SKU 結尾係 `A`，搵對應 base SKU（去掉 `A`）
- 如果搵到 pair，合併為一張 multi-pack 卡顯示
- 如果搵唔到 pair，當獨立產品顯示

**inventory.html 合併邏輯重點：**
```javascript
// 偵測邏輯（renderGrid 內）
const baseSku = p.sku.replace(/A$/, '');
const isPackA = p.sku !== baseSku;
const pair = data.find(x => x.sku === baseSku);

if (isPackA && pair) {
  // 係 pack A，同 base 合併顯示
  // 由 base SKU 嗰條 render 主卡，pack A 做第二個 tab
} else if (data.find(x => x.sku === baseSku + 'A')) {
  // 係 base SKU，而且有 pack A 存在
  // render 為 multi-pack 卡
} else {
  // 獨立產品，單卡顯示
}
```

---

## 常見錯誤

| 錯誤 | 現象 | 解決 |
|------|------|------|
| 孤兒條目 | 兩張合併卡並排 | 刪除冇 SKU 嘅舊版條目（有 `packs` / `label1` / `label2` 嗰個） |
| SKU 錯配 | Tab 切換唔到 / 價格錯 | 檢查 `data-sku` 同 `switchPack()` 參數 |
| 圖片唔變 | Tab 切換圖片唔更新 | 檢查 `data-img` 路徑同 `switchPack()` 內 `img.src` 更新 |
| BOGO 唔認 | 買一送一唔生效 | 更新 `FRESH_NOODLE_NAMES_1PLUS1` / `DUMPLING_NAMES_1PLUS1` 陣列 |

---

## 完整檢查清單

新增一卡兩 SKU 產品時，依序檢查：

- [ ] **products_v2.json**：兩個獨立 SKU 條目（base + A），冇 `packs` 欄位
- [ ] **index.html**：手動插入合併卡 HTML，測試 Tab 切換
- [ ] **BOGO 列表**：如適用促銷，更新對應 `*_NAMES_1PLUS1` 陣列
- [ ] **圖片檔案**：上傳 `local_img` 對應圖片到 `images/` 文件夾
- [ ] **Git**：commit + push
- [ ] **Firebase**：deploy hosting
- [ ] **測試**：前台 Tab 切換、倉庫系統顯示、購物車加入

---

## 參考範例

| 產品 | Base SKU | Pack A SKU | 狀態 |
|------|----------|------------|------|
| 椰菜鮮肉餃 | YH805 | YH805A | ✅ 已上線 |
| 南瓜麵 | YH301 | YH301A | ✅ 已上線 |
| 鮑魚罐頭 | YH401 | YH401A | ✅ 已上線 |
| 素纖麵 | YH201 | YH201A | ✅ 已上線 |

---

## 相關文件

- `products_v2.json` — 產品資料來源（標準）
- `index.html` — 前台網店（手動插入合併卡）
- `inventory.html` — 倉庫系統（自動合併邏輯）
- `sw-frontend.js` — Service Worker（cache 版本管理）

---

*最後更新：2026-07-23*
*作者：QClaw*
