import sys; sys.stdout.reconfigure(encoding='utf-8')
c = open('inventory.html','r',encoding='utf-8-sig').read()
anchor = "getElementById('logSidebar').innerHTML"
idx = c.find(anchor)
print(c[idx:idx+1500])
