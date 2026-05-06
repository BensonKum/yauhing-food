# -*- coding: utf-8 -*-
import re, subprocess

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\full_analysis.txt', 'wb') as f:
    # Run git log
    r = subprocess.run(['git', 'log', '--oneline', '-8'], cwd=r'C:\Users\admin\.qclaw\workspace\yauhing-food', capture_output=True, text=True)
    f.write(('Git log:\n%s\n' % r.stdout).encode('utf-8'))
    
    # Check status
    r2 = subprocess.run(['git', 'status'], cwd=r'C:\Users\admin\.qclaw\workspace\yauhing-food', capture_output=True, text=True)
    f.write(('Git status: %s\n' % r2.stdout).encode('utf-8'))
    
    # Show the complete p-card structure for all 14 no-image cards
    data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
    
    f.write(('\n=== All 14 no-image cards ===\n').encode('utf-8'))
    idx = 0
    for m in re.finditer(b'<div class="p-card no-image"', data):
        pos = m.start()
        # Find card end
        depth = 1
        i = pos + 100
        while i < len(data) and depth > 0:
            if data[i:i+5] == b'<div ':
                depth += 1
                i += 5
            elif data[i:i+6] == b'</div>':
                depth -= 1
                i += 6
                if depth == 0:
                    break
            else:
                i += 1
        card_end = i
        card_data = data[pos:card_end]
        
        grad = re.search(b'grad-ch">([^<]+)', card_data)
        pn = re.search(b'p-name">([^<]+)', card_data)
        cat = re.search(b'data-cat="([^"]+)"', card_data)
        
        g = (grad.group(1).decode('utf-8', errors='replace') if grad else 'NO-GRAD')
        p = (pn.group(1).decode('utf-8', errors='replace') if pn else 'NO-PNAME')
        c = (cat.group(1).decode('utf-8', errors='replace') if cat else 'NO-CAT')
        
        f.write(('\n%d. byte %d: cat="%s" grad="%s" pname="%s" (%d bytes)\n' % (
            idx+1, pos, c, g, p, len(card_data))).encode('utf-8'))
        idx += 1
    
    # Show the suxian section end - where does it actually close?
    # The last suxian card (豆乳麵) should end at some byte
    suxian_cards = [(m.start(), m.start()) for m in re.finditer(b'data-cat="\xe7\xb4\xa0\xe7\xba\x96\xe9\xba\xb5"', data)]
    
    if suxian_cards:
        last_pos = suxian_cards[-1][0]
        depth = 1
        i = last_pos + 100
        while i < len(data) and depth > 0:
            if data[i:i+5] == b'<div ':
                depth += 1
                i += 5
            elif data[i:i+6] == b'</div>':
                depth -= 1
                i += 6
                if depth == 0:
                    break
            else:
                i += 1
        last_suxian_end = i
        f.write(('\nLast suxian (豆乳麵) card ends at byte %d\n' % last_suxian_end).encode('utf-8'))
        
        # Show the exact bytes between last suxian end and first fresh powder (58689)
        gap = data[last_suxian_end:58689]
        f.write(('Gap (%d bytes):\n' % len(gap)).encode('utf-8'))
        f.write(gap.decode('utf-8', errors='replace').encode('utf-8'))
        f.write(u'\n\n'.encode('utf-8'))
        
        # Check: is there anything BEFORE the 上海麵 card that looks out of place?
        # Check bytes 58500-58689
        check = data[58500:58689]
        f.write(('Area 58500-58689 (%d bytes):\n' % len(check)).encode('utf-8'))
        f.write(check.decode('utf-8', errors='replace').encode('utf-8'))
        f.write(u'\n\n'.encode('utf-8'))
        
        # Check: what comes AFTER the 上海麵 card?
        sh_end = data.find(b'</div></div>', 58689) + 12
        f.write(('上海麵 card ends at %d\n' % sh_end).encode('utf-8'))
        f.write(('After 上海麵 (next 200 bytes):\n').encode('utf-8'))
        f.write(data[sh_end:sh_end+200].decode('utf-8', errors='replace').encode('utf-8'))