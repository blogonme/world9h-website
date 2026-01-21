#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all HTML files with encoding issues
"""

import sys
from pathlib import Path

# Set UTF-8 output for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Base directory
base_dir = Path(r'd:\Project\world9h.com\world9h-website')

# Files with issues from the report
files_to_fix = [
    'world9h.com/about.html',
    'world9h.com/contact.html',
    'world9h.com/index.html',
    'world9h.com/Logistics.html',
    'world9h.com/services.html',
    'zh/world9h.com/index.html',
    'world9h.com/4/2/1313559.html',
    'world9h.com/4/2/1334296.html',
    'world9h.com/4/2/1334299.html',
    'world9h.com/4/2/1360287.html',
    'world9h.com/4/2/1360288.html',
]

print("=" * 80)
print("BATCH FIX: Encoding Issues")
print("=" * 80)

fixed_count = 0
error_count = 0

for file_path in files_to_fix:
    full_path = base_dir / file_path
    
    try:
        # Read file
        with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        original_content = content
        
        # Fix HTML entity for Chinese
        content = content.replace('&#20013;&#25991;', '中文')
        
        # Fix any replacement characters in language switcher spans
        # This is a more targeted fix for spans that might have garbled text
        import re
        
        # Find language switcher spans and fix them
        def fix_span(match):
            span_content = match.group(1)
            # If it contains replacement characters, replace with Chinese
            if '�' in span_content or '\ufffd' in span_content:
                return '<span>中文</span>'
            return match.group(0)
        
        content = re.sub(r'<span>([^<>]*?)</span>', fix_span, content)
        
        # Only write if content changed
        if content != original_content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Fixed: {file_path}")
            fixed_count += 1
        else:
            print(f"[SKIP] No changes needed: {file_path}")
    
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        error_count += 1

print("\n" + "=" * 80)
print(f"[SUMMARY]")
print(f"  Files processed: {len(files_to_fix)}")
print(f"  Files fixed: {fixed_count}")
print(f"  Errors: {error_count}")
print("=" * 80)

if fixed_count > 0:
    print(f"\n[SUCCESS] Fixed {fixed_count} files!")
    print(f"\nRecommendation: Refresh your browser to see the changes.")
else:
    print(f"\n[INFO] No files needed fixing.")
