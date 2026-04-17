import re

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html', encoding='utf-8-sig') as f:
    content = f.read()

# Find and print the showStoreSelect function
idx = content.find('function showStoreSelect')
print('Found showStoreSelect at:', idx)
print(content[idx:idx+600])
print('\n---\n')

# Find and print selectStore function
idx2 = content.find('function selectStore')
print('Found selectStore at:', idx2)
print(content[idx2:idx2+400])
