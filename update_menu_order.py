import os
import re

def update_html_menu(filepath):
    # print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return

    # --- 统一处理逻辑 ---
    # 正则表达式：能够匹配跨行的 <ul> 标签及内容，特别是 class 分布在多行的情况
    # 使用 [^>]*? 来容纳包括换行符在内的属性占位
    menu_pattern = r'(<ul[^>]*?class\s*=\s*["\']zz-menu zz-menu--horizontal["\'][^>]*?>)(.*?)(</ul>)'
    
    def replacer(match):
        prefix = match.group(1)
        items_html = match.group(2)
        suffix = match.group(3)
        
        # 提取各个 li 块。兼容跨行
        item_pattern = r'(<li[^>]*?class\s*=\s*["\']zz-menu-item[^>]*?["\'][^>]*?>.*?</li>)'
        items = re.findall(item_pattern, items_html, re.DOTALL)
        
        if len(items) < 5:
            return match.group(0)

        # 识别项目
        mapping = {}
        # 为了精确识别，我们先根据 URL，再根据关键词
        for item in items:
            item_lower = item.lower()
            
            # HOME / 首页
            if 'data-url="/"' in item or 'index.html' in item_lower or '首页' in item or '>index<' in item_lower or '>home<' in item_lower:
                mapping['HOME'] = item
            
            # NEWS / 新闻中心
            elif 'logistics.html' in item_lower or '新闻中心' in item or '>news<' in item_lower:
                mapping['NEWS'] = item
            
            # SERVICE / 业务范围
            elif 'services.html' in item_lower or '业务范围' in item or '>service<' in item_lower or '>services<' in item_lower:
                mapping['SERVICE'] = item
            
            # CONTACT / 联系我们
            elif 'contact.html' in item_lower or '联系我们' in item or '>contact us<' in item_lower:
                mapping['CONTACT'] = item
            
            # ABOUT / 关于我们
            elif 'about.html' in item_lower or '关于我们' in item or '>about us<' in item_lower or '>about<' in item_lower:
                mapping['ABOUT'] = item

        # 检查是否识别全了
        needed = ['HOME', 'NEWS', 'SERVICE', 'CONTACT', 'ABOUT']
        # 允许有超过 5 个项，但至少要有这 5 个
        if all(k in mapping for k in needed):
            new_order_list = [mapping[k] for k in needed]
            # 如果原菜单中有其他项，按原样附在后面（虽然本站通常只有这5个）
            seen_items = set(mapping.values())
            others = [i for i in items if i not in seen_items]
            
            new_items_html = "".join(new_order_list) + "".join(others)
            return prefix + new_items_html + suffix
        else:
            # print(f"  Warning: Incomplete items in {filepath}. Found: {list(mapping.keys())}")
            return match.group(0)

    # 应用替换
    new_content = re.sub(menu_pattern, replacer, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Successfully Updated: {filepath}")
    # else:
    #     print(f"  No changes: {filepath}")

def process_all():
    # 扫描所有子目录，寻找 .html 文件
    for root, dirs, files in os.walk('.'):
        # 排除 .git 和镜像缓存目录
        if '.git' in root: continue
        
        for file in files:
            if file.lower().endswith('.html'):
                full_path = os.path.join(root, file)
                update_html_menu(full_path)

if __name__ == "__main__":
    print("Starting global menu order update...")
    process_all()
    print("Update complete!")
