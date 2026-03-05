#!/usr/bin/env python3
"""提取DeepSeek对话 - 第三版"""
import re
import html

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符")

# 方法1: 查找包含对话的文本块
# 根据之前找到的索引，直接提取
idx = content.find('When a flat metal ring')
if idx > 0:
    # 向前找 > 符号
    start = content.rfind('>', 0, idx) + 1
    # 向后找 < 符号
    end = content.find('<', idx)
    user_question = content[start:end]
    print(f"\n用户问题: {user_question[:200]}")

# 方法2: 查找包含中文注释的meta content
# 查找较长的content属性
all_content = re.findall(r'content="([^"]{500,})"', content)
print(f"\n找到 {len(all_content)} 个长content属性")

for i, c in enumerate(all_content[:5]):
    text = html.unescape(c)
    if '对话' in text or '用户' in text or 'ring' in text.lower():
        print(f"\n=== 候选 {i+1} (长度: {len(text)}) ===")
        print(text[:500])
        print("...")
        # 保存这个
        with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_deepseek.md', 'w', encoding='utf-8') as f:
            f.write(f"# DeepSeek对话记录\n\n{text}")
        print("\n✅ 已保存!")
        break
