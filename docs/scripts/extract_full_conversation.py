#!/usr/bin/env python3
"""完整提取DeepSeek对话 - 最终版"""
import re
import html

# 读取HTML文件
with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    raw_html = f.read()

print(f"HTML文件大小: {len(raw_html)} 字符")

# 策略：查找所有文本内容，筛选出对话相关的
def extract_all_text_blocks(html_content):
    """提取所有可能的文本块"""
    # 查找 >...< 之间的文本
    pattern = re.compile(r'>([^<]{50,})<')
    matches = pattern.findall(html_content)
    
    # 解码HTML实体
    decoded = [html.unescape(m.strip()) for m in matches]
    return decoded

def find_conversation_segments(text_blocks):
    """找出对话片段"""
    keywords = ['ring', 'fountain', 'when a flat', 'dimensionless', 'froude', 'weber', 'density', 'viscosity', 'surface tension']
    segments = []
    
    for block in text_blocks:
        block_lower = block.lower()
        # 检查是否包含关键词
        if any(kw in block_lower for kw in keywords):
            segments.append(block)
    
    return segments

# 提取所有文本块
all_blocks = extract_all_text_blocks(raw_html)
print(f"找到 {len(all_blocks)} 个文本块")

# 找出对话片段
conversation_segments = find_conversation_segments(all_blocks)
print(f"找到 {len(conversation_segments)} 个对话片段")

# 合并并去重
unique_segments = []
seen = set()
for seg in conversation_segments:
    key = seg[:100]  # 使用前100字符作为键
    if key not in seen:
        seen.add(key)
        unique_segments.append(seg)

print(f"去重后: {len(unique_segments)} 个片段")

# 显示前几个片段
for i, seg in enumerate(unique_segments[:5]):
    print(f"\n=== 片段 {i+1} (长度: {len(seg)}) ===")
    print(seg[:400] if len(seg) > 400 else seg)
    print("..." if len(seg) > 400 else "")

# 合并为完整对话
full_conversation = "\n\n---\n\n".join(unique_segments)

# 保存为Markdown
markdown_content = f"""# IYPT 2026 Ring Fountain - DeepSeek对话记录

**日期**: 2026-03-04  
**来源**: DeepSeek AI  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics  
**原始链接**: https://chat.deepseek.com/share/j9j76ov07sbbghih61

---

## 📋 完整对话内容

{full_conversation}

---

## 📝 分析要点

### 核心问题
当平金属环从一定高度落入水箱时，会产生一个能将水喷射到高空的喷泉。喷泉的最大高度如何依赖于环的参数？

### 关键参数
- 环的直径 $D$
- 环的厚度/宽度 $w$  
- 环的材料密度 $\rho_{ring}$
- 下落高度 $H$
- 水的密度 $\rho_{water}$
- 表面张力 $\sigma$
- 动力粘度 $\mu$

### 无量纲分析框架
- **Froude数**: $Fr = V/\sqrt{gD}$ — 惯性 vs 重力
- **Weber数**: $We = \rho V^2 D/\sigma$ — 惯性 vs 表面张力  
- **Bond数**: $Bo = \rho g D^2/\sigma$ — 重力 vs 表面张力
- **密度比**: $\rho_{ring}/\rho_{water}$

### 物理机制
1. **入水冲击** - 环撞击水面产生高压区
2. **空腔形成** - 环的动能转化为流体动能，形成轴对称空腔
3. **空腔坍缩** - 表面张力和重力驱动空腔壁向内收缩
4. **射流形成** - 底部液体被加速向上形成Worthington射流
5. **喷泉高度** - 动能转化为势能决定最大高度

---

*自动生成于 2026-03-04*  
*原始文件: DeepSeek (2026_3_4 12：46：05).html*
*提取脚本: extract_full_conversation.py*
"""

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_deepseek_full.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print(f"\n✅ 已保存 ring_fountain_deepseek_full.md")
print(f"总对话长度: {len(full_conversation)} 字符")
