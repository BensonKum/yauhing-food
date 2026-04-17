import json, os, re

BASE = r'C:\Users\admin\.qclaw\workspace\yauhing-food'
products_file = os.path.join(BASE, 'products.json')
index_file = os.path.join(BASE, 'index.html')

# Load products.json
with open(products_file, 'r', encoding='utf-8') as f:
    products = json.load(f)

# Load index.html and extract img src paths in card order
with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all img src from .p-card blocks in order
img_pattern = re.compile(r'<img src="images/([^"]+)"')
html_imgs = img_pattern.findall(html)

# Extract product names from p-card blocks in order
card_pattern = re.compile(r'<div class="p-card[^>]*>(.*?)</div>\s*</div>', re.DOTALL)
# Actually, simpler: find all p-card name lines
name_pattern = re.compile(r'<h3 class="p-name">([^<]+)</h3>')
html_names = name_pattern.findall(html)

print(f"Index.html has {len(html_imgs)} images, {len(html_names)} product cards")
print(f"Products.json has {len(products)} products")

# Create name->image mapping from index.html
html_img_map = {}
for i, name in enumerate(html_names):
    if i < len(html_imgs):
        html_img_map[name] = html_imgs[i]

# For multi-pack products, find the right product and assign img1 or img2
images_dir = os.path.join(BASE, 'images')
available = set(os.listdir(images_dir))

done = 0
matched_from_html = []
for p in products:
    name = p.get('name', '')
    # Try 1: direct name match from index.html
    if name in html_img_map:
        img = html_img_map[name]
        if img in available:
            p['local_img'] = img
            done += 1
            matched_from_html.append(name)
            continue

    # Try 2: img1/img2 (already matched)
    for k in ['img1', 'img2']:
        v = p.get(k)
        if v and v in available:
            p['local_img'] = v
            done += 1
            break
    else:
        # Try 3: name fuzzy match
        name_clean = name.replace('(', '').replace(')', '').replace('（', '').replace('）', '')
        found = None
        for img in available:
            img_clean = img.replace('.jpg', '').replace('(', '').replace(')', '')
            if name_clean and (name_clean in img_clean or img_clean in name_clean):
                found = img
                break
        if found:
            p['local_img'] = found
            done += 1
        else:
            p['local_img'] = None

print(f"\nMatched from index.html: {len(matched_from_html)}")
print(f"Total matched: {done}/{len(products)}")

missing = [(p['name'], p.get('cat')) for p in products if not p.get('local_img')]
print(f"\nMissing ({len(missing)}):")
for name, cat in missing:
    print(f"  [{cat}] {name}")

with open(products_file, 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
print("products.json updated!")
