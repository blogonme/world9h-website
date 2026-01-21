import os
import re

target_dir = r'd:\Project\world9h.com\world9h-website\zh'
asset_dirs = ['p.cdn-static.cn', 'i.cdn-static.cn', 'static.cdn-static.cn', 'res.wx.qq.com', 'hm.baidu.com', 'zz.bdstatic.com']

def replace_path(match):
    p = match.group(1)
    for ad in asset_dirs:
        if ad in p:
            if p.startswith('./'): return '\"../' + p[2:] + '\"'
            if p.startswith('../'): return '\"../../' + p[3:] + '\"'
            if p.startswith(ad): return '\"../' + p + '\"'
    return match.group(0)

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = re.sub(r'\"([^\"]+)\"', replace_path, content)
                
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Updated {file}')
            except Exception as e:
                print(f'Error {file}: {e}')
