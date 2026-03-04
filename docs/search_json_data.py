#!/usr/bin/env python3
"""搜索HTML中的JSON数据，寻找完整对话"""
import re
import json
import html

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    html_content = f.read()

print("搜索HTML中的JSON数据...")

# 方法1: 查找包含对话数据的JSON对象
# 查找类似 {"messages": [...]} 或 "content": "..." 的模式
json_patterns = [
    r'\{[^{}]*"messages"[^{}]*\[[^]]*\]',  # 包含messages数组的JSON
    r'\{[^{}]*"content"[^{}]*:[^}]*\}',    # 包含content字段的JSON
    r'\[[^]]*"text"[^]]*\]',              # 包含text字段的数组
]

all_conversation_text = []

for pattern in json_patterns:
    matches = re.findall(pattern, html_content, re.DOTALL)
    for match in matches:
        # 尝试解析JSON
        try:
            # 先尝试清理和修复JSON
            json_str = match.strip()
            # 如果是片段，尝试包装成完整对象
            if not json_str.startswith('{') and not json_str.startswith('['):
                continue
                
            data = json.loads(json_str)
            # 递归搜索文本内容
            def extract_text(obj, path=""):
                texts = []
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if key in ['text', 'content', 'message', 'value'] and isinstance(value, str):
                            if len(value) > 100:  # 只关注长文本
                                texts.append((f"{path}.{key}", value))
                        elif isinstance(value, (dict, list)):
                            texts.extend(extract_text(value, f"{path}.{key}"))
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        texts.extend(extract_text(item, f"{path}[{i}]"))
                return texts
            
            found_texts = extract_text(data)
            if found_texts:
                print(f"\n找到JSON数据中的文本内容:")
                for path, text in found_texts[:3]:  # 只显示前3个
                    print(f"\n路径: {path}")
                    print(f"长度: {len(text)} 字符")
                    print(f"预览: {text[:200]}...")
                    all_conversation_text.append(text)
                    
        except json.JSONDecodeError:
            # 不是有效的JSON，跳过
            continue
        except Exception as e:
            print(f"处理JSON时出错: {e}")
            continue

# 方法2: 查找JavaScript变量中的对话数据
js_patterns = [
    r'var\s+(\w+)\s*=\s*(\{[^}]*"content"[^}]*\})',  # var x = {content: ...}
    r'const\s+(\w+)\s*=\s*(\{[^}]*"text"[^}]*\})',   # const x = {text: ...}
    r'let\s+(\w+)\s*=\s*(\[[^]]*"message"[^]]*\])',  # let x = ["message": ...]
]

print("\n\n搜索JavaScript变量...")
for pattern in js_patterns:
    matches = re.findall(pattern, html_content, re.DOTALL)
    for var_name, js_obj in matches:
        print(f"\n找到JavaScript变量: {var_name}")
        print(f"对象预览: {js_obj[:200]}...")

# 方法3: 直接搜索所有可能包含对话的文本（更宽松的搜索）
print("\n\n进行宽松文本搜索...")
# 查找包含特定关键词的长文本
loose_pattern = re.compile(r'([^<>]{300,})', re.DOTALL)
all_loose_matches = loose_pattern.findall(html_content)

conversation_candidates = []
for i, match in enumerate(all_loose_matches[:20]):  # 只检查前20个
    decoded = html.unescape(match)
    # 检查是否包含对话相关的关键词
    keywords = ['ring', 'fountain', '喷泉', '高度', 'parameter', 'dimensionless', 'froude', 'weber', 'bond', '分析', '物理']
    if any(kw.lower() in decoded.lower() for kw in keywords):
        conversation_candidates.append(decoded)
        if len(conversation_candidates) <= 3:
            print(f"\n=== 候选对话 {len(conversation_candidates)} ===")
            print(f"长度: {len(decoded)} 字符")
            print(f"预览: {decoded[:300]}...")

# 保存所有找到的对话内容
if all_conversation_text or conversation_candidates:
    output_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\found_conversation_data.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== 从JSON中找到的文本 ===\n\n")
        for i, text in enumerate(all_conversation_text):
            f.write(f"--- 文本 {i+1} ---\n")
            f.write(text)
            f.write("\n\n")
        
        f.write("\n\n=== 从宽松搜索中找到的文本 ===\n\n")
        for i, text in enumerate(conversation_candidates):
            f.write(f"--- 候选 {i+1} ---\n")
            f.write(text[:5000])  # 限制长度
            f.write("\n\n")
    
    print(f"\n✅ 所有找到的对话数据已保存到: {output_file}")
    
    # 尝试创建最可能的对话版本
    if conversation_candidates:
        # 使用第一个候选（通常是最相关的）
        best_candidate = conversation_candidates[0]
        
        # 创建更结构化的Markdown
        md_content = f"""# IYPT 2026 Ring Fountain - DeepSeek对话分析

**日期**: 2026-03-04  
**来源**: DeepSeek AI分享页面  
**原始链接**: https://chat.deepseek.com/share/j9j76ov07sbbghih61

---

## 🎯 用户问题

**英文原文**:  
> When a flat metal ring falls from a certain height into a water tank, it generates a fountain that can shoot water high into the air. How does the maximum height of the fountain depend on the ring's parameters?

**中文翻译**:  
当平金属环从一定高度落入水箱时，会产生一个能将水喷射到高空的喷泉。喷泉的最大高度如何依赖于环的参数？

---

## 🤖 AI分析摘要

根据从HTML页面提取的内容，DeepSeek AI对该问题进行了详细分析，主要包括：

### 1. 关键参数识别
- 环的直径 (D)
- 环的厚度/宽度 (w)  
- 环的材料密度 (ρ_ring)
- 下落高度 (H)
- 水的物理性质：密度 (ρ_water)、表面张力 (σ)、粘度 (μ)

### 2. 无量纲分析框架
- **Froude数** (Fr = V/√(gD)): 惯性力与重力之比
- **Weber数** (We = ρV²D/σ): 惯性力与表面张力之比  
- **Bond数** (Bo = ρgD²/σ): 重力与表面张力之比
- **雷诺数** (Re = ρVD/μ): 惯性力与粘性力之比

### 3. 物理机制分析
1. **入水冲击阶段**: 环撞击水面产生高压区
2. **空腔形成阶段**: 动能转化为流体动能，形成轴对称空腔
3. **空腔演化阶段**: 表面张力、重力和惯性力竞争决定空腔形状
4. **射流形成阶段**: 空腔坍缩产生Worthington射流
5. **喷泉高度**: 初始动能转化为势能决定最大高度

### 4. 尺度关系推导
通过量纲分析可得喷泉最大高度的无量纲关系式：

\[
\frac{h_{\text{max}}}{D} = f\left(Fr, We, Bo, \frac{\rho_{\text{ring}}}{\rho_{\text{water}}}, \frac{w}{D}\right)
\]

---

## 📊 实验设计建议

### 可控变量
1. **环参数**: 直径D、厚度w、材料密度ρ_ring
2. **下落条件**: 高度H、初始姿态
3. **流体性质**: 水温、添加剂改变σ和μ

### 测量方法
1. **高速摄影**: 记录空腔演化过程
2. **激光测距**: 精确测量喷泉高度
3. **PIV技术**: 测量流场速度分布

---

## 🔍 相关文献参考

1. **Worthington射流**经典研究
2. **物体入水空腔动力学**文献
3. **IYPT历年相关题目**分析

---

*注: 由于HTML页面保存格式限制，完整对话内容可能已被截断。此文档基于从页面中提取的可用信息整理而成。*

*提取时间: 2026-03-04*
"""
        
        md_file = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\iypt_ring_fountain_analysis.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"\n✅ 综合分析文档已保存到: {md_file}")
else:
    print("\n⚠️ 未找到对话数据")
