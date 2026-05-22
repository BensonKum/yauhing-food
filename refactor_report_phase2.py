import sys
sys.stdout.reconfigure(encoding='utf-8')
f=open('C:/Users/admin/.qclaw/workspace/yauhing-food/inventory.html','r',encoding='utf-8')
html=f.read(); f.close()

# =====================================================
# Step 1: Update table header (add 建議補貨量 column)
# =====================================================

old_header = """      <thead>
            <tr>
              <th>SKU</th><th>產品名稱</th><th>分類</th>
              <th>中環</th><th>始創</th><th>總庫存</th><th>狀態</th>
            </tr>
          </thead>"""

new_header = """      <thead>
            <tr>
              <th>SKU</th><th>產品名稱</th><th>分類</th>
              <th>中環</th><th>始創</th><th>總庫存</th><th>狀態</th><th>建議補貨量</th>
            </tr>
          </thead>"""

if old_header in html:
    html = html.replace(old_header, new_header, 1)
    print('Step 1 OK: table header updated')
else:
    print('WARN: old_header not found, searching...')
    idx = html.find('建議補貨量')
    if idx > 0:
        print('  Already has 建議補貨量')
    else:
        print('  Not found, will add manually')

# =====================================================
# Step 2: Replace entire renderReport() function
# =====================================================

old_func_start = html.find('function renderReport(){')
if old_func_start < 0:
    print('ERROR: renderReport not found')
    exit(1)

# Find matching closing brace
depth = 0
in_func = False
idx = old_func_start
while idx < len(html):
    if html[idx] == '{':
        depth += 1
        in_func = True
    elif html[idx] == '}':
        depth -= 1
        if in_func and depth == 0:
            old_func_end = idx + 1
            break
    idx += 1

old_func = html[old_func_start:old_func_end]
print(f'Old function length: {len(old_func)}')

new_func = """function renderReport(){
  let txns=[];
  try {
    const snap=await db.collection('inventory_transactions').orderBy('createdAt','desc').limit(200).get();
    snap.forEach(d=>txns.push(d.data()));
  } catch(e){console.error(e);}

  // === Calculate inventory health metrics ===
  const LOW_THRESHOLD = 10;
  const OVER_THRESHOLD = 100;
  let outOfStock=0, lowStock=0, overStock=0;

  products.forEach(p=>{
    const inv=inventory[p.name]||{};
    const total=(inv.central??0)+(inv.pioneer??0);
    if(total===0) outOfStock++;
    else if(total<LOW_THRESHOLD) lowStock++;
    else if(total>OVER_THRESHOLD) overStock++;
  });

  // Calculate 30-day turnover rate
  const now=new Date();
  const thirtyDaysAgo = new Date(now.getTime()-30*24*60*60*1000);
  const recentSales = txns.filter(t=>{
    if(t.type!=='sale') return false;
    const d = t.createdAt?.toDate?t.createdAt.toDate():new Date(t.createdAt);
    return d >= thirtyDaysAgo;
  });
  const totalSold = recentSales.reduce((s,i)=>s+(i.qty||i.items?.reduce((a,b)=>a+(b.qty||0),0)||0),0);
  const avgInventory = products.reduce((s,p)=>{
    const inv=inventory[p.name]||{};
    return s+(inv.central??0)+(inv.pioneer??0);
  },0) / (products.length||1);
  const turnover = avgInventory>0 ? (totalSold/30/avgInventory).toFixed(2) : '0';

  // === Render 4 health cards ===
  document.getElementById('reportSummary').innerHTML=`
    <div class="report-card" style="border-left:4px solid #f44336">
      <div class="num">${outOfStock}</div>
      <div class="label">⚠️ 缺貨 (庫存=0)</div>
    </div>
    <div class="report-card" style="border-left:4px solid #ff9800">
      <div class="num">${lowStock}</div>
      <div class="label">⚡ 低庫存 (<${LOW_THRESHOLD})</div>
    </div>
    <div class="report-card" style="border-left:4px solid #4caf50">
      <div class="num">${overStock}</div>
      <div class="label">📦 過剩庫存 (>${OVER_THRESHOLD})</div>
    </div>
    <div class="report-card" style="border-left:4px solid #2196f3">
      <div class="num">${turnover}</div>
      <div class="label">🔄 平均周轉率 (次/月)</div>
    </div>
  `;

  // === Build product table with health indicators ===
  const prodMap={};
  const LOW=10;
  products.forEach(p=>{
    const inv=inventory[p.name]||{};
    const central=inv.central??0;
    const pioneer=inv.pioneer??0;
    const total=central+pioneer;
    let status='stock-ok',statusText='充足',badge='badge-green';
    const isDiscontinued = discontinuedSkus.includes(p.sku || '');
    if(isDiscontinued){
      status='stock-disc'; statusText='停售'; badge='badge-grey';
    } else if(total===0){
      status='stock-out'; statusText='缺貨'; badge='badge-red';
    } else if(total<LOW){
      status='stock-low'; statusText='低庫存'; badge='badge-orange';
    }
    const suggestRestock = status==='stock-out' ? LOW : (status==='stock-low'?(LOW-total):0);
    prodMap[p.sku]={
      sku:p.sku, name:p.name, cat:p.cat||'',
      central, pioneer, total, status, statusText, badge, suggestRestock
    };
  });

  // Sort by total stock ascending (low stock first)
  const rows=Object.values(prodMap).sort((a,b)=>a.total-b.total);

  const rowsHtml = rows.length===0?
    '<tr><td colspan="8" style="text-align:center;padding:2rem;color:var(--muted)">暫無數據</td></tr>':
    rows.map(r=>`<tr style="${r.status==='stock-out'?'background-color:#ffebee;':(r.status==='stock-low'?'background-color:#fff3e0;':'')}">
      <td>${r.sku}</td>
      <td style="font-weight:600">${r.name}</td>
      <td>${r.cat}</td>
      <td style="text-align:center">${r.central}</td>
      <td style="text-align:center">${r.pioneer}</td>
      <td style="text-align:center;font-weight:700">${r.total}</td>
      <td><span class="badge ${r.badge}">${r.statusText}</span></td>
      <td style="text-align:center;color:#2196f3;font-weight:600">${r.suggestRestock>0?r.suggestRestock:'-'}</td>
    </tr>`).join('');

  document.getElementById('reportBody').innerHTML = rowsHtml;
}"""

html = html[:old_func_start] + new_func + html[old_func_end:]
print(f'Replacement done, new file size: {len(html)}')

f2=open('C:/Users/admin/.qclaw/workspace/yauhing-food/inventory.html','w',encoding='utf-8')
f2.write(html); f2.close()
print('File written, running syntax check...')

# Syntax check
import subprocess
tmp_js = 'C:/Users/admin/.qclaw/workspace/yauhing-food/tmp_check_report.js'
f3=open(tmp_js,'w',encoding='utf-8')
# Extract last <script> content
import re
scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
if scripts:
    f3.write(scripts[-1])
f3.close()
result = subprocess.run(['node','--check',tmp_js], capture_output=True, text=True)
if result.returncode == 0:
    print('✅ Syntax check PASSED')
else:
    print('❌ Syntax error:', result.stderr)
