c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# Read around position 81984 to see the OLD editTransaction
print('=== Around 81984 ===')
print(repr(c[81970:82100]))
print()

print('=== Around 82048 ===')
print(repr(c[82030:82200]))
