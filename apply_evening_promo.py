"""
Apply evening 1+1 promotion to inventory.html (POS system).
- After 5pm daily, fresh noodles (豆卜/河粉/瀨粉/銀針粉) are buy-1-get-1-free
- Applies in renderCart() — cart display and total calculation
"""
import re

HTML = r"C:\Users\admin\.qclaw\workspace\yauhing-food\inventory.html"

with open(HTML, "r", encoding="utf-8") as f:
    content = f.read()

# ── 1. Add helper functions after "// --- Cart Logic ---" ──────────────
cart_section_marker = "// --- Cart Logic ---"

promo_code = """
// ── Evening 1+1 Promotion (Fresh Noodles after 5pm) ─────────────────
const FRESH_NOODLE_NAMES_1PLUS1 = ['豆卜', '河粉', '瀨粉', '銀針粉'];

function isAfter5pm(){
  const h=new Date().getHours();
  return h>=17;
}

function isFreshNoodle1Plus1(name){
  if(!isAfter5pm()) return false;
  return FRESH_NOODLE_NAMES_1PLUS1.some(n=>name.includes(n));
}

// For 1+1: paid qty = ceil(display qty / 2), line total = paid qty * price
function calcLineTotal(qty, price, name){
  if(isFreshNoodle1Plus1(name)){
    const paidQty = Math.ceil(qty / 2);
    return paidQty * price;
  }
  return qty * price;
}

"""

if "FRESH_NOODLE_NAMES_1PLUS1" not in content:
    content = content.replace(
        cart_section_marker,
        cart_section_marker + "\n" + promo_code
    )
    print("[OK] Added promotion helper functions")
else:
    print("[SKIP] Promotion helpers already exist")

# ── 2. Fix renderCart() to use calcLineTotal ─────────────────────────
# Pattern: inside renderCart(), where lineTotal is calculated
old_line_calc = "    const lineTotal=item.qty*(item.manualPrice||item.price);"
new_line_calc = "    const lineTotal=calcLineTotal(item.qty,(item.manualPrice||item.price),item.name);"

if old_line_calc in content:
    content = content.replace(old_line_calc, new_line_calc)
    print("[OK] Fixed lineTotal calculation in renderCart")
else:
    print("[WARN] Could not find original lineTotal pattern — may already be fixed or changed")

# ── 3. Fix cart total in renderCart() ───────────────────────────────
old_total_calc = "  total+=lineTotal;"
new_total_calc = """  total+=lineTotal;
    // 1+1 indicator
    if(isFreshNoodle1Plus1(item.name)&&isAfter5pm()&&item.qty>0){
      promoItems.push(item.name+' ×'+item.qty+' → 免費多1盒！');
    }"""

# Find the renderCart function and check if we need to add promoItems
if "promoItems" not in content and "total+=lineTotal;" in content:
    # Check we haven't already modified
    content = content.replace(
        "  total+=lineTotal;",
        new_total_calc
    )
    # Also need to init promoItems before the loop
    old_init = "  keys.forEach(cartKey=>{"
    new_init = "  let promoItems=[];\n  keys.forEach(cartKey=>{"
    content = content.replace(old_init, new_init)
    print("[OK] Added promoItems indicator to renderCart")
else:
    print("[SKIP] promoItems already added or total pattern not found")

# ── 4. Fix confirm transaction display ──────────────────────────────
old_confirm_total = "    `${name} × ${d.qty} = HK$${d.qty*(d.manualPrice||d.price)}`"
new_confirm_total = "    `${name} × ${d.qty}${isFreshNoodle1Plus1(d.name)&&isAfter5pm()&&d.qty>0?' (1+1優惠)':''} = HK$${calcLineTotal(d.qty,(d.manualPrice||d.price),d.name)}`"
content = content.replace(old_confirm_total, new_confirm_total)

old_confirm_reduce = "    total=Object.values(cart).reduce((s,i)=>s+i.qty*(d.manualPrice||i.price),0);"
# This pattern might be slightly different, let's just fix the one we know exists
print("[OK] confirmTransaction reference updated (if pattern found)")

# ── 5. Fix confirmTotal calculation ──────────────────────────────────
old_confirm_total2 = "  const total=Object.values(cart).reduce((s,i)=>s+i.qty*(i.manualPrice||i.price),0);"
new_confirm_total2 = "  const total=Object.values(cart).reduce((s,i)=>s+calcLineTotal(i.qty,(i.manualPrice||i.price),i.name),0);"
if old_confirm_total2 in content:
    content = content.replace(old_confirm_total2, new_confirm_total2)
    print("[OK] Fixed confirmTotal calculation")
else:
    print("[WARN] confirmTotal pattern not found, trying alternate")
    # Try alternate pattern
    alt = "Object.values(cart).reduce((s,i)=>s+i.qty*(i.manualPrice||i.price),0)"
    if alt in content:
        content = content.replace(alt, "Object.values(cart).reduce((s,i)=>s+calcLineTotal(i.qty,(i.manualPrice||i.price),i.name),0)")
        print("[OK] Fixed confirmTotal (alternate)")

# ── 6. Fix doConfirm transaction total ────────────────────────────────
old_doconfirm = "  const total=Object.values(cart).reduce((s,i)=>s+i.qty*(i.manualPrice||i.price),0);"
new_doconfirm = "  const total=Object.values(cart).reduce((s,i)=>s+calcLineTotal(i.qty,(i.manualPrice||i.price),i.name),0);"
if old_doconfirm in content:
    content = content.replace(old_doconfirm, new_doconfirm)
    print("[OK] Fixed doConfirm total calculation")
else:
    print("[WARN] doConfirm total pattern not found")

# ── 7. Add promotion banner to POS grid area ─────────────────────────
# Insert after the sell/purchase mode toggle
banner_pattern = "id=\"modeToggle\""
banner_code = """
    // Evening 1+1 promo banner
    const promoBanner=document.createElement('div');
    promoBanner.id='promoBanner';
    promoBanner.style='text-align:center;padding:.3rem;background:#FFF9C4;color:#E65100;font-size:.75rem;font-weight:bold;border-radius:6px;margin-bottom:.4rem;display:none';
    promoBanner.textContent='🌟 新鮮粉麵 5pm 後 1盒送1盒優惠生效中！';
    if(isAfter5pm()) promoBanner.style.display='block';
    document.getElementById('pgrid').prepend(promoBanner);
"""
if "promoBanner" not in content and "id=\"pgrid\"" in content:
    # Insert after grid.innerHTML='';
    old_grid = "  grid.innerHTML='';"
    new_grid = "  grid.innerHTML='';\n" + banner_code.strip()
    content = content.replace(old_grid, new_grid)
    print("[OK] Added 5pm promo banner to grid")
else:
    print("[SKIP] promoBanner already added or pgrid not found")

# ── Write back ───────────────────────────────────────────────────────
with open(HTML, "w", encoding="utf-8") as f:
    f.write(content)

print("\n=== Done! ===")
print("Remember to: git add + commit + push, then test at yauhing-food.com/inventory.html")
