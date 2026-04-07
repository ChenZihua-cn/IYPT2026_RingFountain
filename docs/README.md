# IYPT 2026 Ring Fountain - 研究文档库

**项目**: IYPT 2026 Problem - Ring Fountain  
**最后更新**: 2026-03-05

---

## 📁 目录结构

```
docs/
├── 📄 README.md                    # 本文件
├── 📄 DOCUMENTATION_INDEX.md       # 完整文档索引与导读
│
├── 📁 analysis/                    # 理论分析文档 ⭐
│   ├── claude_full_analysis.md     # Claude完整分析（核心）
│   ├── tank_size_effect_analysis.md # 水槽尺寸效应（核心）
│   ├── ai_analysis_comparison.md   # AI分析对比
│   ├── latest_theory_supplement.md # 最新理论补充
│   └── ... (其他分析文档)
│
├── 📁 references/                  # 参考文献
│   ├── PAPER_CITATIONS.md          # 完整论文引用（含BibTeX）
│   └── papers_reference.md         # 论文参考列表
│
├── 📁 papers/                      # 论文PDF库 ⭐
│   ├── README.md                   # 论文库说明
│   └── *.pdf (8篇论文)             # arXiv预印本
│
├── 📁 scripts/                     # Python脚本工具
│   ├── README.md                   # 脚本使用说明
│   ├── download_*.py               # 论文下载脚本
│   └── extract_*.py                # 对话提取脚本
│
├── 📁 raw_data/                    # 原始文本数据
│   └── *.txt                       # 提取的对话内容
│
└── 📁 raw_html/                    # 原始HTML文件
    └── *.html                      # SingleFile保存的AI对话
```

---

## 🚀 快速开始

### **必读文档**（30分钟）
1. [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - 完整索引
2. [analysis/claude_full_analysis.md](analysis/claude_full_analysis.md) - 理论框架
3. [analysis/tank_size_effect_analysis.md](analysis/tank_size_effect_analysis.md) - 尺寸效应

### **必读论文**（1小时）
1. [papers/Jana_etal_2025_Impacting_spheres.pdf](papers/Jana_etal_2025_Impacting_spheres.pdf) - 最新综述
2. [papers/Gekle_Gordillo_2009_Worthington_Jets.pdf](papers/Gekle_Gordillo_2009_Worthington_Jets.pdf) - 核心机制

---

## 📊 文档统计

| 类别 | 数量 | 位置 |
|------|------|------|
| 理论分析 | 10篇 | `analysis/` |
| 参考文献 | 2篇 | `references/` |
| 论文PDF | 8篇 | `papers/` |
| Python脚本 | 22个 | `scripts/` |
| 原始数据 | 5个 | `raw_data/` |
| 原始HTML | 3个 | `raw_html/` |

---

## 💡 使用建议

### **实验设计者**
→ 阅读 `analysis/claude_full_analysis.md` + `papers/Aristoff_etal_2008_Water_entry_spheres.pdf`

### **理论分析者**
→ 阅读 `analysis/` 目录所有文档 + `papers/Jana_etal_2025_Impacting_spheres.pdf`

### **新成员入门**
→ 按顺序阅读 DOCUMENTATION_INDEX → analysis/claude_full_analysis → papers/README

---

## 🔧 工具使用

```bash
# 下载论文
cd scripts
python download_all_papers.py

# 提取对话
python extract_latest_deepseek.py
```

---

## 📞 维护信息

- **项目**: IYPT 2026 - Ring Fountain Problem
- **维护**: 研究团队
- **更新**: 2026-03-05

---

*文档结构清晰化完成*