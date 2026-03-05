#!/usr/bin/env python3
"""提取SingleFile保存的HTML对话内容为Markdown - 优化版"""
import re
import html

def extract_all_text_blocks(filepath):
    """提取所有文本块"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有较长的文本段落（可能是对话内容）
    # 过滤掉CSS、JS代码
    text_blocks = []
    
    # 模式：>文本内容<
    matches = re.findall(r'>([^<]{50,20000})<', content)
    
    for text in matches:
        text = html.unescape(text.strip())
        # 过滤掉代码、CSS等
        if any(skip in text for skip in ['{', '}', '@media', 'function(', '.css', 'padding:', 'margin:', 'display:', 'color:', 'font-size:', 'background:', 'var(--']):
            continue
        if text.startswith('data:') or text.startswith('http'):
            continue
        # 保留有意义的文本
        if len(text) > 100 and any(c.isalpha() for c in text):
            text_blocks.append(text)
    
    return text_blocks

def identify_deepseek_dialog(text_blocks):
    """识别DeepSeek对话结构"""
    user_msg = None
    ai_msgs = []
    
    for text in text_blocks:
        # 用户问题特征
        if text.startswith('When a flat metal ring') or ('falls from' in text and 'height' in text and len(text) < 800):
            if not user_msg:
                user_msg = text
        # AI回复特征
        elif any(keyword in text for keyword in ['Solution:', 'Step 1', 'Analysis:', 'Physical mechanism', 'Froude number', 'Weber number']):
            if len(text) > 500:
                ai_msgs.append(text)
    
    return user_msg, ai_msgs

def identify_claude_dialog(text_blocks):
    """识别Claude对话结构"""
    user_msg = None
    ai_msgs = []
    
    for text in text_blocks:
        # 用户问题
        if 'maximum fountain height' in text.lower() and len(text) < 500:
            if not user_msg:
                user_msg = text
        # AI回复
        elif len(text) > 500 and any(k in text.lower() for k in ['impact', 'cavity', 'jet', 'worthington', 'physics']):
            ai_msgs.append(text)
    
    return user_msg, ai_msgs

def create_markdown(source, date, user_msg, ai_msg):
    """创建Markdown文档"""
    md = f"""# IYPT 2026 Ring Fountain - {source}对话记录

**日期**: {date}  
**来源**: {source} AI  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics

---

## 📝 用户问题

{user_msg if user_msg else '*未提取到用户问题*'}

---

## 🤖 AI分析

{ai_msg if ai_msg else '*未提取到AI回复*'}

---

## 📊 内容概要

### 核心物理机制
1. **入水冲击** - 金属环撞击水面产生高压，形成空腔
2. **空腔演化** - 惯性、表面张力、重力竞争导致空腔坍缩
3. **射流形成** - 空腔底部液体被加速向上，形成Worthington射流
4. **喷泉高度** - 初始动量与浮力/重力平衡决定最大高度

### 关键无量纲数
- **Froude数** Fr = V/sqrt(gD) - 惯性 vs 重力
- **Weber数** We = ρV²D/σ - 惯性 vs 表面张力
- **Bond数** Bo = ρgD²/σ - 重力 vs 表面张力

---

*文件自动生成于 2026-03-04*  
*原始HTML存档保留在 docs/ 目录*
"""
    return md

if __name__ == '__main__':
    # 处理DeepSeek文件
    print("提取 DeepSeek 对话...")
    blocks = extract_all_text_blocks(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html')
    print(f"  找到 {len(blocks)} 个文本块")
    user, ai_list = identify_deepseek_dialog(blocks)
    ai = ai_list[0] if ai_list else None
    
    md_content = create_markdown("DeepSeek", "2026-03-04", user, ai)
    with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_deepseek.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    print("  ✓ 已保存 ring_fountain_deepseek.md")
    
    # 处理Claude文件
    print("\n提取 Claude 对话...")
    blocks = extract_all_text_blocks(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\Claude (2026_3_1 23：14：04).html')
    print(f"  找到 {len(blocks)} 个文本块")
    user, ai_list = identify_claude_dialog(blocks)
    ai = ai_list[0] if ai_list else None
    
    md_content = create_markdown("Claude", "2026-03-01", user, ai)
    with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_claude.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    print("  ✓ 已保存 ring_fountain_claude.md")
    
    print("\n✅ 全部完成!")
