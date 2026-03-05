#!/usr/bin/env python3
"""提取所有相关文本块"""
import re
import html

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    html_content = f.read()

print("正在提取所有可能包含对话的文本块...")

# 查找所有文本块（包括那些在标签属性中的）
# 方法1: 查找属性值
attr_pattern = re.compile(r'="([^"]{100,})"')
attr_matches = attr_pattern.findall(html_content)

print(f"找到 {len(attr_matches)} 个长属性值")

# 查找包含关键词的属性
keywords = ['ring', 'fountain', '水', '喷泉', '对话', '用户', 'dimensionless', 'froude', 'weber', 'height', 'maximum']
conversation_parts = []

for i, attr in enumerate(attr_matches):
    decoded = html.unescape(attr)
    if any(kw.lower() in decoded.lower() for kw in keywords):
        if len(decoded) > 100:  # 只关注较长的内容
            conversation_parts.append((i, decoded))
            if len(conversation_parts) <= 3:  # 只显示前几个
                print(f"\n=== 属性块 {i} (长度: {len(decoded)}) ===")
                print(decoded[:400])
                if len(decoded) > 400:
                    print("...")

# 方法2: 查找标签间的文本
text_pattern = re.compile(r'>([^<]{100,})<')
text_matches = text_pattern.findall(html_content)

print(f"\n找到 {len(text_matches)} 个标签间长文本")

for i, text in enumerate(text_matches[:10]):  # 只检查前10个
    decoded = html.unescape(text.strip())
    if any(kw.lower() in decoded.lower() for kw in keywords):
        print(f"\n=== 文本块 {i} (长度: {len(decoded)}) ===")
        print(decoded[:400])
        if len(decoded) > 400:
            print("...")
        conversation_parts.append((f"text_{i}", decoded))

# 保存所有找到的部分
if conversation_parts:
    print(f"\n总共找到 {len(conversation_parts)} 个对话相关部分")
    
    # 合并所有部分
    all_parts = []
    for idx, part in conversation_parts:
        all_parts.append(f"--- 部分 {idx} ---\n{part}\n")
    
    combined = "\n".join(all_parts)
    
    # 保存到文件
    with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\all_conversation_parts.txt', 'w', encoding='utf-8') as f:
        f.write(combined)
    
    print(f"\n✅ 所有对话部分已保存到 all_conversation_parts.txt")
    
    # 现在尝试创建一个更简洁的版本
    # 查找最可能是完整对话的部分（通常是包含"对话内容"或"用户"的部分）
    full_conversation = None
    for idx, part in conversation_parts:
        if '对话内容' in part or '用户（第一轮提问）' in part:
            full_conversation = part
            print(f"\n找到可能是完整对话的部分 (索引: {idx})")
            print(f"长度: {len(part)} 字符")
            print(f"前500字符预览:")
            print(part[:500])
            break
    
    if full_conversation:
        # 创建Markdown文件
        md_content = f"""# IYPT 2026 Ring Fountain - DeepSeek对话记录

**日期**: 2026-03-04  
**来源**: DeepSeek AI  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics  
**原始链接**: https://chat.deepseek.com/share/j9j76ov07sbbghih61

---

## 📋 完整对话内容

{full_conversation}

---

## 📝 核心问题摘要

**用户问题**:  
当平金属环从一定高度落入水箱时，会产生一个能将水喷射到高空的喷泉。喷泉的最大高度如何依赖于环的参数？

**关键参数**:
- 环的直径 (D)
- 环的厚度/宽度 (w)
- 环的材料密度 (ρ_ring)
- 下落高度 (H)
- 水的性质：密度 (ρ_water)、表面张力 (σ)、粘度 (μ)

**分析方法**:
- 量纲分析/无量纲分析
- 关键无量纲数：Froude数、Weber数、Bond数
- 物理机制分析：入水冲击、空腔演化、射流形成

---

*提取时间: 2026-03-04*  
*来源: DeepSeek AI对话分享页面*
"""
        
        with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\deepseek_ring_fountain_conversation.md', 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"\n✅ 完整对话已保存到 deepseek_ring_fountain_conversation.md")
    else:
        print("\n⚠️ 未找到完整的对话结构，但已保存所有找到的部分")
else:
    print("未找到任何对话相关部分")
