c = open('inventory.html', 'r', encoding='utf-8-sig').read()

script_start = c.rfind('<script>')
script_end = c.rfind('</script>')
main_script = c[script_start+8:script_end]

# Simpler approach: just count raw quotes
dq_count = main_script.count('"')
sq_count = main_script.count("'")

print(f'Raw double-quote count: {dq_count}')
print(f'Raw single-quote count: {sq_count}')
print(f'Double quote is ODD: {dq_count % 2 == 1}')
print(f'Single quote is ODD: {sq_count % 2 == 1}')

# Find ALL " positions and check balance more carefully
# Walk through tracking state
depth = 0  # paren depth
brace = 0  # brace depth
bracket = 0  # bracket depth  
in_single = False
in_double = False
in_comment_line = False
in_comment_block = False

i = 0
while i < len(main_script):
    ch = main_script[i]
    
    # Check for comments first
    if not in_single and not in_double:
        if i < len(main_script) - 1:
            two = main_script[i:i+2]
            if two == '//':
                in_comment_line = True
            elif two == '/*':
                in_comment_block = True
                i += 2
                continue
        
        if ch == '\n' and in_comment_line:
            in_comment_line = False
    
    if in_comment_line or in_comment_block:
        if in_comment_block and i < len(main_script) - 1 and main_script[i:i+2] == '*/':
            in_comment_block = False
        i += 1
        continue
    
    # String handling (simple)
    if ch == '"' and not in_single:
        # Simple: count it
        in_double = not in_double
    elif ch == "'" and not in_double:
        in_single = not in_single
    elif not in_single and not in_double:
        if ch == '(': depth += 1
        elif ch == ')': depth -= 1
        elif ch == '{': brace += 1
        elif ch == '}': brace -= 1
        elif ch == '[': bracket += 1
        elif ch == ']': bracket -= 1
    
    i += 1

print(f'\nFinal states:')
print(f'in_double={in_double}, in_single={in_single}')
print(f'depth={depth} (parens), brace={brace} (braces), bracket={bracket}')

if in_double or in_single:
    print('\n⚠️ UNCLOSED STRING DETECTED!')
