# Ring Fountain CFD Simulation - Base Case

## 概述

这个OpenFOAM案例模拟金属环从高度H自由下落撞击水面产生喷泉的物理过程。使用`overInterDyMFoam`求解器进行3D流固耦合模拟。

## 物理模型

- **求解器**: overInterDyMFoam (重叠网格 + VOF两相流 + 六自由度运动)
- **流体**: 水-空气两相流
- **湍流模型**: k-ω SST
- **运动**: 六自由度刚体运动（重力驱动）

## 几何参数

- **圆环**: 外径D=0.1m, 厚度t=0.005m, 宽度w=0.01m
- **计算域**: 0.5m × 0.5m × 1.0m (长×宽×高)
- **水深**: 0.5m
- **下落高度**: H=0.2m

## 运行说明

### 前提条件

1. 安装OpenFOAM (v12或v2412)
   - 基金会版: `source /opt/openfoam12/etc/bashrc`
   - OpenCFD版: `source /usr/lib/openfoam/openfoam2412/etc/bashrc`

2. 确保Python可用（用于生成STL几何）

### 运行步骤

在WSL或Linux终端中：

```bash
# 1. 进入案例目录
cd ring_fountain/base_case

# 2. (可选) 修改圆环参数
# 编辑 ../../scripts/generate_ring_stl.py 中的参数

# 3. 运行仿真
./Allrun

# 4. 后处理
paraFoam  # 打开ParaView可视化
```

### 手动运行（逐步）

如果需要手动控制每个步骤：

```bash
# 1. 生成背景网格
blockMesh

# 2. 生成圆环STL几何
python ../../scripts/generate_ring_stl.py
mv ring.stl constant/triSurface/

# 3. 网格细化
snappyHexMesh -overwrite

# 4. 设置初始条件
setFields

# 5. 并行分解（可选）
decomposePar

# 6. 运行求解器（串行）
overInterDyMFoam

# 或并行运行（4核）
mpirun -np 4 overInterDyMFoam -parallel
reconstructPar
```

### 清理案例

```bash
./Allclean
```

## 输出结果

### 时间目录
- `0/`, `0.001/`, `0.002/`, ..., `1.0/`: 各时间步的场文件

### 关键文件
- `U`: 速度场
- `p_rgh`: 修正压力
- `alpha.water`: 水的体积分数
- `k`, `omega`: 湍流量

### 监控数据
- `postProcessing/probes/`: 探针点数据（喷泉高度）
- `postProcessing/forces/`: 流体作用力
- `postProcessing/sixDoFRigidBodyState/`: 圆环运动数据

### 日志文件
- `log.blockMesh`: 网格生成日志
- `log.snappyHexMesh`: 网格细化日志
- `log.overInterDyMFoam`: 求解器日志

## 可视化

### ParaView

```bash
paraFoam
```

在ParaView中：
1. 打开案例
2. 查看alpha.water等值面（α=0.5）显示自由表面
3. 查看速度矢量、压力分布
4. 创建动画

### 喷泉高度提取

探针点数据在`postProcessing/probes/`目录。使用Python处理：

```python
import pandas as pd
import matplotlib.pyplot as plt

# 读取探针数据
data = pd.read_csv('postProcessing/probes/0/probeInfo.csv', skiprows=range(10))

# 绘制不同高度的时间序列
# ...
```

## 参数修改

### 修改圆环几何

编辑`../../scripts/generate_ring_stl.py`：

```python
D = 0.1      # 外径 [m]
t = 0.005    # 厚度 [m]
w = 0.01     # 宽度 [m]
```

### 修改初始条件

编辑`constant/sixDoFRigidBodyMotion/state`：

```cpp
centreOfMass    (0 0 0.55);      // 初始位置
velocity        (0 0 -1.98);     // 初始速度
mass            0.117;            // 质量
```

### 修改仿真参数

编辑`system/controlDict`：

```cpp
endTime 1.0;     // 仿真结束时间
deltaT  0.0001;  // 时间步长
```

## 故障排除

### 问题1: blockMesh失败
**检查**: 几何定义是否正确
**解决**: 查看`log.blockMesh`中的错误信息

### 问题2: snappyHexMesh失败
**检查**: STL文件是否存在且有效
**解决**: 使用Python脚本重新生成STL

### 问题3: 求解器发散
**检查**: 时间步长是否过小
**解决**: 减小`deltaT`或调整`maxCo`

### 问题4: 内存不足
**检查**: 网格是否过大
**解决**: 减小网格尺寸或增加系统内存

## 验证

### 与理论对比

将CFD结果与理论预测对比：

1. **喷泉高度**: 理论 h_max ∝ H
2. **无量纲关系**: h_max/D = f(Fr, We, η)

### 与实验对比

与Gekle & Gordillo (2010)数据对比：
- 空腔形状演化
- 喷射速度
- 气泡环形成时间

## 后续工作

1. **参数扫描**: 修改圆环D、t、H参数
2. **网格收敛性**: 测试不同网格尺寸
3. **时间步独立性**: 验证数值精度
4. **标度律拟合**: 从数据提取h_max(D, t, H)关系

## 参考资料

- `implementation_plan.md`: 详细实施计划
- `theory.md`: 理论推导
- `experiments.md`: 实验设计
- `prompt.md`: CFD构建指南
- `openfoam_guide.md`: OpenFOAM使用指南

## 联系方式

如有问题，请查看项目文档或联系开发团队。

---

*Last updated: 2026-03-06*