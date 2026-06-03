c = open('inventory.html', 'r', encoding='utf-8-sig').read()

import re

# Remove OLD function definitions (non-window.xxx versions)
# Pattern: function editTransaction(id){ ... } (not inside window.xxx)

# For editTransaction - remove the OLD version (with alert)
old_edit_pattern = r'function editTransaction\(id\)\{\s*alert\([^)]+\);\s*\}'
new_edit = '// OLD editTransaction removed'

c = re.sub(old_edit_pattern, new_edit, c, count=1)
print('Removed OLD editTransaction')

# For deleteTransaction - remove the OLD version (with db.collection)
old_delete_pattern = r'function deleteTransaction\(id\)\{[^}]*db\.collection[^}]*\}[^}]*\}'
new_delete = '// OLD deleteTransaction removed'

c = re.sub(old_delete_pattern, new_delete, c, count=1, flags=re.DOTALL)
print('Removed OLD deleteTransaction')

# Verify only window.xxx versions remain
print(f"\nVerification:")
print(f"  'function editTransaction' count: {c.count('function editTransaction')}")
print(f"  'window.editTransaction' count: {c.count('window.editTransaction')}")
print(f"  'function deleteTransaction' count: {c.count('function deleteTransaction')}")
print(f"  'window.deleteTransaction' count: {c.count('window.deleteTransaction')}")

open('inventory.html', 'w', encoding='utf-8-sig').write(c)
print('\nSaved')
