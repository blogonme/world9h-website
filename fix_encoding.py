#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix corrupted Chinese characters in index.html
"""

import re

# File path
file_path = r'd:\Project\world9h.com\world9h-website\index.html'

# Read file
with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find the corrupted pattern and replace with correct Chinese
# The pattern is: ><span>CORRUPTED_CHARS</span></a
# We need to replace it with: ><span>中文</span></a

# Use regex to find and replace the corrupted span content
pattern = r'(<span>)[^<>]*?(</span></a)'
replacement = r'\1中文\2'

# Find the specific line with language switcher
lines = content.split('\n')
modified = False

for i, line in enumerate(lines):
    # Look for the language switcher line with img tag and span
    if 'p.cdn-static.cn/77918_1689669803884230fe.png' in line and '<span>' in line:
        # This is the Chinese language option line
        old_line = line
        # Replace the span content
        new_line = re.sub(r'(<span>).*?(</span>)', r'\1中文\2', line)
        if new_line != old_line:
            lines[i] = new_line
            modified = True
            print(f"[OK] Fixed line {i+1}")
            print(f"  Old: {old_line.strip()}")
            print(f"  New: {new_line.strip()}")

if modified:
    # Save the file
    content = '\n'.join(lines)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n[SUCCESS] File saved with correct Chinese characters")
else:
    print("[INFO] No changes needed")

print("\nDone!")
