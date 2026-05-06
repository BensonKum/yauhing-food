data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# Check the exact bytes around 58680-58720
print('Bytes 58680-58720 (hex):')
chunk = data[58680:58720]
for i, b in enumerate(chunk[:40]):
    print(f'{58680+i:04x}: {b:02x} {"["+chr(b)+"]" if 32<=b<127 else ""}')
print()

# Check the insert point more carefully
# The last p-card should have closed at 58684, insertion at 58689
print('Bytes 58684-58710:')
for i, b in enumerate(chunk[4:30]):
    print(f'{58684+i:04x}: {b:02x} {"["+chr(b)+"]" if 32<=b<127 else ""}')