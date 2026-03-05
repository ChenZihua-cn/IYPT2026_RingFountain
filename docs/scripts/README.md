# IYPT 2026 Ring Fountain - 脚本工具集

**目录**: `docs/scripts/`  
**用途**: 提取、处理和下载与研究相关的数据和论文  
**更新时间**: 2026-03-05

---

## 📂 脚本分类

### **1. 对话提取脚本** (HTML → Markdown/文本)

用于从SingleFile保存的HTML文件中提取AI对话内容。

| 脚本名 | 功能 | 来源文件 | 输出 |
|--------|------|----------|------|
| `extract_claude.py` | 提取Claude对话 | `Claude (2026_3_1 23:14:04).html` | `claude_conversation_summary.md` |
| `extract_all_blocks.py` | 提取所有文本块 | `DeepSeek (2026_3_4 12:46:05).html` | `all_conversation_parts.txt` |
| `extract_conversation.py` | 提取对话内容 | DeepSeek HTML | `conversation_simple.txt` |
| `extract_deepseek_manual.py` | 手动提取DeepSeek | DeepSeek HTML | `deepseek_ring_fountain_conversation.md` |
| `extract_deepseek_v4.py` | DeepSeek提取v4 | DeepSeek HTML | 各种输出 |
| `extract_latest_deepseek.py` | 提取最新DeepSeek对话 | `DeepSeek (2026_3_4 22:44:11).html` | `latest_theory_supplement.md` |
| `extract_dialog.py` | 对话框提取 | DeepSeek HTML | - |
| `extract_dialog_v2.py` | 对话框提取v2 | DeepSeek HTML | - |
| `extract_final.py` | 最终提取版本 | DeepSeek HTML | - |
| `extract_final_v2.py` | 最终提取v2 | DeepSeek HTML | - |
| `extract_full_conversation.py` | 完整对话提取 | DeepSeek HTML | - |
| `extract_v3.py` | 提取版本3 | DeepSeek HTML | - |
| `final_extract.py` | 最终提取 | DeepSeek HTML | - |
| `read_deepseek.py` | 读取DeepSeek文件 | DeepSeek HTML | - |

### **2. 文档生成脚本**

| 脚本名 | 功能 | 输入 | 输出 |
|--------|------|------|------|
| `create_claude_full_doc.py` | 生成Claude完整分析文档 | 提取的文本 | `claude_full_analysis.md` |
| `check_claude_file.py` | 检查Claude文件 | HTML文件 | 文件信息报告 |

### **3. 数据处理脚本**

| 脚本名 | 功能 | 用途 |
|--------|------|------|
| `search_json_data.py` | 搜索JSON数据 | 在HTML中查找JSON格式的对话数据 |
| `search_json_simple.py` | 简化版JSON搜索 | 快速搜索JSON数据 |

### **4. 论文下载脚本**

| 脚本名 | 功能 | 输出位置 |
|--------|------|----------|
| `download_papers_simple.py` | 简单论文下载 | `../papers/` |
| `download_all_papers.py` | 批量论文下载 | `../papers/` |
| `download_key_papers.py` | 下载关键论文 | `../papers/` |
| `search_and_download.py` | 搜索并列出论文 | `../papers/search_results.txt` |

---

## 🚀 使用指南

### **提取最新DeepSeek对话**
```bash
python extract_latest_deepseek.py
```
输出: `latest_theory_supplement.md`, `tank_size_effect_analysis.md`

### **下载所有相关论文**
```bash
python download_all_papers.py
```
输出: `../papers/*.pdf`

### **搜索arXiv论文**
```bash
python search_and_download.py
```
输出: `../papers/search_results.txt`

---

## 📊 脚本使用统计

### **已使用的脚本**
1. ✅ `extract_claude.py` - 成功提取Claude对话
2. ✅ `extract_latest_deepseek.py` - 成功提取最新理论补充
3. ✅ `create_claude_full_doc.py` - 生成完整分析文档
4. ✅ `download_all_papers.py` - 下载5篇基础论文
5. ✅ `download_key_papers.py` - 下载3篇关键论文
6. ✅ `search_and_download.py` - 搜索相关论文

### **保留但未使用的脚本**
- `extract_all_blocks.py` - 保留用于调试
- `extract_conversation.py` - 早期版本
- `extract_deepseek_manual.py` - 手动提取方法
- `search_json_data.py` - JSON搜索方法

---

## 🔧 技术说明

### **依赖库**
所有脚本仅使用Python标准库：
- `re` - 正则表达式
- `html` - HTML解析
- `os` - 文件操作
- `urllib.request` - 网络请求
- `xml.etree.ElementTree` - XML解析

### **Python版本**
- Python 3.8+
- 无需额外安装依赖

### **编码**
- 所有脚本使用UTF-8编码
- 支持中英文混合内容

---

## 📁 文件对应关系

```
scripts/
├── extract_claude.py → ../claude_conversation_summary.md
├── extract_latest_deepseek.py → ../latest_theory_supplement.md
│                              → ../tank_size_effect_analysis.md
├── create_claude_full_doc.py → ../claude_full_analysis.md
├── download_all_papers.py → ../papers/*.pdf
└── search_and_download.py → ../papers/search_results.txt
```

---

## 📝 脚本开发历史

### **迭代过程**
1. **v1**: `extract_conversation.py` - 基础提取
2. **v2**: `extract_deepseek_v4.py` - 改进提取逻辑
3. **v3**: `extract_dialog.py` - 针对对话框结构
4. **v4**: `extract_final.py` - 最终稳定版本
5. **v5**: `extract_latest_deepseek.py` - 针对最新对话优化

### **论文下载**
1. **v1**: `download_papers_simple.py` - 基础下载
2. **v2**: `download_all_papers.py` - 批量下载
3. **v3**: `search_and_download.py` - 集成搜索

---

## 💡 使用建议

### **对于新用户**
1. 首先运行 `download_key_papers.py` 获取关键论文
2. 运行 `extract_latest_deepseek.py` 获取最新理论补充
3. 阅读生成的Markdown文档

### **对于开发者**
1. 参考 `extract_latest_deepseek.py` 了解最新的提取方法
2. 参考 `download_all_papers.py` 了解批量下载逻辑
3. 可以基于现有脚本开发新的提取/下载功能

---

## 🔒 注意事项

1. **网络请求**: 论文下载脚本需要网络连接
2. **arXiv限制**: 请遵守arXiv的使用政策，不要频繁请求
3. **文件权限**: 确保有写入 `../papers/` 目录的权限
4. **存储空间**: 论文PDF可能占用较多空间（总计约30MB）

---

## 🐛 故障排除

### **下载失败**
- 检查网络连接
- 尝试使用VPN（某些地区可能无法访问arXiv）
- 检查防火墙设置

### **提取失败**
- 确保HTML文件存在且未损坏
- 检查文件路径是否正确
- 尝试使用不同的提取脚本

---

## 📞 维护信息

- **创建日期**: 2026-03-04
- **最后更新**: 2026-03-05
- **维护者**: IYPT 2026 Ring Fountain研究团队
- **问题反馈**: 在文档中记录问题

---

*本README与脚本同步更新*