# -*- coding: utf-8 -*-
import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\all_suxian_raw.txt', 'wb') as f:
    suxian_cat = b'data-cat="\xe7\xb4\xa0\xe7\xba\x96\xe9\xba\xb5"'  # 素纖麵 (with wrong char)
    suxian_correct = b'data-cat="\xe7\xb4\xa0\xe7\xb4\xab\xe9\xba\xb5"'  # 素纖麵 (correct)
    
    f.write(('Wrong char (e7ba96): %d\n' % data.count(suxian_cat)).encode('utf-8'))
    f.write(('Correct char (e7b4ab): %d\n' % data.count(suxian_correct)).encode('utf-8'))
    
    # Find all suxian cards with correct encoding
    f.write(('\n=== All 7 素纖麵 cards (with correct UTF-8 check) ===\n').encode('utf-8'))
    count = 0
    for m in re.finditer(suxian_cat, data):
        pos = m.start()
        # Get card start
        card_start = data.rfind(b'<div', 0, pos)
        # Find where this card ends
        # Look for the p-card closing </div>
        # Each p-card should end with </div></div> (card end + parent close)
        search_start = pos
        # Find first </div>
        div1 = data.find(b'</div>', search_start)
        # Find second </div>
        div2 = data.find(b'</div>', div1 + 6)
        card_end = div2 + 6
        
        seg = data[card_start:card_end]
        opens = seg.count(b'<div')
        closes = seg.count(b'</div>')
        
        grad = re.search(b'grad-ch">([^<]+)', seg)
        pn = re.search(b'p-name">([^<]+)', seg)
        name = (grad.group(1).decode('utf-8', errors='replace') if grad else '?')
        pname = (pn.group(1).decode('utf-8', errors='replace') if pn else '?')
        
        f.write(('\n--- Card %d at byte %d ---\n' % (count+1, card_start)).encode('utf-8'))
        f.write(('Name: %s | p-name: %s\n' % (name, pname)).encode('utf-8'))
        f.write(('Card bytes: %d to %d (len=%d)\n' % (card_start, card_end, len(seg))).encode('utf-8'))
        f.write(('<div count: %d, </div> count: %d\n' % (opens, closes)).encode('utf-8'))
        f.write(('Status: %s\n' % ('OK' if opens==closes else 'MISMATCH')).encode('utf-8'))
        
        # Also show first 200 chars of raw HTML
        f.write(('Raw HTML (first 300 bytes):\n').encode('utf-8'))
        f.write(seg[:300].decode('utf-8', errors='replace').encode('utf-8'))
        f.write(u'\n'.encode('utf-8'))
        count += 1
    
    # Now check the area between last suxian card and first fresh powder (58689)
    last_end = 0
    for m in re.finditer(suxian_cat, data):
        search_start = m.start()
        div1 = data.find(b'</div>', search_start)
        div2 = data.find(b'</div>', div1 + 6)
        card_end = div2 + 6
        if card_end > last_end:
            last_end = card_end
    
    f.write(('\n=== Gap analysis (last suxian to fresh powder) ===\n').encode('utf-8'))
    f.write(('Last suxian ends at byte %d\n' % last_end).encode('utf-8'))
    f.write('First fresh powder at byte 58689\n'.encode('utf-8'))
    if last_end > 0 and last_end < 58689:
        gap = data[last_end:58689]
        f.write(('Gap: %d bytes\n' % len(gap)).encode('utf-8'))
        f.write(('Content: %s\n' % gap.decode('utf-8', errors='replace')[:500]).encode('utf-8'))
        # Check div balance in gap
        gap_opens = gap.count(b'<div')
        gap_closes = gap.count(b'</div>')
        f.write(('Gap <div>: %d, </div>: %d, balance: %s\n' % (
            gap_opens, gap_closes, 'OK' if gap_opens==gap_closes else 'MISMATCH'
        )).encode('utf-8'))
    
    # Check overall file structure around suxian cards
    # Specifically look for orphan elements
    f.write(('\n=== Check for orphan divs near suxian ===\n').encode('utf-8'))
    # Find area around byte 53000-59000
    segment = data[53000:59000]
    f.write(('Area 53000-59000: <div>=%d </div>=%d balance=%s\n' % (
        segment.count(b'<div'), segment.count(b'</div>'),
        'OK' if segment.count(b'<div')==segment.count(b'</div>') else 'MISMATCH'
    )).encode('utf-8'))