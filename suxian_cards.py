# -*- coding: utf-8 -*-
import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\suxian_cards.txt', 'wb') as f:
    suxian_cat = b'data-cat="\xe7\xb4\xa0\xe7\xba\x96\xe9\xba\xb5"'
    
    f.write('=== 7 素纖麵 cards - detailed analysis ===\n'.encode('utf-8'))
    
    for idx, m in enumerate(re.finditer(suxian_cat, data)):
        pos = m.start()
        # Get full card area (find enclosing p-card)
        # p-card starts at the nearest <div class="p-card before pos
        pcard_start = data.rfind(b'<div class="p-card', 0, pos)
        # p-card ends at </div> (the closing of p-card itself, not inner divs)
        # Strategy: find the p-card closing by looking at nesting
        # Start after pcard_start, look for </div> that matches the p-card structure
        search_pos = pcard_start + 100
        depth = 1
        i = search_pos
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
        pcard_end = i
        
        card_data = data[pcard_start:pcard_end]
        
        grad_m = re.search(b'grad-ch">([^<]+)', card_data)
        pn_m = re.search(b'p-name">([^<]+)', card_data)
        img_m = re.search(b'src="([^"]+)"', card_data)
        note_m = re.search(b'p-note">([^<]+)', card_data)
        
        g = (grad_m.group(1).decode('utf-8', errors='replace') if grad_m else 'NO GRAD-CH')
        p = (pn_m.group(1).decode('utf-8', errors='replace') if pn_m else 'NO P-NAME')
        img = (img_m.group(1).decode('utf-8', errors='replace') if img_m else 'NO IMG')
        note = (note_m.group(1).decode('utf-8', errors='replace') if note_m else 'NO NOTE')
        
        opens = card_data.count(b'<div')
        closes = card_data.count(b'</div>')
        
        f.write(('\n--- Card %d: byte %d to %d ---\n' % (idx+1, pcard_start, pcard_end)).encode('utf-8'))
        f.write(('grad-ch: %s\n' % g).encode('utf-8'))
        f.write(('p-name: %s\n' % p).encode('utf-8'))
        f.write(('img: %s\n' % img).encode('utf-8'))
        f.write(('note: %s\n' % note).encode('utf-8'))
        f.write(('<div>: %d, </div>: %d, balance: %s\n' % (opens, closes, 'OK' if opens==closes else 'MISMATCH')).encode('utf-8'))
        
        # Check for any orphan divs or unusual structures
        # Look for 素纖麵 in the card text
        suxian_bytes = b'\xe7\xb4\xa0\xe7\xba\x96\xe9\xba\xb5'
        count_in_card = card_data.count(suxian_bytes)
        f.write(('素纖麵 occurrences in card: %d\n' % count_in_card).encode('utf-8'))
    
    # Check overall file for the overall div mismatch
    f.write(('\n=== Overall div balance ===\n').encode('utf-8'))
    total_open = data.count(b'<div')
    total_close = data.count(b'</div>')
    f.write(('<div>: %d, </div>: %d\n' % (total_open, total_close)).encode('utf-8'))
    f.write(('MISMATCH: %d\n' % abs(total_open - total_close)).encode('utf-8'))
    
    # Check all 62 p-cards div balance
    f.write(('\n=== All 62 p-card div balance ===\n').encode('utf-8'))
    mismatch_count = 0
    for m in re.finditer(b'<div class="p-card ', data):
        pcard_start = m.start()
        search_pos = pcard_start + 100
        depth = 1
        i = search_pos
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
        pcard_end = i
        card_data = data[pcard_start:pcard_end]
        opens = card_data.count(b'<div')
        closes = card_data.count(b'</div>')
        if opens != closes:
            mismatch_count += 1
            grad_m = re.search(b'grad-ch">([^<]+)', card_data)
            g = (grad_m.group(1).decode('utf-8', errors='replace') if grad_m else '?')
            f.write(('MISMATCH at byte %d (%s): %d open vs %d close\n' % (pcard_start, g, opens, closes)).encode('utf-8'))
    f.write(('\nTotal p-card mismatches: %d\n' % mismatch_count).encode('utf-8'))