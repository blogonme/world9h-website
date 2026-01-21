#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify translation completeness - check for remaining English content
"""

import sys
import re
from pathlib import Path

# Set UTF-8 output for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Base directory
base_dir = Path(r'd:\Project\world9h.com\world9h-website')
zh_dir = base_dir / 'zh'

# English patterns to check
ENGLISH_CHECKS = [
    'THE NINE INTERNATIONAL SUPPLY CHAIN',
    'HOME',
    'ABOUT US',
    'SERVICE',
    'CONTACT US',
    'NEWS',
    'LEARN MORE',
    'READ MORE',
]

print("=" * 80)
print("Translation Verification")
print("=" * 80)

# Main pages to check
main_pages = [
    'index.html',
    'about.html',
    'services.html',
    'contact.html',
    'Logistics.html',
]

issues_found = []

for page in main_pages:
    page_path = zh_dir / page
    
    if not page_path.exists():
        print(f"[SKIP] File not found: {page}")
        continue
    
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    page_issues = []
    
    # Check for English patterns
    for pattern in ENGLISH_CHECKS:
        if pattern in content:
            count = content.count(pattern)
            page_issues.append(f"Found '{pattern}' ({count} times)")
    
    # Check for common English words in visible content
    # Extract text between > and < (rough approximation)
    visible_text = re.findall(r'>([^<>]+)<', content)
    english_words = []
    
    for text in visible_text:
        text = text.strip()
        # Skip if it's just whitespace, numbers, or symbols
        if not text or text.isspace() or text.isdigit():
            continue
        # Check if it contains English letters (but allow mixed content)
        if re.search(r'\b[A-Z][a-z]+\b', text):
            # Common English words that might appear
            if any(word in text for word in ['Home', 'About', 'Service', 'Contact', 'News', 'More', 'Read', 'Learn']):
                if text not in english_words:
                    english_words.append(text[:50])  # Limit length
    
    if page_issues:
        print(f"\n[!] {page}")
        for issue in page_issues:
            print(f"    {issue}")
        issues_found.extend(page_issues)
    
    if english_words and len(english_words) > 0:
        print(f"\n[?] Possible English content in {page}:")
        for word in english_words[:5]:  # Show first 5
            print(f"    '{word}'")

print("\n" + "=" * 80)

if issues_found:
    print(f"[WARNING] Found {len(issues_found)} potential issues")
    print("Some English content may still remain in the files.")
else:
    print(f"[OK] No critical English patterns found!")
    print("Translation appears complete.")

print("=" * 80)
