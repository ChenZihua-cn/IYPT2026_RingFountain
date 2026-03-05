# IYPT 2026 Ring Fountain - 文档索引

**项目**: IYPT 2026 Problem - Ring Fountain  
**最后更新**: 2026-03-05  
**文档版本**: v1.0

---

## 📁 目录结构

```
docs/
├── 📄 核心分析文档
│   ├── ai_analysis_comparison.md          # AI分析对比
│   ├── claude_full_analysis.md            # Claude完整分析
│   ├── claude_conversation_summary.md     # Claude对话摘要
│   ├── deepseek_ring_fountain_conversation.md  # DeepSeek对话
│   ├── latest_theory_supplement.md        # 最新理论补充
│   ├── tank_size_effect_analysis.md       # 水槽尺寸效应分析
│   └── extracted_conversation_summary.md  # 提取的对话摘要
│
├── 📄 参考文献
│   ├── PAPER_CITATIONS.md                 # 完整论文引用
│   └── papers_reference.md                # 论文参考列表
│
├── 📁 papers/                             # 论文库 (8篇PDF)
│   ├── README.md                          # 论文库说明
│   ├── Jana_etal_2025_Impacting_spheres.pdf
│   ├── Gekle_Gordillo_2009_Worthington_Jets.pdf
│   ├── Sen_etal_2022_Elastocapillary_Worthington_jets.pdf
│   ├── Truscott_Aristoff_2008_Dynamics_of_Water_Entry.pdf
│   ├── Aristoff_etal_2008_Water_entry_spheres.pdf
│   ├── Truscott_etal_2012_Spinning_spheres.pdf
│   ├── Bergmann_etal_2009_Cavity_formation.pdf
│   ├── Cohen_2012_Soap_bubbles.pdf
│   ├── download_log.txt                   # 下载记录
│   └── search_results.txt                 # 搜索结果
│
├── 📁 scripts/                            # 脚本工具 (19个Python脚本)
│   ├── README.md                          # 脚本说明
│   ├── download_papers_simple.py          # 简单下载
│   ├── download_all_papers.py             # 批量下载
│   ├── download_key_papers.py             # 关键论文下载
│   ├── search_and_download.py             # 搜索下载
│   ├── extract_latest_deepseek.py         # 提取最新对话
│   ├── extract_claude.py                  # 提取Claude对话
│   ├── create_claude_full_doc.py          # 生成完整文档
│   └── [其他提取脚本...]
│
├── 📄 原始数据
│   ├── all_conversation_parts.txt         # 所有对话片段
│   ├── latest_conversation_raw.txt        # 最新对话原始文本
│   ├── conversation_simple.txt            # 简化对话
│   └── raw_extract.txt                    # 原始提取
│
└── 📄 原始HTML (SingleFile保存)
    ├── Claude (2026_3_1 23:14:04).html
    ├── DeepSeek (2026_3_4 12:46:05).html
    └── DeepSeek (2026_3_4 22:44:11).html
```

---

## 📊 文档统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **分析文档** | 8篇 | Markdown格式的理论分析 |
| **论文PDF** | 8篇 | arXiv预印本，总计约30MB |
| **Python脚本** | 19个 | 提取、下载、处理工具 |
| **原始HTML** | 3个 | SingleFile保存的AI对话 |
| **文本数据** | 5个 | 提取的原始对话内容 |

---

## 📖 核心文档导读

### **1. 理论分析** (必读)

#### **a. Claude完整分析**
- **文件**: `claude_full_analysis.md`
- **来源**: Claude AI对话
- **内容**: 
  - 无量纲分析框架
  - 五个无量纲数 (Fr, We, Bo, Re, ρ_m/ρ_w)
  - 喷泉高度标度律推导
  - 能量传递机制

#### **b. 最新理论补充**
- **文件**: `latest_theory_supplement.md` + `tank_size_effect_analysis.md`
- **来源**: DeepSeek最新对话
- **内容**:
  - 水槽尺寸效应
  - 边界条件影响
  - 扩展的无量纲参数 (δ_H, δ_W, Γ)

#### **c. AI分析对比**
- **文件**: `ai_analysis_comparison.md`
- **内容**: Claude与DeepSeek分析的异同

### **2. 实验参考**

#### **a. 论文库**
- **位置**: `papers/`
- **核心论文**:
  - Jana et al. (2025) - 冲击理论综述
  - Gekle & Gordillo (2009) - Worthington喷射
  - Truscott & Aristoff (2008) - 水入射动力学

#### **b. 完整引用**
- **文件**: `PAPER_CITATIONS.md`
- **内容**: 所有论文的详细引用信息

### **3. 工具脚本**

#### **a. 论文下载**
- **位置**: `scripts/`
- **主要脚本**:
  - `download_all_papers.py` - 批量下载
  - `search_and_download.py` - 搜索arXiv

#### **b. 对话提取**
- **主要脚本**:
  - `extract_latest_deepseek.py` - 提取最新理论
  - `extract_claude.py` - 提取Claude对话

---

## 🎯 快速开始指南

### **对于新成员**

1. **阅读核心文档** (30分钟)
   ```
   1. claude_full_analysis.md
   2. tank_size_effect_analysis.md
   3. ai_analysis_comparison.md
   ```

2. **浏览论文库** (1小时)
   ```
   阅读 papers/README.md
   重点阅读:
   - Jana et al. (2025) - 理论基础
   - Gekle & Gordillo (2009) - 核心机制
   ```

3. **了解工具** (15分钟)
   ```
   阅读 scripts/README.md
   ```

### **对于实验设计者**

1. **理论基础**: `claude_full_analysis.md`
2. **实验方法**: `papers/Aristoff_etal_2008_Water_entry_spheres.pdf`
3. **参数范围**: `latest_theory_supplement.md`

### **对于理论分析者**

1. **标度律推导**: `claude_full_analysis.md`
2. **经典理论**: `papers/Gekle_Gordillo_2009_Worthington_Jets.pdf`
3. **最新进展**: `papers/Jana_etal_2025_Impacting_spheres.pdf`

---

## 🔍 关键词索引

### **物理概念**
| 概念 | 相关文档 |
|------|----------|
| Wagner冲击理论 | `claude_full_analysis.md`, Jana et al. (2025) |
| Worthington喷射 | `tank_size_effect_analysis.md`, Gekle & Gordillo (2009) |
| 空腔动力学 | `latest_theory_supplement.md`, Bergmann et al. (2009) |
| 无量纲分析 | `claude_full_analysis.md` |
| 水槽尺寸效应 | `tank_size_effect_analysis.md` |

### **无量纲数**
| 符号 | 名称 | 定义 | 相关文档 |
|------|------|------|----------|
| Fr | Froude数 | v₀/√(gD) | `claude_full_analysis.md` |
| We | Weber数 | ρ_w v₀² D/σ | `claude_full_analysis.md` |
| Bo | Bond数 | ρ_w g D²/σ | `claude_full_analysis.md` |
| Re | Reynolds数 | ρ_w v₀ D/μ | `claude_full_analysis.md` |
| δ_H | 深度比 | H_tank/D | `tank_size_effect_analysis.md` |
| δ_W | 宽度比 | W/D | `tank_size_effect_analysis.md` |

### **研究方法**
| 方法 | 相关文档/脚本 |
|------|---------------|
| 量纲分析 | `claude_full_analysis.md` |
| 实验设计 | `papers/Aristoff_etal_2008_Water_entry_spheres.pdf` |
| CFD模拟 | `latest_theory_supplement.md` |
| 论文下载 | `scripts/download_all_papers.py` |
| 对话提取 | `scripts/extract_latest_deepseek.py` |

---

## 📈 文档发展历史

### **Phase 1: 对话提取** (2026-03-04)
- ✅ 提取Claude对话
- ✅ 提取DeepSeek对话
- ✅ 生成分析文档

### **Phase 2: 论文收集** (2026-03-05)
- ✅ 搜索arXiv论文
- ✅ 下载8篇核心论文
- ✅ 整理引用信息

### **Phase 3: 理论深化** (2026-03-05)
- ✅ 提取最新理论补充
- ✅ 分析水槽尺寸效应
- ✅ 扩展无量纲框架

### **Phase 4: 文档整合** (2026-03-05)
- ✅ 创建文档索引
- ✅ 整理脚本目录
- ✅ 编写README文档

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
2. claude_full_analysis.md
3. tank_size_effect_analysis.md
4. ai_analysis_comparison.md
5. PAPER_CITATIONS.md
6. papers/README.md
7. scripts/README.md
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

*最后更新: 2026-03-05*  
*版本: v1.0*  
*状态: 活跃维护中*