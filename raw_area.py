data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# Show bytes 58670-58750 raw with hex
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\raw_area.txt', 'w', encoding='utf-8') as f:
    f.write('Bytes 58670-58750:\n')
    for i in range(58670, 58750):
        b = data[i]
        c = chr(b) if 32 <= b < 127 else ''
        f.write(f'{i:05d}: {b:02x}  {c}\n')
    f.write('\nDecoded 58670-58750:\n')
    f.write(data[58670:58750].decode('utf-8', errors='replace'))