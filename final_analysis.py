# -*- coding: utf-8 -*-
import re

data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\final_analysis.txt', 'wb') as f:
    # Check git status via file read
    try:
        git_status = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\.git\HEAD', 'rb').read()
        f.write(('Git HEAD: %s\n' % git_status).encode('utf-8'))
    except:
        f.write('Cannot read git HEAD\n'.encode('utf-8'))
    
    f.write(('\n=== All 14 no-image cards ===\n').encode('utf-8'))
    idx = 0
    for m in re.finditer(b'<div class="p-card no-image"', data):
        pos = m.start()
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
        
        f.write(('%d. byte %d: cat=%s grad=%s pname=%s (%d bytes)\n' % (
            idx+1, pos, c, g, p, len(card_data))).encode('utf-8'))
        idx += 1
    
    # Where does the last suxian card really end?
    suxian_last_pos = 58035  # 豆乳麵
    depth = 1
    i = suxian_last_pos + 100
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
    
    f.write(('\nLast suxian ends at byte %d\n' % last_suxian_end).encode('utf-8'))
    f.write('First fresh at 58689\n'.encode('utf-8'))
    f.write('Gap: %d bytes\n' % (58689 - last_suxian_end).encode('utf-8'))
    
    # Check the closing of last suxian card
    # The last suxian card has multi-pack and ends with pk-sw divs
    # Let's see exactly what the last card contains
    last_card = data[58035:last_suxian_end]
    f.write(('\nLast suxian card (豆乳麵) full HTML:\n').encode('utf-8'))
    f.write(last_card.decode('utf-8', errors='replace').encode('utf-8'))
    f.write('\n\n'.encode('utf-8'))
    
    # Check: what are the last bytes before byte 58689?
    f.write('Bytes 58400-58689:\n'.encode('utf-8'))
    f.write(data[58400:58689].decode('utf-8', errors='replace').encode('utf-8'))
    f.write('\n\n'.encode('utf-8'))
    
    # Count divs in the gap (58468-58689)
    gap = data[last_suxian_end:58689]
    f.write('Gap div count: %d <div, %d </div>\n' % (gap.count(b'<div'), gap.count(b'</div>')))
    
    # Show the card structure at 58689 (first fresh)
    f.write('\n=== First fresh powder card (58689) full HTML ===\n'.encode('utf-8'))
    sh_depth = 1
    sh_i = 58689 + 100
    while sh_i < len(data) and sh_depth > 0:
        if data[sh_i:sh_i+5] == b'<div ':
            sh_depth += 1
            sh_i += 5
        elif data[sh_i:sh_i+6] == b'</div>':
            sh_depth -= 1
            sh_i += 6
            if sh_depth == 0:
                break
        else:
            sh_i += 1
    sh_end = sh_i
    f.write(data[58689:sh_end].decode('utf-8', errors='replace').encode('utf-8'))