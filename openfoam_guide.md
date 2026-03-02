# OpenFOAM 使用指南 (WSL环境)

## 快速参考

### 进入项目
```bash
cd ~/ringfountain
```

### OpenFOAM版本切换

```bash
# 方法1: 使用配置的函数（推荐）
openfoam12          # 基金会版 OpenFOAM 12
openfoam2412        # OpenCFD版 OpenFOAM 2412

# 方法2: 手动source（如果函数失效）
# 基金会版
source /opt/openfoam12/etc/bashrc

# OpenCFD版  
source /usr/lib/openfoam/openfoam2412/etc/bashrc
```

### 验证安装
```bash
# 检查版本
foamVersion

# 查看环境变量
echo $WM_PROJECT_DIR
echo $WM_PROJECT_USER_DIR

# 查看求解器列表
ls $FOAM_APPBIN | grep -i foam
```

---

## OpenFOAM案例结构

标准OpenFOAM案例包含以下目录：

```
caseName/
├── 0/                      # 初始条件和边界条件
│   ├── U                   # 速度场
│   ├── p                   # 压力场
│   └── alpha.water         # 体积分数（多相流）
├── constant/
│   ├── transportProperties # 物性参数
│   ├── turbulenceProperties # 湍流模型
│   └── polyMesh/
│       └── blockMeshDict   # 网格定义
├── system/
│   ├── controlDict         # 控制参数
│   ├── fvSchemes           # 离散格式
│   ├── fvSolution          # 求解器设置
│   └── decomposeParDict    # 并行分解
└── Allrun                  # 运行脚本（可选）
└── Allclean                # 清理脚本（可选）
```

---

## 多相流求解器选择

对于Ring Fountain问题，推荐以下求解器：

### 1. interFoam（首选）
**适用**: 两相不可压缩流动，VOF方法追踪界面
```bash
interFoam
```

**特点**:
- 使用VOF（Volume of Fluid）方法
- 适合自由表面流动
- 开源稳定，文档丰富

### 2. overInterDyMFoam
**适用**: 动网格 + 多相流
```bash
overInterDyMFoam
```

**特点**:
- 支持动网格（物体运动）
- 可以模拟圆环入水过程
- 适合流固耦合问题

### 3. multiphaseInterFoam
**适用**: 多相流（超过两相）
```bash
multiphaseInterFoam
```

**特点**:
- 支持三相及以上
- 如果有空气-水-蒸汽需要考虑

---

## 基本操作流程

### 1. 创建案例
```bash
# 复制模板
cp -r $FOAM_TUTORIALS/multiphase/interFoam/laminar/damBreak ./myCase
cd myCase
```

### 2. 生成网格
```bash
# 使用blockMesh（简单几何）
blockMesh

# 或者使用snappyHexMesh（复杂几何）
blockMesh
snappyHexMesh -overwrite
```

### 3. 设置初始条件
编辑 `0/` 目录下的文件：
- `U`: 速度场初始值和边界条件
- `p`: 压力场
- `alpha.water`: 水的体积分数（0=空气，1=水）

### 4. 运行求解器
```bash
# 串行运行
interFoam

# 并行运行（4核）
decomposePar
mpirun -np 4 interFoam -parallel
reconstructPar
```

### 5. 后处理
```bash
# 使用ParaView
paraFoam

# 或者命令行采样
postProcess -func sampleDict
```

---

## Ring Fountain专用设置

### 几何参数
对于圆环入水问题，关键几何参数：
- `D`: 圆环直径 (m)
- `t`: 圆环厚度 (m)
- `H`: 下落高度 (m)
- `V = sqrt(2gH)`: 入水速度 (m/s)

### 边界条件设置

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

### 物性参数
编辑 `constant/transportProperties`:

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

---

## 实用脚本

### Allrun 模板
```bash
#!/bin/bash

cd "${0%/*}" || exit

# 清理
./Allclean

# 生成网格
blockMesh

# 检查网格
checkMesh

# 设置初始条件
setFields

# 运行求解器
interFoam | tee log.interFoam

# 后处理
foamLog log.interFoam
```

### Allclean 模板
```bash
#!/bin/bash

cd "${0%/*}" || exit

# 删除计算结果
foamCleanTutorials

# 或者手动清理
rm -rf 0.* [1-9]* processor*
rm -f log.*
```

---

## 常见问题

### Q1: 如何查看案例是否正常运行？
```bash
# 实时查看残差
tail -f log.interFoam

# 检查连续性误差
grep "Continuity error" log.interFoam
```

### Q2: 如何提取自由表面高度？
```bash
# 使用sample工具
postProcess -func sample

# 或者在ParaView中使用"Plot Over Line"
```

### Q3: 如何加速计算？
```bash
# 并行计算（假设8核）
decomposePar
mpirun -np 8 interFoam -parallel
reconstructPar
```

### Q4: 两个OpenFOAM版本如何选择？
- **OpenFOAM 12 (基金会版)**: 开源社区驱动，更新较慢但更稳定
- **OpenFOAM 2412 (OpenCFD版)**: 商业公司开发，新功能更多

建议：对于Ring Fountain，两者都可以使用。如果遇到问题，可以尝试另一个版本。

---

## 学习资源

### 官方教程
```bash
# 查看教程位置
echo $FOAM_TUTORIALS

# 推荐的多相流教程
ls $FOAM_TUTORIALS/multiphase/interFoam/
```

### 推荐教程案例
1. **damBreak** - 溃坝（最经典）
2. **damBreakWithObstacle** - 带障碍物的溃坝
3. **sloshingTank2D** - 液舱晃动

### 查看命令帮助
```bash
# 求解器帮助
interFoam -help

# 工具帮助
blockMesh -help
setFields -help
```

---

## 下一步

1. 运行 damBreak 教程熟悉流程
2. 修改几何参数研究影响
3. 建立圆环入水案例
4. 参数扫描分析

---

*Happy Foaming! 🌊*
