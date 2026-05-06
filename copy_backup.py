# -*- coding: utf-8 -*-
import shutil
src = r'C:\Users\admin\Desktop\QClaw\備份\祐興網站\20260507_044447_fresh_powder_placeholder'
dst = r'C:\Users\admin\.qclaw\workspace\yauhing-food'

shutil.copy(src + '\\index.html', dst + '\\backup_index.html')
shutil.copy(src + '\\products.json', dst + '\\backup_products.json')

import os
f1 = os.path.getsize(dst + '\\backup_index.html')
f2 = os.path.getsize(dst + '\\backup_products.json')
print('Copied: index.html %d bytes, products.json %d bytes' % (f1, f2))