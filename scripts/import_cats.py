"""
喵扎特数据 → CampusCat DEFAULT_CATS 映射脚本
读取 cats-base.json，映射为 CampusCat 的 DEFAULT_CATS 数组格式
"""

import json
import re
from pathlib import Path

# === 配置 ===
SOURCE_JSON = Path("E:/CodeArtsAgentProject/DownCat/data/cats-base.json")
TARGET_HTML = Path("e:/WorkBuddyFun/校园流浪猫项目/demo/index.html")
OUTPUT_JS = Path("e:/WorkBuddyFun/校园流浪猫项目/scripts/generated_cats.js")

# 根据名字猜测毛色（基于常见认知）
NAME_COLOR_MAP = {
    '阿珍': '未知', '莲蓉c': '未知', '灯泡': '白色', '白炽灯': '白色',
    '叉烧': '橘色/黄色', '灯罩': '未知', '蛋蛋': '未知', '夏夏': '未知',
    '小勒': '未知', '芝芝': '未知', '莲蓉包': '未知', '桃桃': '未知',
    '黄皮': '橘色/黄色', '三花菲菲': '三花', '蛋卷蛋散': '未知', '小乱': '未知',
    '橘橘': '橘色/黄色', '橘白': '橘白', '陈皮': '橘色/黄色', '瑞士卷': '未知',
    '可可': '棕色/咖啡色', '中线': '未知', '芽芽': '未知', '斑斑': '未知',
    '方便面': '橘色/黄色', '椰丝': '白色', '化化': '未知', '奶口': '未知',
    '忽必烈': '未知', '八顿': '未知', '棕棕': '棕色/咖啡色',
    # 留园观察
    '凉桔': '橘色/黄色', '小黑蛋': '黑色', '立顿': '未知', '福瑞': '未知',
    '布朗尼': '棕色/咖啡色', '椰云': '白色', '帕帕': '未知', '花荣': '未知',
    '奶糖': '白色', '奶冻': '白色', '素素': '白色', '黑大郎': '黑色',
    '瓜瓜': '未知', '杰尼龟': '未知', '笨笨': '未知', '砂糖桔': '橘色/黄色',
    '熊狸': '未知', '丁丁': '未知', '鼠鼠': '灰色', '当当': '未知',
    '图牛': '未知', '脆果': '未知', '墩墩': '未知', '小贼': '未知',
    '花瑁': '玳瑁', '虎仔': '狸花（条纹）', '冰橙': '橘色/黄色', '灰瑁': '灰色/玳瑁',
    '麦旋风': '黑色/白色',
}

# 根据名字猜测性格（谨慎保守，只填非常确定的）
NAME_PERSONALITY_MAP = {
    '叉烧': '待观察',   # 高人气猫
    '阿珍': '待观察',   # 年度候选
    '笨笨': '待观察',
    '忽必烈': '待观察',
    '小贼': '待观察',
}


def guess_color(name):
    """根据名字关键词推测毛色"""
    name_lower = name
    if '黑' in name_lower:
        return '黑色'
    if '白' in name_lower and '橘' not in name_lower:
        return '白色'
    if '橘' in name_lower or '黄' in name_lower:
        return '橘色/黄色'
    if '花' in name_lower and '三' in name_lower:
        return '三花'
    if '三花' in name_lower:
        return '三花'
    if '灰' in name_lower:
        return '灰色'
    if '蓝' in name_lower:
        return '蓝色'
    if '棕' in name_lower or '咖啡' in name_lower or '可可' in name_lower:
        return '棕色/咖啡色'
    if '狸' in name_lower or '虎' in name_lower:
        return '狸花（条纹）'
    if '瑁' in name_lower:
        return '玳瑁'
    if '奶' in name_lower:
        return '白色'
    if '椰' in name_lower:
        return '白色'
    if '巧克力' in name_lower or '布朗尼' in name_lower:
        return '棕色/咖啡色'
    # 特定已知
    return NAME_COLOR_MAP.get(name, '未知')


def map_cat(cat, new_id):
    """将喵扎特一条猫咪记录映射为 CampusCat 格式"""
    name = cat['name']
    status = cat['status']
    tags = cat.get('tags', [])
    likes = cat.get('likes', 0)

    # 从标签推断绝育状态
    if '已绝育' in tags:
        neutered = True
    elif '未绝育' in tags or '待绝育' in tags:
        neutered = False
    else:
        neutered = None  # 未知

    # 从标签推断健康状态
    health_status = '未知'
    for tag in tags:
        if tag in ('健康', '已绝育'):
            health_status = '健康'
            break

    # 生成备注：包含原始状态和标签信息
    note_parts = [f"来源：广贝才猫协（喵扎特），❤️ {likes}"]
    if tags:
        note_parts.append(f"标签：{'、'.join(tags)}")
    if status == '待领养':
        note_parts.append('待领养中')
    elif status == '留园观察':
        note_parts.append('留园观察中')

    notes = '；'.join(note_parts)

    return {
        'id': new_id,
        'name': name,
        'gender': '未知',
        'age': '未知',
        'neutered': neutered,
        'personality': NAME_PERSONALITY_MAP.get(name, '待观察'),
        'location': '广东财经大学',
        'color': guess_color(name),
        'healthStatus': health_status,
        'firstSeen': '',
        'notes': notes,
        'isDefault': True,
        'sourceStatus': status,   # 原始状态
        'sourceLikes': likes,      # 原始点赞数
    }


def main():
    # 1. 读取源数据
    with open(SOURCE_JSON, 'r', encoding='utf-8') as f:
        source = json.load(f)

    # 2. 合并所有猫到一个列表
    all_cats = []
    for category, data in source['categories'].items():
        for cat in data['cats']:
            all_cats.append((cat, category))

    # 3. 按 id 排序后重新编号
    # 原数据：待领养 1-31, 留园观察 101-129
    # 新编号：统一 1-62
    all_cats.sort(key=lambda x: x[0]['id'])

    campus_cats = []
    for new_id, (cat, category) in enumerate(all_cats, 1):
        mapped = map_cat(cat, new_id)
        mapped['notes'] = f"[{category}] {mapped['notes']}"
        campus_cats.append(mapped)

    print(f"✅ 共映射 {len(campus_cats)} 只猫")

    # 4. 统计
    adopted_count = sum(1 for c in campus_cats if c['sourceStatus'] == '待领养')
    observe_count = sum(1 for c in campus_cats if c['sourceStatus'] == '留园观察')
    print(f"   待领养: {adopted_count} | 留园观察: {observe_count}")

    # 5. 生成 JS 代码
    js_lines = ["// 自动生成：喵扎特数据 → CampusCat DEFAULT_CATS", f"// 生成时间：2026-05-29", f"// 数据来源：广贝才猫协（小小喵扎特小程序）", f"// 共 {len(campus_cats)} 只猫", "const DEFAULT_CATS = ["]
    for i, cat in enumerate(campus_cats):
        # 构建 JS 对象字面量
        neutered_val = 'null' if cat['neutered'] is None else str(cat['neutered']).lower()
        fields = [
            f"id: {cat['id']}",
            f"name: '{cat['name']}'",
            f"gender: '{cat['gender']}'",
            f"age: '{cat['age']}'",
            f"neutered: {neutered_val}",
            f"personality: '{cat['personality']}'",
            f"location: '{cat['location']}'",
            f"color: '{cat['color']}'",
            f"healthStatus: '{cat['healthStatus']}'",
            f"firstSeen: '{cat['firstSeen']}'",
            f"notes: '{cat['notes']}'",
            f"isDefault: true",
        ]
        comma = ',' if i < len(campus_cats) - 1 else ''
        js_lines.append(f"    {{ {', '.join(fields)} }}{comma}")
    js_lines.append("];")

    js_content = '\n'.join(js_lines)

    # 6. 写入生成文件
    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✅ JS 数组已写入: {OUTPUT_JS}")

    # 7. 打印前 3 条预览
    print("\n--- 前 3 条预览 ---")
    for cat in campus_cats[:3]:
        print(json.dumps(cat, ensure_ascii=False, indent=2))

    # 8. 统计颜色分布
    from collections import Counter
    colors = Counter(c['color'] for c in campus_cats)
    print(f"\n--- 毛色分布 ---")
    for color, count in colors.most_common():
        print(f"  {color}: {count} 只")

    return campus_cats, js_content


if __name__ == '__main__':
    cats, js = main()
