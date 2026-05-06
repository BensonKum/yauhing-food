# -*- coding: utf-8 -*-
import re
data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\card_structure.txt', 'wb') as f:
    # Look at a few p-cards to understand the structure
    for m in re.finditer(b'<div class="p-card ', data):
        pos = m.start()
        # Read 600 bytes from card start
        chunk = data[pos:pos+600]
        f.write(('=== Card at byte %d (first 600 bytes) ===\n' % pos).encode('utf-8'))
        f.write(chunk[:600].decode('utf-8', errors='replace').encode('utf-8'))
        f.write('\n\n'.encode('utf-8'))
        if pos > 58000:  # only show first 3
            break

    # Check the area AFTER last suxian card (58468) and BEFORE first fresh (58689)
    f.write('=== Gap 58468-58689 (221 bytes) ===\n'.encode('utf-8'))
    gap = data[58468:58689]
    f.write(gap.decode('utf-8', errors='replace').encode('utf-8'))
    f.write('\n\n'.encode('utf-8'))
    
    # Now check: where does each card close?
    # Look at card from 58689 (上海麵)
    f.write('=== 上海麵 card 58689 full structure ===\n'.encode('utf-8'))
    chunk = data[58689:58689+800]
    f.write(chunk.decode('utf-8', errors='replace').encode('utf-8'))
    f.write('\n\n'.encode('utf-8'))
    
    # Check for missing </div> between cards
    # The pattern: after one card's </div></div>, the next card starts
    f.write('=== Looking for card boundaries ===\n'.encode('utf-8'))
    # Find all p-card starts
    starts = [m.start() for m in re.finditer(b'<div class="p-card ', data)]
    f.write(('Total p-cards: %d\n' % len(starts)).encode('utf-8'))
    f.write(('First few starts: %s\n' % starts[:5]).encode('utf-8'))
    
    # Check the boundary after byte 58689 card
    # If divs are balanced per card (3 open, 2 close), there must be 1 extra </div> somewhere
    # Look at what comes after the 上海麵 card (59115 is next card start)
    f.write('\n=== After 上海麵 card (around 59000-59120) ===\n'.encode('utf-8'))
    area = data[58900:59120]
    f.write(area.decode('utf-8', errors='replace').encode('utf-8'))
    f.write('\n'.encode('utf-8'))
    
    # Check for raw bytes pattern
    f.write('\n=== Hex 58900-59120 ===\n'.encode('utf-8'))
    # Find the </div></div> pattern
    div_end = data.find(b'</div></div>', 58689)
    f.write(('First </div></div> after 58689: byte %d\n' % div_end).encode('utf-8'))
    if div_end > 0:
        f.write(('Context: %s\n' % data[div_end:div_end+50].decode('utf-8', errors='replace')).encode('utf-8'))
    
    # Count missing </div>: total <div>=563, </div>=562. 1 missing.
    # Where is it? Probably inside cards.
    # Check if the MISSING one is per-card (all 62 cards missing 1 each = 62 missing)
    # OR if it's a single global issue
    # 62 cards × 2 closes = 124 expected closes from cards
    # But we're only counting the TOTAL </div> in the whole file
    # The overall file has 563 <div> and 562 </div>
    # That's only 1 missing total, NOT per card
    
    f.write('\n=== REANALYSIS ===\n'.encode('utf-8'))
    f.write(('Total <div>: %d, Total </div>: %d\n' % (data.count(b'<div'), data.count(b'</div>'))).encode('utf-8'))
    f.write('Only 1 missing </div> in entire file!\n'.encode('utf-8'))
    
    # Check: does the p-card structure actually need 3 closing </div>s?
    # <div class="p-card">  -- 1
    #   <div class="p-img">  -- 2  
    #   </div>
    #   <div class="p-info">  -- 3
    #   </div>
    # </div>
    # That's 3 opens, 3 closes = balanced
    # But the file only has 2 closes per card (3 open, 2 close counted)
    # That means the p-card itself is not closed properly
    
    # Check: is there a pattern where the closing </div></div> comes from TWO cards merged?
    # Like: </div></div>  (closes card1-info + card1-card)
    # Then next card immediately starts?
    
    # Find ALL occurrences of </div></div> (double close)
    double_closes = [m.start() for m in re.finditer(b'</div></div>', data)]
    f.write(('\nDouble close </div></div> at %d positions: %s\n' % (len(double_closes), double_closes)).encode('utf-8'))
    
    # Count single </div>
    single_close = data.count(b'</div>') - 2 * data.count(b'</div></div>')
    f.write(('Single close </div> (not part of double): %d\n' % single_close).encode('utf-8'))