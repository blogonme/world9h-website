import os
import re

root_dir = r'd:\Project\world9h.com\world9h-website'
zh_dir = os.path.join(root_dir, 'zh')

# Update English files to point to Chinese version
# Look for <a href="...cn.world9h.com/zh...">...中文...</a>
# Replace with <a href="zh/{relative_path}">...中文...</a>
# But wait, relative path depends on where we are.
# If in root index.html: href="zh/index.html"
# If in world9h.com/about.html: href="../zh/world9h.com/about.html" (since zh is at root)

def update_english_files():
    for root, dirs, files in os.walk(root_dir):
        if 'zh' in dirs: dirs.remove('zh') # Don't go into zh
        
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                rel_path_from_root = os.path.relpath(path, root_dir)
                
                # Calculate path to zh counterpart
                # zh counterpart is at root_dir/zh/rel_path_from_root
                
                # We need relative link from 'path' to 'root_dir/zh/rel_path_from_root'
                # Path to root: os.path.relpath(root_dir, root)
                to_root = os.path.relpath(root_dir, root)
                if to_root == '.': to_root = ''
                else: to_root += '/'
                
                zh_link = f'{to_root}zh/{rel_path_from_root}'.replace('\\', '/')
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex to match the Chinese link
                # <a href="http://cn.world9h.com/zh"><img ...><span>&#20013;&#25991;</span></a>
                pattern = re.compile(r'(<a href=")[^"]*?cn\.world9h\.com/zh[^"]*?("><img [^>]*?><span>&#20013;&#25991;</span></a>)', re.IGNORECASE)
                
                new_content = pattern.sub(f'\\1{zh_link}\\2', content)
                
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Updated EN file: {rel_path_from_root} -> Link to {zh_link}')

# Update Chinese files to point to English version
# Look for <a href="index.html">...English...</a> (This might be tricky if it was relative)
# English structure is mirrored.
def update_chinese_files():
    for root, dirs, files in os.walk(zh_dir):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                rel_path_from_zh = os.path.relpath(path, zh_dir)
                
                # Counterpart is at root_dir/rel_path_from_zh
                
                # Path from current file to root_dir
                # Current file is at zh_dir/rel_sub
                # path to zh_dir is os.path.relpath(zh_dir, root)
                to_zh = os.path.relpath(zh_dir, root)
                # to root_dir is ../to_zh
                
                en_link = os.path.join(to_zh, '..', rel_path_from_zh).replace('\\', '/')
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex to match English link. 
                # It currently points to neighbor English file probably (since we copied it)
                # Or it points to 'index.html' (absolute-ish)
                # In original EN: <a href="index.html">...English...</a>
                # In ZH copy: same.
                # We want to force it to point to {en_link}
                
                # Match <a href="...">...English...</a>
                pattern = re.compile(r'(<a href=")[^"]*?("><img [^>]*?><span>English</span></a>)', re.IGNORECASE)
                
                new_content = pattern.sub(f'\\1{en_link}\\2', content)
                 
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Updated ZH file: {rel_path_from_zh} -> Link to {en_link}')

if __name__ == '__main__':
    update_english_files()
    update_chinese_files()
