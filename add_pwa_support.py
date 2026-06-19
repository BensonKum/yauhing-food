#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add PWA support to inventory.html
Usage: python add_pwa_support.py
"""

import re

INVENTORY_FILE = 'inventory.html'

def add_pwa_support():
    try:
        with open(INVENTORY_FILE, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        print(f"Read {INVENTORY_FILE}")
    except Exception as e:
        print(f"Cannot read file: {e}")
        return

    # 1. Add PWA meta tags after <title>
    head_tags = """
    <!-- PWA Support -->
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#000000">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Yau Hing Inventory">
    <link rel="apple-touch-icon" href="/icons/icon-152x152.png">
    """

    pattern1 = r'(<title>.*?</title>)'
    replacement1 = r'\1' + head_tags

    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        print("Added PWA meta tags to <head>")
    else:
        print("WARNING: Cannot find <title> tag")

    # 2. Add Service Worker registration before </body>
    sw_script = """
    
    <!-- PWA Service Worker Registration -->
    <script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
              console.log('SW registered:', registration);
              if (registration.waiting) {
                registration.waiting.postMessage({ type: 'SKIP_WAITING' });
              }
            })
            .catch(error => {
              console.log('SW registration failed:', error);
            });
        });
      }
    </script>
    """

    pattern2 = r'(</body>)'
    replacement2 = sw_script + r'\1'

    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        print("Added Service Worker registration script")
    else:
        print("WARNING: Cannot find </body> tag")

    # Save file
    try:
        with open(INVENTORY_FILE, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        print(f"\nDone! {INVENTORY_FILE} updated")
    except Exception as e:
        print(f"Cannot save file: {e}")
        return

if __name__ == '__main__':
    add_pwa_support()
