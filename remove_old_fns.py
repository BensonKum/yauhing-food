c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# The OLD functions to remove
old_edit = "function editTransaction(id){\n  alert('編輯功能開發中，稍後推出...\\nID: '+id);\n}"
old_delete = "function deleteTransaction(id){\n  if(!confirm('確定刪除此交易？')) return;\n  db.collection('inventory_transactions').doc(id).delete().then(()=>{\n    alert('已刪除');\n    renderLog();\n  });\n}"

print(f'OLD editTransaction found: {old_edit in c}')
print(f'OLD deleteTransaction found: {old_delete in c}')

if old_edit in c:
    c = c.replace(old_edit, '// OLD editTransaction removed', 1)
    print('  -> Removed')
    
if old_delete in c:
    c = c.replace(old_delete, '// OLD deleteTransaction removed', 1)
    print('  -> Removed')

open('inventory.html', 'w', encoding='utf-8-sig').write(c)
print('Saved')
