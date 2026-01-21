#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix file structure - move files from zh/world9h.com to zh/ and remove duplicates
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
zh_dir = base_dir / 'zh'
zh_world9h_dir = zh_dir / 'world9h.com'

print("=" * 80)
print("Fixing File Structure")
print("=" * 80)

# Check if zh/world9h.com exists
if not zh_world9h_dir.exists():
    print("[INFO] zh/world9h.com directory does not exist. Nothing to fix.")
    sys.exit(0)

# Get all HTML files from zh/world9h.com
html_files = list(zh_world9h_dir.rglob('*.html'))

print(f"\nFound {len(html_files)} HTML files in zh/world9h.com/")

moved_count = 0
error_count = 0

for html_file in html_files:
    try:
        # Get relative path from zh/world9h.com
        rel_path = html_file.relative_to(zh_world9h_dir)
        
        # Target file path in zh/
        target_file = zh_dir / rel_path
        
        # Create parent directories if needed
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file (overwrite if exists)
        if target_file.exists():
            target_file.unlink()
        
        shutil.move(str(html_file), str(target_file))
        print(f"[OK] Moved: {rel_path}")
        moved_count += 1
        
    except Exception as e:
        print(f"[ERROR] {html_file}: {e}")
        error_count += 1

print("\n" + "=" * 80)
print(f"[SUMMARY]")
print(f"  Files moved: {moved_count}")
print(f"  Errors: {error_count}")
print("=" * 80)

# Try to remove empty zh/world9h.com directory
try:
    if zh_world9h_dir.exists():
        # Remove empty subdirectories
        for item in sorted(zh_world9h_dir.rglob('*'), reverse=True):
            if item.is_dir() and not any(item.iterdir()):
                item.rmdir()
                print(f"[OK] Removed empty directory: {item.relative_to(zh_dir)}")
        
        # Remove zh/world9h.com if empty
        if not any(zh_world9h_dir.iterdir()):
            zh_world9h_dir.rmdir()
            print(f"[OK] Removed empty directory: world9h.com")
except Exception as e:
    print(f"[WARNING] Could not remove directories: {e}")

if moved_count > 0:
    print(f"\n[SUCCESS] Moved {moved_count} files from zh/world9h.com/ to zh/!")
