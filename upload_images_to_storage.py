"""
Upload all images/ to Firebase Storage and generate inventory.html URL mappings.
Run once: python upload_images_to_storage.py
"""
import os
import json
from google.cloud import storage
from google.oauth2 import service_account

# ── Config ──────────────────────────────────────────────────────────
WORKSPACE = r"C:\Users\admin\.qclaw\workspace\yauhing-food"
IMAGES_DIR = os.path.join(WORKSPACE, "images")
KEY_PATH   = os.path.join(WORKSPACE, "serviceAccountKey.json")
BUCKET     = "yauhing-food.appspot.com"
STORAGE_PREFIX = "products"   # Firebase Storage path prefix

# ── Auth ─────────────────────────────────────────────────────────────
creds = service_account.Credentials.from_service_account_file(KEY_PATH)
client = storage.Client(credentials=creds, project=creds.project_id)
bucket = client.bucket(BUCKET)

# ── Upload ──────────────────────────────────────────────────────────
# Only upload files (skip folders like "placeholders/")
skipped = []
uploaded = []

files = [f for f in os.listdir(IMAGES_DIR)
         if os.path.isfile(os.path.join(IMAGES_DIR, f))]

print(f"Found {len(files)} files in images/")

for fname in sorted(files):
    local_path = os.path.join(IMAGES_DIR, fname)
    storage_path = f"{STORAGE_PREFIX}/{fname}"

    blob = bucket.blob(storage_path)
    blob.upload_from_filename(local_path, content_type="image/jpeg")
    blob.make_public()

    url = f"https://firebasestorage.googleapis.com/v0/b/{BUCKET}/o/{STORAGE_PREFIX}%2F{fname}?alt=media"
    uploaded.append((fname, url))
    print(f"  [OK] {fname}")

print(f"\n=== Upload Complete ===")
print(f"Total: {len(uploaded)} files")

# ── Write JS mapping ────────────────────────────────────────────────
# Generate a JS object for inventory.html
mapping_lines = ["// Firebase Storage image URLs (auto-generated)", "const firebaseStorageImages = {"]
for fname, url in uploaded:
    safe_name = fname.replace("'", "\\'")
    mapping_lines.append(f"  '{safe_name}': '{url}',")
mapping_lines.append("};")

mapping_js = "\n".join(mapping_lines)

# Write to a separate JS file for easy include
mapping_file = os.path.join(WORKSPACE, "firebase_storage_images.js")
with open(mapping_file, "w", encoding="utf-8") as f:
    f.write(mapping_js)

print(f"\nMapping written to: {mapping_file}")
print("\n=== Next Step ===")
print("1. Commit the new JS file: firebase_storage_images.js")
print("2. Update inventory.html to include the JS and use firebaseStorageImages[name]")
print("3. For now, print the mapping for review:")
print("\n--- URL Mapping (first 10) ---")
for fname, url in uploaded[:10]:
    print(f"{fname}: {url}")
