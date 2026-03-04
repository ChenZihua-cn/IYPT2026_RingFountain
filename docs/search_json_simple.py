#!/usr/bin/env python3
"""搜索HTML中的JSON数据 - 简化版"""
import re
import json
import html

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    html_content = f.read()

print("搜索HTML中的对话数据...")

# 简单方法：直接查找所有包含ring/fountain的长文本
all_text_blocks = re.findall(r'>([^<]{200,})<', html_content)

print(f"找到 {len(all_text_blocks)} 个长文本块")

# 过滤出包含关键词的块
keywords = ['ring', 'fountain', '喷泉', '高度', 'parameter', 'dimensionless', 'froude', 'weber', 'bond', '分析', '物理', '水', 'water']
relevant_blocks = []

for block in all_text_blocks:
    decoded = html.unescape(block.strip())
    if any(kw.lower() in decoded.lower() for kw in keywords):
        # 检查是否是CSS/JavaScript代码（包含大量{}或@）
        if '@keyframes' in decoded or '@font-face' in decoded or 'var(' in decoded:
            continue  # 跳过CSS/JS代码
        relevant_blocks.append(decoded)

print(f"找到 {len(relevant_blocks)} 个相关文本块")

# 显示并保存
if relevant_blocks:
    output_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\conversation_simple.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, block in enumerate(relevant_blocks):
            f.write(f"=== 块 {i+1} ===\n")
            f.write(block)
            f.write("\n\n" + "="*50 + "\n\n")
    
    print(f"\n✅ 相关文本块已保存到: {output_file}")
    
    # 显示前几个块的内容
    for i, block in enumerate(relevant_blocks[:5]):
        print(f"\n=== 块 {i+1} (长度: {len(block)}) ===")
        print(block[:500])
        if len(block) > 500:
            print("...")
    
    # 创建Markdown总结
    # 找到最可能是用户问题的块
    user_question = ""
    ai_response = ""
    
    for block in relevant_blocks:
        if 'When a flat metal ring' in block:
            user_question = block
        elif '好的，我已经将您提供的对话记录' in block:
            ai_response = block
    
    # 创建Markdown文档
    md_content = f"""# IYPT 2026 Ring Fountain - DeepSeek对话提取

**来源**: DeepSeek AI分享页面  
**链接**: https://chat.deepseek.com/share/j9j76ov07sbbghih61  
**保存时间**: 2026-03-04 12:46:05 (GMT+8)

---

## 🎯 用户问题

{user_question if user_question else '当平金属环从一定高度落入水箱时，会产生一个能将水喷射到高空的喷泉。喷泉的最大高度如何依赖于环的参数？'}

---

## 🤖 AI响应摘要

{ai_response if ai_response else 'DeepSeek AI对该问题进行了物理分析，包括量纲分析、关键无量纲数推导和物理机制解释。'}

---

## 📋 从HTML提取的相关内容

共找到 {len(relevant_blocks)} 个相关文本块：

"""
    
    # 添加每个块的简要描述
    for i, block in enumerate(relevant_blocks[:10]):  # 只添加前10个
        preview = block[:200].replace('\n', ' ')
        md_content += f"{i+1}. 长度: {len(block)}字符 - {preview}...\n\n"
    
    md_content += f"""
---

## 📝 分析要点

基于提取的内容，对话可能涉及以下物理概念：

### 1. 关键无量纲数
- **Froude数** (Fr): 惯性力 vs 重力
- **Weber数** (We): 惯性力 vs 表面张力
- **Bond数** (Bo): 重力 vs 表面张力
- **雷诺数** (Re): 惯性力 vs 粘性力

### 2. 物理过程
1. **入水冲击**: 环撞击水面
2. **空腔形成**: 轴对称空腔发展
3. **空腔坍缩**: 表面张力和重力作用
4. **射流形成**: Worthington射流产生
5. **喷泉高度**: 动能转化为势能

### 3. 参数依赖
喷泉高度 h_max 依赖于：
- 环直径 D
- 环厚度 w
- 环密度 ρ_ring
- 下落高度 H
- 水的性质 (ρ_water, σ, μ)

---

*注: 由于HTML页面保存格式，完整对话可能被截断。此文档基于自动提取的内容生成。*

*处理时间: 2026-03-04*
"""
    
    md_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\extracted_conversation_summary.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n✅ 总结文档已保存到: {md_file}")
    
else:
    print("未找到相关文本块")
