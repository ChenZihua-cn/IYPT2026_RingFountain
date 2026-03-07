import json
import re

# 读取JSON文件
with open(r'C:\Users\30856\OneDrive\Desktop\chat-export-1772795183823.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取所有originalContent
original_contents = []

def extract_from_dict(d):
    """递归提取字典中的originalContent"""
    if isinstance(d, dict):
        if 'originalContent' in d:
            content = d['originalContent']
            # 获取标题或上下文信息
            title = d.get('title', '')
            chat_title = ''
            if 'chat' in d and isinstance(d['chat'], dict):
                chat_title = d['chat'].get('title', '')
            original_contents.append({
                'title': title or chat_title,
                'content': content
            })
        for value in d.values():
            extract_from_dict(value)
    elif isinstance(d, list):
        for item in d:
            extract_from_dict(item)

extract_from_dict(data)

# 写入整理后的文件
output_file = r'c:\Users\30856\Desktop\IYPT2026_RingFountain\original_contents_整理.md'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# 聊天记录 OriginalContent 整理\n\n")
    f.write(f"共提取到 {len(original_contents)} 条 originalContent\n\n")
    f.write("---\n\n")

    for i, item in enumerate(original_contents, 1):
        title = item['title'] or f"对话 {i}"
        f.write(f"## {i}. {title}\n\n")
        f.write(item['content'])
        f.write("\n\n---\n\n")

print(f"已提取 {len(original_contents)} 条 originalContent")
print(f"结果已保存到: {output_file}")
