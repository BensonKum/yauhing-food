
// --- Firebase Config ---
const fb = firebase.initializeApp({
  apiKey: "AIzaSyAeRezKIwd93M1CHc-JtKFKIYtGAW9mVFk",
  authDomain: "yauhing-food.firebaseapp.com",
  projectId: "yauhing-food"
});
const db = firebase.firestore();
const auth = firebase.auth();

// --- Edit Transaction Functions ---

async function populateEditProductList() {
    try {
        const snap = await db.collection('inventory').get();
        const datalist = document.getElementById('editProductList');
        datalist.innerHTML = '';
        const seen = new Set();
        snap.forEach(doc => {
            const name = doc.id;
            if(!seen.has(name)){
                seen.add(name);
                const opt = document.createElement('option');
                opt.value = name;
                datalist.appendChild(opt);
            }
        });
    } catch(e) { console.error('populateEditProductList error:', e); }
}

async function openEditModal(id) {
    await populateEditProductList();
    try {
        const doc = await db.collection('inventory_transactions').doc(id).get();
        if(!doc.exists) { alert('交易不存在'); return; }
        const data = doc.data();
        window._editTxId = id;
        const container = document.getElementById('editTransactionItems');
        container.innerHTML = '';
        if(data.items && data.items.length > 0) {
            data.items.forEach(item => {
                container.innerHTML += buildEditItemRow(item.name||'', item.pack||'', item.qty||0);
            });
        } else {
            container.innerHTML = '<p>此交易無貨品記錄</p>';
        }
        document.getElementById('editTransactionModal').style.display = 'block';
    } catch(e) {
        console.error(e);
        alert('載入交易失敗: ' + e.message);
    }
}

function buildEditItemRow(name, pack, qty) {
    return '<div class="edit-item-row">' +
        '<input class="item-name" list="editProductList" value="' + name + '" placeholder="貨品名稱">' +
        '<input class="item-pack" value="' + pack + '" placeholder="包裝">' +
        '<input class="item-qty" type="number" value="' + qty + '" placeholder="數量" min="0">' +
        '<span class="remove-item" onclick="this.parentElement.remove()">✕</span>' +
        '</div>';
}

function closeEditModal() {
    document.getElementById('editTransactionModal').style.display = 'none';
}

function addEditItemRow() {
    const container = document.getElementById('editTransactionItems');
    container.innerHTML += buildEditItemRow('', '', 0);
}

async function saveEditTransaction() {
    if(!window._editTxId) { alert('無交易ID'); return; }
    const rows = document.querySelectorAll('#editTransactionItems .edit-item-row');
    const items = [];
    rows.forEach(row => {
        const name = row.querySelector('.item-name').value.trim();
        const pack = row.querySelector('.item-pack').value.trim();
        const qty = parseInt(row.querySelector('.item-qty').value) || 0;
        if(name && qty > 0) { items.push({ name, pack, qty }); }
    });
    if(items.length === 0) { alert('至少需要一項貨品'); return; }
    if(!confirm('確定保存修改？')) return;
    try {
        await db.collection('inventory_transactions').doc(window._editTxId).update({
            items: items,
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        });
        closeEditModal();
        renderLog();
    } catch(e) {
        console.error(e);
        alert('保存失敗: ' + e.message);
    }
}

// --- State ---
let products = [];
// --- Discontinued Products (停售) ---
const discontinuedSkus = ['YH017']; // Add SKUs here to mark as 停售
let cart = {};       // {cartKey: {qty, price, cat, pack}}
let selectedPack = {}; // {productName: selectedPackLabel}
let currentMode = 'sale';
let currentStore = null;  // 'central' | 'pioneer'
let currentUser = null;
let isAdminUser = false;  // Global admin flag
let isSMUser = false;    // Global SM (Store Manager) flag
let userStore = null;    // Employee's assigned home store (central/pioneer)
let currentCat = '全部';

// --- PIN Login State ---
let pinFailCount = 0;
let pinLockedUntil = 0;

// --- Load Products from products.json ---
fetch('products.json').then(r=>r.json()).then(data=>{
  products = data;
  renderCatBar();
  renderGrid();
}).catch(e=>console.error('products.json load failed:',e));

// --- Auth ---
auth.onAuthStateChanged(user=>{
  if(user){ currentUser=user; showApp(); }
  else {
    currentUser=null;
    document.getElementById('authOverlay').style.display='flex';
    document.getElementById('userInfo').textContent='';
  }
});

// --- PIN Login Functions ---
function showPinLogin(){
  document.getElementById('emailLoginForm').style.display='none';
  document.getElementById('pinLoginForm').style.display='block';
  // Check if locked
  checkPinLock();
  // Setup PIN input (only bind listeners ONCE)
  const digits = document.querySelectorAll('.pin-digit');
  digits.forEach((d, i) => {
    d.value = '';
    if(!d.dataset.pinBound){
      d.dataset.pinBound = '1';
      d.addEventListener('keydown', function(e){
        if(e.key >= '0' && e.key <= '9'){
          e.preventDefault(); // prevent default to avoid double-input on some browsers
          this.value = e.key;
          if(i < 3) digits[i+1].focus();
          else {
            this.blur();
            // Auto-submit when 4th digit entered
            setTimeout(()=>pinLogin(), 150);
          }
        } else if(e.key === 'Backspace'){
          this.value = '';
          if(i > 0) digits[i-1].focus();
        } else if(e.key === 'Enter'){
          pinLogin();
        }
      });
    }
  });
  digits[0].focus();
}

function showEmailLogin(){
  document.getElementById('pinLoginForm').style.display='none';
  document.getElementById('emailLoginForm').style.display='block';
}

function checkPinLock(){
  const lockMsg = document.getElementById('pinLockMsg');
  const btn = document.getElementById('pinLoginBtn');
  if(pinLockedUntil > Date.now()){
    const remain = Math.ceil((pinLockedUntil - Date.now()) / 1000);
    lockMsg.textContent = 'PIN 已鎖定，請等待 ' + remain + ' 秒';
    lockMsg.style.display = 'block';
    btn.disabled = true;
    // Clear existing digits
    document.querySelectorAll('.pin-digit').forEach(d=>{d.value='';d.disabled=true;});
    // Countdown timer
    clearInterval(window._pinTimer);
    window._pinTimer = setInterval(()=>{
      if(pinLockedUntil <= Date.now()){
        clearInterval(window._pinTimer);
        lockMsg.style.display='none';
        btn.disabled = false;
        document.querySelectorAll('.pin-digit').forEach(d=>d.disabled=false);
        document.querySelector('.pin-digit').focus();
      } else {
        const r = Math.ceil((pinLockedUntil - Date.now()) / 1000);
        lockMsg.textContent = 'PIN 已鎖定，請等待 ' + r + ' 秒';
      }
    }, 1000);
  } else {
    lockMsg.style.display='none';
    btn.disabled = false;
    document.querySelectorAll('.pin-digit').forEach(d=>d.disabled=false);
  }
}

async function pinLogin(){
  const digits = document.querySelectorAll('.pin-digit');
  let pin = '';
  digits.forEach(d => { pin += d.value; });
  
  if(pin.length !== 4){
    document.getElementById('authError').textContent = '請輸入完整 4 位 PIN';
    return;
  }
  
  // Check lock
  if(pinLockedUntil > Date.now()){ checkPinLock(); return; }
  
  document.getElementById('authError').textContent = '';
  const btn = document.getElementById('pinLoginBtn');
  btn.textContent = '驗證中...';
  btn.disabled = true;
  
  try {
    // Query Firestore for matching PIN
    const snap = await db.collection('employees').where('pin', '==', pin).get();
    
    if(snap.empty){
      handlePinFail('PIN 不正確');
      return;
    }
    
    if(snap.size > 1){
      // Multiple matches — rare case, show names to pick
      btn.textContent = '確認登入';
      btn.disabled = false;
      document.getElementById('authError').textContent = '發現多個帳號，請用電郵登入';
      // Reset PIN inputs
      digits.forEach(d=>d.value='');
      digits[0].focus();
      return;
    }
    
    // Exactly 1 match — login successful
    const empData = snap.docs[0].data();
    const empId = snap.docs[0].id;
    
    // Set user state (mock user object for PIN login)
    currentUser = {
      email: empData.email || ('pin@' + empId),
      isPinLogin: true,
      uid: 'pin_' + empId
    };
    
    // Determine role/store from employee record
    const role = empData.role || '';
    const empStore = empData.store || '';  // Prefer explicit store field
    isAdminUser = (role === 'admin' || role === 'sm');
    isSMUser = (role === 'sm');

    // Store priority: explicit store field > infer from role > null
    if(empStore){
      userStore = empStore;
    } else if(role === 'pioneer'){
      userStore = 'pioneer';
    } else if(role === 'central'){
      userStore = 'central';
    } else {
      userStore = null;  // Unknown — will try email fallback or show dialog
    }
    
    // Reset fail count on success
    pinFailCount = 0;
    
    document.getElementById('authOverlay').style.display = 'none';
    document.getElementById('userInfo').textContent = (empData.name || '員工') + ' (PIN)';
    
    // Navigate based on role
    if(isAdminUser || isSMUser){
      showEmployeeTab();
      showStoreSelect();
    } else if(userStore){
      selectStore(userStore);
    } else {
      // No store info in Firestore — show store selection dialog
      console.warn('PIN login: no store/role set for', empData.name, '(id:', empId, ') — showing store selector');
      showStoreSelect();
    }
    
    btn.textContent = '確認登入';
    btn.disabled = false;
    
  } catch(err){
    console.error('PIN login error:', err);
    handlePinFail('登入失敗，請重試');
  }
}

function handlePinFail(msg){
  pinFailCount++;
  const btn = document.getElementById('pinLoginBtn');
  btn.textContent = '確認登入';
  btn.disabled = false;
  document.getElementById('authError').textContent = msg;
  
  // Clear PIN inputs
  document.querySelectorAll('.pin-digit').forEach(d=>{d.value='';});
  document.querySelector('.pin-digit').focus();
  
  // Lock after 5 failed attempts
  if(pinFailCount >= 5){
    pinLockedUntil = Date.now() + (5 * 60 * 1000); // 5 minutes
    pinFailCount = 0;
    checkPinLock();
  }
}

function authLogin(){
  const email=document.getElementById('authEmail').value.trim();
  const pass=document.getElementById('authPass').value;
  if(!email||!pass){document.getElementById('authError').textContent='請輸入電郵及密碼';return;}
  document.getElementById('authError').textContent='';
  auth.signInWithEmailAndPassword(email,pass)
    .then(()=>{document.getElementById('authOverlay').style.display='none';})
    .catch(e=>{
      if(e.code==='auth/user-not-found'||e.code==='auth/wrong-password'){
        document.getElementById('authError').textContent='電郵或密碼錯誤';
      } else {document.getElementById('authError').textContent=e.message;}
    });
}

async function showApp(){
  document.getElementById('authOverlay').style.display='none';
  document.getElementById('userInfo').textContent=currentUser.email;
  // Auto-detect store from email IMMEDIATELY (no Firestore dependency)
  const email = currentUser ? currentUser.email.toLowerCase() : '';
  if(email === 'admin@yauhing.hk'){
    // Admin: show store selection dialog
    showStoreSelect();
  } else if(email.includes('central')){
    selectStore('central');
  } else if(email.includes('pioneer')){
    selectStore('pioneer');
  } else {
    // Unknown email pattern: fall back to store select
    showStoreSelect();
  }
}

// --- Store Select ---
async function showStoreSelect(){
  const email = currentUser ? currentUser.email.toLowerCase() : '';

  // Step 1: Admin & SM -> show dialog so they can pick any store
  if(email === 'admin@yauhing.hk'){
    isAdminUser = true;
    isSMUser = false;
    showEmployeeTab();
    document.getElementById('storeDialog').classList.add('show');
    return;
  }

  // Step 2: For other accounts, try Firestore employees collection
  try {
    const empSnap = await db.collection('employees').where('email','==',email).get();
    if(!empSnap.empty){
      const empData = empSnap.docs[0].data();
      if(empData.role === 'admin'){
        isAdminUser = true;
        isSMUser = false;
        showEmployeeTab();
        document.getElementById('storeDialog').classList.add('show');
        return;
      }
      if(empData.role === 'sm'){
        isAdminUser = true;   // SM has admin-level store access
        isSMUser = true;
        showEmployeeTab();
        document.getElementById('storeDialog').classList.add('show');
        return;
      }
      userStore = empData.role;
      if(userStore && (userStore === 'sm' || userStore === 'central' || userStore === 'pioneer')){
        isSMUser = true;
        showEmployeeTab();
      }
    }
  } catch(e){ console.error('employees query failed:', e); }

  // Step 3: Email pattern fallback
  if(!userStore){
    if(email.includes('central')) userStore = 'central';
    else if(email.includes('pioneer')) userStore = 'pioneer';
  }

  isAdminUser = false;
  isSMUser = false;
  if(userStore) {
    selectStore(userStore);
  } else {
    // Unknown store: show dialog but hide irrelevant buttons
    lockStoreDialogButtons(email);
    document.getElementById('storeDialog').classList.add('show');
  }
}

// Hide store buttons that don't belong to the logged-in user's email domain
function lockStoreDialogButtons(email){
  var btnC = document.getElementById('storeBtnCentral');
  var btnP = document.getElementById('storeBtnPioneer');
  if(!btnC || !btnP) return;
  if(email.includes('central')){
    btnP.style.display = 'none';
    btnC.style.display = '';
  } else if(email.includes('pioneer')){
    btnC.style.display = 'none';
    btnP.style.display = '';
  }
  // admin/SM: show both (default)
}
function selectStoreDisplay(store){
  currentStore = store;
  const btn = document.getElementById('storeBtn');
  if (store === 'central') {
    btn.textContent = '🏠 中環店 ✓';
    btn.className = 'store-badge central';
    document.getElementById('topbarStore').textContent = '中環街市1樓P04C';
  } else {
    btn.textContent = '🏬 始創店 ✓';
    btn.className = 'store-badge pioneer';
    document.getElementById('topbarStore').textContent = '旺角始創中心地下KIOSK J';
  }
  loadInventory();
}

async function selectStore(store){
  const email = currentUser ? currentUser.email.toLowerCase() : '';
  const isAdmin = (email === 'admin@yauhing.hk');
  
  // Admin & SM: allow any store selection
  // Non-admin/non-SM: enforce store permission
  if(!isAdminUser && !isSMUser){
    let allowed = null;
    if(email.includes('central')) allowed = 'central';
    else if(email.includes('pioneer')) allowed = 'pioneer';
    if(allowed && store !== allowed){
      toast('你沒有權限使用此分店');
      return;
    }
  }

  currentStore = store;
  const btn = document.getElementById('storeBtn');
  if (store === 'central') {
    btn.textContent = '🏠 中環店 ✓';
    btn.className = 'store-badge central';
    document.getElementById('topbarStore').textContent = '中環街市1樓P04C';
  } else {
    btn.textContent = '🏬 始創店 ✓';
    btn.className = 'store-badge pioneer';
    document.getElementById('topbarStore').textContent = '旺角始創中心地下KIOSK J';
  }
  document.getElementById('storeDialog').classList.remove('show');
  lockStoreFilters();

  // Ensure POS tab is visible and active after store selection
  try {
    switchTab('pos');
    setMode('sale');
  } catch(e) {
    console.warn('selectStore: tab/mode init error:', e);
  }

  loadInventory().catch(err => {
    console.error('selectStore: loadInventory failed:', err);
    toast('載入產品失敗，請刷新頁面');
  });
}

// Lock report/log store filter for non-admin/SM based on their assigned store
function lockStoreFilters(){
  const repStore = document.getElementById('repStore');
  const logStore = document.getElementById('logStore');
  if(!repStore || !logStore) return;

  if(isAdminUser){
    // Admin only: can see all stores
    repStore.disabled = false;
    repStore.classList.remove('locked-filter');
    logStore.disabled = false;
    logStore.classList.remove('locked-filter');
  } else {
    // SM and regular employee: lock to their assigned store only
    const storeToLock = currentStore || userStore;
    if(storeToLock){
      repStore.value = storeToLock;
      repStore.disabled = true;
      repStore.classList.add('locked-filter');
      logStore.value = storeToLock;
      logStore.disabled = true;
      logStore.classList.add('locked-filter');
    }
  }
}

// --- Inventory Loading ---
let inventory = {}; // {productName: {central: n, pioneer: n}}

async function loadInventory(){
  try {
    const snap = await db.collection('inventory').get();
    inventory={};
    snap.forEach(d=>{inventory[d.id]=d.data();});
  } catch(e){
    console.error('inventory load error:',e);
  }
  renderGrid();
}

// --- Mode ---
function setMode(mode){
  currentMode=mode;
  const sale=document.getElementById('modeSale');
  const pur=document.getElementById('modePurchase');
  const cartTitle=document.getElementById('cartTitle');
  const cartSub=document.getElementById('cartSub');
  const confirmBtn=document.getElementById('confirmBtn');
  if(mode==='sale'){
    sale.className='mode-btn active';
    pur.className='mode-btn';
    cartTitle.textContent='📤 銷售清單';
    cartSub.textContent='選擇銷售產品，確認後自動扣減庫存';
    confirmBtn.className='btn-confirm btn-confirm-sale';
    confirmBtn.textContent='✅ 確認交易';
  } else {
    sale.className='mode-btn';
    pur.className='mode-btn active-purchase';
    cartTitle.textContent='📥 進貨清單';
    cartSub.textContent='選擇進貨產品，確認後自動增加庫存';
    confirmBtn.className='btn-confirm btn-confirm-purchase';
    confirmBtn.textContent='✅ 確認進貨';
  }
}

// --- Category Bar ---
function renderCatBar(){
  const cats=['全部',...new Set(products.map(p=>p.cat))];
  const bar=document.getElementById('pcatBar');
  bar.innerHTML='';
  cats.forEach(cat=>{
    const btn=document.createElement('button');
    btn.className='pcat-btn'+(cat===currentCat?' active':'');
    btn.textContent=cat;
    btn.onclick=()=>{currentCat=cat;renderCatBar();renderGrid();};
    bar.appendChild(btn);
  });
}

// --- Product Grid ---
function parseMultiPrice(priceStr){
  // priceStr like "HKD 25 (細樽裝) / HKD 40 (大樽裝)"
  const result={};
  if(!priceStr||!priceStr.includes('/')) return result;
  priceStr.split(' / ').forEach(seg=>{
    const m=seg.match(/HKD\s*([\d.]+)\s*\(([^)]+)\)/);
    if(m) result[m[2]]=parseFloat(m[1]);
  });
  return result;
}

function getPackOptions(p){
  if(!p.label1) return null;
  const multiPrices=parseMultiPrice(p.price);
  const opts=[];
  if(p.label1) opts.push({label:p.label1,img:p.img1,price:multiPrices[p.label1]||0});
  if(p.label2) opts.push({label:p.label2,img:p.img2,price:multiPrices[p.label2]||0});
  return opts.length>0?opts:null;
}

function getSelectedPack(p){
  const saved=selectedPack[p.name];
  const opts=getPackOptions(p);
  if(!opts) return null;
  return saved&&opts.find(o=>o.label===saved)?saved:opts[0].label;
}

function getPackPrice(p,packLabel){
  const opts=getPackOptions(p);
  if(!opts) return getPriceNum(p.price);
  const opt=opts.find(o=>o.label===packLabel);
  if(opt) return opt.price;
  return getPriceNum(p.price);
}

function getPackImg(p,packLabel){
  const opts=getPackOptions(p);
  if(!opts) return p.local_img||null; // single-pack: local_img already has correct filename
  // Multi-pack: use img1 or img2 filename from opts
  const opt=opts.find(o=>o.label===packLabel)||opts[0];
  return opt.img||p.local_img||null;
}

function renderGrid(){
  const filtered=currentCat==='全部'?products:products.filter(p=>p.cat===currentCat);
  const grid=document.getElementById('pgrid');
  grid.innerHTML='';
  filtered.forEach(p=>{
    const inv=inventory[p.name]||{};
    const stock=currentStore?(inv[currentStore]??'—'):'—';
    const stockClass=typeof stock==='number'?(stock===0?'zero':stock<5?'low':''):'';
    const packOpts=getPackOptions(p);
    const selPack=getSelectedPack(p);
    const cartKey=selPack?p.name+'|'+selPack:p.name;
    const inCart=cart[cartKey]||{qty:0,price:getPackPrice(p,selPack),cat:p.cat,pack:selPack};
    const packImg=getPackImg(p,selPack);

    const card=document.createElement('div');
    card.className='pcard';

    // Image
    const imgWrap=document.createElement('div');
    imgWrap.className='pcard-img';
    if(packImg){
      const img=document.createElement('img');
      img.src='images/'+packImg;
      img.style='width:100%;height:100%;object-fit:cover;';
      img.onerror=()=>{img.style.display='none';imgWrap.textContent='🍜';};
      imgWrap.appendChild(img);
      imgWrap.classList.add('has-img');
    } else {
      imgWrap.textContent='🍜';
    }

    // Body
    const body=document.createElement('div');
    body.className='pcard-body';

    const name=document.createElement('div');
    name.className='pcard-name';
    name.textContent=p.name;

    // Price
    const price=document.createElement('div');
    price.className='pcard-price';
    price.textContent=p.price;

    // Stock
    const stockDiv=document.createElement('div');
    stockDiv.className='pccard-stock '+stockClass;
    stockDiv.textContent=typeof stock==='number'?`庫存：${stock} 件`:stock;

    // Pack selector (if multi-pack)
    if(packOpts&&packOpts.length>0){
      const packRow=document.createElement('div');
      packRow.style.cssText='display:flex;gap:.3rem;margin-bottom:.4rem;flex-wrap:wrap';
      packOpts.forEach(opt=>{
        const btn=document.createElement('button');
        btn.style.cssText=`padding:.2rem .55rem;border-radius:50px;font-size:.68rem;border:1.5px solid ${selPack===opt.label?'var(--red)':'var(--bd)'};background:${selPack===opt.label?'var(--red)':'white'};color:${selPack===opt.label?'white':'var(--muted)'};cursor:pointer;font-family:'Noto Sans TC',sans-serif;transition:var(--tr);`;
        btn.textContent=opt.label;
        btn.onclick=(e)=>{e.stopPropagation();selectedPack[p.name]=opt.label;renderGrid();};
        packRow.appendChild(btn);
      });
      body.appendChild(name);
      body.appendChild(packRow);
      body.appendChild(price);
      body.appendChild(stockDiv);
    } else {
      body.appendChild(name);
      body.appendChild(price);
      body.appendChild(stockDiv);
    }

    // Qty controls
    const qtyCtrl=document.createElement('div');
    qtyCtrl.className='qty-ctrl';

    const minus=document.createElement('button');
    minus.className='qty-btn'+(currentMode==='purchase'?' green':'');
    minus.textContent='−';
    minus.onclick=(e)=>{e.stopPropagation();changeQty(cartKey,-1,p,selPack);};

    const num=document.createElement('span');
    num.className='qty-num';
    num.textContent=inCart.qty;

    const plus=document.createElement('button');
    plus.className='qty-btn';
    plus.textContent='+';
    plus.onclick=(e)=>{e.stopPropagation();changeQty(cartKey,1,p,selPack);};

    qtyCtrl.appendChild(minus);
    qtyCtrl.appendChild(num);
    qtyCtrl.appendChild(plus);
    body.appendChild(qtyCtrl);
    card.appendChild(imgWrap);
    card.appendChild(body);
    grid.appendChild(card);
  });
}

// --- Cart Logic ---
function changeQty(cartKey,delta,p,selPack){
  // Allow if store is selected OR if user is logged in as employee (store inferred from email)
  if(!currentStore){
    const email = currentUser ? currentUser.email.toLowerCase() : '';
    // Infer store from email pattern
    if(email.includes('central')){ currentStore = 'central'; selectStoreDisplay('central'); }
    else if(email.includes('pioneer')){ currentStore = 'pioneer'; selectStoreDisplay('pioneer'); }
    else {
      toast('請先選擇分店');
      showStoreSelect();
      return;
    }
  }
  if(!cart[cartKey]){
    cart[cartKey]={qty:0,price:getPackPrice(p,selPack),cat:p.cat,name:p.name,pack:selPack};
  }
  cart[cartKey].qty+=delta;
  if(cart[cartKey].qty<=0){delete cart[cartKey];}
  renderCart();
  renderGrid();
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
