c = open('inventory.html', 'r', encoding='utf-8-sig').read()

pos = 55159
print(f'Character at {pos}: {repr(c[pos])}')
print(f'Context (pos-80 to pos+20):')
print(repr(c[pos-80:pos+20]))
print()
print('Decoded context:')
print(c[pos-80:pos+20])
