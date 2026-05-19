
}

function renderCart(){
  const container=document.getElementById('cartItems');
  const keys=Object.keys(cart);
  if(keys.length===0){
    container.innerHTML=`<div class="cart-empty"><div class="cart-empty-icon">🛒</div>尚未加入任何項目<br>從左邊選擇產品</div>`;
    document.getElementById('cartTotal').textContent='HK$0';
    document.getElementById('cartCount').innerHTML='共 <span>0</span> 款產品';
    return;
  }
  let total=0;let html='';let count=0;
  keys.forEach(cartKey=>{
    const item=cart[cartKey];
    const lineTotal=item.qty*item.price;
    total+=lineTotal;count+=item.qty;
    const displayName=item.pack?`${item.name}（${item.pack}）`:item.name;
    html+=`<div class="cart-item">
      <div class="ci-info"><div class="ci-name">${displayName}</div><div class="ci-price">HK$${item.price}/件</div></div>
      <div class="ci-qty">×${item.qty}</div>
      <div class="ci-total">HK$${lineTotal}</div>
      <button class="ci-remove" onclick="removeItem('${cartKey.replace(/'/g,"\\'")}')">✕</button>
    </div>`;
  });
  container.innerHTML=html;
  document.getElementById('cartTotal').textContent='HK$'+total;
  document.getElementById('cartCount').innerHTML=`共 <span>${count}</span> 件產品，<span>${keys.length}</span> 款`;
}

function removeItem(cartKey){delete cart[cartKey];renderCart();renderGrid();}
function clearCart(){cart={};renderCart();renderGrid();}

function getPriceNum(priceStr){
  const m=String(priceStr).match(/[\d.]+/);
  return m?parseFloat(m[0]):0;
}

// --- Confirm & Save ---
function confirmTransaction(){
  if(Object.keys(cart).length===0){toast('請先加入產品');return;}
  if(!currentStore){toast('請先選擇分店');showStoreSelect();return;}
  const items=Object.entries(cart).map(([name,d])=>
    `${name} × ${d.qty} = HK$${d.qty*d.price}`
  ).join('\n');
  const total=Object.values(cart).reduce((s,i)=>s+i.qty*i.price,0);
  document.getElementById('confirmTitle').textContent=
    currentMode==='sale'?'📤 確認銷售交易？':'📥 確認進貨記錄？';
  document.getElementById('confirmMsg').innerHTML=
    `<div style="text-align:left;font-size:.8rem;background:#f5f5f5;border-radius:8px;padding:.6rem;margin-bottom:.5rem">${items.replace(/\n/g,'<br>')}</div><strong>合計：HK$${total}</strong><br><span style="font-size:.72rem;color:var(--muted)">分店：${currentStore==='central'?'中環店':'始創店'}</span>`;
  document.getElementById('confirmDialog').classList.add('show');
}

function closeConfirm(){
  document.getElementById('confirmDialog').classList.remove('show');
}

async function doConfirm(){
  closeConfirm();
  const storeField=currentStore;
  const delta=currentMode==='sale'?-1:1;
  const total=Object.values(cart).reduce((s,i)=>s+i.qty*i.price,0);
  const timestamp=Date.now();
  const txId='TX'+(''+timestamp).slice(-10);

  try {
    // Save transaction with full product info (incl. pack)
    await db.collection('inventory_transactions').add({
      txId, type:currentMode, store:storeField,
      items:Object.entries(cart).map(([cartKey,d])=>({
        name:d.name, pack:d.pack||null, qty:d.qty, price:d.price, lineTotal:d.qty*d.price
      })),
      total, user:currentUser.email,
      createdAt:firebase.firestore.FieldValue.serverTimestamp()
    });

    // Update inventory — group by product name (ignore pack variant)
    const batch=db.batch();
    const byProduct={};
    for(const [cartKey,item] of Object.entries(cart)){
      const pName=item.name;
      if(!byProduct[pName]) byProduct[pName]=0;
      byProduct[pName]+=item.qty;
    }
    for(const [pName,qty] of Object.entries(byProduct)){
      const ref=db.collection('inventory').doc(pName);
      batch.set(ref,{[storeField]:firebase.firestore.FieldValue.increment(qty*delta)},{merge:true});
    }
    await batch.commit();
    await loadInventory();
  } catch(e){
    console.error('save error:',e);
    toast('儲存失敗：'+e.message);
    return;
  }

  // Show receipt
  let rh='<div class="receipt-row"><span style="font-weight:600">時間</span><span>'+new Date().toLocaleString('zh-HK')+'</span></div>';
  rh+='<div class="receipt-row"><span style="font-weight:600">分店</span><span>'+(storeField==='central'?'中環店':'始創店')+'</span></div>';
  rh+='<div class="receipt-row"><span style="font-weight:600">單據號</span><span>'+txId+'</span></div>';
  rh+='<div style="border-top:1px dashed var(--bd);margin:.3rem 0"></div>';
  for(const [cartKey,item] of Object.entries(cart)){
    const displayName=item.pack?`${item.name}（${item.pack}）`:item.name;
    rh+=`<div class="receipt-row">
      <span style="flex:1">${displayName}<br><span style="font-size:.7rem;color:var(--muted)">HK$${item.price} × ${item.qty}</span></span>
      <span>HK$${item.qty*item.price}</span>
    </div>`;
  }
  document.getElementById('receiptItems').innerHTML=rh;
  document.getElementById('receiptSub').textContent=
    currentMode==='sale'?'📤 銷售單據':'📥 進貨單據';
  document.getElementById('receiptTotal').textContent='HK$'+total;
  document.getElementById('receiptModal').classList.add('show');
  cart={};
  renderCart();
  toast(currentMode==='sale'?'✅ 銷售已記錄，庫存已扣減':'✅ 進貨已記錄，庫存已增加');
}

function closeReceipt(){
  document.getElementById('receiptModal').classList.remove('show');
}

// --- Toast ---
function toast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2500);
}
window.showToast = toast; // Alias for compatibility

// --- Mobile Cart ---
function toggleMobileCart(){
  document.getElementById('cartPanel').classList.toggle('open');
}

// --- Tab Navigation ---
let currentTab = 'pos';


// --- Employee Management (Admin Only) ---
let editingEmpId = null;

function showEmployeeTab(){ document.getElementById('tabEmployee').style.display = 'block'; }
function hideEmployeeTab(){ document.getElementById('tabEmployee').style.display = 'none'; }

async function renderEmployeeList(){
  if(!isAdminUser && !isSMUser) return;
  const empList = document.getElementById('empList');
  empList.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--muted)">載入中...</div>';
  
  try {
    let snap;
    if(isAdminUser && !isSMUser){ snap = await db.collection('employees').orderBy('createdAt','desc').get(); }
    else { snap = await db.collection('employees').where('role','in',['central','pioneer','sm']).get(); }
    const emps = []; snap.forEach(d => emps.push({id: d.id, ...d.data()}));
    const myStore = userStore;
    const canEdit = (emp) => isAdminUser ? true : (emp.role !== 'admin' && emp.role === myStore);
    const btnHtml = '<button onclick="showAddEmployee()" style="display:block;width:100%;padding:.8rem;background:var(--green);color:white;border:none;border-radius:10px;font-size:1rem;font-weight:600;cursor:pointer;font-family:Noto Sans TC,sans-serif;margin-bottom:1rem">＋ 新增員工</button>';
    if(emps.length === 0){
      empList.innerHTML = btnHtml + '<div style="text-align:center;padding:1.5rem;color:var(--muted)">暫無員工記錄</div>';
      return;
    }
    
    empList.innerHTML = btnHtml + emps.map(e => `
      <div class="emp-card">
        <div class="emp-info">
          <div class="emp-name">${e.name || '—'}<span class="emp-role ${e.role}">${e.role==='admin'?'Admin':e.role==='sm'?'區域主管':e.role==='central'?'中環':'始創'}</span></div>
          <div class="emp-email">${e.email || '（無電郵）'}${e.phone ? ' | 📱 ' + e.phone : ''}</div>
        </div>
        <div class="emp-actions">
          ${canEdit(e) ? `<button class="btn-emp-edit" onclick="editEmployee('${e.id}')">✏️</button><button class="btn-emp-del" onclick="deleteEmployee('${e.id}')">🗑️</button>` : ''}
        </div>
      </div>
    `).join('');
  } catch(err){
    console.error(err);
    empList.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--red)">載入失敗：請確認Firestore規則已更新</div>';
  }
}

function showAddEmployee(){
  editingEmpId = null;
  document.getElementById('empModalTitle').textContent = '＋ 新增員工';
  document.getElementById('empName').value = '';
  document.getElementById('empEmail').value = '';
  document.getElementById('empPhone').value = '';
  document.getElementById('empRole').value = 'central';
  document.getElementById('empPwd').value = '';
  document.getElementById('empPwdRow').style.display = '';
  document.getElementById('addEmpModal').style.display = 'flex';
}

function closeAddEmployee(){
  document.getElementById('addEmpModal').style.display = 'none';
  editingEmpId = null;
}

async function editEmployee(id){
  try {
    const doc = await db.collection('employees').doc(id).get();
    if(!doc.exists){ toast('找不到員工'); return; }
    const e = doc.data();
    editingEmpId = id;
    document.getElementById('empModalTitle').textContent = '✏️ 編輯員工';
    document.getElementById('empName').value = e.name || '';
    document.getElementById('empEmail').value = (e.email || '');
    document.getElementById('empPhone').value = e.phone || '';
    document.getElementById('empRole').value = e.role || 'central';
    document.getElementById('empPwdRow').style.display = 'none';
  document.getElementById('addEmpModal').style.display = 'flex';
  } catch(err){
    console.error(err);
    toast('讀取失敗');
  }
}

async function deleteEmployee(id){
  if(!confirm('確定要刪除此員工？')) return;
  if(isSMUser && !isAdminUser){
    const doc = await db.collection('employees').doc(id).get();
    if(doc.exists && doc.data().role === 'admin'){ toast('無法刪除管理員帳號'); return; }
  }
  try {
    await db.collection('employees').doc(id).delete();
    toast('已刪除');
    renderEmployeeList();
  } catch(err){
    console.error(err);
    toast('刪除失敗');
  }
}

async function saveEmployee(){
  const name = document.getElementById('empName').value.trim();
  const email = document.getElementById('empEmail').value.trim().toLowerCase();
  const role = document.getElementById('empRole').value;
  const pwd = document.getElementById('empPwd').value;
  const phone = document.getElementById('empPhone').value.trim();
  
  if(!name){ toast('請填寫姓名'); return; }
  
  // Generate PIN from phone last 4 digits
  let pin = '';
  if(phone && phone.length >= 4){
    pin = phone.slice(-4);
    // Validate PIN is all digits
    if(!/^[0-9]{4}$/.test(pin)){ toast('手機號碼最後4位必須是數字'); return; }
  }
  
  try{
    if(editingEmpId){
      const updateData = {name, email: email || null, role};
      if(phone) updateData.phone = phone;
      if(pin) updateData.pin = pin;
      await db.collection('employees').doc(editingEmpId).update(updateData);
      toast('已更新');
    } else {
      // Generate a unique doc ID for PIN-only employees
      const empId = email ? email : ('emp_' + Date.now() + '_' + Math.random().toString(36).substr(2,6));
      if(email){
      if(!pwd || pwd.length < 6){ toast('請設定密碼（至少6位）'); return; }
      // Create Firebase Auth via REST API (won't kick admin out)
      const apiKey = firebase.app().options.apiKey;
      const resp = await fetch('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=' + apiKey, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email: email, password: pwd, returnSecureToken: false})
      });
      const rd = await resp.json();
      if(!resp.ok){ toast(rd.error && rd.error.message ? rd.error.message : '帳號建立失敗'); return; }
      }
      const newData = {name, email: email || null, role, createdAt: firebase.firestore.FieldValue.serverTimestamp()};
      if(phone) newData.phone = phone;
      if(pin) newData.pin = pin;
      await db.collection('employees').doc(empId).set(newData);
      await db.collection('employees').doc(empId).set(newData);
      if(!email){ toast('員工已建立（PIN 登入，無電郵）'); }
      else { toast('員工帳號已建立'); }
      toast('員工帳號已建立');
    }
    closeAddEmployee();
    renderEmployeeList();
  } catch(err){
    console.error(err);
    toast(err.message || '儲存失敗');
  }
}

// Expose employee functions to global scope for onclick
window.showEmployeeTab = showEmployeeTab;
window.hideEmployeeTab = hideEmployeeTab;
window.renderEmployeeList = renderEmployeeList;
window.showAddEmployee = showAddEmployee;
window.closeAddEmployee = closeAddEmployee;
window.editEmployee = editEmployee;
window.deleteEmployee = deleteEmployee;
window.saveEmployee = saveEmployee;
window.showPinLogin = showPinLogin;
window.showEmailLogin = showEmailLogin;
window.pinLogin = pinLogin;

function switchTab(tab){
  currentTab=tab;
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
  document.getElementById('tab'+tab.charAt(0).toUpperCase()+tab.slice(1)).classList.add('active');
  document.getElementById('tabContent'+tab.charAt(0).toUpperCase()+tab.slice(1)).classList.add('active');
  if(tab==='report'){ lockStoreFilters(); renderReport(); }
  if(tab==='log'){ lockStoreFilters(); renderLog(); }
  if(tab==='employee') renderEmployeeList();
}

// --- Report Tab ---
async function renderReport(){
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

  document.getElementById('reportSummary').innerHTML=`
    <div class="report-card"><div class="num orange">${todaySaleCount}</div><div class="label">今日銷售筆數</div></div>
    <div class="report-card"><div class="num">HK$${todaySale.toLocaleString()}</div><div class="label">今日銷售額</div></div>
    <div class="report-card"><div class="num green">${todayPurchase.toLocaleString()}</div><div class="label">今日進貨額</div></div>
    <div class="report-card"><div class="num">${Object.keys(inventory).length||0}</div><div class="label">產品已追蹤</div></div>
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
}

// --- Log Tab ---
let quickDays = 30;
function setQuickDate(days){
  quickDays = days;
  const dateInput = document.getElementById('logDate');
  document.querySelectorAll('#tabContentLog .report-filter button').forEach(b=>{
    b.style.background='white'; b.style.color='var(--txt)';
  });
  if(event && event.target){
    event.target.style.background='var(--red)';
    event.target.style.color='white';
  }
  if(days === 0){
    const t = new Date();
    dateInput.value = t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');
  } else if(days === 1){
    const t = new Date(); t.setDate(t.getDate()-1);
    dateInput.value = t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');
  } else {
    dateInput.value = '';
  }
  renderLog();
}

async function renderLog(){
  let txns=[];
  try {
    const snap=await db.collection('inventory_transactions').orderBy('createdAt','desc').limit(200).get();
    snap.forEach(d=>txns.push({id:d.id,...d.data()}));
  } catch(e){console.error(e);}

  const now2 = new Date();
  const y=now2.getFullYear(), m=now2.getMonth(), d=now2.getDate();
  let fromDate=null, toDate=null;
  const selDate = document.getElementById('logDate').value;
  if(selDate){
    fromDate = new Date(selDate+'T00:00:00');
    toDate = new Date(selDate+'T23:59:59');
  } else if(quickDays > 1){
    fromDate = new Date(now2);
    fromDate.setDate(fromDate.getDate()-quickDays+1);
    fromDate.setHours(0,0,0,0);
    toDate = new Date(now2); toDate.setHours(23,59,59,999);
  }
  const inDateRange = (t) => {
    if(!fromDate) return true;
    const d2 = t.createdAt ? t.createdAt.toDate() : new Date();
    return d2 >= fromDate && d2 <= toDate;
  };

  const storeFilter=document.getElementById('logStore').value;
  const typeFilter=document.getElementById('logType').value;
  txns=txns.filter(t=>{
    if(storeFilter!=='all'&&t.store!==storeFilter) return false;
    if(typeFilter!=='all'&&t.type!==typeFilter) return false;
    if(!inDateRange(t)) return false;
    return true;
  });

  const sales = txns.filter(t=>t.type==='sale'&&inDateRange(t)).reduce((s,t)=>s+(t.total||0),0);
  const purchase = txns.filter(t=>t.type==='purchase'&&inDateRange(t)).reduce((s,t)=>s+(t.total||0),0);
  const net = sales - purchase;
  const todayStr = y+'-'+String(m+1).padStart(2,'0')+'-'+String(d).padStart(2,'0');

  // Left sidebar cards
  document.getElementById('logSidebar').innerHTML =
    '<div class="log-card" style="background:#fffde7;border-left:4px solid #ffc107;height:55px"></div>' +
    '<div class="log-card" style="background:#e8f5e9;border-left:4px solid #4caf50"><div class="label">銷售</div><div class="num" style="color:#2e7d32;font-weight:700">HK$'+sales.toLocaleString()+'</div></div>' +
    '<div class="log-card" style="background:#fff3e0;border-left:4px solid #ff9800"><div class="label">進貨</div><div class="num" style="color:#e65100;font-weight:700">HK$'+purchase.toLocaleString()+'</div></div>' +
    '<div class="log-card" style="background:#e3f2fd;border-left:4px solid #2196f3"><div class="label">淨額</div><div class="num" style="color:#1565c0;font-weight:700">'+(net>=0?'+':'')+'HK$'+net.toLocaleString()+'</div></div>' +
    '<div class="log-card log-date-card">' +
      '<div class="quick-btns">' +
        '<button class="quick-btn'+(quickDays===1?' active':'')+'" data-days="1">今日</button>' +
        '<button class="quick-btn'+(quickDays===3?' active':'')+'" data-days="3">3日</button>' +
        '<button class="quick-btn'+(quickDays===7?' active':'')+'" data-days="7">7日</button>' +
        '<button class="quick-btn'+(quickDays===30?' active':'')+'" data-days="30">30日</button>' +
      '</div>' +
      '<input type="date" id="logDateInput" value="'+todayStr+'" onchange="quickDays=0;renderLog()">' +
    '</div>';

  // Right side: summary + list
  document.getElementById('logSummary').innerHTML = '';

  if(txns.length===0){
    document.getElementById('logList').innerHTML='<div style="text-align:center;padding:3rem;color:var(--muted)">暫無交易記錄<br><small>在POS頁面完成交易後，記錄會顯示在這裡</small></div>';
    return;
  }

  document.getElementById('logList').innerHTML=txns.map(t=>{
    const dt=t.createdAt?new Date(t.createdAt.toDate()):new Date();
    const dtStr=dt.toLocaleString('zh-HK',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'});
    const itemsStr=t.items&&t.items.length>0?
      t.items.map(i=>`${i.name}${i.pack?'('+i.pack+')':''} × ${i.qty}`).join(', '):'—';
    const adminBtns = (isAdminUser || isSMUser) ? '<button class="log-edit-btn" onclick="editTransaction("' + t.id + '")">✏️</button><button class="log-del-btn" onclick="deleteTransaction("' + t.id + '")">🗑️</button>' : '';
    return '<div class="log-entry">' +
      '<div style="flex:1">' +
        '<div class="log-meta">' + dtStr + ' · <span class="log-type ' + t.type + '">' + (t.type==='sale'?'📤 銷售':'📥 進貨') + '</span> · ' + (t.store==='central'?'中環':'始創') + ' · ' + (t.user||'') + '</div>' +
        '<div class="log-items">' + itemsStr + '</div>' +
      '</div>' +
      '<div style="display:flex;align-items:center;gap:.5rem;">' +
        '<div class="log-total">HK$' + (t.total||0) + '</div>' +
        adminBtns +
      '</div>' +
    '</div>';
  }).join('');
}

// OLD editTransaction removed

// OLD deleteTransaction removed

// Quick button click handler for log date card
document.getElementById('logSidebar').addEventListener('click', function(e){
  if(e.target.classList.contains('quick-btn')){
    const days = parseInt(e.target.dataset.days);
    quickDays = days;
    document.getElementById('logDateInput').value = '';
    renderLog();
  }
});




// Edit transaction - opens modal for editing
window.editTransaction = async function(id) {
  openEditModal(id);
};


// Delete transaction - simple confirm-based deletion
window.deleteTransaction = async function(id) {
  if(!confirm('Confirm DELETE this transaction? This cannot be undone.')) return;
  try {
    await db.collection('inventory_transactions').doc(id).delete();
    alert('Transaction deleted');
    renderLog();
  } catch(e) {
    console.error(e);
    alert('Delete failed: ' + e.message);
  }
}

// window expose (at end, so all functions are defined)
function doLogout(){
  // Reset all state
  currentUser = null;
  isAdminUser = false;
  isSMUser = false;
  userStore = null;
  currentStore = '';
  cart = {};
  pinFailCount = 0;
  // Sign out from Firebase Auth (safe even if not logged in via auth)
  try { auth.signOut(); } catch(e){ /* ignore */ }
  // Reset UI
  document.getElementById('storeBtn').textContent='選擇分店 ▼';
  document.getElementById('storeBtn').className='store-badge central';
  document.getElementById('userInfo').textContent = '';
  document.getElementById('topbarStore').textContent = '';
  // Show login overlay
  document.getElementById('authOverlay').style.display = 'flex';
  document.getElementById('emailLoginForm').style.display = 'block';
  document.getElementById('pinLoginForm').style.display = 'none';
  // Clear PIN inputs
  document.querySelectorAll('.pin-digit').forEach(d=>{d.value='';d.disabled=false;});
}
window.changeQty=changeQty;window.removeItem=removeItem;window.clearCart=clearCart;
window.confirmTransaction=confirmTransaction;window.doConfirm=doConfirm;window.closeReceipt=closeReceipt;
window.setMode=setMode;window.showStoreSelect=showStoreSelect;window.selectStore=selectStore;
window.authLogin=authLogin;window.toggleMobileCart=toggleMobileCart;window.switchTab=switchTab;
window.doLogout=doLogout;
window.renderReport=renderReport;window.renderLog=renderLog;
window.openEditModal=openEditModal;window.closeEditModal=closeEditModal;window.buildEditItemRow=buildEditItemRow;window.addEditItemRow=addEditItemRow;window.saveEditTransaction=saveEditTransaction;
