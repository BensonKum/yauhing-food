with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', encoding='utf-8') as f:
    c = f.read()

# Card 3 starts at 42158, ends at 42494
card3_start = 42158
card3_end = 42494

# Remove card 3 (including the newline after it)
c = c[:card3_start] + c[card3_end:]

print(f'Removed card 3 (range {card3_start}-{card3_end})')

with open(r'C:\Users\user\.qclaw\workspace\yauhing-food\index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done - now should have only 2 cards')
