# -*- coding: utf-8 -*-
import shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

src = r'C:\Users\admin\Desktop\QClaw\備份\祐興網站\20260507_044447_fresh_powder_placeholder'
dst = r'C:\Users\admin\.qclaw\workspace\yauhing-food'

# 1. Backup current
shutil.copy(dst + '\\index.html', dst + '\\index_revert_backup.html')

# 2. Restore from backup
shutil.copy(src + '\\index.html', dst + '\\index.html')
shutil.copy(src + '\\products.json', dst + '\\products.json')
print('Files restored from backup')

# 3. Verify
size = __import__('os').path.getsize(dst + '\\index.html')
print('index.html size:', size)

# 4. Git commit
r1 = subprocess.run(['git', 'add', '-A'], cwd=dst, capture_output=True)
r2 = subprocess.run(['git', 'status'], cwd=dst, capture_output=True, text=True)
print('Git status:', r2.stdout)

# 5. Commit
r3 = subprocess.run(['git', 'commit', '-m', 'Revert to clean placeholder state (backup 20260507_044447)'], cwd=dst, capture_output=True, text=True)
print('Commit:', r3.stdout, r3.stderr)

# 6. Push
r4 = subprocess.run(['git', 'push'], cwd=dst, capture_output=True, text=True)
print('Push:', r4.stdout, r4.stderr)