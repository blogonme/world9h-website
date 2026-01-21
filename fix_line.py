#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct fix for line 605 in index.html
"""

# File path
file_path = r'd:\Project\world9h.com\world9h-website\index.html'

# Read all lines
with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print(f"\nLine 605 before fix:")
print(repr(lines[604]))

# Directly replace line 605 (index 604)
# The line should contain the language switcher with Chinese text
if '<span>' in lines[604] and '</span>' in lines[604]:
    # Extract the part before and after the span
    before_span = lines[604].split('<span>')[0] + '<span>'
    after_span = '</span>' + lines[604].split('</span>')[1]
    # Reconstruct with correct Chinese
    lines[604] = before_span + '中文' + after_span
    print(f"\nLine 605 after fix:")
    print(repr(lines[604]))
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("\n[SUCCESS] File updated!")
else:
    print("\n[ERROR] Line 605 doesn't match expected pattern")
