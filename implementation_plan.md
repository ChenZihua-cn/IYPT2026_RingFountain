# CFD仿真实现计划：金属环入水喷泉模拟

> **📊 进度总览**: 阶段1配置完成(95%)，阶段2配置完成(100%)，阶段3-5待开始 | **整体完成度**: ~40%
>
> **✅ 已完成**: 基础案例完整配置、监控输出配置、Python工具、自动化脚本、文档
>
> **⏳ 待进行**: 基础案例测试运行、参数扫描框架、验证研究、结果分析
>
> **⚠️ 重要**: 所有配置文件已创建但**未实际运行测试**，需要在OpenFOAM环境中验证

---

## 上下文与目标

本项目旨在构建一个完整的OpenFOAM CFD仿真框架，用于研究IYPT 2026第3题：当扁平金属环从高度H下落撞击水面时产生的喷泉现象。目标是确定喷泉最大高度$h_{max}$如何依赖于圆环参数（直径$D$、厚度$t$、下落高度$H$）。

### 问题的重要性
- **科学价值**：理解复杂流固耦合过程中的能量转换机制
- **工程应用**：为入水冲击、空泡动力学、喷雾形成等提供理论指导
- **验证理论**：验证基于Gekle & Gordillo (2009)空腔坍缩理论的修正标度律

### 现有基础
1. **理论框架**：`theory.md`中完整的无量纲分析和物理模型
2. **OpenFOAM案例模板**：`disk_impact/`和`disk_entry/`提供基础配置
3. **验证数据**：Gekle & Gordillo (2010)实验数据用于CFD验证
4. **实验设计**：`experiments.md`提供实验参数范围和测量方法

## 技术决策（基于用户选择）

### 几何建模：3D全模型
- **理由**：捕捉可能的非对称效应，提供更真实的物理模拟
- **方法**：使用snappyHexMesh + STL圆环几何
- **替代路径**：可先开发2D轴对称版本进行快速验证

### 求解器策略：overInterDyMFoam（重叠网格）
- **理由**：处理大位移运动时网格质量保持良好，避免变形问题
- **优势**：圆环作为独立网格组件嵌入背景网格，运动稳定
- **配置复杂性**：中等，需要设置重叠网格区域和插值

### 参数研究：完整参数扫描
- **范围**：直径$D$（3水平）× 厚度比$t/D$（3水平）× 下落高度$H$（5水平）= 45个案例
- **目标**：系统研究参数影响，建立经验关系式$\frac{h_{max}}{D} = f(Fr, We, \eta)$
- **计算成本**：约90天串行时间，可通过并行化减少到9天（10节点）

## 实施方案

### 阶段1：基础案例开发（2周）

> **✅ 状态**: 配置文件已创建完成，待实际运行测试
> **完成度**: 95%
> **已创建文件**: 20+个配置文件，包括所有必需的system/constant/0目录文件
> **⚠️ 待验证**: 需要在OpenFOAM环境中实际运行以验证配置正确性

#### 1.1 几何创建
**关键文件**：
- ✅ `ring_fountain/base_case/constant/triSurface/ring.stl` - 圆环几何文件 **(已生成)**
- ✅ `ring_fountain/base_case/system/blockMeshDict` - 背景网格定义 **(已配置)**
- ✅ `ring_fountain/base_case/system/snappyHexMeshDict` - 局部网格细化 **(已配置)**
- ✅ `ring_fountain/base_case/system/topoSetDict` - 细胞区域定义 **(已配置)**

**圆环STL生成参数**：
- 外径$R$ = $D/2$
- 内径$r$ = $(D-2t)/2$
- 宽度$w$ = 常数（如0.01m）
- ✅ 使用Python脚本生成：`scripts/generate_ring_stl.py` **(已实现)**

#### 1.2 物理模型配置

> **✅ 状态**: 已完成

**关键文件**：
- ✅ `ring_fountain/base_case/constant/phaseProperties` - 水-空气两相 **(已配置)**
- ✅ `ring_fountain/base_case/constant/physicalProperties.*` - 物性参数 **(已配置)**
- ✅ `ring_fountain/base_case/constant/momentumTransport` - k-ω SST **(已配置)**
- ✅ `ring_fountain/base_case/constant/g` - 重力场 **(已配置)**

**物性参数**：
```
水：ρ=1000 kg/m³, ν=1e-6 m²/s
空气：ρ=1.2 kg/m³, ν=1.48e-5 m²/s
表面张力：σ=0.07 N/m
```

#### 1.3 重叠网格配置

> **✅ 状态**: 已完成配置，待实际运行验证

**关键文件**：
- ✅ `ring_fountain/base_case/constant/dynamicMeshDict` - 动网格设置 **(已配置)**
- ✅ `ring_fountain/base_case/constant/sixDoFRigidBodyMotion/` - 六自由度配置 **(已配置)**
- ✅ `ring_fountain/base_case/system/fvSolution` - 重叠网格求解器设置 **(已配置)**

**关键配置**：
```cpp
// dynamicMeshDict
dynamicFvMesh   dynamicOversetFvMesh;
solver          overInterDyMFoam;

// 六自由度运动
sixDoFRigidBodyMotionCoeffs {
    patches     (ringSurface);
    innerDistance 0.05;
    outerDistance 0.35;
    mass        m_ring;  // 圆环质量
    centreOfMass (0 0 0.1);  // 初始位置（水面以上）
    restraints {
        gravity {
            type    gravity;
            g       (0 0 -9.81);
        }
    }
}
```

#### 1.4 初始条件与边界条件

> **✅ 状态**: 已完成配置

**关键文件**：
- ✅ `ring_fountain/base_case/0/U` - 速度场 **(已配置)**
- ✅ `ring_fountain/base_case/0/p_rgh` - 修正压力 **(已配置)**
- ✅ `ring_fountain/base_case/0/alpha.water` - 水体积分数 **(已配置)**
- ✅ `ring_fountain/base_case/0/k, omega, nut` - 湍流变量 **(已配置)**
- ✅ `ring_fountain/base_case/system/setFieldsDict` - 初始场设置 **(已配置)**

**初始条件**：
- 圆环速度：$\mathbf{U}_{ring} = (0, 0, -\sqrt{2gH})$
- 流体速度：$\mathbf{U} = 0$
- 相分数：$z<0$时$\alpha=1$（水），$z>0$时$\alpha=0$（空气）
- 压力：静水压力分布

### 阶段2：监控与输出配置（1周）

> **✅ 状态**: 已完成配置
> **完成度**: 100%
> **说明**: 在controlDict中已配置所有函数对象

#### 2.1 喷泉高度提取

> **✅ 方法1**: 探针点阵列 - 已在controlDict中配置10个探针点
> **✅ 方法2**: 自由表面提取 - 已在controlDict中配置surfaces函数对象
**方法1：探针点阵列**
```cpp
// system/probes
probeLocations (
    (0 0 0.1) (0 0 0.2) (0 0 0.3)  // 垂直阵列
    // ... 更多高度点
);
fields (alpha.water);
writeInterval 0.001;
```

**方法2：自由表面提取**
```cpp
// system/surfaces
isoSurfaceField alpha.water;
isoSurfaceValue 0.5;
```

#### 2.2 力和运动数据

> **✅ 状态**: 已在controlDict中配置

```cpp
// ✅ system/controlDict中已配置forces函数对象
patches (ringSurface);
writeControl timeStep;

// ✅ system/controlDict中已配置sixDoFRigidBodyState函数对象
writeInterval 1;
```

### 阶段3：参数化框架开发（2周）

> **⏳ 状态**: 未开始 (0%)
> **说明**: 需要等待基础案例验证成功后开始开发
> **预计开始时间**: 基础案例测试运行成功后

#### 3.1 参数扫描脚本
**⏳ 待创建主脚本**：`parametric_study/scripts/run_parameter_sweep.py`
```python
参数范围：
- D: [0.05, 0.1, 0.2] m
- t/D: [0.01, 0.05, 0.1]
- H: [0.1, 0.2, 0.5, 1.0, 2.0] m
```

**案例生成逻辑**：
1. 复制基础案例模板
2. 修改几何参数（STL生成 + 网格重生成）
3. 更新初始条件（速度、位置）
4. 更新物性参数（质量、惯性矩）

#### 3.2 自动化运行管道
```python
for D in diameters:
    for t in thicknesses:
        for H in heights:
            case_dir = generate_case(D, t, H)
            run_openfoam_case(case_dir, n_cores=8)
            extract_results(case_dir)
```

### 阶段4：验证与确认（2周）

> **⏳ 状态**: 未开始 (0%)
> **说明**: 需要基础案例成功运行并产生初步结果后开始
> **预计开始时间**: 基础案例验证完成后

#### 4.1 网格收敛性研究
**网格级别**：
- 粗：$\Delta x \approx D/20$, ~100k单元
- 中：$\Delta x \approx D/40$, ~500k单元
- 细：$\Delta x \approx D/80$, ~2M单元

**收敛准则**：喷泉高度变化<5%

#### 4.2 时间步长独立性
**时间步长**：$1\times10^{-4}$, $5\times10^{-5}$, $2\times10^{-5}$ s
**CFL条件**：$CFL = U\Delta t/\Delta x < 1$

#### 4.3 文献数据对比
**对比基准**：Gekle & Gordillo (2010)圆盘入水数据
**对比指标**：
- 空腔形状演化
- 气泡环形成时间
- 喷泉高度与速度关系

### 阶段5：结果分析与报告（1周）

> **⏳ 状态**: 未开始 (0%)
> **说明**: 需要参数扫描完成后进行
> **预计开始时间**: 获得45个案例数据后

#### 5.1 数据收集与处理
**⏳ 待创建脚本**：`parametric_study/scripts/collect_results.py`
**输出**：`results/processed/all_results.csv`

#### 5.2 标度律拟合
**目标公式**：$\frac{h_{max}}{D} = C \cdot Fr^a \cdot We^b \cdot \eta^c$
**拟合方法**：多元非线性回归
**验证**：与理论预测和实验数据对比

## 关键文件修改清单

### 从现有disk_impact案例继承的文件
1. **[disk_impact/system/controlDict](disk_impact/system/controlDict)**
   - 修改：`application`改为`overInterDyMFoam`
   - 修改：`endTime`延长到1.0s（完整喷泉演化）
   - 修改：`deltaT`减小到$1\times10^{-4}$ s
   - 添加：`probes`和`surfaces`函数对象

2. **[disk_impact/system/fvSchemes](disk_impact/system/fvSchemes)**
   - 保持：现有离散格式
   - 添加：重叠网格插值格式

3. **[disk_impact/constant/momentumTransport](disk_impact/constant/momentumTransport)**
   - 修改：湍流模型改为k-ω SST

### 需要创建的新文件

#### ✅ 已完成 (阶段1-2)

1. ✅ **`ring_fountain/base_case/constant/dynamicMeshDict`** - 动网格配置 **(已创建)**
2. ✅ **`ring_fountain/base_case/system/snappyHexMeshDict`** - 网格细化 **(已创建)**
3. ✅ **`ring_fountain/base_case/system/topoSetDict`** - 区域定义 **(已创建)**
4. ✅ **`ring_fountain/base_case/system/blockMeshDict`** - 背景网格 **(已创建)**
5. ✅ **`ring_fountain/base_case/0/*`** - 所有初始条件文件 **(已创建)**
6. ✅ **`ring_fountain/base_case/constant/triSurface/ring.stl`** - 圆环几何 **(已生成)**
7. ✅ **`ring_fountain/base_case/Allrun`** - 运行脚本 **(已创建)**
8. ✅ **`ring_fountain/base_case/Allclean`** - 清理脚本 **(已创建)**
9. ✅ **`ring_fountain/base_case/README.md`** - 使用说明 **(已创建)**
10. ✅ **`scripts/generate_ring_stl.py`** - STL生成工具 **(已创建)**

> **注意**: controlDict中已配置probes、surfaces、forces、sixDoFRigidBodyState等函数对象，无需单独文件

#### ⏳ 待完成 (阶段3-5)

1. ⏳ **`parametric_study/scripts/run_parameter_sweep.py`** - 自动化参数扫描主脚本
2. ⏳ **`parametric_study/scripts/extract_fountain_height.py`** - 喷泉高度提取脚本
3. ⏳ **`parametric_study/scripts/collect_results.py`** - 结果汇总脚本
4. ⏳ **`parametric_study/scripts/plot_scaling_law.py`** - 标度律可视化脚本

## 技术挑战与解决方案

### 挑战1：重叠网格配置复杂性
**解决方案**：
1. 先创建简单的验证案例（圆球入水）
2. 逐步添加复杂性（圆盘→圆环）
3. 使用OpenFOAM教程案例作为参考

### 挑战2：数值不稳定（界面振荡）
**解决方案**：
1. 启用界面压缩：`interfaceCompression`项
2. 限制时间步长：$CFL < 0.5$
3. 使用MULES格式进行相分数输运

### 挑战3：计算资源需求高
**解决方案**：
1. 并行计算：8核并行，减少计算时间约6-8倍
2. 自适应时间步长：动态调整保持CFL稳定
3. 分阶段网格细化：先在粗网格上验证物理模型

### 挑战4：喷泉高度精确提取
**解决方案**：
1. 多方法验证：探针点 + 自由表面提取 + 图像处理
2. 高时间分辨率：输出间隔0.001s
3. 后处理算法：智能识别水柱前锋

## 验证策略

### 内部验证
1. **网格收敛性**：三个网格级别对比
2. **时间步长独立性**：三个时间步长对比
3. **质量守恒**：检查相分数总量变化
4. **能量平衡**：计算能量转换效率

### 外部验证
1. **文献对比**：Gekle & Gordillo (2010)圆盘入水数据
2. **理论验证**：动量/能量守恒检查
3. **趋势验证**：参数影响趋势是否物理合理

### 不确定性量化
1. **数值误差**：基于网格和时间步长收敛性估计
2. **建模误差**：湍流模型、表面张力模型影响
3. **参数不确定性**：物性参数变化影响

## 预期成果

### 计算成果
1. **参数数据库**：45个案例的完整仿真结果
2. **标度律关系**：$\frac{h_{max}}{D} = f(Fr, We, \eta)$经验公式
3. **验证报告**：CFD与理论/实验对比分析

### 可视化成果
1. **动画视频**：喷泉形成全过程
2. **关键帧图像**：入水冲击、空腔演化、气泡环形成、喷泉喷射
3. **参数影响图**：$h_{max}$随$D$, $t$, $H$变化曲线

### 文档成果
1. **技术报告**：CFD方法、结果、分析
2. **用户指南**：如何运行和扩展仿真
3. **数据存档**：原始和处理后数据

## 成功标准

### 技术成功标准
1. ✅ 案例成功运行到物理时间1.0s
2. ✅ 网格收敛性验证通过（误差<5%）
3. ✅ 时间步长独立性验证通过
4. ✅ 与Gekle & Gordillo数据对比误差<15%

### 科学成功标准
1. ✅ 获得物理合理的喷泉高度数据
2. ✅ 建立经验标度律关系式
3. ✅ 验证修正标度律预测
4. ✅ 揭示关键参数影响机制

## 时间表与里程碑

| 阶段 | 时间 | 里程碑 | 可交付物 |
|------|------|--------|----------|
| 阶段1 | 第1-2周 | 基础案例运行成功 | 可运行的base_case |
| 阶段2 | 第3周 | 喷泉高度提取验证 | 监控配置和提取脚本 |
| 阶段3 | 第4-5周 | 参数扫描框架完成 | 自动化脚本系统 |
| 阶段4 | 第6-7周 | 验证与确认完成 | 验证报告和误差分析 |
| 阶段5 | 第8周 | 最终结果分析 | 标度律关系和完整报告 |

## 资源需求

### 计算资源
- **单次模拟**：500k-2M网格，24-72小时（8核并行）
- **参数扫描**：45案例，~90天串行，~9天并行（10节点）
- **存储需求**：50-100 GB/案例，总计2-4 TB

### 软件环境
- **OpenFOAM版本**：v12（基金会版）或v2412（OpenCFD版）
- **WSL配置**：内存≥16GB，处理器≥8核
- **Python环境**：NumPy, Pandas, Matplotlib, VTK

### 人力投入
- **CFD专家**：主导技术实施（主要角色）
- **物理分析师**：结果解释和理论对比
1. **脚本开发**：自动化框架开发

## 风险与缓解

### 技术风险
1. **重叠网格配置失败**
   - **缓解**：先使用interDyMFoam作为备用方案
   - **缓解**：从简单几何开始逐步复杂化

2. **数值发散或不稳定**
   - **缓解**：逐步增加复杂性（静态→动网格→重叠网格）
   - **缓解**：使用更稳定的数值格式和更小的时间步长

3. **计算时间超出预期**
   - **缓解**：先在粗网格上验证，再细化网格
   - **缓解**：使用更多计算节点并行

### 科学风险
1. **物理模型不准确**
   - **缓解**：与文献数据系统对比验证
   - **缓解**：进行敏感性分析识别关键参数

2. **参数范围选择不当**
   - **缓解**：基于理论分析选择物理相关范围
   - **缓解**：先进行小规模探索性研究

## 扩展性与未来工作

### 短期扩展
1. **表面张力影响**：添加表面活性剂模拟
2. **非轴对称效应**：研究倾斜入水或旋转效应
3. **尺度效应**：扩展到不同尺度范围

### 长期扩展
1. **多相流扩展**：考虑蒸汽相（空化效应）
2. **结构响应**：柔性圆环变形耦合
3. **优化设计**：寻找最大化喷泉高度的几何参数

## 结论

本计划提供了一个系统、可行的OpenFOAM CFD仿真实施方案，用于研究金属环入水喷泉现象。方案基于现有的`disk_impact`案例模板，采用先进的overInterDyMFoam重叠网格技术，实现真实的3D流固耦合模拟。通过完整的参数扫描和严格的验证策略，计划将产生可靠的CFD数据，用于验证理论模型、指导实验设计，并最终回答喷泉高度对圆环参数的依赖关系这一核心科学问题。

实施这个计划需要约8周时间和中等规模的计算资源，但将产生高质量的科学研究成果，为IYPT 2026第3题提供深入的数值模拟支持。

---

## 📊 实施状态详细说明

### ✅ 已完成工作总结 (2026-03-06)

#### 1. 基础案例完整配置 ✅ (95%)

**已创建的文件结构**:
```
ring_fountain/base_case/
├── 0/                          # ✅ 初始条件 (6个文件)
│   ├── U                        # 速度场
│   ├── p_rgh                    # 修正压力
│   ├── alpha.water              # 水体积分数
│   ├── k                        # 湍流动能
│   ├── omega                    # 比耗散率
│   └── nut                      # 湍流粘度
├── constant/
│   ├── triSurface/
│   │   └── ring.stl             # ✅ 圆环几何 (已生成)
│   ├── dynamicMeshDict          # ✅ 动网格配置
│   ├── sixDoFRigidBodyMotion/
│   │   ├── restraints           # ✅ 运动约束
│   │   └── state                # ✅ 初始状态
│   ├── phaseProperties          # ✅ 相属性
│   ├── physicalProperties.water # ✅ 水物性
│   ├── physicalProperties.air   # ✅ 空气物性
│   ├── momentumTransport         # ✅ k-ω SST
│   └── g                        # ✅ 重力场
├── system/
│   ├── controlDict              # ✅ 求解器+监控配置
│   ├── fvSchemes                # ✅ 离散格式
│   ├── fvSolution               # ✅ 求解器设置
│   ├── blockMeshDict            # ✅ 背景网格
│   ├── snappyHexMeshDict        # ✅ 网格细化
│   ├── topoSetDict              # ✅ 区域选择
│   ├── decomposeParDict         # ✅ 并行分解
│   └── setFieldsDict            # ✅ 初始场设置
├── Allrun                       # ✅ 自动运行脚本
├── Allclean                     # ✅ 清理脚本
└── README.md                    # ✅ 使用说明
```

**总计**: 已创建 20+ 个配置文件

#### 2. Python工具开发 ✅ (100%)

- ✅ `scripts/generate_ring_stl.py`: 参数化生成圆环STL几何
  - 支持自定义D, t, w, center, resolution
  - 输出标准ASCII STL格式
  - 已生成默认圆环(D=0.1m)

#### 3. 自动化脚本 ✅ (100%)

- ✅ `Allrun`: 完整的自动化运行流程
  - 网格生成 → 细化 → 初始条件 → 求解器 → 后处理
  - 包含错误检查和状态输出

- ✅ `Allclean`: 清理脚本

#### 4. 监控与输出配置 ✅ (100%)

在controlDict中配置的函数对象:
- ✅ probes: 10个探针点 (z=0.05m至0.5m，间隔0.05m)
- ✅ fountainSurface: 自由表面提取 (α=0.5等值面)
- ✅ forces: 流体作用力监控
- ✅ sixDoFRigidBodyState: 圆环运动数据

#### 5. 文档完成 ✅ (100%)

- ✅ `implementation_plan.md`: 实施计划 (本文档)
- ✅ `ring_fountain/base_case/README.md`: 案例使用说明

### ⏳ 待完成工作 (优先级排序)

#### 🔴 高优先级 - 本周必须完成

1. **基础案例测试运行** ⏳
   - 在OpenFOAM环境中执行`./Allrun`
   - 诊断并修复配置错误
   - 验证案例能运行到endTime=1.0s
   - 提取初步的h_max数据
   - 预计时间: 1-2天

2. **初步结果验证** ⏳
   - ParaView可视化检查
   - 确认圆环下落、撞击、空腔形成、喷泉喷射
   - 与理论趋势对比(量级检查)
   - 预计时间: 0.5天

#### 🟡 中优先级 - 本月完成

3. **配置调优** ⏳
   - 根据初步结果调整参数
   - 优化数值稳定性
   - 调整监控配置
   - 预计时间: 1-2天

4. **网格收敛性研究** ⏳
   - 三个网格级别对比
   - 验证h_max收敛性
   - 预计时间: 3-5天

5. **时间步长独立性** ⏳
   - 三个时间步长对比
   - 验证数值精度
   - 预计时间: 2-3天

#### 🟢 低优先级 - 后续完成

6. **参数扫描框架开发** ⏳ (预计1周)
   - run_parameter_sweep.py
   - 案例管理系统

7. **批量计算** ⏳ (预计1-3周)
   - 45个参数组合
   - 并行计算优化

8. **深入分析** ⏳ (预计2-4周)
   - 标度律拟合
   - 技术报告
   - 可视化材料

### ⚠️ 重要说明与简化假设

#### 配置完成但未验证

所有配置文件已基于OpenFOAM标准和理论分析创建，但**未实际运行测试**。可能存在的问题:

**高风险区域**:
- 🔴 重叠网格(dynamicOversetFvMesh)配置可能需要调试
- 🔴 六自由度运动耦合稳定性未知
- 🟡 VOF界面追踪可能出现数值振荡
- 🟡 时间步长δt=0.0001s可能需要调整

**缓解策略**:
- 从粗网格开始验证
- 准备interDyMFoam作为备用方案
- 详细记录日志用于诊断

#### 简化假设 (为后续优化预留)

**几何简化**:
- 使用简单六面体背景网格(非圆柱形)
- 未实现边界层网格(addLayers=false)
- 圆环为完美几何(无加工误差)

**物理简化**:
- 未考虑空化效应
- 假设恒温(无热传递)
- 使用RANS湍流模型(非LES/DES)

**初始条件简化**:
- 流体完全静止
- 水面完全平整
- 圆环完全水平

这些简化在初步验证阶段是合理的，可在后续研究中逐步完善。

### 📋 下一步行动清单

**立即行动** (今天或明天):
- [ ] 在WSL中检查OpenFOAM环境
- [ ] 进入`ring_fountain/base_case/`目录
- [ ] 执行`./Allrun`开始测试运行
- [ ] 监控`log.overInterDyMFoam`查看求解器状态

**本周目标**:
- [ ] 基础案例成功运行到endTime
- [ ] 获得初步的h_max数据
- [ ] ParaView可视化验证

**本月目标**:
- [ ] 完成网格收敛性研究
- [ ] 完成时间步长独立性验证
- [ ] 与文献数据初步对比

---

**最后更新**: 2026-03-06
**当前状态**: 配置阶段完成，进入测试运行阶段