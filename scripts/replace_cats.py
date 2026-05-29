"""
将 generated_cats.js 中的 DEFAULT_CATS 替换到 index.html 中
"""
import re
from pathlib import Path

TARGET_HTML = Path("e:/WorkBuddyFun/校园流浪猫项目/demo/index.html")
GENERATED_JS = Path("e:/WorkBuddyFun/校园流浪猫项目/scripts/generated_cats.js")

# 读取新数据（只提取数组部分，不要 const DEFAULT_CATS = 前缀和结尾分号）
with open(GENERATED_JS, 'r', encoding='utf-8') as f:
    js_content = f.read()

# 提取数组内容（从第一个 [ 到最后一个 ]; 之前）
match = re.search(r'const DEFAULT_CATS = (\[[\s\S]*?\]);', js_content)
if not match:
    print("❌ 无法从 generated_cats.js 提取数组")
    exit(1)

new_array = match.group(1)

# 读取 index.html
with open(TARGET_HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# 找到原来的 DEFAULT_CATS = [...] 并替换
old_pattern = r'const DEFAULT_CATS = \[[\s\S]*?\];'
old_match = re.search(old_pattern, html)
if not old_match:
    print("❌ 无法在 index.html 找到 DEFAULT_CATS")
    exit(1)

# 替换
new_block = f'const DEFAULT_CATS = {new_array};'
html_new = html[:old_match.start()] + new_block + html[old_match.end():]

with open(TARGET_HTML, 'w', encoding='utf-8') as f:
    f.write(html_new)

print(f"✅ DEFAULT_CATS 已替换（{len(new_block)} 字符）")

# 验证行数
lines = html_new.split('\n')
print(f"   文件总行数: {len(lines)}")

# 验证 DEFAULT_CATS 条目数
cat_count = new_array.count('id: ')
print(f"   猫咪条目数: {cat_count}")
