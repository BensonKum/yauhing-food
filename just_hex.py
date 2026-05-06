data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\hex_out.txt', 'wb') as f:
    chunk = data[58689:58750]
    f.write(chunk.hex().encode('utf-8'))
    f.write(u'\n'.encode('utf-8'))
    f.write(u'\n'.encode('utf-8'))
    f.write(chunk[:50].decode('utf-8', errors='replace').encode('utf-8'))