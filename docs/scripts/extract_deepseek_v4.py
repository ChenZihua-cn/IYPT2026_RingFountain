#!/usr/bin/env python3
"""DeepSeek对话提取 - v4 - 直接从原始HTML解析"""
import re
import html

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    raw = f.read()

print(f"文件大小: {len(raw)} 字符")

# 查找包含 "When a flat metal ring" 的完整内容
# 在SingleFile中，完整内容可能在 JSON 或特定的 HTML 结构中

# 策略1: 查找所有用户消息和AI回复的模式
# DeepSeek通常有特定的CSS类或结构

# 尝试查找 data 属性或特定的div
# 查找被截断的文本周围的内容
start_phrase = "When a flat metal ring falls from a certain height into a water tank"
start_idx = raw.find(start_phrase)

if start_idx > 0:
    # 向前找到标签开始
    tag_start = raw.rfind('>', 0, start_idx)
    # 向后找到标签结束 - 这可能是一段很长的文本
    # 查找后面的多个结束标签
    
    # 尝试找到完整的文本 - 可能在同一行或连续的标签中
    search_window = raw[start_idx:start_idx + 10000]
    print("找到起始位置，窗口内容预览:")
    print(search_window[:500])
    
    # 查找这个文本后面跟着什么
    after_text = raw[start_idx + len(start_phrase):start_idx + len(start_phrase) + 200]
    print(f"\n文本后面跟着: {after_text}")

# 策略2: 查找可能包含完整对话的 script 或 JSON
json_pattern = re.search(r'"text":\s*"([^"]{200,})"', raw)
if json_pattern:
    print("\n找到可能的JSON文本块")
    print(json_pattern.group(1)[:500])

# 策略3: 直接搜索中文内容（用户提到了中英文混合）
chinese_pattern = re.search(r'好的.*中文注释', raw)
if chinese_pattern:
    idx = chinese_pattern.start()
    print(f"\n找到中文内容在位置 {idx}")
    print(raw[idx:idx+300])

# 策略4: 搜索特定模式 - 用户问题通常在blockquote或特定class中
# 在SingleFile中，可能保存在某个特定的注释或属性中
comment_pattern = re.findall(r'<!--([^>]{500,})-->', raw)
if comment_pattern:
    print(f"\n找到 {len(comment_pattern)} 个长注释")
    for c in comment_pattern[:2]:
        if 'ring' in c.lower() or 'fountain' in c.lower():
            print(f"相关注释: {c[:400]}")

# 保存找到的原始文本片段
print("\n" + "="*50)
print("正在尝试提取完整内容...")

# 尝试直接提取从 When a flat metal ring 开始的一大段文本
# 找到起始位置
start = raw.find(start_phrase)
if start > 0:
    # 向后读取一大段，直到遇到明显的HTML结束标记
    chunk = raw[start:start + 50000]
    # 查找第一个 </ 后面的 >，这可能是内容结束的地方
    # 或者查找特定模式
    
    # 简单方法：提取前50000字符，然后清理
    print(f"提取块长度: {len(chunk)}")
    
    # 保存原始提取内容供人工检查
    with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\raw_extract.txt', 'w', encoding='utf-8') as f:
        f.write(chunk)
    print("原始提取已保存到 raw_extract.txt")
