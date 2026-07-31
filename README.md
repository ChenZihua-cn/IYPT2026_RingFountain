# IYPT 2026 Problem 3: Ring Fountain

## 项目简介

本项目研究**圆环喷泉**（Ring Fountain）现象，解决IYPT 2026第3题：

> "When a flat metal ring falls from a certain height into a water tank, it generates a fountain that can shoot water high into the air. How does the maximum height of the fountain depend on the ring's parameters?"

> 当扁平金属环从一定高度落入水箱时，会产生一个能将水喷射到高空的喷泉。喷泉的最大高度如何依赖于圆环的参数？

## 物理机制

Ring Fountain涉及复杂的流体力学过程：

1. **入水冲击**（Water Entry）：圆环撞击水面形成空腔
2. **空腔演化**（Cavity Dynamics）：圆环下沉拖曳形成轴对称空腔
3. **空腔断裂**（Pinch-off）：空腔壁面不稳定性导致断裂，形成气泡环
4. **气泡环上升**（Toroidal Bubble Rise）：气泡环在浮力作用下上升
5. **喷泉形成**（Fountain Formation）：气泡环到达水面破裂，释放能量形成喷泉

## 关键无量纲参数

### 基本无量纲数

- **弗劳德数**：$Fr = V/\sqrt{gD} = \sqrt{2H/D}$（惯性力/重力）
- **韦伯数**：$We = \rho V^2 D/\sigma$（惯性力/表面张力）
- **邦德数**：$Bo = \rho g D^2/\sigma$（重力/表面张力）
- **厚径比**：$\eta = t/D$（圆环几何形状参数）
- **内径比**：$\alpha = r/R$（圆环内径与外径之比）

### 喷泉高度的无量纲关系

根据白金汉π定理，喷泉高度可以表示为：

$$\boxed{\frac{h_{max}}{D} = f\left(Fr, We, Bo, \eta, \alpha\right)}$$

### 修正标度律（基于Gekle & Gordillo空腔坍缩理论）

基于空腔坍缩动力学的最新理论进展，喷泉高度的标度律修正为：

\[
h_{\text{max}} \propto \left(\frac{\rho_m}{\rho_w}\right)^2 \left(\frac{t}{R}\right)^2 \frac{(1-\alpha^2)^2}{[\gamma_0 + \gamma_1(1-\alpha)^p]^6} H
\]

其中：
- $\rho_m/\rho_w$：材料密度比（金属/水）
- $R = D/2$：圆环外半径
- $\gamma_0 > 0$：圆盘($\alpha=0$)基线值
- $\gamma_1 \ge 0$：内壁聚焦效应强度
- $p > 0$：聚焦效应变化速率

此修正消除了原模型在$\alpha \to 0$时的发散问题，确保实心盘有有限喷泉高度，并正确描述了内孔聚焦效应。

### 经验关系

对于初步估计，可采用以下经验关系：

$$\frac{h_{max}}{D} \sim Fr^a \cdot We^b \cdot \eta^c$$

其中指数 $a, b, c$ 需要通过实验或数值模拟确定。理论估计：$a \approx 1$（与入水速度平方成正比），$b < 0$（表面张力抑制喷泉），$c > 0$（厚圆环产生更大空腔）。

## 文件结构

```
ringfountain/
├── README.md              # 项目说明
├── CLAUDE.md              # AI agent 指导文件
├── cases/                 # OpenFOAM 模拟案例
│   ├── ring_entry/        # 圆环入水（主案例，6-DOF刚体运动）
│   └── ring_sweep/        # 参数扫描案例（已运行，数据存档）
├── scripts/               # 工具脚本
│   └── postprocessing/
│       └── check_data.py  # 模拟数据检验工具
├── docs/                  # 文档（理论分析、论文库、参考文献）
│   ├── Theory.md          # 理论推导与控制方程
│   ├── analysis/          # 理论分析文档（10篇）
│   ├── papers/            # 论文库（13篇PDF）
│   └── references/        # 参考文献与引用
└── data/                  # 实验与模拟数据（待建立）
```

The `cases/` directory contains two OpenFOAM cases:
- **ring_entry/** — FSI simulation using `rigidBodyMotion` (6-DOF rigid body coupled with VOF). Under active debugging for stability.
- **ring_sweep/base/** — Prescribed-motion simulation using `solidBody`/`linearMotion`. Completed successfully; validated reference case for cavity dynamics.

## OpenFOAM Foundation版v12配置与快速开始

### 环境要求
- **操作系统**：WSL2 (Ubuntu 20.04/22.04) 或 Linux
- **OpenFOAM版本**：Foundation版 v12
- **依赖工具**：git, python3, paraFoam (ParaView)

### 快速安装（WSL）
```bash
# 1. 安装OpenFOAM Foundation版v12
sudo apt-get update
sudo apt-get install -y openfoam12

# 2. 配置环境（添加到 ~/.bashrc）
echo "source /opt/openfoam12/etc/bashrc" >> ~/.bashrc
source ~/.bashrc

# 3. 验证安装
foamVersion  # 应显示 "OpenFOAM-12"
```

### 版本切换
```bash
# 使用配置的函数（如果已设置）
openfoam12          # 切换到Foundation版 OpenFOAM 12

# 或手动source
source /opt/openfoam12/etc/bashrc
```

### 快速开始（运行第一个案例）
```bash
# 1. 进入项目目录
cd ~/ringfountain

# 2. 激活OpenFOAM v12环境
openfoam12

# 3. 运行圆环入水案例
cd cases/ring_entry
./Allrun

# 4. 查看结果
paraFoam
```

### 验证环境
```bash
# 检查版本
foamVersion

# 查看环境变量
echo $WM_PROJECT_DIR    # 应显示 /opt/openfoam12
echo $FOAM_APPBIN       # 查看求解器路径

# 查看可用求解器
ls $FOAM_APPBIN | grep -i foam
```

### 常见问题
1. **命令未找到**：确保已正确source bashrc文件
2. **权限问题**：使用`sudo`安装，但运行案例时不需要
3. **路径错误**：检查`$WM_PROJECT_DIR`是否正确指向OpenFOAM 12

### 下一步
运行验证案例后，继续阅读"案例设置与求解器选择"部分，了解如何配置自己的模拟。

## 数值模拟方法

### 求解器

使用 OpenFOAM Foundation v12 模块化框架的 `foamRun -solver incompressibleVoF`（等价于传统 `interFoam`）进行两相 VOF 模拟。

### 动网格策略

两种方法，适应不同需求：

| 方法 | 配置 | 用途 |
|------|------|------|
| **FSI**（流固耦合）| `rigidBodyMotion` + Newmark + Pz-only 约束 | ring_entry：求解完整的刚体-流体耦合运动 |
| **Prescribed**（预设运动）| `solidBody` + `linearMotion` | ring_sweep：指定恒定速度，消除 FSI 不稳定性 |

FSI 方法通过 `dynamicMeshDict` 中 `accelerationRelaxation`（0.3）和 `accelerationDamping`（0.99）阻尼求解器振荡，但由于入水瞬间的力-加速度反馈环路，仍易出现 FPE 崩溃。

### 计算域

- **几何**：0.3×0.3×0.6 m 矩形域
- **网格局数**：~161K cells（20×20×40 六面体底网 × 2 加密，snappyHexMesh level 4–6 细化环面）
- **水深**：0.3 m（z=0 至 z=0.3）
- **环初始高度**：z = 0.35 m（水面以上 5 cm）

### 关键物理参数

| 参数 | 符号 | 值 |
|------|------|-----|
| 环外径 | D | 0.05 m |
| 环厚度 | t | 0.0025 m |
| 环宽度 | w | 0.01 m |
| 环质量 | m | 0.029 kg（钢，ρ=7800 kg/m³）|
| 表面张力 | σ | 0.07 N/m |
| 水密度/粘度 | ρ, ν | 1000 kg/m³, 1e-6 m²/s |
| 空气密度/粘度 | ρ, ν | 1 kg/m³, 1.48e-5 m²/s |

### 后处理与验证

```bash
# 探头数据（z=0.05–0.50m 跟踪 alpha.water、U、p_rgh）
ls postProcessing/probes/

# 环面受力
ls postProcessing/forces/

# 数据诊断脚本
python3 scripts/postprocessing/check_data.py          # ring_entry
python3 scripts/postprocessing/check_data.py -c ring_sweep/base
```

## 当前进展

- [x] 无量纲分析框建立：Fr, We, Bo, η, α 五个控制参数
- [x] 文献调研：13 篇论文，覆盖 Wagner 冲击理论、Worthington 射流、空腔动力学
- [x] ring_sweep/base 预设运动案例成功运行 — 空腔动力学已通过验证
- [ ] ring_entry FSI 稳定性调试（入水冲击 FPE 崩溃）
- [ ] 从 FSI 运行中提取环速度衰减曲线
- [ ] 自动参数扫描脚本（sweep.py）
- [ ] 喷泉高度标度律拟合
- [ ] 实验验证

## 参考资源

- **理论推导**：[docs/Theory.md](docs/Theory.md)
- **文档索引**：[docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)
- **论文库**：13 篇 PDF（`docs/papers/`），详见 [papers/README.md](docs/papers/README.md)
- **AGENTS.md**：扩展开发指南与论文引用
- **CLAUDE.md**：AI agent 快速参考
- **ring_entry README**：[cases/ring_entry/README.md](cases/ring_entry/README.md) — 已知问题与调试指南
- **ring_sweep README**：[cases/ring_sweep/README.md](cases/ring_sweep/README.md) — 参数扫描策略

## 更新日志

- **2026-07-31**：更新 README 以匹配实际求解器配置；标记实际完成进度
- **2026-04-07**：重建README，专注于OpenFOAM Foundation版v12
- **2026-03-06**：理论标度律修正更新
- **2026-03-02**：项目初始化

---

*Physics is not about clever answers, but about disciplined reasoning constrained by reality.*