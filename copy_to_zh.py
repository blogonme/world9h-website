#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copy English HTML files to zh directory and translate content to Chinese
"""

import sys
import shutil
from pathlib import Path

# Set UTF-8 output for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Base directory
base_dir = Path(r'd:\Project\world9h.com\world9h-website')
source_dir = base_dir / 'world9h.com'
target_dir = base_dir / 'zh'

# Ensure target directory exists
target_dir.mkdir(exist_ok=True)

print("=" * 80)
print("STEP 1: Copying English HTML files to zh directory")
print("=" * 80)

# Files to copy
html_files = list(source_dir.rglob('*.html'))

copied_count = 0
error_count = 0

for html_file in html_files:
    try:
        # Get relative path from source_dir
        rel_path = html_file.relative_to(source_dir)
        
        # Target file path
        target_file = target_dir / rel_path
        
        # Create parent directories if needed
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(html_file, target_file)
        print(f"[OK] Copied: {rel_path}")
        copied_count += 1
        
    except Exception as e:
        print(f"[ERROR] {html_file}: {e}")
        error_count += 1

print("\n" + "=" * 80)
print(f"[SUMMARY]")
print(f"  Files copied: {copied_count}")
print(f"  Errors: {error_count}")
print("=" * 80)

if copied_count > 0:
    print(f"\n[SUCCESS] Copied {copied_count} files to zh directory!")
else:
    print(f"\n[INFO] No files copied.")
