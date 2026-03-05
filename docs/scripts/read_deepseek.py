#!/usr/bin/env python3
"""直接读取DeepSeek HTML并提取对话"""
import re

with open(r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\DeepSeek (2026_3_4 12：46：05).html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"文件大小: {len(content)} 字符")

# 搜索关键文本
keywords = ['When a flat metal ring', 'fountain', 'maximum height', 'dimensionless']
for kw in keywords:
    if kw.lower() in content.lower():
        idx = content.lower().find(kw.lower())
        print(f"\n找到 '{kw}' 在位置 {idx}")
        # 显示上下文
        start = max(0, idx - 100)
        end = min(len(content), idx + 300)
        print(f"上下文: ...{content[start:end]}...")
        break
