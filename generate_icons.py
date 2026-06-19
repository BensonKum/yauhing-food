#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PWA Icon Generator
Usage: python generate_icons.py <logo.png>
"""

import sys
import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Need Pillow: pip install Pillow")
    sys.exit(1)

ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

def generate_icons(logo_path, output_dir='icons'):
    if not os.path.exists(logo_path):
        print(f"File not found: {logo_path}")
        sys.exit(1)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        img = Image.open(logo_path)
        print(f"Read LOGO: {logo_path}")
        print(f"Size: {img.size[0]}x{img.size[1]}")
        print(f"Format: {img.format}")
    except Exception as e:
        print(f"Cannot read image: {e}")
        sys.exit(1)

    # Convert to RGBA if needed (for transparency support)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    for size in ICON_SIZES:
        output_path = os.path.join(output_dir, f"icon-{size}x{size}.png")
        try:
            resized = img.resize((size, size), Image.LANCZOS)
            resized.save(output_path, "PNG")
            print(f"Generated: icon-{size}x{size}.png")
        except Exception as e:
            print(f"Failed ({size}x{size}): {e}")

    print(f"\nDone! All icons saved to {output_dir}/")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_icons.py <logo.png>")
        sys.exit(1)
    
    logo_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'icons'
    
    generate_icons(logo_path, output_dir)
