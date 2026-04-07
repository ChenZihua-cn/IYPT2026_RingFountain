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

## 文件结构（简洁架构）

```
ringfountain/
├── README.md              # 项目说明
├── cases/                 # 模拟案例
│   ├── disk_impact/       # 圆盘冲击
│   ├── disk_entry/        # 圆盘入水
│   └── ring_entry/        # 圆环入水（主案例）
├── scripts/               # 工具脚本
│   ├── preprocessing/     # 预处理
│   ├── postprocessing/    # 后处理
│   └── utilities/         # 实用工具
├── docs/                  # 文档
│   ├── theory.md          # 理论推导
│   └── openfoam_guide.md  # OpenFOAM指南
└── data/                  # 数据
    ├── experimental/      # 实验数据
    └── simulation/        # 模拟结果
```

### 核心目录说明

- **cases/**：OpenFOAM模拟案例，每个案例包含完整的配置（0/, constant/, system/）
- **scripts/**：Python脚本，用于网格生成、结果分析和可视化
- **docs/**：项目文档，包括理论背景和软件使用指南
- **data/**：输入输出数据，保持原始数据和处理后的数据分离

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

# 3. 运行圆盘冲击案例
cd cases/disk_impact
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

## 案例设置与求解器选择

### 控制方程（引用自 Theory.md）

Ring Fountain问题涉及水和空气的两相流动以及金属环的运动。控制方程由**流体动力学方程**和**刚体六自由度运动方程**组成。

#### 1.1 流体动力学方程
采用不可压缩Navier-Stokes方程结合VOF方法：

- **连续性方程**：
  \[
  \nabla \cdot \mathbf{U} = 0
  \]

- **动量方程**：
  \[
  \frac{\partial \rho \mathbf{U}}{\partial t} + \nabla \cdot (\rho \mathbf{U} \mathbf{U}) = -\nabla p^* + \nabla \cdot \left[ \mu_{eff} (\nabla \mathbf{U} + \nabla \mathbf{U}^T) \right] + \rho \mathbf{g} + \mathbf{f}_{\sigma} + \mathbf{f}_{FSI}
  \]
  其中 $\rho$ 和 $\mu$ 是体积分数加权的混合密度和动力粘度。

- **相分数输运方程（VOF）**：
  \[
  \frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{U}) + \nabla \cdot [\mathbf{U}_c \alpha (1-\alpha)] = 0
  \]
  其中 $\alpha$ 是水的体积分数（$\alpha=1$ 为水，$\alpha=0$ 为空气）。

#### 1.2 刚体运动方程
金属环被视为刚体，受重力和流体压力作用：

- **平动**：
  \[
  m \frac{d \mathbf{U}_{rigid}}{dt} = m\mathbf{g} + \oint_{S} (-p\mathbf{n} + \boldsymbol{\tau} \cdot \mathbf{n}) dS + \mathbf{F}_{contact}
  \]

- **转动**：
  \[
  \mathbf{I} \frac{d \boldsymbol{\omega}}{dt} = \oint_{S} (\mathbf{r} \times (-p\mathbf{n} + \boldsymbol{\tau} \cdot \mathbf{n})) dS
  \]

### 求解器策略

#### 推荐求解器（OpenFOAM Foundation版v12）
对于Ring Fountain问题，推荐以下求解器：

1. **`interFoam`**（首选）
   - **适用**：两相不可压缩流动，VOF方法追踪界面
   - **特点**：开源稳定，文档丰富，适合自由表面流动
   - **命令**：`interFoam`

2. **`overInterDyMFoam`**
   - **适用**：动网格 + 多相流，适合物体运动
   - **特点**：支持动网格，可以模拟圆环入水过程
   - **命令**：`overInterDyMFoam`

3. **`multiphaseInterFoam`**
   - **适用**：多相流（超过两相）
   - **特点**：支持三相及以上，如果有空气-水-蒸汽需要考虑
   - **命令**：`multiphaseInterFoam`

#### 求解器选择建议
- **初学者**：从`interFoam`开始，运行简化案例
- **完整模拟**：使用`overInterDyMFoam`进行流固耦合模拟
- **高级用户**：根据具体需求选择或自定义求解器

### 计算域与边界条件

#### 计算域设置
- **几何**：圆柱形区域，分为空气和水两部分
- **初始相分布**：下半部分设为水 ($\alpha=1$)，上半部分设为空气 ($\alpha=0$)
- **初始场**：
  - 圆环初始位置：高于水面一个小距离
  - 初始速度：$U_{ring} = \sqrt{2gh}$（下落高度 $h$）
  - 压力场：依据静水压力分布初始化

#### 边界条件示例（重叠网格策略）
```cpp
// 0/U (速度场)
boundaryField {
    inlet {
        type            fixedValue;
        value           uniform (0 0 -V);  // 向下速度
    }
    outlet {
        type            pressureInletOutletVelocity;
        value           uniform (0 0 0);
    }
    walls {
        type            noSlip;  // 无滑移壁面
    }
}

// 0/alpha.water (体积分数)
boundaryField {
    inlet {
        type            fixedValue;
        value           uniform 0;  // 空气入口（圆环）
    }
    default {
        type            inletOutlet;
        inletValue      uniform 0;
        value           uniform 0;
    }
}
```

### 物性参数设置
编辑 `constant/transportProperties`：

```cpp
phases (water air);

water {
    transportModel  Newtonian;
    nu              1e-06;      // 运动粘度 [m^2/s]
    rho             1000;       // 密度 [kg/m^3]
}

air {
    transportModel  Newtonian;
    nu              1.48e-05;
    rho             1;
}

// 表面张力
sigma           0.07;           // 水-空气 [N/m]
```

### 几何参数定义
对于圆环入水问题，关键几何参数：
- `D`: 圆环直径 (m)
- `t`: 圆环厚度 (m)
- `H`: 下落高度 (m)
- `V = sqrt(2gH)`: 入水速度 (m/s)

### 输出控制
为测量喷泉高度，建议设置：

1. **探针点 (Probes)**：在圆环中心正上方不同高度设置探针，监控`alpha.water`
2. **自由表面提取**：提取 $\alpha = 0.5$ 的等值面，计算垂直方向最大 $z$ 坐标
3. **高时间分辨率**：入水瞬间和喷泉形成初期，每0.001秒输出一次

### 完整案例配置流程
1. **创建案例**：复制模板或现有案例
2. **修改几何**：调整`constant/polyMesh/blockMeshDict`中的尺寸
3. **设置物性**：编辑`constant/transportProperties`
4. **配置边界条件**：修改`0/`目录下的场文件
5. **设置求解器参数**：调整`system/fvSchemes`和`system/fvSolution`
6. **运行**：执行`./Allrun`或手动运行求解器

### 验证与调试
- **网格检查**：运行`checkMesh`验证网格质量
- **初始场检查**：使用`paraFoam`可视化初始条件
- **收敛性监控**：查看`log.interFoam`中的残差和连续性误差
- **结果验证**：与理论预测或实验数据对比

## 研究计划

### Phase 1: 理论分析（第1-2周）
- [ ] 建立无量纲参数关系
- [ ] 文献调研（arXiv水入冲击论文）
- [ ] 尺度律推导

### Phase 2: 数值模拟（第3-6周）
- [ ] 圆盘入水简化验证
- [ ] 圆环入水完整模拟
- [ ] 参数扫描（D, H, t）

### Phase 3: 实验验证（第7-8周）
- [ ] 搭建实验装置
- [ ] 高速摄影记录
- [ ] 数据对比分析

### Phase 4: 报告撰写（第9-10周）
- [ ] 结果整理
- [ ] 误差分析
- [ ] 报告生成

## 参考资源

### 关键论文
1. **Water entry of small disks, cones, or anything** (arXiv:2510.27622)
   - 统一尺度律预测空腔断裂模式
   
2. **Acoustic Signatures of Pinch-Off Cavities** (arXiv:2602.22761)
   - 空腔断裂动力学

3. **Cavity dynamics in water entry at low Froude numbers** (MIT)
   - 空腔动力学经典理论

### 工具与软件
- **OpenFOAM**: CFD模拟（Foundation版v12）
- **ParaView**: 后处理可视化
- **Python/MATLAB**: 数据分析
- **Git**: 版本控制

### 项目文档
- **理论推导**：`docs/theory.md` 或 `theory.md`
- **OpenFOAM指南**：`docs/openfoam_guide.md` 或 `openfoam_guide.md`
- **实验设计**：`docs/experiments.md` 或 `experiments.md`
- **完整文档索引**：`docs/DOCUMENTATION_INDEX.md`

### 学习资源
- **OpenFOAM官方教程**：`$FOAM_TUTORIALS`
- **多相流教程**：`$FOAM_TUTORIALS/multiphase/interFoam/`
- **推荐案例**：damBreak, damBreakWithObstacle, sloshingTank2D

### 在线资源
- **OpenFOAM文档**：https://www.openfoam.com/documentation
- **Foundation版Wiki**：https://openfoamwiki.net/
- **CFD在线论坛**：https://www.cfd-online.com/Forums/openfoam/

## 联系方式

- **项目创建**：2026-03-02
- **最后更新**：2026-04-07
- **项目维护**：研究团队
- **问题反馈**：通过GitHub Issues或直接联系维护者

### 更新日志
- **2026-04-07**：重建README，专注于OpenFOAM Foundation版v12
- **2026-03-06**：理论标度律修正更新
- **2026-03-05**：文档索引建立
- **2026-03-02**：项目初始化

### 贡献指南
欢迎通过以下方式贡献：
1. **报告问题**：提交GitHub Issue
2. **改进文档**：提交Pull Request更新文档
3. **添加功能**：扩展脚本或案例库
4. **分享数据**：提供实验或模拟数据用于验证

### 许可证
本项目文档采用开放许可，具体许可证信息请查看LICENSE文件（如存在）。

---

*Physics is not about clever answers, but about disciplined reasoning constrained by reality.*