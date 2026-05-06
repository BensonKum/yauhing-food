with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb') as f:
    raw = f.read()

pg_div_open = raw.find(b'<div class="pg" id="pg">')
count = 0
p = pg_div_open

while p < len(raw):
    next_open = raw.find(b'<div', p+1)
    next_close = raw.find(b'</div>', p+1)
    
    if next_close < 0:
        break
    
    use_open = next_open >= 0 and next_open < next_close
    use_close = not use_open
    
    if use_close:
        count -= 1
        if count == 0:
            pg_close = next_close
            # Write result to file
            with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\result.txt', 'w', encoding='utf-8') as out:
                out.write(f'pg div CLOSES at byte: {pg_close}\n')
                chunk = raw[pg_close:pg_close+200].decode('utf-8', errors='replace')
                out.write(f'Context: {chunk[:200]}\n')
                out.write(f'pg div spans bytes {pg_div_open} to {pg_close}\n')
                out.write(f'Total size: {pg_close - pg_div_open} bytes\n')
            print(f'SUCCESS: pg close at {pg_close}')
            break
        p = next_close + 5
    else:
        count += 1
        p = next_open + 4