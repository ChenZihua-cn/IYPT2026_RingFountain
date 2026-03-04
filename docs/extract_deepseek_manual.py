#!/usr/bin/env python3
"""手动提取DeepSeek HTML中的对话内容"""
import re
import html

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符")

# 查找所有meta标签
meta_pattern = r'<meta[^>]*content="([^"]+)"[^>]*>'
metas = re.findall(meta_pattern, content)
print(f"\n找到 {len(metas)} 个meta标签")

# 查找description
for meta in metas:
    if 'When a flat metal ring' in meta or 'fountain' in meta.lower():
        print(f"\n相关meta: {html.unescape(meta)[:500]}")

# 查找所有较长的纯文本（不包括样式和代码）
# DeepSeek的内容可能嵌套在特定的div结构中
print("\n\n查找长文本块...")

# 尝试查找包含物理内容的段落
physics_keywords = ['maximum height', 'fountain', 'velocity', 'diameter', 'density', 'surface tension']
all_matches = re.findall(r'>([^<]{100,10000})<', content)

relevant_texts = []
for match in all_matches:
    text = html.unescape(match.strip())
    # 过滤掉CSS和JS
    if any(x in text for x in ['{', '}', '@import', 'function(', '.css', 'padding:', 'margin:']):
        continue
    # 保留包含物理关键词的文本
    if any(kw in text.lower() for kw in physics_keywords) and len(text) > 200:
        relevant_texts.append(text)

print(f"找到 {len(relevant_texts)} 条相关文本")

# 显示前5条
for i, text in enumerate(relevant_texts[:5]):
    print(f"\n{'='*50}")
    print(f"文本 {i+1} (长度: {len(text)})")
    print('='*50)
    print(text[:600])
    if len(text) > 600:
        print("...")
