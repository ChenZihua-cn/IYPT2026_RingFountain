#!/usr/bin/env python3
"""最终版：提取DeepSeek和Claude对话为Markdown"""
import re
import html

def extract_deepseek():
    """提取DeepSeek对话 - 从meta description中获取"""
    with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 从meta description提取
    desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', content)
    if desc_match:
        full_desc = html.unescape(desc_match.group(1))
        return full_desc
    return None

def extract_claude():
    """提取Claude对话 - 从长文本块中获取"""
    with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\Claude (2026_3_1 23：14：04).html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Claude的内容分布在多个文本块中
    matches = re.findall(r'>([^<]{500,20000})<', content)
    
    user_question = None
    ai_response = []
    
    for match in matches:
        text = html.unescape(match.strip())
        # 过滤CSS/JS
        if any(x in text for x in ['{', '}', '@media', '.css', 'padding:', 'margin:', 'function(']):
            continue
        # 用户问题
        if 'maximum fountain height' in text.lower() and len(text) < 400:
            user_question = text
        # AI回复（包含物理分析）
        elif len(text) > 800 and any(k in text.lower() for k in ['impact', 'cavity', 'worthington', 'physics']):
            ai_response.append(text)
    
    return user_question, ai_response[0] if ai_response else None

def create_deepseek_md(content):
    """创建DeepSeek Markdown"""
    md = f"""# IYPT 2026 Ring Fountain - DeepSeek对话记录

**日期**: 2026-03-04  
**来源**: DeepSeek AI  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics

---

## 📋 完整对话内容

{content}

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
    return md

def create_claude_md(user, ai):
    """创建Claude Markdown"""
    md = f"""# IYPT 2026 Ring Fountain - Claude对话记录

**日期**: 2026-03-01  
**来源**: Claude AI  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics

---

## 📝 用户问题

{user if user else '*未提取到问题*'}

---

## 🤖 AI分析

{ai if ai else '*未提取到回复*'}

---

## 📊 核心物理机制

### 1. 初始冲击与空腔形成
- **冲击与压力脉冲**: 环撞击水面产生极高局部压力
- **空腔形成**: 高Re和高Fr条件下，物体拖曳瞬态空腔

### 2. 空腔坍缩与流动聚焦
- **坍缩机制**: 惯性、表面张力、重力竞争
- **环形几何效应**: 内外空腔壁坍缩相互作用，流动聚焦

### 3. 射流形成与喷泉上升
- **射流生成机制**: 空腔底部液体被加速向上，形成Worthington射流
- **喷泉高度决定因素**:
  - 初始动量通量
  - 有效负浮力通量
  - 夹带效应
  - 环境条件

---

*自动生成于 2026-03-04*  
*原始文件: Claude (2026_3_1 23：14：04).html*
"""
    return md

if __name__ == '__main__':
    print("提取 DeepSeek 对话...")
    deepseek_content = extract_deepseek()
    if deepseek_content:
        md = create_deepseek_md(deepseek_content)
        with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_deepseek.md', 'w', encoding='utf-8') as f:
            f.write(md)
        print("  ✓ 已保存 ring_fountain_deepseek.md")
    else:
        print("  ✗ 未能提取内容")
    
    print("\n提取 Claude 对话...")
    user, ai = extract_claude()
    if user or ai:
        md = create_claude_md(user, ai)
        with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_claude.md', 'w', encoding='utf-8') as f:
            f.write(md)
        print("  ✓ 已保存 ring_fountain_claude.md")
    else:
        print("  ✗ 未能提取内容")
    
    print("\n✅ 全部完成!")
