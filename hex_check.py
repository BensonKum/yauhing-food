# -*- coding: utf-8 -*-
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\hex_check.txt', 'wb') as f:
    # Find first grad-ch after 58689
    gp = data.find(b'grad-ch">', 58689)
    if gp >= 0:
        ge = data.find(b'<', gp+9)
        name_bytes = data[gp+9:ge]
        f.write((u'grad-ch bytes:\n').encode('utf-8'))
        f.write((u'hex: ' + name_bytes.hex() + u'\n').encode('utf-8'))
        f.write((u'decoded: ' + name_bytes.decode('utf-8', errors='replace') + u'\n').encode('utf-8'))
        # Check each character
        for i, c in enumerate(name_bytes.decode('utf-8', errors='replace')):
            b = name_bytes[i*3:(i+1)*3] if i*3+3 <= len(name_bytes) else name_bytes[i*3:]
            f.write((u'  char[%d]=%s bytes=%s\n' % (i, c, b.hex())).encode('utf-8'))
    # Try finding 上 byte by byte
    shang = b'\xe4\xb8\x8a'
    f.write((u'\nSearching for 上 (E4B88A): count=%d\n' % data.count(shang)).encode('utf-8'))
    hai = b'\xe6\xb5\xb7'
    f.write((u'Searching for 海 (E6B5B7): count=%d\n' % data.count(hai)).encode('utf-8'))
    # Full 上海麵
    full = b'\xe4\xb8\x8a\xe6\xb5\xb7'
    f.write((u'Searching for 上海: count=%d\n' % data.count(full)).encode('utf-8'))