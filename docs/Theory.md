# **刚体入水流固耦合问题**

> "When a flat metal ring falls from a certain height into a water tank, it generates a fountain that can shoot water high into the air. How does the maximum height of the fountain depend on the ring's parameters?"

> 当扁平金属环从一定高度落入水箱时，会产生一个能将水喷射到高空的喷泉。喷泉的最大高度如何依赖于圆环的参数？

### 1. 控制方程 (Governing Equations)

这个问题的核心物理是水和空气的两相流动，以及金属环的运动。因此，控制方程由两部分组成：**流体动力学方程**和**刚体六自由度运动方程**。

#### 1.1 流体动力学方程
由于涉及水和空气两种不相溶的流体，且伴有剧烈的界面变化，通常采用**不可压缩Navier-Stokes方程**结合**VOF方法**进行求解。

-   **连续性方程**：
    \[
    \nabla \cdot \mathbf{U} = 0
    \]

-   **动量方程 (N-S方程)**：
    \[
    \frac{\partial \rho \mathbf{U}}{\partial t} + \nabla \cdot (\rho \mathbf{U} \mathbf{U}) = -\nabla p^* + \nabla \cdot \left[ \mu_{eff} (\nabla \mathbf{U} + \nabla \mathbf{U}^T) \right] + \rho \mathbf{g} + \mathbf{f}_{\sigma} + \mathbf{f}_{FSI}
    \]
    其中：
    -   \(\mathbf{U}\) 是速度场。
    -   \(p^*\) 是伪动态压力（通常为 \(p - \rho \mathbf{g} \cdot \mathbf{r}\)，用于处理静水压）。
    -   \(\rho\) 和 \(\mu\) 是体积分数加权的混合密度和动力粘度：\(\rho = \alpha \rho_{water} + (1-\alpha) \rho_{air}\)。
    -   \(\mathbf{f}_{\sigma}\) 是表面张力项（基于连续表面力模型，是否需要取决于入水速度和水花尺度。对于高速撞击，表面张力通常可忽略，但如果喷泉极细，可能需要考虑）。
    -   \(\mathbf{f}_{FSI}\) 是流固耦合源项。这里不是指固体应力耦合，而是指**动网格**或**重叠网格**带来的动量源效应，或者是作为浸入边界法的体积力。

-   **相分数输运方程 (VOF方法)**：
    \[
    \frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{U}) + \nabla \cdot [\mathbf{U}_c \alpha (1-\alpha)] = 0
    \]
    其中 \(\alpha\) 是水的体积分数（\(\alpha=1\) 为水，\(\alpha=0\) 为空气）。最后一项是人工压缩项（如OpenFOAM中的 `interfaceCompression`），用于保持界面的锐利。

#### 1.2 刚体运动方程
金属环被视为刚体，受重力和流体压力的作用。其运动由牛顿-欧拉方程描述：

-   **平动**：
    \[
    m \frac{d \mathbf{U}_{rigid}}{dt} = m\mathbf{g} + \oint_{S} (-p\mathbf{n} + \boldsymbol{\tau} \cdot \mathbf{n}) dS + \mathbf{F}_{contact}
    \]
    其中 \(m\) 是圆环质量，\( \oint_{S} ... \) 是流体施加在圆环表面的压力和粘性力的积分，\(\mathbf{F}_{contact}\) 是触底时的接触力（若水箱较浅）。

-   **转动**：
    \[
    \mathbf{I} \frac{d \boldsymbol{\omega}}{dt} = \oint_{S} (\mathbf{r} \times (-p\mathbf{n} + \boldsymbol{\tau} \cdot \mathbf{n})) dS
    \]
    其中 \(\mathbf{I}\) 是惯性张量，\(\boldsymbol{\omega}\) 是角速度，\(\mathbf{r}\) 是相对于质心的力矩臂。

### 2. 求解器策略 (OpenFOAM Solver Selection)

-   **策略：动网格 + 六自由度求解器 (推荐，适合大位移、轻微变形)**
    -   **求解器**：`overInterDyMFoam` 或 `interDyMFoam`
    -   **原理**：
        -   `interDyMFoam`：结合了VOF和动网格技术。网格会随着圆环的运动而变形或重新生成。
        -   `overInterDyMFoam`：使用**重叠网格**技术。将圆环放在一个独立的、质量较好的小网格组件中，嵌入背景网格。这是处理大位移入水问题最稳健的方法，因为它避免了网格的大幅变形。
    -   **控制方程集成**：求解器求解上述的VOF两相流方程。圆环的运动由内置的 `sixDoFRigidBodyMotion` 库根据流体压力和力矩实时计算，并反馈给网格运动模块。

### 3. 计算域与边界条件 (Computational Domain & Boundary Conditions)

#### 3.1 计算域设置
计算域是一个圆柱形区域，分为空气和水两部分。

-   **初始相分布**：下半部分设为水 (\(\alpha=1\))，上半部分设为空气 (\(\alpha=0\))。初始自由表面位于水箱高度处。
-   **初始场**：
    -   圆环初始位置：高于水面一个小距离，赋予一个初始速度 \(U_{ring} = \sqrt{2gh}\)，其中 \(h\) 是下落高度。
    -   速度场 \(\mathbf{U}\)：全流场初始为0。
    -   压力场 \(p\)：依据静水压力分布初始化。

#### 3.2 边界条件 (以重叠网格策略为例)

-   **顶部边界**：
    -   设为 `pressureInletOutletVelocity` 和 `totalPressure`，允许空气自由进出，模拟大气环境。
    -   \(\alpha\)：`inletOutlet`，当空气流入时设为0，流出时为零梯度。

-   **底部边界 (水箱底)**：
    -   无滑移假设：\(\mathbf{U}\) 为 `fixedValue` (0,0,0)。
    -   \(p\)：`fixedFluxPressure`。
    -   \(\alpha\)：`zeroGradient`。

-   **侧壁边界**：
    -   关心壁面反射对喷泉的影响，设为无滑移墙。

-   **圆环表面 (Overlapping Region)**：
    -   这是由重叠网格求解器自动处理的。圆环表面的网格作为组件网格。
    -   \(\mathbf{U}\)：`movingWallVelocity`，耦合 `sixDoFRigidBodyMotion` 计算出的速度。
    -   \(p\)：`fixedFluxPressure`。
    -   \(\alpha\)：`zeroGradient` (假设固体表面不可渗透)。

### 4. 输出控制 (Output Control)

回答“喷泉最大高度依赖于圆环参数”这个问题，并且结合paraview实现可视化。

1.  **基础场输出**：
    -   **变量**：`U`， `p`， `alpha.water`
    -   **频率**：高时间分辨率输出。尤其是在入水瞬间和喷泉形成初期，建议每0.001秒或每几个时间步输出一次，确保能捕捉到喷泉的峰值。

2.  **探针点 (Probes)**：
    -   在圆环中心正上方不同高度设置一系列探针点。
    -   **监控变量**：`alpha.water` 或相分数。
    -   **目的**：当探针点的值从0（空气）变为1（水）时，记录该时刻的高度，即喷泉前锋到达的高度。

3.  **自由表面提取**：
    -   可以设置 `surface` 输出，提取 \(\alpha = 0.5\) 的等值面。然后通过后处理计算该等值面在垂直方向的最大 \(z\) 坐标值。

4.  **力与运动输出 (关键数据)**：
    -   **圆环运动数据**：利用 `sixDoFRigidBodyMotion` 的函数对象，输出圆环的质心位置 \((x, y, z)\)、线速度 \((U_x, U_y, U_z)\) 和加速度。
    -   **流体作用力**：输出流体作用在圆环上的合力与力矩。
