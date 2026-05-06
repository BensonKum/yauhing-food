import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

ct_pos = data.find(b'id="ct"')
segment = data[ct_pos:ct_pos+3000].decode('utf-8', errors='replace')

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\ct_content.txt', 'w', encoding='utf-8') as f:
    f.write(f'CT at byte {ct_pos}\n\n')
    f.write(segment[:2000])