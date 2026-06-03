import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('inventory.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find renderEmployeeList and add console.log debugging
old = """async function renderEmployeeList(){
  if(!isAdminUser && !isSMUser) return;
  const empList = document.getElementById('empList');
  empList.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--muted)">載入中...</div>';
  
  try {
    let snap;
    if(isAdminUser && !isSMUser){ snap = await db.collection('employees').orderBy('createdAt','desc').get(); }
    else { snap = await db.collection('employees').where('role','in',['central','pioneer','sm']).get(); }"""

new = """async function renderEmployeeList(){
  console.log('[EMP] renderEmployeeList called. isAdminUser='+isAdminUser+' isSMUser='+isSMUser+' userStore='+userStore);
  if(!isAdminUser && !isSMUser){ console.log('[EMP] SKIP: not admin nor SM'); return; }
  const empList = document.getElementById('empList');
  if(!empList){ console.error('[EMP] ERROR: empList element not found!'); return; }
  empList.innerHTML = '<div style="text-align:center;padding:2rem;color:var(--muted)">載入中...</div>';
  
  try {
    let snap;
    if(isAdminUser && !isSMUser){
      console.log('[EMP] Querying as ADMIN (all employees, ordered)');
      snap = await db.collection('employees').orderBy('createdAt','desc').get();
    } else {
      console.log('[EMP] Querying as SM/NonAdmin (central/pioneer/sm only)');
      snap = await db.collection('employees').where('role','in',['central','pioneer','sm']).get();
    }
    console.log('[EMP] Firestore query returned '+snap.size+' results');"""

if old in c:
    c = c.replace(old, new, 1)
    
    # Also add more debug after the query
    old2 = "const emps = []; snap.forEach(d => emps.push({id: d.id, ...d.data()}));"
    new2 = """const emps = []; snap.forEach(d => emps.push({id: d.id, ...d.data()}));
    console.log('[EMP] Parsed '+emps.length+' employees:', emps.map(e=>e.name+'('+e.role+')').join(', '));"""
    
    c = c.replace(old2, new2, 1)
    
    with open('inventory.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Debug logging added to renderEmployeeList()")
else:
    print("❌ Could not find target code block")
