#!/usr/bin/env python3
"""检查Claude HTML文件"""
import os

file_path = r'C:\Users\30856\Desktop\IYPT2026_RingFountain\docs\Claude (2026_3_1 23：14：04).html'

# 检查文件大小
size = os.path.getsize(file_path)
print(f"Claude HTML文件大小: {size} 字节")
print(f"约为 {size/1024/1024:.2f} MB")

# 读取前1000字符查看结构
with open(file_path, 'r', encoding='utf-8') as f:
    first_chunk = f.read(2000)

print("\n=== 文件开头2000字符 ===")
print(first_chunk)

# 搜索关键词
keywords = ['ring', 'fountain', 'metal', 'water', 'height', '喷泉', '金属', '水']
print("\n=== 搜索关键词 ===")
for keyword in keywords:
    if keyword.lower() in first_chunk.lower():
        print(f"找到 '{keyword}'")
        
# 查找可能的对话开始
if 'When a flat metal ring' in first_chunk:
    print("\n找到用户问题开始")
    
# 查找Claude的响应
if 'Claude' in first_chunk:
    print("找到'Claude'关键词")
