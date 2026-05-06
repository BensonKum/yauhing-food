data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()

# Precise: find the LAST p-card's p-price closing, then the card's closing </div>
last_card = data.rfind(b'p-card ')
last_price = data.find(b'p-price', last_card)

# Find </div> after price
d1 = data.find(b'</div>', last_price)
print('price div close:', d1)
# Find next </div>
d2 = data.find(b'</div>', d1+1)
print('p-info div close:', d2)
# Find next </div> (p-card close)
d3 = data.find(b'</div>', d2+1)
print('p-card div close:', d3)

print('\nContext around d3 (58680-58710):')
chunk = data[58680:58710]
print(chunk.decode('utf-8', errors='replace'))

print(f'\nInsert point: {d3+5}')
print('Will insert after:', data[d3:d3+10])