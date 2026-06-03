c = open('inventory.html', 'r', encoding='utf-8-sig').read()

script_start = c.rfind('<script>')
script_end = c.rfind('</script>')
main_script = c[script_start+8:script_end]

# Binary search: split the script in half and test each half
mid = len(main_script) // 2

# Find a safe split point (not inside a string or comment)
# Simple approach: find the last ; or } before mid
safe_split = main_script.rfind(';', 0, mid)
if safe_split == -1:
    safe_split = main_script.rfind('\n', 0, mid)

print(f'Total length: {len(main_script)}')
print(f'Split at: {safe_split}')

part1 = main_script[:safe_split+1]
part2 = main_script[safe_split+1:]

with open('tmp_part1.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(part1)
with open('tmp_part2.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write(part2)

print(f'Part1: {len(part1)} chars -> tmp_part1.js')
print(f'Part2: {len(part2)} chars -> tmp_part2.js')
