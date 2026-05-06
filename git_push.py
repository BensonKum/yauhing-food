import subprocess
result = subprocess.run(['git', 'add', 'index.html'], cwd=r'C:\Users\admin\.qclaw\workspace\yauhing-food', capture_output=True, text=True)
print('add:', result.returncode, result.stderr)

msg = 'Add 12 fresh noodle product cards (name-only, photo TBD)'
result = subprocess.run(['git', 'commit', '-m', msg], cwd=r'C:\Users\admin\.qclaw\workspace\yauhing-food', capture_output=True, text=True)
print('commit:', result.returncode, result.stdout, result.stderr)

result = subprocess.run(['git', 'push'], cwd=r'C:\Users\admin\.qclaw\workspace\yauhing-food', capture_output=True, text=True)
print('push:', result.returncode, result.stderr)