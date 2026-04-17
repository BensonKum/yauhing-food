import re

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html', encoding='utf-8-sig') as f:
    content = f.read()

# Find showStoreSelect
idx = content.find('function showStoreSelect')
end = content.find('\n}', idx)
print('showStoreSelect:', idx, '-', end)
snippet = content[idx:end+2]
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\store_func.txt', 'w', encoding='utf-8') as f:
    f.write(snippet)

# Find selectStore
idx2 = content.find('function selectStore')
end2 = content.find('\n}', idx2)
snippet2 = content[idx2:end2+2]
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\select_func.txt', 'w', encoding='utf-8') as f:
    f.write(snippet2)

print('Done')
