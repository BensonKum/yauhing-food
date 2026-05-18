function loadReportData() {
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
    // 按類型分組
    const groups = { sale:[], purchase:[], transfer:[], loss:[] };
    snap.forEach(doc => {
      const t = doc.data().type || '';
      if(groups[t]) groups[t].push(doc);
      else groups['sale'].push(doc); // default to sale
    });

    html = '';
    const typeLabels = { sale:'🟢 銷售', purchase:'🔵 進貨', transfer:'🟠 調撥', loss:'🔴 報損' };
    const typeOrder = ['sale','purchase','transfer','loss'];

    typeOrder.forEach(type => {
      if(!groups[type].length) return;
      html += '<div class="rep-group-header">' + typeLabels[type] + ' (' + groups[type].length + '筆)</div>';
      groups[type].forEach(doc => {
      const d = doc.data();
      const dt = d.createdAt ? (d.createdAt.toDate ? d.createdAt.toDate() : new Date(d.createdAt)) : null;
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

      html += '<div class="log-entry" data-toggle="1">'
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


// Event delegation for log entry toggle (Report tab)
document.addEventListener('click', function(e) {
  const entry = e.target.closest('.log-entry');
  if (!entry) return;
  const detail = entry.querySelector('.log-entry-detail');
  if (!detail) return;
  detail.style.display = (detail.style.display === 'block') ? 'none' : 'block';
});

