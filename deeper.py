# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\deeper.txt', 'w', encoding='utf-8') as f:
    # Try all possible UTF-8 variants for 素纖麵
    candidates = [
        (b'\xe7\xb4\xa0\xe7\xb4\xab\xe9\xba\xb5', 'U+7D20/7E4B/9EB5'),
        (b'\xe7\xb4\xa0\xe7\xb4\xab', '2-char 素纖'),
        (b'\xe9\xba\xb5', '3rd char 麵'),
        (b'\xc2\xb5', 'LATIN SMALL LETTER mu'),
        (b'\xcb\x9c', 'LATIN SUBSCRIPT SMALL MU'),
    ]
    for bs, desc in candidates:
        f.write(f'{desc} ({bs.hex()}): {data.count(bs)} times\n')
    
    # Check ct div for 素纖麵
    ct_pos = data.find(b'<div class="ct"')
    ct_end = data.find(b'</div>', ct_pos) + 6
    ct_html = data[ct_pos:ct_end]
    f.write(f'\nCT div: bytes {ct_pos}-{ct_end}, len={len(ct_html)}\n')
    f.write(f'CT raw bytes: {ct_html.hex()}\n')
    f.write(f'CT decoded: {ct_html.decode("utf-8", errors="replace")}\n')
    
    # Search for each character separately in ct
    su = b'\xe7\xb4\xa0'  # 素
    xian = b'\xe7\xb4\xab'  # 纖
    mian = b'\xe9\xba\xb5'  # 麵
    f.write(f'\nIn CT:\n')
    f.write(f'  素 ({su.hex()}): {ct_html.count(su)}\n')
    f.write(f'  纖 ({xian.hex()}): {ct_html.count(xian)}\n')
    f.write(f'  麵 ({mian.hex()}): {ct_html.count(mian)}\n')
    
    # Check the 7 suxian p-cards - look at raw HTML around them
    f.write(f'\n=== Scanning all data-cat attributes ===\n')
    for m in re.finditer(b'data-cat="([^"]+)"', data):
        cat_bytes = m.group(1)
        try:
            cat_str = cat_bytes.decode('utf-8', errors='replace')
        except:
            cat_str = cat_bytes.hex()
        f.write(f'  byte {m.start()}: cat="{cat_str}" raw={cat_bytes.hex()}\n')