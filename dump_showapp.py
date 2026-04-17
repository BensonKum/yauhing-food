with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html', encoding='utf-8-sig') as f:
    c = f.read()

idx = c.find('function showApp')
# Find the next function or section boundary
end = c.find('// ---', idx)
snippet = c[idx:end]

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\showapp.txt', 'w', encoding='utf-8') as f:
    f.write(snippet)

# Also find the onAuthStateChanged section
idx2 = c.find('auth.onAuthStateChanged')
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\onauth.txt', 'w', encoding='utf-8') as f:
    f.write(c[idx2:idx2+300])

print('Done')
