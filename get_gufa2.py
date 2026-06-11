# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('古法大地魚蝦籽麵 (粗)')
# Find card start - look for p-card
card_start = html.rfind('<div class="p-card', max(0, idx-500), idx)
next_card = html.find('<div class="p-card', idx+1)
print(f'Card starts at: {card_start}')
print(f'Next card at: {next_card}')

if card_start >= 0 and next_card > 0:
    card_html = html[card_start:next_card]
    with open('gufa_card.txt', 'w', encoding='utf-8') as f:
        f.write(card_html)
    print(f'Card length: {len(card_html)} chars')
    print('Written to gufa_card.txt')
