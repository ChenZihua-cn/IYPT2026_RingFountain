# IYPT 2026 Ring Fountain - 文档索引

**项目**: IYPT 2026 Problem - Ring Fountain  
**最后更新**: 2026-03-05 21:25  
**文档版本**: v2.0

---

## 📁 目录结构

```
docs/
├── 📁 analysis/                           # 理论分析文档
│   ├── claude_full_analysis.md            # Claude完整分析 ⭐核心
│   ├── tank_size_effect_analysis.md       # 水槽尺寸效应分析 ⭐核心
│   ├── ai_analysis_comparison.md          # AI分析对比
│   ├── latest_theory_supplement.md        # 最新理论补充
│   ├── claude_conversation_summary.md     # Claude对话摘要
│   ├── deepseek_ring_fountain_conversation.md  # DeepSeek对话
│   ├── extracted_conversation_summary.md  # 提取的对话摘要
│   ├── iypt_ring_fountain_dialogue.md     # 对话记录
│   ├── ring_fountain_claude.md            # Claude分析
│   └── ring_fountain_deepseek.md          # DeepSeek分析
│
├── 📁 references/                         # 参考文献
│   ├── PAPER_CITATIONS.md                 # 完整论文引用 ⭐必读
│   └── papers_reference.md                # 论文参考列表
│
├── 📁 papers/                             # 论文库 (13篇PDF)
│   ├── README.md                          # 论文库说明
│   ├── *.pdf                              # 12篇论文
│   ├── download_log.txt                   # 下载记录
│   └── search_results.txt                 # 搜索结果
│
└── 📄 DOCUMENTATION_INDEX.md              # 本文件
```

---

## 📊 文档统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **分析文档** | 10篇 | `analysis/` 目录下的Markdown理论分析 |
| **参考文献** | 2篇 | `references/` 目录下的引用文档 |
| **论文PDF** | 13篇 | `papers/` 目录，arXiv预印本，总计约35MB |
| **Python脚本** | 1个 | `scripts/postprocessing/check_data.py`，数据检验工具 |

---

## 📖 核心文档导读

### **1. 理论分析** (必读) → `analysis/`

#### **a. Claude完整分析** ⭐
- **文件**: `analysis/claude_full_analysis.md`
- **来源**: Claude AI对话
- **内容**: 
  - 无量纲分析框架
  - 五个无量纲数 (Fr, We, Bo, Re, ρ_m/ρ_w)
  - 喷泉高度标度律推导
  - 能量传递机制

#### **b. 水槽尺寸效应分析** ⭐
- **文件**: `analysis/tank_size_effect_analysis.md`
- **来源**: DeepSeek最新对话
- **内容**:
  - 水槽有限尺寸对喷泉的影响
  - 边界条件效应
  - 扩展的无量纲参数 (δ_H, δ_W, Γ)

#### **c. AI分析对比**
- **文件**: `analysis/ai_analysis_comparison.md`
- **内容**: Claude与DeepSeek分析的异同比较

### **2. 参考文献** → `references/`

#### **a. 完整论文引用**
- **文件**: `references/PAPER_CITATIONS.md`
- **内容**: 8篇论文的详细引用信息（含BibTeX格式）

#### **b. 论文参考列表**
- **文件**: `references/papers_reference.md`
- **内容**: 论文列表及下载说明

### **3. 实验参考** → `papers/`

#### **a. 论文库**
- **位置**: `papers/`
- **核心论文**:
  - Jana et al. (2025) - 冲击理论综述
  - Gekle & Gordillo (2009) - Worthington喷射
  - Truscott & Aristoff (2008) - 水入射动力学

### **4. 工具脚本** → `scripts/`

- **`scripts/postprocessing/check_data.py`** — 模拟数据检验：读取环运动学、探针压力和力数据，进行NaN/Inf检测、静水压校验、单调性检查等诊断

---

## 🎯 快速开始指南

### **对于新成员**

1. **阅读核心文档** (30分钟)
   ```
   1. analysis/claude_full_analysis.md
   2. analysis/tank_size_effect_analysis.md
   3. analysis/ai_analysis_comparison.md
   ```

2. **浏览论文库** (1小时)
   ```
   阅读 papers/README.md
   重点阅读:
   - Jana et al. (2025) - 理论基础
   - Gekle & Gordillo (2009) - 核心机制
   ```

### **对于实验设计者**

1. **理论基础**: `analysis/claude_full_analysis.md`
2. **实验方法**: `papers/Aristoff_etal_2008_Water_entry_spheres.pdf`
3. **参数范围**: `analysis/latest_theory_supplement.md`

### **对于理论分析者**

1. **标度律推导**: `analysis/claude_full_analysis.md`
2. **经典理论**: `papers/Gekle_Gordillo_2009_Worthington_Jets.pdf`
3. **最新进展**: `papers/Jana_etal_2025_Impacting_spheres.pdf`

---

## 🔍 关键词索引

### **物理概念**
| 概念 | 相关文档 |
|------|----------|
| Wagner冲击理论 | `analysis/claude_full_analysis.md`, Jana et al. (2025) |
| Worthington喷射 | `analysis/tank_size_effect_analysis.md`, Gekle & Gordillo (2009) |
| 空腔动力学 | `analysis/latest_theory_supplement.md`, Bergmann et al. (2009) |
| 无量纲分析 | `analysis/claude_full_analysis.md` |
| 水槽尺寸效应 | `analysis/tank_size_effect_analysis.md` |

### **无量纲数**
| 符号 | 名称 | 定义 | 相关文档 |
|------|------|------|----------|
| Fr | Froude数 | v₀/√(gD) | `analysis/claude_full_analysis.md` |
| We | Weber数 | ρ_w v₀² D/σ | `analysis/claude_full_analysis.md` |
| Bo | Bond数 | ρ_w g D²/σ | `analysis/claude_full_analysis.md` |
| Re | Reynolds数 | ρ_w v₀ D/μ | `analysis/claude_full_analysis.md` |
| δ_H | 深度比 | H_tank/D | `analysis/tank_size_effect_analysis.md` |
| δ_W | 宽度比 | W/D | `analysis/tank_size_effect_analysis.md` |

### **研究方法**
| 方法 | 相关文档/脚本 |
|------|---------------|
| 量纲分析 | `analysis/claude_full_analysis.md` |
| 实验设计 | `papers/Aristoff_etal_2008_Water_entry_spheres.pdf` |
| CFD模拟 | `analysis/latest_theory_supplement.md` |

---

## 📈 文档发展历史

### **Phase 1: 对话提取** (2026-03-04)
- ✅ 提取Claude对话
- ✅ 提取DeepSeek对话
- ✅ 生成分析文档

### **Phase 2: 论文收集** (2026-03-05)
- ✅ 搜索arXiv论文
- ✅ 下载13篇核心论文
- ✅ 整理引用信息

### **Phase 3: 理论深化** (2026-03-05)
- ✅ 提取最新理论补充
- ✅ 分析水槽尺寸效应
- ✅ 扩展无量纲框架

### **Phase 4: 文档整合** (2026-03-05)
- ✅ 创建清晰的目录结构
- ✅ 整理脚本目录
- ✅ 分类存放所有文件

---

## 🔧 维护与更新

### **定期更新任务**
- [ ] 检查arXiv新论文（每月）
- [ ] 更新实验进展记录
- [ ] 补充新的理论分析

### **文档规范**
- 使用Markdown格式
- 保持UTF-8编码
- 添加更新时间戳
- 维护反向链接

---

## 💡 使用建议

### **文档阅读顺序**
```
1. DOCUMENTATION_INDEX.md (本文件)
2. analysis/claude_full_analysis.md
3. analysis/tank_size_effect_analysis.md
4. analysis/ai_analysis_comparison.md
5. references/PAPER_CITATIONS.md
6. papers/README.md
```

### **论文阅读顺序**
```
1. Truscott & Aristoff (2008) - 基础
2. Gekle & Gordillo (2009) - 核心机制
3. Aristoff et al. (2008) - 实验方法
4. Jana et al. (2025) - 最新进展
```

---

## 📞 联系与支持

- **项目**: IYPT 2026 - Ring Fountain Problem
- **维护**: 研究团队
- **更新**: 持续进行中

---

## 📄 许可说明

- **文档**: 研究团队原创内容
- **论文**: arXiv开放获取，遵循原始许可
- **代码**: 研究团队开发，可自由使用

---

*最后更新: 2026-03-05 21:25*  
*版本: v2.0*  
*状态: 活跃维护中*