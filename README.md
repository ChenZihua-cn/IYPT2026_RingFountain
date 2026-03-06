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

- **弗劳德数**：$Fr = V/\sqrt{gD}$（惯性力/重力）
- **韦伯数**：$We = \rho V^2 D/\sigma$（惯性力/表面张力）
- **邦德数**：$Bo = \rho g D^2/\sigma$（重力/表面张力）
- **厚径比**：$t/D$（圆环厚度/直径）

喷泉高度的无量纲关系：
$$\frac{h_{fountain}}{D} = f\left(Fr, We, Bo, \frac{t}{D}\right)$$

## 文件结构

```
IYPT2026_RingFountain/
├── README.md                          # 本文件
├── theory.md                          # 理论推导文档
├── experiments.md                     # 实验设计方案
├── openfoam_guide.md                  # OpenFOAM使用指南
├── simulations/                       # OpenFOAM模拟案例
│   ├── case1_disk_entry/              # 圆盘入水（简化验证）
│   ├── case2_ring_entry/              # 圆环入水（主体）
│   └── case3_parameter_sweep/         # 参数扫描
├── scripts/                           # 前后处理脚本
│   ├── preprocess.py                  # 网格生成脚本
│   ├── postprocess.py                 # 结果分析脚本
│   └── plot_results.m                 # MATLAB绘图
├── docs/                              # 参考资料
│   └── papers/                        # 相关论文
└── data/                              # 实验数据和模拟结果
    ├── experimental/                  # 实验数据
    └── simulation/                    # 模拟结果
```

## WSL和OpenFOAM配置

### 项目路径

```bash
# Windows路径
C:\Users\30856\Desktop\IYPT2026_RingFountain

# WSL路径（通过符号链接）
~/ringfountain

# 或者完整路径
/mnt/c/Users/30856/Desktop/IYPT2026_RingFountain
```

### OpenFOAM版本切换

```bash
# 基金会版 OpenFOAM 12
openfoam12

# OpenCFD版 OpenFOAM 2412
openfoam2412
```

### 快速开始

```bash
# 进入项目目录
cd ~/ringfountain

# 激活OpenFOAM（选择一个版本）
openfoam2412

# 查看案例
ls simulations/

# 运行案例
cd simulations/case1_disk_entry
./Allrun
```

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

### 工具
- **OpenFOAM**: CFD模拟
- **ParaView**: 后处理可视化
- **Python/MATLAB**: 数据分析

## 联系方式

- 项目创建：2026-03-02
- 最后更新：2026-03-06

---

*Physics is not about clever answers, but about disciplined reasoning constrained by reality.*
