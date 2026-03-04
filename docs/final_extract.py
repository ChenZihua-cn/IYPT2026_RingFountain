#!/usr/bin/env python3
"""最终提取DeepSeek对话内容"""
import re
import html

# 读取HTML文件
with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    html_content = f.read()

print("正在分析HTML结构...")

# 查找包含对话内容的meta标签
# 在SingleFile保存的页面中，对话内容通常保存在描述性meta标签中
meta_pattern = re.compile(r'<meta[^>]+content="([^"]+)"[^>]*>', re.IGNORECASE)
all_meta = meta_pattern.findall(html_content)

print(f"找到 {len(all_meta)} 个meta标签")

# 查找包含对话相关关键词的meta内容
conversation_found = None
for i, content in enumerate(all_meta):
    decoded = html.unescape(content)
    # 检查是否包含对话相关关键词
    keywords = ['对话', '用户', 'ring', 'fountain', 'maximum height', 'dimensionless', 'froude', 'weber']
    if any(kw.lower() in decoded.lower() for kw in keywords):
        if len(decoded) > 500:  # 只关注长内容
            conversation_found = decoded
            print(f"\n在第 {i+1} 个meta标签中找到对话内容")
            print(f"内容长度: {len(decoded)} 字符")
            print(f"前500字符预览:")
            print(decoded[:500])
            break

if conversation_found:
    # 清理并保存对话内容
    conversation = conversation_found.strip()
    
    # 创建Markdown文件
    md_content = f"""# IYPT 2026 Ring Fountain - DeepSeek对话记录

**日期**: 2026-03-04  
**来源**: DeepSeek AI  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics  
**原始链接**: https://chat.deepseek.com/share/j9j76ov07sbbghih61

---

## 📋 完整对话内容

{conversation}

---

## 📝 对话摘要

### 核心物理问题
当平金属环从一定高度落入水箱时，会产生一个能将水喷射到高空的喷泉。喷泉的最大高度如何依赖于环的参数？

### 关键讨论点
1. **无量纲分析** - 使用量纲分析推导关键参数关系
2. **关键无量纲数** - Froude数、Weber数、Bond数
3. **物理机制** - 入水冲击、空腔形成、射流生成
4. **参数依赖性** - 环直径、厚度、密度、下落高度等

### AI分析特点
- 提供了中英文双语注释
- 从基本原理出发进行推导
- 强调无量纲分析的重要性
- 讨论了实验设计和验证方法

---

*提取时间: 2026-03-04*  
*原始文件: DeepSeek (2026_3_4 12：46：05).html*
*注意: 此文件由SingleFile保存的HTML页面中提取，内容可能因保存格式而被截断*
"""
    
    output_path = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\deepseek_conversation_final.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n✅ 对话内容已成功提取并保存到: {output_path}")
    print(f"对话总长度: {len(conversation)} 字符")
    
    # 同时保存原始提取内容用于验证
    raw_output = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\conversation_raw.txt'
    with open(raw_output, 'w', encoding='utf-8') as f:
        f.write(conversation)
    print(f"原始对话内容已保存到: {raw_output}")
    
else:
    print("未找到包含对话内容的meta标签")
    print("\n尝试查找其他可能包含对话的结构...")
    
    # 尝试查找其他可能的结构
    # 查找所有可能包含长文本的部分
    all_text = re.findall(r'>([^<]{200,})<', html_content)
    print(f"\n找到 {len(all_text)} 个长文本块")
    
    # 显示前几个可能相关的文本块
    relevant_blocks = []
    for block in all_text[:20]:
        block_decoded = html.unescape(block)
        if any(kw in block_decoded.lower() for kw in ['ring', 'fountain', '水']):
            relevant_blocks.append(block_decoded)
    
    if relevant_blocks:
        print(f"\n找到 {len(relevant_blocks)} 个相关文本块")
        for i, block in enumerate(relevant_blocks[:3]):
            print(f"\n=== 相关块 {i+1} ===")
            print(block[:300])
            print("...")
    else:
        print("未找到相关文本块")
