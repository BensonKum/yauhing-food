c = open('inventory.html', 'r', encoding='utf-8-sig').read()

script_start = c.rfind('<script>')
script_end = c.rfind('</script>')
main_script = c[script_start+8:script_end]

# Create a minimal HTML test file
test_html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body>
<h1>JS Syntax Test</h1>
<div id="result">Loading...</div>
<script>
try {{
    {main_script}
    document.getElementById('result').innerHTML = '<span style="color:green">JS OK - no syntax errors</span>';
}} catch(e) {{
    document.getElementById('result').innerHTML = '<span style="red">ERROR: ' + e.message + '</span>';
}}
</script>
</body></html>'''

with open('tmp_test_syntax.html', 'w', encoding='utf-8') as f:
    f.write(test_html)

print(f'Written tmp_test_syntax.html ({len(test_html)} chars)')
print(f'Main script: {len(main_script)} chars')
