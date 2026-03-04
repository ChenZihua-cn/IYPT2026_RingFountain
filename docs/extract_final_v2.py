#!/usr/bin/env python3
"""最终版提取 - 使用字符串查找"""
import html

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到对话内容的起点和终点
# 从 "When a flat metal ring" 开始
start_marker = 'When a flat metal ring'
start_idx = content.find(start_marker)

if start_idx == -1:
    print("未找到对话开始标记")
    exit()

# 向前找到 > 符号
content_start = content.rfind('>', 0, start_idx) + 1

# 找到对话结束的位置（查找下一个 meta 标签或 script 标签）
end_markers = ['"><meta', '"></div><script', '"><link']
content_end = len(content)

for marker in end_markers:
    idx = content.find(marker, start_idx)
    if idx != -1 and idx < content_end:
        content_end = idx

# 提取对话内容
raw_conversation = content[content_start:content_end]
conversation = html.unescape(raw_conversation)

print(f"提取的对话长度: {len(conversation)} 字符")
print(f"\n前500字符预览:")
print(conversation[:500])

# 保存为markdown
md = f"""# IYPT 2026 Ring Fountain - DeepSeek对话记录

**日期**: 2026-03-04  
**来源**: DeepSeek AI  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics  
**原始链接**: https://chat.deepseek.com/share/j9j76ov07sbbghih61

---

## 📋 完整对话内容

{conversation}

---

## 📝 内容概要

### 核心物理机制
1. **入水冲击** - 金属环撞击水面产生高压，形成空腔
2. **空腔演化** - 惯性、表面张力、重力竞争导致空腔坍缩
3. **射流形成** - 空腔底部液体被加速向上，形成Worthington射流
4. **喷泉高度** - 初始动量与浮力/重力平衡决定最大高度

### 关键无量纲数
- **Froude数** Fr = V/√(gD) - 惯性 vs 重力
- **Weber数** We = ρV²D/σ - 惯性 vs 表面张力
- **Bond数** Bo = ρgD²/σ - 重力 vs 表面张力

---

*自动生成于 2026-03-04*  
*原始文件: DeepSeek (2026_3_4 12：46：05).html*
"""

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_deepseek.md', 'w', encoding='utf-8') as f:
    f.write(md)

print("\n✅ 已保存 ring_fountain_deepseek.md")
