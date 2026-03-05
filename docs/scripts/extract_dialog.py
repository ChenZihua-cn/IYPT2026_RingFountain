#!/usr/bin/env python3
"""提取SingleFile保存的HTML对话内容为Markdown"""
import re
import html
import sys

def extract_deepseek_dialog(filepath):
    """提取DeepSeek对话"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取og:description（对话摘要）
    desc_match = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"', content)
    summary = html.unescape(desc_match.group(1)) if desc_match else ""
    
    # 提取所有可能的对话内容
    # 查找较长的文本段落
    text_matches = re.findall(r'>([^<]{100,10000})<', content)
    
    # 分类：用户问题（以When/How/What开头）和AI回复（包含分析）
    user_question = None
    ai_response = []
    
    for text in text_matches:
        text = html.unescape(text.strip())
        # 用户问题特征
        if text.startswith('When a flat metal ring') or 'falls from a certain height' in text:
            if not user_question:
                user_question = text
        # AI回复特征
        elif any(keyword in text for keyword in ['Solution', 'Analysis', 'Step 1', 'dimensionless', 'Froude number']):
            if len(text) > 500:
                ai_response.append(text)
    
    return {
        'date': '2026-03-04',
        'source': 'DeepSeek',
        'summary': summary,
        'user_question': user_question,
        'ai_response': ai_response[0] if ai_response else None
    }

def extract_claude_dialog(filepath):
    """提取Claude对话"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Claude的对话结构不同，尝试提取
    text_matches = re.findall(r'>([^<]{100,10000})<', content)
    
    user_question = None
    ai_response = []
    
    for text in text_matches:
        text = html.unescape(text.strip())
        if 'ring' in text.lower() and 'fountain' in text.lower() and len(text) < 500:
            if not user_question:
                user_question = text
        elif len(text) > 500 and any(k in text.lower() for k in ['physics', 'dimensionless', 'theory']):
            ai_response.append(text)
    
    return {
        'date': '2026-03-01',
        'source': 'Claude',
        'user_question': user_question,
        'ai_response': ai_response[0] if ai_response else None
    }

def save_as_markdown(data, output_path):
    """保存为Markdown格式"""
    md_content = f"""# IYPT 2026 Ring Fountain - {data['source']}对话

**日期**: {data['date']}  
**来源**: {data['source']}  
**主题**: IYPT 2026 Problem 3 - Ring Fountain Physics

---

## 用户问题

{data.get('user_question', '未提取到问题')}

---

## AI分析

{data.get('ai_response', '未提取到回复')}

---

## 摘要

{data.get('summary', '')}

---

*自动提取自HTML存档*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"已保存: {output_path}")

if __name__ == '__main__':
    # 提取DeepSeek对话
    deepseek_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html'
    deepseek_data = extract_deepseek_dialog(deepseek_file)
    save_as_markdown(deepseek_data, r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_deepseek.md')
    
    # 提取Claude对话
    claude_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\Claude (2026_3_1 23：14：04).html'
    claude_data = extract_claude_dialog(claude_file)
    save_as_markdown(claude_data, r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\ring_fountain_claude.md')
    
    print("\n提取完成!")
