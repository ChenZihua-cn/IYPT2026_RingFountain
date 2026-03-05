#!/usr/bin/env python3
"""提取DeepSeek对话的完整内容"""
import re
import html

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到包含对话的meta标签（通常有较长的content）
# 查找包含 "When a flat metal ring" 的meta content
pattern = r'content="([^"]{1000,30000})"'
matches = re.findall(pattern, content)

conversation = None
for m in matches:
    if 'When a flat metal ring' in m or 'fountain' in m.lower():
        conversation = html.unescape(m)
        break

if conversation:
    # 格式化对话内容
    md_content = f"""# IYPT 2026 Ring Fountain - DeepSeek对话记录

**日期**: 2026-03-04  
**来源**: DeepSeek AI  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics  
**原始链接**: https://chat.deepseek.com/share/j9j76ov07sbbghih61

---

## 📋 完整对话内容

{conversation}

---

## 📝 内容概要

### 用户问题
当平金属环从一定高度落入水箱时，会产生一个能将水喷射到高空的喷泉。喷泉的最大高度如何依赖于环的参数？

### AI分析要点
1. **无量纲数分析** - Froude数、Weber数、Bond数
2. **尺度分析** - 量纲推导
3. **物理机制** - 入水冲击 → 空腔形成 → 坍缩 → 射流
4. **参数依赖** - 高度、直径、厚度、密度、表面张力

---

*自动生成于 2026-03-04*  
*原始文件: DeepSeek (2026_3_4 12：46：05).html*
"""
    
    with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_deepseek.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print("✅ 已成功提取并保存 ring_fountain_deepseek.md")
    print(f"对话长度: {len(conversation)} 字符")
else:
    print("❌ 未能找到对话内容")
    print(f"检查了 {len(matches)} 个候选内容")
