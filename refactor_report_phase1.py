import sys
sys.stdout.reconfigure(encoding='utf-8')
f=open('C:/Users/admin/.qclaw/workspace/yauhing-food/inventory.html','r',encoding='utf-8')
html=f.read(); f.close()

# =====================================================
# Phase 1: Replace Report Tab Cards (4 cards)
# =====================================================

old_cards = """  <div class="report-wrap">
    <div style="display:flex;gap:.7rem;flex-wrap:wrap;margin-bottom:1.2rem">
      <div class="report-card" style="border-left:4px solid #4caf50">
        <div class="report-label">今日銷售筆數</div>
        <div class="report-num" id="rSaleCount">0</div>
      </div>
      <div class="report-card" style="border-left:4px solid #2196f3">
        <div class="report-label">今日銷售額</div>
        <div class="report-num" id="rSaleTotal">0</div>
      </div>
      <div class="report-card" style="border-left:4px solid #ff9800">
        <div class="report-label">今日進貨額</div>
        <div class="report-num" id="rPurchaseTotal">0</div>
      </div>
      <div class="report-card" style="border-left:4px solid #9c27b0">
        <div class="report-label">產品已追蹤</div>
        <div class="report-num" id="rProductCount">0</div>
      </div>
    </div>"""

new_cards = """  <div class="report-wrap">
    <div style="display:flex;gap:.7rem;flex-wrap:wrap;margin-bottom:1.2rem">
      <div class="report-card" style="border-left:4px solid #f44336">
        <div class="report-label">⚠️ 缺貨</div>
        <div class="report-num" id="rOutOfStock">0</div>
        <div style="font-size:.7rem;color:#888;margin-top:.2rem">庫存 = 0，即刻補貨</div>
      </div>
      <div class="report-card" style="border-left:4px solid #ff9800">
        <div class="report-label">⚡ 低庫存</div>
        <div class="report-num" id="rLowStock">0</div>
        <div style="font-size:.7rem;color:#888;margin-top:.2rem">庫存 < 安全庫存</div>
      </div>
      <div class="report-card" style="border-left:4px solid #4caf50">
        <div class="report-label">📦 過剩庫存</div>
        <div class="report-num" id="rOverStock">0</div>
        <div style="font-size:.7rem;color:#888;margin-top:.2rem">積壓資金，考慮促銷</div>
      </div>
      <div class="report-card" style="border-left:4px solid #2196f3">
        <div class="report-label">🔄 平均周轉率</div>
        <div class="report-num" id="rTurnover">0</div>
        <div style="font-size:.7rem;color:#888;margin-top:.2rem">每週銷售 / 平均庫存</div>
      </div>
    </div>"""

if old_cards in html:
    html = html.replace(old_cards, new_cards, 1)
    print('Phase 1 OK: Cards replaced')
else:
    print('ERROR: old_cards not found!')
    # Try to find similar content
    idx = html.find('今日銷售筆數')
    if idx > 0:
        print('  Found near position:', idx)
    else:
        print('  Cannot find 今日銷售筆數')

f2=open('C:/Users/admin/.qclaw/workspace/yauhing-food/inventory.html','w',encoding='utf-8')
f2.write(html); f2.close()
print('Phase 1 done, size=', len(html))
