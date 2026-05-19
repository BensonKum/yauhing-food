
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