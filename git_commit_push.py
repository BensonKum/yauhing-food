import subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

workspace = r'C:\Users\admin\.qclaw\workspace\yauhing-food'

# Git add
subprocess.run(['git', 'add', 'products.json'], cwd=workspace, capture_output=True)

# Git commit
r = subprocess.run(['git', 'commit', '-m', 'Add 12 fresh noodle products to products.json'], cwd=workspace, capture_output=True, text=True)
print('Commit:', r.stdout or r.stderr)

# Git push
r2 = subprocess.run(['git', 'push'], cwd=workspace, capture_output=True, text=True)
print('Push:', r2.stdout or r2.stderr)