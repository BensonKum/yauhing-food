# report_redesign.py - 報表tab改為左側卡片+右側列表
import re

with open('inventory.html', 'r', encoding='utf-8-sig') as f:
    c = f.read()

# === 1. CSS: 修改 .report-summary 為左側固定寬度垂直排列 ===
old_css = """.report-summary{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.8rem;margin-bottom:1.2rem;
}"""
new_css = """/* Report Tab - Left Sidebar + Right Content Layout */
.report-wrap{display:flex;gap:1.2rem;padding:1.2rem;height:calc(100vh - 68px);overflow:hidden}
.report-sidebar{width:180px;flex-shrink:0;display:flex;flex-direction:column;gap:.6rem}
.report-card{
  background:white;border-radius:12px;padding:.9rem;border:1px solid var(--bd);text-align:center;
}
.report-card .num{font-family:'Noto Serif TC',serif;font-size:1.5rem;font-weight:700;color:var(--red)}
.report-card .num.green{color:var(--green)}
.report-card .num.orange{color:var(--orange)}
.report-card .num.blue{color:#1565C0}
.report-card .label{font-size:.7rem;color:var(--muted);margin-top:.15rem}
.report-card.date-btn{background:#E8D84F;cursor:pointer;border:2px solid #D4A843;transition:all .2s}
.report-card.date-btn:hover{background:#DDD540;transform:scale(1.02)}
.report-card.date-btn .label{font-weight:600;color:#5D4E00}
.report-main{flex:1;overflow-y:auto;display:flex;flex-direction:column}"""

c = c.replace(old_css, new_css)

# === 2. HTML: 替換報表 tab 結構 ===
old_html = """<!-- Report Tab -->
<div class="tab-content" id="tabContentReport">
  <div class="report-wrap">
    <div class="report-summary" id="reportSummary"></div>
    <div class="report-filter">
      <span class="filter-label">分店：</span>
      <select class="filter-select" id="repStore" onchange="renderReport()">
        <option value="all">全部</option>
        <option value="central">中環店</option>
        <option value="pioneer">始創店</option>
      </select>
      <span class="filter-label">狀態：</span>
      <select class="filter-select" id="repStatus" onchange="renderReport()">
        <option value="all">全部</option>
        <option value="alert">⚠️ 低庫存</option>
        <option value="zero">🔴 缺貨</option>
        <option value="discontinued">❌ 停售</option>
      </select>
    </div>
    <div class="report-section">
      <div class="report-section-title">
        📦 庫存概況
        <span class="badge badge-red" id="alertCount"></span>
        <span class="badge badge-orange" id="lowCount"></span>
      </div>
      <div class="report-table">
        <table>
          <thead>
            <tr>
              <th>SKU</th><th>產品名稱</th><th>分類</th>
              <th>中環</th><th>始創</th><th>總庫存</th><th>狀態</th>
            </tr>
          </thead>
          <tbody id="reportBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>"""

new_html = """<!-- Report Tab -->
<div class="tab-content" id="tabContentReport">
  <div class="report-wrap">
    <div class="report-sidebar" id="reportSidebar"></div>
    <div class="report-main">
      <div class="report-filter">
        <span class="filter-label">分店：</span>
        <select class="filter-select" id="repStore" onchange="renderLog()">
          <option value="all">全部</option>
          <option value="central">中環店</option>
          <option value="pioneer">始創店</option>
        </select>
        <span class="filter-label">類型：</span>
        <select class="filter-select" id="repType" onchange="renderLog()">
          <option value="all">全部</option>
          <option value="sale">銷售</option>
          <option value="purchase">進貨</option>
        </select>
      </div>
      <div id="logSummary"></div>
      <div id="logList"></div>
    </div>
  </div>
</div>"""

c = c.replace(old_html, new_html)

# === 3. JS: 修改 renderReport() 為左側卡片+交易列表 ===
old_js = """async function renderReport(){
  let txns=[];
  try {
    const snap=await db.collection('inventory_transactions').orderBy('createdAt','desc').limit(200).get();
    snap.forEach(d=>txns.push(d.data()));
  } catch(e){console.error(e);}

  const today=new Date().toDateString();
  const todayTx=txns.filter(t=>new Date(t.createdAt?.toDate()).toDateString()===today);
  const todaySale=todayTx.filter(t=>t.type==='sale').reduce((s,i)=>s+(i.total||0),0);
  const todaySaleCount=todayTx.filter(t=>t.type==='sale').length;
  const todayPurchase=todayTx.filter(t=>t.type==='purchase').reduce((s,i)=>s+(i.total||0),0);

  document.getElementById('reportSummary').innerHTML=`\\
    <div class="report-card"><div class="num orange">${todaySaleCount}</div><div class="label">今日銷售筆數</div></div>\\
    <div class="report-card"><div class="num">HK$${todaySale.toLocaleString()}</div><div class="label">今日銷售額</div></div>\\
    <div class="report-card"><div class="num green">${todayPurchase.toLocaleString()}</div><div class="label">今日進貨額</div></div>\\
    <div class="report-card"><div class="num">${Object.keys(inventory).length||0}</div><div class="label">產品已追蹤</div></div>\\
  `;

  const prodMap={};
  products.forEach(p=>{
    const inv=inventory[p.name]||{};
    const central=inv.central??0;
    const pioneer=inv.pioneer??0;
    const total=central+pioneer;
    let status='stock-ok',statusText='充足',badge='badge-green';
    // Check if discontinued first
    const isDiscontinued = discontinuedSkus.includes(p.sku || '');
    if(isDiscontinued){
      status='stock-discontinued';statusText='停售';badge='badge-red';
    }else if(total===0){status='stock-zero';statusText='缺貨';badge='badge-red';}
    else if(total<5){status='stock-zero';statusText='庫存緊張';badge='badge-red';}
    else if(total<15){status='stock-low';statusText='偏低';badge='badge-orange';}
    prodMap[p.name]={sku:p.sku||p.name,name:p.name,cat:p.cat,central,pioneer,total,status,statusText,badge};
  });

  const storeFilter=document.getElementById('repStore').value;
  let rows=Object.values(prodMap);
  if(storeFilter!=='all'){
    rows=rows.filter(r=>r[storeFilter]<15);
  }
  const statusFilter=document.getElementById('repStatus').value;
  if(statusFilter==='alert') rows=rows.filter(r=>r.total>0&&r.total<15);
  if(statusFilter==='zero') rows=rows.filter(r=>r.total===0);
  if(statusFilter==='discontinued') rows=rows.filter(r=>r.statusText==='停售');

  let alertN=0,lowN=0,discN=0;
  Object.values(prodMap).forEach(r=>{if(r.statusText==='停售')discN++;else if(r.total===0)alertN++;else if(r.total<15)lowN++;});
  document.getElementById('alertCount').textContent=alertN+' 缺貨';
  document.getElementById('lowCount').textContent=lowN+' 偏低';

  document.getElementById('reportBody').innerHTML=rows.length===0?
    '<tr><td colspan="7" style="text-align:center;padding:2rem;color:var(--muted)">暫無數據</td></tr>':
    rows.map(r=>`<tr>
      <td>${r.sku}</td>
      <td style="font-weight:600">${r.name}</td>
      <td>${r.cat}</td>
      <td style="text-align:center">${r.central}</td>
      <td style="text-align:center">${r.pioneer}</td>
      <td style="text-align:center;font-weight:700">${r.total}</td>
      <td><span class="badge ${r.badge}">${r.statusText}</span></td>
    </tr>`).join('');
}"""

new_js = """async function renderReport(){
  let txns=[];
  try {
    const snap=await db.collection('inventory_transactions').orderBy('createdAt','desc').limit(200).get();
    snap.forEach(d=>txns.push({id:d.id,...d.data()}));
  } catch(e){console.error(e);}

  const today=new Date();
  const y=today.getFullYear(),m=String(today.getMonth()+1).padStart(2,'0'),d=String(today.getDate()).padStart(2,'0');
  const todayStr=y+'-'+m+'-'+d;
  const todayTx=txns.filter(t=>{
    if(!t.createdAt) return false;
    const td=t.createdAt.toDate();
    return td.getFullYear()===y && td.getMonth()===(today.getMonth()) && td.getDate()===today.getDate();
  });
  const todaySale=todayTx.filter(t=>t.type==='sale').reduce((s,i)=>s+(i.total||0),0);
  const todayPurchase=todayTx.filter(t=>t.type==='purchase').reduce((s,i)=>s+(i.total||0),0);

  // Sidebar cards
  document.getElementById('reportSidebar').innerHTML=
    '<div class="report-card"><div class="label">銷售</div><div class="num">HK$'+todaySale.toLocaleString()+'</div></div>'+
    '<div class="report-card"><div class="label">進貨</div><div class="num green">HK$'+todayPurchase.toLocaleString()+'</div></div>'+
    '<div class="report-card"><div class="label">淨額</div><div class="num blue">'+(todaySale-todayPurchase>=0?'+':'')+'HK$'+(todaySale-todayPurchase).toLocaleString()+'</div></div>'+
    '<div class="report-card date-btn" onclick="document.getElementById(\'repDateInput\').click()"><div class="label">選擇日期</div></div>'+
    '<input type="date" id="repDateInput" style="display:none" value="'+todayStr+'" onchange="renderLog()">';

  // Render transaction list (reuse renderLog logic)
  renderLog();
}"""

c = c.replace(old_js, new_js)

with open('inventory.html', 'w', encoding='utf-8-sig') as f:
    f.write(c)

print("OK - inventory.html updated")
