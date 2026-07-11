import sys
sys.path.insert(0, 'C:/Users/user/.qclaw/workspace/yauhing-food')
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('C:/Users/user/.qclaw/firebase-service-account.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

for sku, name, price in [
    ('YM901', '咖喱魚蛋 (8粒裝)', 'HKD 10'),
    ('YM902', '白魚蛋 (8粒裝)', 'HKD 12'),
]:
    doc_ref = db.collection('inventory').document(sku)
    doc_ref.set({
        'name': name,
        'price': price,
        'stock': 0,
        'sku': sku,
        'cat': '凍品',
        'pioneer': 0,
        'central': 0,
        'lastUpdated': ''
    })
    print(f'Added {sku} to Firestore')

# Verify
docs = db.collection('inventory').limit(3).get()
for d in docs:
    print(f'Firestore doc: {d.id} -> {d.to_dict().get("name","")}')
print('Done!')
