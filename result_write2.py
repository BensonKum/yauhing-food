# -*- coding: utf-8 -*-
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\result.txt', 'wb') as f:
    f.write((u'File size: ' + str(len(data)) + u'\n').encode('utf-8'))
    sh = u'\u4e0a\u6d77\u9ea4'.encode('utf-8')  # 上海麵
    f.write((u'shanghai count: ' + str(data.count(sh)) + u'\n').encode('utf-8'))
    f.write((u'total cards: ' + str(data.count(b'<div class="p-card ')) + u'\n').encode('utf-8'))
    f.write((u'no-image: ' + str(data.count(b'p-card no-image')) + u'\n').encode('utf-8'))
    # Find first grad-ch after 58689
    p = data.find(b'grad-ch">', 58689)
    if p >= 0:
        e = data.find(b'<', p+9)
        name = data[p+9:e]
        f.write((u'first grad-ch: ' + name.decode('utf-8', errors='replace') + u'\n').encode('utf-8'))
    f.write(u'Done\n'.encode('utf-8'))