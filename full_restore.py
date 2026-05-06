# -*- coding: utf-8 -*-
import shutil, subprocess, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src = r'C:\Users\admin\Desktop\QClaw\備份\祐興網站\20260507_044447_fresh_powder_placeholder'
dst = r'C:\Users\admin\.qclaw\workspace\yauhing-food'

# List all files in backup
files = []
for root, dirs, filenames in os.walk(src):
    for f in filenames:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, src)
        files.append((full, rel))
        print('Backup:', rel)

print('\n--- Restoring ---\n')

# Copy each file
for src_file, rel_path in files:
    dst_file = os.path.join(dst, rel_path)
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    shutil.copy2(src_file, dst_file)
    print('Restored:', rel_path)

# Check size of restored index.html
size = os.path.getsize(dst + '\\index.html')
print('\nindex.html size:', size)

# Count divs
data = open(dst + '\\index.html', 'rb').read()
print('<div>:', data.count(b'<div'))
print('</div>:', data.count(b'</div>'))

print('\n--- Git commit ---\n')

subprocess.run(['git', 'add', '-A'], cwd=dst, capture_output=True)
r = subprocess.run(['git', 'status'], cwd=dst, capture_output=True, text=True)
print(r.stdout)

r2 = subprocess.run(['git', 'commit', '-m', 'Restore from backup 20260507_044447'], cwd=dst, capture_output=True, text=True)
print(r2.stdout or r2.stderr)

r3 = subprocess.run(['git', 'push'], cwd=dst, capture_output=True, text=True)
print(r3.stdout or r3.stderr)