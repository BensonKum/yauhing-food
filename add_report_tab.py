import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# --- 1. 加 Report tab 按鈕到 tab-bar ---
old_tab_bar = '''  <div class="tab-bar">
    <button class="tab-btn active" id="tabPos" onclick="switchTab('pos')">&#x1F6D2; POS</button>
    <button class="tab-btn" id="tabEmployee" onclick="switchTab('employee')" style="display:none">&#x1F465; 員工</button>
  </div>'''

new_tab_bar = '''  <div class="tab-bar">
    <button class="tab-btn active" id="tabPos" onclick="switchTab('pos')">&#x1F6D2; POS</button>
    <button class="tab-btn" id="tabReport" onclick="switchTab('report')">&#x1F4CA; 報表</button>
    <button class="tab-btn" id="tabEmployee" onclick="switchTab('employee')" style="display:none">&#x1F465; 員工</button>
  </div>'''

if old_tab_bar in content:
    content = content.replace(old_tab_bar, new_tab_bar)
    print('OK - added Report tab button')
else:
    print('ERROR - tab-bar not found')
    # debug
    idx = content.find('tab-bar')
    if idx >= 0:
        print('Found tab-bar at pos %d:' % idx)
        print(repr(content[idx:idx+300]))
    else:
        print('tab-bar not found at all')

# --- 2. 加 Report tab 內容（喺 tabContentEmployee 前面）---
report_tab_html = '''
<!-- Report Tab -->
<div class="tab-content" id="tabContentReport">
<div class="report-wrap">
  <!-- 篩選列 -->
  <div class="report-filter">
    <select id="repStore">
      <option value="">全部分店</option>
      <option value="central">中環街市</option>
      <option value="pioneer">旺角始創</option>
    </select>
    <select id="repType">
      <option value="">全部類型</option>
      <option value="sale">銷售</option>
      <option value="purchase">進貨</option>
      <option value="transfer">調撥</option>
      <option value="loss">報損</option>
    </select>
    <input type="date" id="repFrom">
    <span>至</span>
    <input type="date" id="repTo">
    <button class="quick-btn" onclick="setRepQuick('today')">今日</button>
    <button class="quick-btn" onclick="setRepQuick('month')">今月</button>
    <button class="rep-search-btn" onclick="loadReportData()">&#x1F50D; 搜尋</button>
  </div>

  <!-- 交易列表 -->
  <div class="log-list" id="repList"></div>
</div>
</div>
'''

old_emp = '<!-- Employee Tab (Admin Only) -->'
if old_emp in content:
    content = content.replace(old_emp, report_tab_html + '\n' + old_emp)
    print('OK - added Report tab content')
else:
    print('ERROR - Employee tab marker not found')

# --- 3. 加 CSS（喺 </style> 前面）---
css_to_add = '''
/* --- Report Tab --- */
.report-wrap{
  padding:1.2rem;overflow-y:auto;height:calc(100vh - 68px);
}
.report-filter{
  display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;
  margin-bottom:1rem;
}
.report-filter select,.report-filter input[type="date"]{
  padding:.4rem .7rem;border-radius:var(--r);border:1px solid var(--bd);
  font-size:.82rem;font-family:'Noto Sans TC',sans-serif;
}
.quick-btn{
  padding:.4rem .9rem;border-radius:50px;border:1px solid var(--bd);
  background:transparent;font-size:.8rem;cursor:pointer;transition:var(--tr);
  font-family:'Noto Sans TC',sans-serif;color:var(--muted);
}
.quick-btn:hover{background:var(--bd);color:var(--txt)}
.rep-search-btn{
  padding:.4rem 1rem;border-radius:50px;border:none;
  background:var(--green);color:white;font-size:.8rem;cursor:pointer;
  font-family:'Noto Sans TC',sans-serif;transition:var(--tr);
}
.rep-search-btn:hover{opacity:.85}
.log-list{max-height:calc(100vh - 180px);overflow-y:auto}
.log-entry{
  border:1px solid var(--bd);border-radius:var(--r);
  padding:.7rem 1rem;margin-bottom:.6rem;cursor:pointer;transition:var(--tr);
}
.log-entry:hover{box-shadow:var(--sh1)}
.log-entry-header{display:flex;justify-content:space-between;font-size:.85rem;margin-bottom:.3rem}
.log-entry-type{padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:600}
.log-entry-type.sale{background:#e8f5e9;color:var(--green)}
.log-entry-type.purchase{background:#e3f2fd;color:#1565c0}
.log-entry-type.transfer{background:#fff3e0;color:#e65100}
.log-entry-type.loss{background:#ffebee;color:#c62828}
.log-entry-items{font-size:.8rem;color:var(--muted);margin-top:.3rem}
.log-entry-detail{font-size:.78rem;color:var(--muted);margin-top:.5rem;padding-top:.5rem;border-top:1px dashed var(--bd);display:none}
'''

old_style_end = '</style>'
if css_to_add not in content and old_style_end in content:
    content = content.replace(old_style_end, css_to_add + '\n' + old_style_end)
    print('OK - added CSS')
else:
    print('ERROR - style tag not found or CSS already exists')

# --- 4. 加 JavaScript（喺 </script> 前面，firebase 初始化之後）---
js_to_add = '''
// --- Report Tab Functions ---
function setRepQuick(period) {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  const today = y + '-' + m + '-' + d;

  if (period === 'today') {
    document.getElementById('repFrom').value = today;
    document.getElementById('repTo').value = today;
  } else if (period === 'month') {
    document.getElementById('repFrom').value = y + '-' + m + '-01';
    document.getElementById('repTo').value = today;
  }
  loadReportData();
}

async function loadReportData() {
  const store = document.getElementById('repStore').value;
  const type = document.getElementById('repType').value;
  const dateFrom = document.getElementById('repFrom').value;
  const dateTo = document.getElementById('repTo').value;

  if (!store) {
    alert('請先選擇分店');
    return;
  }

  console.log('[loadReportData] store:' + store + ' type:' + type + ' from:' + dateFrom + ' to:' + dateTo);

  try {
    let q = db.collection('inventory_transactions')
      .where('store', '==', store);

    if (type) {
      q = q.where('type', '==', type);
    }

    if (dateFrom) {
      q = q.where('createdAt', '>=', dateFrom);
    }
    if (dateTo) {
      // Add 1 day to include the end date
      const d = new Date(dateTo + 'T00:00:00');
      d.setDate(d.getDate() + 1);
      const toStr = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
      q = q.where('createdAt', '<', toStr);
    }

    q = q.orderBy('createdAt', 'desc').limit(200);

    const snap = await q.get();
    console.log('[loadReportData] results:' + snap.size);

    let html = '';
    snap.forEach(doc => {
      const d = doc.data();
      const dt = d.createdAt ? new Date(d.createdAt) : null;
      const dateStr = dt ? (dt.getFullYear() + '/' + String(dt.getMonth()+1).padStart(2,'0') + '/' + String(dt.getDate()).padStart(2,'0') + ' ' + String(dt.getHours()).padStart(2,'0') + ':' + String(dt.getMinutes()).padStart(2,'0')) : '';
      const typeName = d.type === 'sale' ? '銷售' : (d.type === 'purchase' ? '進貨' : (d.type === 'transfer' ? '調撥' : (d.type === 'loss' ? '報損' : d.type)));
      const items = d.items || [];
      const itemStr = items.map(i => i.name + ' x' + i.qty).join(', ');
      const total = d.total || 0;

      let detailHtml = '<div class="log-entry-detail">';
      detailHtml += '&#x1F4CB; 詳情：<br>';
      items.forEach(i => {
        detailHtml += '• ' + i.name + ' — HK$' + (i.price || 0) + ' x ' + i.qty + ' = HK$' + ((i.price || 0) * i.qty) + '<br>';
      });
      detailHtml += '&#x1F4B0; 總額：HK$' + total + ' &nbsp;&nbsp; &#x1F3EA; 分店：' + (d.store === 'central' ? '中環街市' : '旺角始創');
      detailHtml += '</div>';

      html += '<div class="log-entry" onclick="this.querySelector(\'.log-entry-detail\').style.display = (this.querySelector(\'.log-entry-detail\').style.display === \'block\' ? \'none\' : \'block\')">'
        + '<div class="log-entry-header">'
        + '<span class="log-entry-type ' + (d.type || '') + '">' + typeName + '</span>'
        + '<span>' + dateStr + '</span>'
        + '</div>'
        + '<div class="log-entry-items">' + itemStr + '</div>'
        + detailHtml
        + '</div>';
    });

    document.getElementById('repList').innerHTML = html || '<div style="text-align:center;color:var(--muted);padding:2rem">未有交易記錄</div>';
  } catch(e) {
    console.error('[loadReportData] error:', e);
    alert('載入失敗: ' + e.message);
  }
}
'''

# 搵 </script> 前面（最後一個 </script>，即係 Firebase SDK 之後）
last_script_idx = content.rfind('</script>')
if last_script_idx > 0 and js_to_add not in content:
    content = content[:last_script_idx] + js_to_add + '\n' + content[last_script_idx:]
    print('OK - added JavaScript functions')
else:
    print('ERROR - </script> not found or JS already exists')

# 存檔
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('\n=== Done! ===')
print('Next: verify the file, then commit + push')
