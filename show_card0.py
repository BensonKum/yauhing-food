c = open('inventory.html', 'r', encoding='utf-8-sig').read()

# Card 0 at 79196 is the date card closing, the dummy should be right after
# Let's look at position 79150 to see the full picture
chunk = c[79100:79300]
with open('tmp_card0_full.txt', 'w', encoding='utf-8') as f:
    f.write(chunk)
print('Written')
