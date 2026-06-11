# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('古法大地魚蝦籽麵 (粗)')
card_start = html.rfind('<div class="product-card', max(0, idx-500), idx)
next_card = html.find('<div class="product-card', idx+1)
print(f'Card starts at: {card_start}')
print(f'Next card at: {next_card}')

if card_start >= 0 and next_card > 0:
    card_html = html[card_start:next_card]
    with open('gufa_card.txt', 'w', encoding='utf-8') as f:
        f.write(card_html)
    print(f'Card length: {len(card_html)} chars')
    print('Written to gufa_card.txt')
else:
    print('ERROR: could not find boundaries')
    # Try broader search
    if card_start < 0:
        # Find product-card differently
        snippet = html[idx-300:idx]
        with open('debug.txt', 'w', encoding='utf-8') as f:
            f.write(snippet)
        print('Wrote debug.txt (context before)')
