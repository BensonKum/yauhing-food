with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb') as f:
    raw = f.read()

# Just scan the area around 53000-54000
print('Bytes 53230-54000:')
chunk = raw[53230:54000]
decoded = chunk.decode('utf-8', errors='replace')
print(decoded[:300])