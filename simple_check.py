import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\simple_out.txt', 'w', encoding='utf-8') as f:
    f.write(f'File size: {len(data)}\n')
    
    shanghai = b'\xe4\xb8\x8a\xe6\xb5\xb7'
    count = data.count(shanghai)
    f.write(f'Shanghai count: {count}\n')
    
    f.write(f'Total p-card: {data.count(b"<div class=\"p-card ")}\n')
    f.write(f'Total no-image: {data.count(b"p-card no-image")}\n')
    
    grad_pos = data.find(b'grad-ch">', 58689)
    if grad_pos >= 0:
        end = data.find(b'<', grad_pos + 9)
        name = data[grad_pos+9:end].decode('utf-8', errors='replace')
        f.write(f'First grad-ch: {name}\n')
    
    f.write('Done\n')