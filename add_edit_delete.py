c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# Add editTransaction and deleteTransaction functions
# Insert after the quick button handler (which is after renderLog)
js_to_add = '''
function editTransaction(id){
  alert('編輯交易功能開發中\\nID: '+id);
}

function deleteTransaction(id){
  if(!confirm('確定刪除這筆交易？')) return;
  db.collection('inventory_transactions').doc(id).delete().then(()=>{
    alert('已刪除');
    renderLog();
  }).catch(e=>alert('刪除失敗: '+e.message));
}

'''

# Find the quick button handler and insert after it
idx = c.find('// Quick button click handler for log date card')
if idx >= 0:
    # Find end of that block (next empty line or next function)
    # Insert before it
    c = c[:idx] + js_to_add + c[idx:]
    print('OK: editTransaction + deleteTransaction added')
else:
    print('FAIL: Quick button handler not found')

open('inventory.html', 'w', encoding='utf-8-sig').write(c)
