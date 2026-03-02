# Ring Fountain 理论推导

## 1. 问题描述与物理图像

当扁平金属圆环从高度 $H$ 自由下落，以速度 $V$ 垂直撞击水面时，会产生一系列复杂的流体力学现象，最终形成向上喷射的喷泉。

### 1.1 完整物理过程

```
阶段1: 入水冲击
    圆环撞击水面 → 初始空腔形成
    
阶段2: 空腔演化
    圆环下沉 → 空腔拉长 → 壁面收缩
    
阶段3: 空腔断裂 (Pinch-off)
    空腔颈部收缩 → 气泡环脱离
    
阶段4: 气泡环上升
    气泡环在浮力作用下上升 → 自诱导涡环运动
    
阶段5: 喷泉形成
    气泡环到达水面破裂 → 能量释放 → 水柱喷射
```

## 2. 无量纲分析

### 2.1 相关物理量

**几何参数**:
- 圆环直径: $D$ [m]
- 圆环厚度: $t$ [m]
- 下落高度: $H$ [m]

**运动参数**:
- 入水速度: $V = \sqrt{2gH}$ [m/s]

**流体物性**:
- 水密度: $\rho$ [kg/m³]
- 空气密度: $\rho_a$ [kg/m³]
- 水的动力粘度: $\mu$ [Pa·s]
- 表面张力系数: $\sigma$ [N/m]
- 重力加速度: $g$ [m/s²]

**目标量**:
- 喷泉最大高度: $h_{max}$ [m]

### 2.2 无量纲数

#### 弗劳德数 (Froude Number)
$$Fr = \frac{V}{\sqrt{gD}} = \sqrt{\frac{2H}{D}}$$

**物理意义**: 惯性力与重力之比
- $Fr \ll 1$: 重力主导，缓慢入水
- $Fr \gg 1$: 惯性力主导，快速冲击

#### 韦伯数 (Weber Number)
$$We = \frac{\rho V^2 D}{\sigma}$$

**物理意义**: 惯性力与表面张力之比
- $We \ll 1$: 表面张力重要，空腔稳定
- $We \gg 1$: 惯性力主导，空腔不稳定

#### 邦德数 (Bond Number)
$$Bo = \frac{\rho g D^2}{\sigma}$$

**物理意义**: 重力与表面张力之比
- 仅依赖于几何和物性，与速度无关

#### 厚径比
$$\eta = \frac{t}{D}$$

**物理意义**: 圆环的几何形状参数

#### 密度比
$$\beta = \frac{\rho_a}{\rho} \approx 0.001$$

### 2.3 无量纲关系

根据白金汉π定理，喷泉高度可以表示为：

$$\boxed{\frac{h_{max}}{D} = f\left(Fr, We, Bo, \eta\right)}$$

或者等价地：

$$\frac{h_{max}}{D} = f\left(\frac{H}{D}, \frac{\rho V^2 D}{\sigma}, \frac{\rho g D^2}{\sigma}, \frac{t}{D}\right)$$

## 3. 理论模型

### 3.1 入水冲击阶段

#### 动量定理分析

圆环入水时，动量传递给流体：

$$M_{ring} V = \rho V_{cavity} V_{jet}$$

其中:
- $M_{ring} = \rho_m \pi D t \cdot w$ (圆环质量，$w$为宽度)
- $V_{cavity}$: 空腔体积
- $V_{jet}$: 射流特征速度

#### 能量守恒

圆环初始势能转化为：
- 流体动能
- 表面能
- 粘性耗散
- 气泡环势能

$$M_{ring} g H = E_{kinetic} + E_{surface} + E_{dissipation} + E_{bubble}$$

### 3.2 空腔动力学

#### 空腔形状

对于薄圆盘入水，空腔形状可以用以下方程描述：

$$R(z) = R_0 \left(\frac{z}{z_0}\right)^n$$

其中 $n \approx 0.5$ 对于深空腔。

#### 空腔断裂条件

空腔断裂发生在壁面收缩速度等于空腔底部运动速度时：

$$\frac{dR}{dt}\bigg|_{pinch} = V_{bottom}$$

根据文献 [arXiv:2510.27622]，断裂深度为：

$$z_{pinch} \propto D \cdot Fr^{2/3} \cdot We^{-1/3}$$

### 3.3 气泡环动力学

#### 气泡环体积

断裂时捕获的气体体积：

$$V_{gas} \approx \pi \int_0^{z_{pinch}} R(z)^2 dz$$

#### 气泡环上升速度

根据Morton-Turner理论，气泡环上升速度：

$$V_{rise} = C \sqrt{\frac{g V_{gas}}{D_{ring}}}$$

其中 $C$ 是形状系数，$D_{ring}$ 是气泡环直径。

### 3.4 喷泉高度估计

#### 能量方法

气泡环到达水面时的能量转化为喷泉动能：

$$\frac{1}{2} M_{water} V_{fountain}^2 = E_{bubble} - E_{surface, release}$$

其中 $M_{water}$ 是被推动的水的质量。

#### 尺度律预测

根据文献分析和量纲分析，喷泉高度的经验关系：

$$\frac{h_{max}}{D} \sim Fr^a \cdot We^b \cdot \eta^c$$

其中指数 $a, b, c$ 需要通过实验或数值模拟确定。

**理论估计**:
- 从能量考虑：$a \approx 1$（与入水速度平方成正比）
- 表面张力影响：$b < 0$（表面张力抑制喷泉）
- 几何影响：$c > 0$（厚圆环产生更大空腔）

## 4. 简化分析：圆盘入水

### 4.1 为什么选择圆盘？

圆盘入水是Ring Fountain的简化版本：
- 几何更简单（只有直径 $D$，没有厚度 $t$）
- 理论更成熟
- 可以作为验证案例

### 4.2 圆盘入水的尺度律

对于薄圆盘：

$$\frac{h_{max}}{D} = C \cdot Fr^\alpha \cdot We^\beta$$

其中根据文献：
- $C \approx 0.5 - 1.0$（常数）
- $\alpha \approx 0.8 - 1.0$（接近线性）
- $\beta \approx -0.2 - 0$（弱依赖）

### 4.3 从圆盘到圆环的修正

圆环与圆盘的主要区别：
1. 质量分布：圆环中心是空的
2. 空腔形状：圆环产生更复杂的空腔
3. 气泡环形成：圆环可能产生多个气泡环

修正因子：

$$\frac{h_{ring}}{h_{disk}} = f(\eta) = 1 - k\eta$$

其中 $\eta = t/D$，$k$ 为待定常数。

## 5. 数值模拟策略

### 5.1 CFD方法选择

**VOF方法**（Volume of Fluid）:
- 适合追踪水-气界面
- OpenFOAM的interFoam求解器
- 计算成本适中

**Phase-Field方法**:
- 界面处理更平滑
- 适合表面张力主导的情况
- 计算成本较高

### 5.2 网格要求

**关键区域加密**:
- 入水区域：高剪切，需要细化
- 自由表面：界面追踪，需要细化
- 空腔壁面：曲率大，需要细化

**网格尺寸估计**:
- 圆环厚度方向：至少10个单元
- 自由表面附近：$\Delta x \approx D/100$

### 5.3 时间步长

CFL条件：

$$\Delta t < C_{CFL} \frac{\Delta x}{V}$$

对于空腔动力学，通常 $C_{CFL} = 0.5$。

### 5.4 验证和确认

**验证**（Verification）:
- 网格无关性检验
- 时间步长无关性检验
- 与理论解对比（如存在）

**确认**（Validation）:
- 与实验数据对比
- 与文献结果对比
- 参数趋势合理性检验

## 6. 实验设计

### 6.1 实验参数范围

**几何参数**:
- 圆环直径 $D$: 2 - 10 cm
- 厚径比 $\eta$: 0.05 - 0.3

**运动参数**:
- 下落高度 $H$: 5 - 50 cm
- 入水速度 $V$: 1 - 3 m/s

**无量纲范围**:
- $Fr$: 1 - 10
- $We$: 100 - 5000
- $Bo$: 50 - 1000

### 6.2 测量方法

**喷泉高度测量**:
- 高速摄影（>1000 fps）
- 背景标尺标定
- 图像处理提取

**空腔演化观测**:
- 侧面高速摄影
- 底部透明水箱
- LED背光照明

**同步测量**:
- 入水时刻触发
- 多机位同步

## 7. 预期结果与讨论

### 7.1 参数影响预测

| 参数 | 增加时的预期影响 | 物理机制 |
|------|----------------|---------|
| $H$ (下落高度) | $h_{max}$ 增加 | 更多能量输入 |
| $D$ (直径) | $h_{max}/D$ 可能减小 | 能量分散到更大区域 |
| $t$ (厚度) | $h_{max}$ 先增后减 | 最优空腔体积 |
| $\sigma$ (表面张力) | $h_{max}$ 减小 | 抑制空腔形成 |

### 7.2 关键科学问题

1. **最优几何**: 是否存在使喷泉最高的最优厚径比 $\eta$？
2. **尺度效应**: 小尺度（cm）和大尺度（m）的规律是否一致？
3. **重复性**: 气泡环的形成是否具有随机性？

## 8. 参考文献

1. Aristoff, J.M. & Bush, J.W.M. (2009). Water entry of small hydrophobic bodies. *J. Fluid Mech.*
2. Bergmann, R. et al. (2009). Controlled impact of a disk on a water surface. *Phys. Fluids.*
3. Gekle, S. & Gordillo, J.M. (2011). Generation and breakup of Worthington jets after cavity collapse. *Phys. Rev. Lett.*
4. **arXiv:2510.27622** - Water entry of small disks, cones, or anything (强烈推荐)
5. **arXiv:2602.22761** - Acoustic Signatures of Pinch-Off Cavities

---

*Last updated: 2026-03-02*
