#!/usr/bin/env python3
"""提取最新的DeepSeek对话内容（2026-03-04 22:44:11）"""
import re
import html
import os

file_path = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 22：44：11).html'

print(f"正在读取最新DeepSeek对话文件...")
print(f"文件路径: {file_path}")

# 检查文件是否存在
if not os.path.exists(file_path):
    print(f"错误: 文件不存在")
    exit(1)

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"文件大小: {len(html_content)} 字符")
print(f"约为 {len(html_content)/1024/1024:.2f} MB")

# 方法：查找所有长文本块
all_text_blocks = re.findall(r'>([^<]{200,})<', html_content)
print(f"\n找到 {len(all_text_blocks)} 个长文本块")

# 过滤出包含关键词的块
keywords = ['ring', 'fountain', '金属环', '喷泉', '高度', 'parameter', 
            'dimensionless', 'froude', 'weber', 'bond', '物理', '分析', 
            '理论', '补充', 'water', 'impact', 'cavity', 'jet']

relevant_blocks = []

for i, block in enumerate(all_text_blocks):
    decoded = html.unescape(block.strip())
    
    # 跳过CSS/JS代码（常见模式）
    skip_patterns = ['@keyframes', '@font-face', 'var(', '.ds-', '.Button_', 
                     'KaTeX_', '--font-', 'rgb(', 'linear-gradient', 'background-color']
    
    if any(pattern in decoded for pattern in skip_patterns):
        continue
    
    # 检查是否包含关键词
    if any(kw.lower() in decoded.lower() for kw in keywords):
        relevant_blocks.append(decoded)
        
        # 显示前几个块的预览
        if len(relevant_blocks) <= 3:
            print(f"\n=== 相关块 {len(relevant_blocks)} (原始索引: {i}) ===")
            print(f"长度: {len(decoded)} 字符")
            print(f"预览: {decoded[:300]}...")

print(f"\n总计找到 {len(relevant_blocks)} 个相关文本块")

# 保存所有相关块到文件
if relevant_blocks:
    output_txt = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\latest_conversation_raw.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        for i, block in enumerate(relevant_blocks):
            f.write(f"=== 块 {i+1} ===\n")
            f.write(block)
            f.write("\n\n" + "="*60 + "\n\n")
    
    print(f"\n✅ 原始相关文本块已保存到: {output_txt}")
    
    # 尝试识别用户问题和AI回答
    user_question = ""
    ai_response = []
    theory_supplement = []
    
    for block in relevant_blocks:
        # 查找用户问题（通常以英文问题开始）
        if 'When a flat metal ring' in block or '当平金属环' in block:
            user_question = block
        # 查找可能的AI回答
        elif '好的' in block or '根据' in block or '补充' in block or '理论' in block:
            ai_response.append(block)
        # 查找理论补充内容
        elif 'Fr' in block or 'We' in block or 'Bo' in block or '雷诺数' in block:
            theory_supplement.append(block)
    
    print(f"\n识别结果:")
    print(f"- 用户问题: {'已找到' if user_question else '未找到'}")
    print(f"- AI回答块: {len(ai_response)} 个")
    print(f"- 理论补充块: {len(theory_supplement)} 个")
    
    # 创建结构化的Markdown文档
    md_content = f"""# IYPT 2026 Ring Fountain - 最新理论补充

**来源**: DeepSeek AI最新对话  
**文件**: DeepSeek (2026_3_4 22：44：11).html  
**保存时间**: 2026-03-04 22:44:11 (中国标准时间)  
**提取时间**: 2026-03-04  
**性质**: 理论补充与深化分析

---

## 🎯 对话背景

此对话是之前DeepSeek对话的延续或补充，可能包含对金属环喷泉问题的进一步理论分析、公式推导或物理机制探讨。

---

## 📋 提取的对话内容

共提取到 {len(relevant_blocks)} 个相关文本块：

### 关键块预览：
"""
    
    # 添加每个块的预览
    for i, block in enumerate(relevant_blocks[:10]):  # 只显示前10个
        preview = block[:300].replace('\n', ' ')
        md_content += f"\n**块 {i+1}** (长度: {len(block)}字符):\n"
        md_content += f"> {preview}...\n"
    
    # 添加完整内容（如果块不太多）
    if len(relevant_blocks) <= 15:
        md_content += f"""

---

## 📝 完整内容

"""
        for i, block in enumerate(relevant_blocks):
            md_content += f"\n### 块 {i+1}\n\n{block}\n\n---\n"
    else:
        md_content += f"""

---

## 📝 部分重要内容

由于内容较多，以下是部分重要块的内容：

"""
        # 选择最可能包含理论补充的块
        important_blocks = []
        for block in relevant_blocks:
            # 根据关键词判断重要性
            importance_score = 0
            importance_keywords = ['公式', '推导', '理论', '分析', '机制', '物理', 
                                  'Fr', 'We', 'Bo', 'Re', '无量纲', '标度律']
            for kw in importance_keywords:
                if kw in block:
                    importance_score += 1
            
            if importance_score >= 2:
                important_blocks.append(block)
        
        if important_blocks:
            for i, block in enumerate(important_blocks[:5]):
                md_content += f"\n### 重要块 {i+1}\n\n{block}\n\n"
        else:
            # 如果没有明显的重要块，使用前几个
            for i, block in enumerate(relevant_blocks[:5]):
                md_content += f"\n### 块 {i+1}\n\n{block}\n\n"
    
    md_content += f"""
---

## 🔍 内容分析

### 可能包含的理论补充
基于关键词分析，此对话可能包含以下方面的理论补充：

1. **无量纲分析深化** - 对Froude数、Weber数、Bond数等更详细的讨论
2. **物理机制细化** - 对空腔形成、坍缩、射流生成等过程的更深入分析
3. **公式推导完善** - 对喷泉高度标度律的进一步数学推导
4. **参数依赖研究** - 对环几何参数影响的更系统分析
5. **实验设计建议** - 针对理论预测的实验验证方案

### 与之前对话的关系
此对话可能是对之前DeepSeek对话的补充，可能涉及：
- 对用户质疑的回应
- 对Claude分析的进一步对比
- 新的理论见解或推导
- 实验验证方法的讨论

---

## 📚 建议的后续处理

1. **内容分类**: 将提取的内容按主题分类（理论推导、实验设计、物理机制等）
2. **与之前对话整合**: 将此补充内容整合到已有的分析框架中
3. **关键公式提取**: 提取对话中出现的数学公式和推导
4. **物理概念整理**: 整理对话中涉及的物理概念和理论

---

## 🏷️ 关键词
IYPT 2026, 金属环喷泉, 理论补充, DeepSeek, 物理机制, 无量纲分析, 最新对话

---

*文档生成时间: 2026-03-04*  
*基于DeepSeek最新对话的HTML内容提取*  
*注: 由于HTML页面结构复杂，提取内容可能不完整*
"""
    
    md_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\latest_theory_supplement.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n✅ 理论补充文档已保存到: {md_file}")
    
    # 同时创建一个更简洁的版本，专注于可能的理论内容
    if theory_supplement:
        theory_content = "\n\n".join(theory_supplement)
        theory_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\pure_theory_content.txt'
        with open(theory_file, 'w', encoding='utf-8') as f:
            f.write(theory_content)
        print(f"✅ 纯理论内容已保存到: {theory_file}")
        
else:
    print("\n⚠️ 未找到相关文本块")
    print("\n尝试其他提取方法...")
    
    # 尝试查找属性中的内容
    attr_pattern = re.compile(r'content="([^"]{100,})"')
    attr_matches = attr_pattern.findall(html_content)
    print(f"找到 {len(attr_matches)} 个长属性值")
    
    # 查找包含关键词的属性
    found_attrs = []
    for i, attr in enumerate(attr_matches[:20]):
        decoded = html.unescape(attr)
        if any(kw.lower() in decoded.lower() for kw in keywords[:10]):
            found_attrs.append(decoded)
            print(f"\n属性 {i+1} (长度: {len(decoded)}):")
            print(decoded[:200])
            print("...")
    
    if found_attrs:
        print(f"\n找到 {len(found_attrs)} 个相关属性值")
        # 保存属性内容
        with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\attrs_content.txt', 'w', encoding='utf-8') as f:
            for i, attr in enumerate(found_attrs):
                f.write(f"=== 属性 {i+1} ===\n")
                f.write(attr)
                f.write("\n\n")
        print("属性内容已保存")
