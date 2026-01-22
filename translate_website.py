#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate all English content in zh directory to Chinese
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

# Translation mappings
TRANSLATIONS = {
    # Company name
    'THE NINE INTERNATIONAL SUPPLY CHAIN': '九鸿国际供应链管理有限公司',
    'The Nine International Supply Chain': '九鸿国际供应链管理有限公司',
    
    # Navigation
    'HOME': '首页',
    'ABOUT US': '关于我们',
    'SERVICE': '业务范围',
    'SERVICES': '业务范围',
    'CONTACT US': '联系我们',
    'NEWS': '新闻中心',
    
    # Menu items (case variations)
    'Home': '首页',
    'About Us': '关于我们',
    'About': '关于我们',
    'Service': '业务范围',
    'Services': '业务范围',
    'Contact Us': '联系我们',
    'Contact': '联系我们',
    'News': '新闻中心',
    
    # Common terms
    'Commodity Trade': '大宗商品贸易',
    'ILC': '国际信用证',
    'International Letter of Credit': '国际信用证',
    'Supply Chain Management': '供应链管理',
    'Logistics': '物流',
    'Trading': '贸易',
    'Import': '进口',
    'Export': '出口',
    
    # Buttons and CTAs
    'LEARN MORE': '了解更多',
    'Learn More': '了解更多',
    'READ MORE': '阅读更多',
    'Read More': '阅读更多',
    'Subscribe': '订阅',
    'SUBSCRIBE': '订阅',
    'Submit': '提交',
    'SUBMIT': '提交',
    'Send': '发送',
    'SEND': '发送',
    
    # Form fields
    'Enter your email': '输入您的邮箱',
    'Your Name': '您的姓名',
    'Your Email': '您的邮箱',
    'Your Message': '您的留言',
    'Name': '姓名',
    'Email': '邮箱',
    'Phone': '电话',
    'Message': '留言',
    'Subject': '主题',
    
    # Footer
    'All Rights Reserved': '版权所有',
    'Privacy Policy': '隐私政策',
    'Terms of Service': '服务条款',
    'Follow Us': '关注我们',
    
    # Common phrases
    'Welcome to': '欢迎来到',
    'Our Services': '我们的服务',
    'Our Team': '我们的团队',
    'Get in Touch': '联系我们',
    'Latest News': '最新动态',
    'More Information': '更多信息',
}

# Longer content translations
CONTENT_TRANSLATIONS = {
    # About page content
    'We are a prominent player in the global supply chain industry': '我们是全球供应链行业的重要参与者',
    'specializing in commodity trade and international logistics': '专注于大宗商品贸易和国际物流',
    
    # Service descriptions
    'We provide comprehensive supply chain solutions': '我们提供全面的供应链解决方案',
    'Our services include': '我们的服务包括',
    'Professional team with years of experience': '拥有多年经验的专业团队',
    
    # Contact
    'Feel free to contact us': '欢迎随时联系我们',
    'We are here to help': '我们随时为您服务',
    'Office Address': '办公地址',
    'Business Hours': '营业时间',
}

def translate_content(content):
    """Translate English content to Chinese"""
    
    # First pass: Direct replacements (longer phrases first)
    for en, zh in sorted(CONTENT_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        content = content.replace(en, zh)
    
    # Second pass: Common terms and navigation
    for en, zh in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        # Use word boundary for more accurate replacement
        content = re.sub(r'\b' + re.escape(en) + r'\b', zh, content)
    
    return content

def translate_file(file_path):
    """Translate a single HTML file"""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Translate content
        content = translate_content(content)
        
        # Update language switcher links
        # English link should point to ../world9h.com/
        content = re.sub(
            r'<a href="[^"]*">\s*<img[^>]*77918_1689670187788430fe\.jpg[^>]*>\s*<span>English</span>',
            lambda m: m.group(0).replace('href="', 'href="../world9h.com/').replace('href="../world9h.com/../world9h.com/', 'href="../world9h.com/'),
            content
        )
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return None

print("=" * 80)
print("Translating Website Content to Chinese")
print("=" * 80)

# Find all HTML files in zh directory
html_files = list(zh_dir.rglob('*.html'))

print(f"\nFound {len(html_files)} HTML files to translate\n")

translated_count = 0
skipped_count = 0
error_count = 0

for html_file in html_files:
    rel_path = html_file.relative_to(zh_dir)
    
    result = translate_file(html_file)
    
    if result is True:
        print(f"[OK] Translated: {rel_path}")
        translated_count += 1
    elif result is False:
        print(f"[SKIP] No changes: {rel_path}")
        skipped_count += 1
    else:
        error_count += 1

print("\n" + "=" * 80)
print(f"[SUMMARY]")
print(f"  Files processed: {len(html_files)}")
print(f"  Files translated: {translated_count}")
print(f"  Files skipped: {skipped_count}")
print(f"  Errors: {error_count}")
print("=" * 80)

if translated_count > 0:
    print(f"\n[SUCCESS] Translated {translated_count} files!")
else:
    print(f"\n[INFO] No files needed translation.")
