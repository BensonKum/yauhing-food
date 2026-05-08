# -*- coding: utf-8 -*-
import subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

dst = r'C:\Users\admin\.qclaw\workspace\yauhing-food'
subprocess.run(['git', 'add', '網站工作流程.md'], cwd=dst, capture_output=True)
r = subprocess.run(['git', 'commit', '-m', 'Add website workflow documentation'], cwd=dst, capture_output=True, text=True)
print(r.stdout or r.stderr)
r2 = subprocess.run(['git', 'push'], cwd=dst, capture_output=True, text=True)
print(r2.stdout or r2.stderr)