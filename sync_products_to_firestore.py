# -*- coding: utf-8 -*-
# 將本地 products_v2.json (107 款) sync 去 Firestore /products 集合
# 用 firebase_admin (service account) 寫入，bypass firestore.rules
# doc id = sku (方便 inventory 日後按 sku 讀取)
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SA_KEY = r"C:\Users\user\.qclaw\firebase-service-account.json"
SRC = os.path.join(BASE, "products_v2.json")

import firebase_admin
from firebase_admin import credentials, firestore

def main():
    # 去 BOM
    raw = open(SRC, "r", encoding="utf-8-sig").read()
    data = json.loads(raw)
    if not isinstance(data, list):
        print("ERROR: products_v2.json 頂層唔係 array"); sys.exit(1)
    print("本地產品數: %d" % len(data))

    cred = credentials.Certificate(SA_KEY)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    col = db.collection("products")
    ok = 0; skip = 0; err = 0
    for p in data:
        sku = p.get("sku")
        if not sku:
            print("SKIP 無 sku: %s" % p.get("name", "?"))
            skip += 1; continue
        try:
            col.document(str(sku)).set(p)
            ok += 1
        except Exception as e:
            print("ERROR %s: %s" % (sku, e))
            err += 1
    print("=== sync 完成: 寫入 %d, 跳過 %d, 失敗 %d ===" % (ok, skip, err))
    # 驗證 server 端數量
    real = len(list(col.stream()))
    print("Firestore /products 實際 docs: %d" % real)

if __name__ == "__main__":
    main()
