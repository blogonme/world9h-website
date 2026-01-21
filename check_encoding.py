#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check all HTML files for encoding errors and fix them
"""

import os
import re
import sys
from pathlib import Path

# Set UTF-8 output for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Base directory
base_dir = Path(r'd:\Project\world9h.com\world9h-website')

# Find all HTML files
html_files = list(base_dir.rglob('*.html'))

print(f"Found {len(html_files)} HTML files\n")
print("=" * 80)

# Track issues
issues_found = []
files_with_issues = []
files_to_fix = {}

for html_file in html_files:
    try:
        # Read file with error handling
        with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        file_issues = []
        needs_fix = False
        
        # Check for replacement character (indicates encoding problems)
        if '\ufffd' in content or '�' in content:
            count = content.count('\ufffd') + content.count('�')
            file_issues.append(f"Found {count} replacement characters")
            needs_fix = True
        
        # Check for HTML entities that should be Chinese
        if '&#20013;&#25991;' in content:
            count = content.count('&#20013;&#25991;')
            file_issues.append(f"Found HTML entity &#20013;&#25991; - {count} occurrences")
            needs_fix = True
        
        # Check for common garbled patterns in language switcher
        span_matches = re.findall(r'<span>([^<>]*)</span>', content)
        for match in span_matches:
            if '�' in match or '\ufffd' in match:
                file_issues.append(f"Garbled text in span: '{match[:20]}...'")
                needs_fix = True
        
        if file_issues:
            rel_path = html_file.relative_to(base_dir)
            files_with_issues.append(str(rel_path))
            print(f"\n[FILE] {rel_path}")
            for issue in file_issues:
                print(f"  [!] {issue}")
                issues_found.append({
                    'file': str(rel_path),
                    'issue': issue
                })
            
            if needs_fix:
                files_to_fix[str(html_file)] = content
        
    except Exception as e:
        rel_path = html_file.relative_to(base_dir)
        print(f"\n[ERROR] {rel_path}: {e}")

print("\n" + "=" * 80)
print(f"\n[SUMMARY]")
print(f"  Total files scanned: {len(html_files)}")
print(f"  Files with issues: {len(files_with_issues)}")
print(f"  Total issues found: {len(issues_found)}")

if files_with_issues:
    print(f"\n[FILES NEEDING ATTENTION]")
    for file in files_with_issues:
        print(f"  - {file}")
    
    # Save report
    report_file = base_dir / 'encoding_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"Encoding Check Report\n")
        f.write(f"=" * 80 + "\n\n")
        f.write(f"Total files scanned: {len(html_files)}\n")
        f.write(f"Files with issues: {len(files_with_issues)}\n\n")
        for issue in issues_found:
            f.write(f"{issue['file']}: {issue['issue']}\n")
    
    print(f"\n[REPORT] Saved to: encoding_report.txt")
else:
    print(f"\n[OK] No encoding issues found!")

print("\n" + "=" * 80)
