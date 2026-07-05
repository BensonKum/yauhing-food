import json
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime, timezone, timedelta

cred = credentials.Certificate(r'C:\Users\user\.qclaw\firebase-service-account.json')
initialize_app(cred)
db = firestore.client()

docs = list(db.collection('inventory_transactions').order_by('createdAt', direction=firestore.Query.DESCENDING).limit(200).stream())
txns = []
for d in docs:
    data = d.to_dict(); data['_id'] = d.id; txns.append(data)

hk = timezone(timedelta(hours=8))
dataRows = []
for t in txns:
    dt = t.get('createdAt')
    if not dt:
        continue
    dt = dt.astimezone(hk)
    dtStr = dt.strftime('%m/%d %H:%M')
    typeLabel = 'IN' if t.get('type') == 'purchase' else 'OUT'
    storeLabel = 'central' if t.get('store') == 'central' else 'pioneer'
    items = t.get('items') or []
    if not items and t.get('productName'):
        items = [{'sku': t.get('productCode', ''), 'name': t.get('productName'),
                  'qty': t.get('qty', 1), 'price': t.get('price', 0)}]
    for i in items:
        rawSku = i.get('sku') or i.get('productCode') or ''
        name = i.get('name') or i.get('productName') or rawSku
        qty = i.get('qty') or 1
        price = float(i.get('price') or 0)
        lineTotal = float(i.get('lineTotal') or (qty * price))
        dataRows.append([dtStr, typeLabel, storeLabel, rawSku, name, qty, price, lineTotal])

clean = [r for r in dataRows if (r[3] and str(r[3]).strip() != '') or (r[4] and str(r[4]).strip() != '')]
print('TOTAL raw:', len(dataRows), '| after ghost guard:', len(clean))
print('FIRST 3 rows:')
for idx, r in enumerate(clean[:3]):
    print('  row', 6 + idx, '| SKU=', repr(r[3]), '| name=', repr(r[4]), '| qty=', r[5])
print('ANY row with empty SKU and empty name (ghost)?',
      any((not r[3] or str(r[3]).strip() == '') and (not r[4] or str(r[4]).strip() == '') for r in clean))
