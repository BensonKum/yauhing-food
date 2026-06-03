
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

/