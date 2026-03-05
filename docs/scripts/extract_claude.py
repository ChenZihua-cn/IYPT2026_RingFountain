#!/usr/bin/env python3
"""提取Claude对话内容"""
import re
import html

file_path = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\Claude (2026_3_1 23：14：04).html'

print("正在读取Claude HTML文件...")
with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"文件大小: {len(html_content)} 字符")

# 方法1: 查找所有文本块
all_text_blocks = re.findall(r'>([^<]{200,})<', html_content)
print(f"找到 {len(all_text_blocks)} 个长文本块")

# 过滤出包含关键词的块
keywords = ['ring', 'fountain', 'metal', 'water', 'height', '喷泉', '金属', '水', 'parameter', 'dimensionless', 'froude', 'weber', 'bond', '物理', '分析']
relevant_blocks = []

for block in all_text_blocks:
    decoded = html.unescape(block.strip())
    # 跳过CSS/JS代码
    if '@keyframes' in decoded or '@font-face' in decoded or 'var(' in decoded or '.Button_' in decoded:
        continue
    
    # 检查是否包含关键词
    if any(kw.lower() in decoded.lower() for kw in keywords):
        relevant_blocks.append(decoded)

print(f"找到 {len(relevant_blocks)} 个相关文本块")

# 显示并保存
if relevant_blocks:
    output_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\claude_conversation_simple.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, block in enumerate(relevant_blocks):
            f.write(f"=== 块 {i+1} ===\n")
            f.write(block)
            f.write("\n\n" + "="*50 + "\n\n")
    
    print(f"\n✅ 相关文本块已保存到: {output_file}")
    
    # 显示前几个块的内容
    for i, block in enumerate(relevant_blocks[:10]):
        print(f"\n=== 块 {i+1} (长度: {len(block)}) ===")
        print(block[:500])
        if len(block) > 500:
            print("...")
    
    # 尝试识别用户问题和Claude回答
    user_question = ""
    claude_response = []
    
    for block in relevant_blocks:
        if 'When a flat metal ring' in block or '当平金属环' in block:
            user_question = block
        elif 'Claude' in block or 'claude' in block.lower():
            claude_response.append(block)
    
    # 创建Markdown文档
    md_content = f"""# IYPT 2026 Ring Fountain - Claude对话记录

**来源**: Claude AI聊天页面  
**链接**: https://claude.ai/chat/7fbe75ad-bc30-4fca-9914-a2aebdd104a5  
**保存时间**: 2026-03-01 23:14:04 (GMT+8)

---

## 🎯 用户问题

{user_question if user_question else '未找到明确用户问题，可能包含在对话中'}

---

## 🤖 Claude响应摘要

{" ".join(claude_response[:3]) if claude_response else 'Claude的响应内容需要进一步提取'}

---

## 📋 从HTML提取的相关内容

共找到 {len(relevant_blocks)} 个相关文本块：

"""
    
    # 添加每个块的简要描述
    for i, block in enumerate(relevant_blocks[:20]):  # 只添加前20个
        preview = block[:200].replace('\n', ' ')
        md_content += f"{i+1}. 长度: {len(block)}字符 - {preview}...\n\n"
    
    md_content += f"""
---

## 📝 初步分析

基于提取的内容，Claude对话可能包含：

### 可能涉及的主题
1. 金属环入水喷泉的物理机制
2. 量纲分析和无量纲数推导
3. 实验设计和参数优化
4. 与其他AI分析（如DeepSeek）的对比

### 需要进一步处理
由于HTML页面结构复杂，完整对话可能需要：
1. 更精细的文本提取
2. 对话结构识别
3. 用户消息与AI响应的分离

---

*注: 此文档基于自动提取的内容生成，可能不完整。*

*处理时间: 2026-03-04*
"""
    
    md_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\claude_conversation_summary.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n✅ 总结文档已保存到: {md_file}")
    
else:
    print("未找到相关文本块")
    
    # 尝试其他方法：查找属性中的内容
    print("\n尝试其他提取方法...")
    attr_pattern = re.compile(r'content="([^"]{100,})"')
    attr_matches = attr_pattern.findall(html_content)
    print(f"找到 {len(attr_matches)} 个长属性值")
    
    # 查找包含关键词的属性
    for i, attr in enumerate(attr_matches[:10]):
        decoded = html.unescape(attr)
        if any(kw.lower() in decoded.lower() for kw in keywords[:5]):
            print(f"\n属性 {i+1} (长度: {len(decoded)}):")
            print(decoded[:300])
            print("...")
