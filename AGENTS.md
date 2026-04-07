# AGENTS.md - Ring Fountain Project

> This file provides essential information for AI coding agents working on the Ring Fountain project.

## Project Overview

This repository contains research on the **Ring Fountain phenomenon** (IYPT 2026 Problem 3), investigating how a flat metal ring falling into water generates a fountain that shoots water high into the air.

**Research Question**: "How does the maximum height of the fountain depend on the ring's parameters?"

### Physics Background

The Ring Fountain involves complex fluid dynamics:

1. **Water Entry**: Ring impacts water surface, creating a cavity
2. **Cavity Dynamics**: Ring sinks, dragging an axisymmetric cavity
3. **Pinch-off**: Cavity wall instability causes断裂, forming a toroidal bubble
4. **Bubble Rise**: Toroidal bubble rises due to buoyancy
5. **Fountain Formation**: Bubble reaches surface, releases energy creating fountain

### Key Dimensionless Parameters

| Parameter | Symbol | Formula | Physical Meaning |
|-----------|--------|---------|------------------|
| Froude number | Fr | V/√(gD) | Inertia/Gravity |
| Weber number | We | ρV²D/σ | Inertia/Surface tension |
| Bond number | Bo | ρgD²/σ | Gravity/Surface tension |
| Thickness ratio | η | t/D | Ring geometry |
| Inner radius ratio | α | r/R | Ring hollowness |

**Scaling Law** (dimensionless fountain height):

```
h_max/D = f(Fr, We, Bo, η, α)
```

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| CFD Solver | OpenFOAM | Foundation v12 | Two-phase flow simulation |
| Pre/Post-processing | Python | 3.x | Mesh generation, data analysis |
| Visualization | ParaView | Latest | Result visualization |
| Version Control | Git | - | Code management |

### OpenFOAM Foundation v12

This project specifically uses the **OpenFOAM Foundation edition v12** (not OpenCFD/ESI version).

**Installation (Ubuntu/WSL)**:
```bash
sudo apt-get update
sudo apt-get install -y openfoam12
echo "source /opt/openfoam12/etc/bashrc" >> ~/.bashrc
source ~/.bashrc
```

**Verify Installation**:
```bash
foamVersion          # Should output "OpenFOAM-12"
echo $WM_PROJECT_DIR # Should be /opt/openfoam12
```

### Python Environment

Python is used for preprocessing (mesh generation) and postprocessing (data analysis).

**Setup**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy scipy matplotlib pandas
```

## Project Structure

```
ringfountain/
├── README.md              # Main project documentation (Chinese/English)
├── CLAUDE.md             # Claude Code guidance
├── Theory.md             # Theoretical derivation and equations
├── AGENTS.md             # This file - agent guidance
├── cases/                # OpenFOAM simulation cases [TO BE CREATED]
│   ├── disk_impact/      # Disk impact validation case
│   ├── disk_entry/       # Disk water entry case
│   └── ring_entry/       # Main ring entry case
├── scripts/              # Python utilities [TO BE CREATED]
│   ├── preprocessing/    # Mesh generation, parameter sweep
│   ├── postprocessing/   # Data extraction, visualization
│   └── utilities/        # Common functions
├── docs/                 # Documentation
│   └── OpenFOAM Foundation v12 进阶教程.pdf  # Advanced tutorial (Chinese)
└── data/                 # Data storage [TO BE CREATED]
    ├── experimental/     # High-speed camera measurements
    └── simulation/       # CFD output data
```

**Current Status**: The documentation files exist. The `cases/`, `scripts/`, and `data/` directories need to be created as the project progresses.

## OpenFOAM Case Structure

Each case in `cases/` follows standard OpenFOAM directory structure:

```
cases/ring_entry/
├── 0/                    # Initial conditions
│   ├── U                 # Velocity field
│   ├── p                 # Pressure field
│   └── alpha.water       # Phase fraction (VOF)
├── constant/
│   ├── polyMesh/
│   │   └── blockMeshDict # Mesh definition
│   ├── transportProperties   # Fluid properties
│   └── g                 # Gravity vector
├── system/
│   ├── controlDict       # Time control, output settings
│   ├── fvSchemes         # Discretization schemes
│   ├── fvSolution        # Solver settings
│   └── decomposeParDict  # Parallel decomposition
├── Allrun                # Script to run entire case
└── Allclean              # Script to clean results
```

## Build and Run Commands

### OpenFOAM Workflow

```bash
# 1. Activate OpenFOAM environment
openfoam12              # Or: source /opt/openfoam12/etc/bashrc

# 2. Navigate to case
cd cases/ring_entry

# 3. Generate mesh
blockMesh

# 4. Check mesh quality
checkMesh

# 5. Set initial fields (if needed)
setFields

# 6. Run solver
interFoam               # Basic two-phase
# OR
overInterDyMFoam        # With overset mesh for rigid body motion

# 7. Run in parallel (optional)
decomposePar
mpirun -np 4 interFoam -parallel
reconstructPar

# 8. Visualize
paraFoam
```

### Case Management Scripts

Standard OpenFOAM scripts in each case directory:

| Script | Purpose |
|--------|---------|
| `./Allrun` | Run complete case: mesh → solver → post-process |
| `./Allclean` | Clean results while preserving configuration |

## Solver Selection Guide

Choose solver based on simulation requirements:

| Solver | Application | When to Use |
|--------|-------------|-------------|
| `interFoam` | Two-phase VOF, stationary mesh | Simplified validation, fixed ring position |
| `overInterDyMFoam` | Moving objects with overset grid | **Recommended** - Full ring entry with 6-DOF motion |
| `multiphaseInterFoam` | Three+ phases | If vapor phase needs to be modeled |

**Recommendation**: Start with `interFoam` for validation, then use `overInterDyMFoam` for the full simulation with rigid body motion.

## Physical Parameters

### Fluid Properties (constant/transportProperties)

```cpp
phases (water air);

water {
    transportModel  Newtonian;
    nu              1e-06;      // Kinematic viscosity [m²/s]
    rho             1000;       // Density [kg/m³]
}

air {
    transportModel  Newtonian;
    nu              1.48e-05;
    rho             1;
}

sigma   0.07;   // Surface tension [N/m]
```

### Ring Parameters (Typical Values)

| Parameter | Symbol | Typical Range | Unit |
|-----------|--------|---------------|------|
| Diameter | D | 0.01 – 0.1 | m |
| Thickness | t | 0.001 – 0.01 | m |
| Drop height | H | 0.1 – 1.0 | m |
| Impact velocity | V = √(2gH) | Calculated | m/s |

## Development Conventions

### Naming Conventions

- **Case directories**: Use `snake_case` (e.g., `disk_impact`, `ring_entry`)
- **Python scripts**: Use `snake_case.py` (e.g., `generate_mesh.py`)
- **OpenFOAM fields**: Follow standard naming (`U`, `p`, `alpha.water`)

### Case Creation Workflow

1. **Copy template** from existing case or `$FOAM_TUTORIALS/multiphase/interFoam/`
2. **Modify geometry** in `constant/polyMesh/blockMeshDict`
3. **Set fluid properties** in `constant/transportProperties`
4. **Configure boundary conditions** in `0/` directory
5. **Adjust solver settings** in `system/fvSchemes` and `system/fvSolution`
6. **Set output control** in `system/controlDict`
7. **Test** with `./Allrun`

### Python Script Guidelines

```python
#!/usr/bin/env python3
"""
Script description following Google docstring style.

Example:
    python script.py --diameter 0.05 --height 0.5
"""

import numpy as np
import os

# Use relative paths from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..', '..')

# Main function for clarity
def main():
    pass

if __name__ == '__main__':
    main()
```

## Testing and Validation

### Mesh Quality Check

Always verify mesh before running:

```bash
checkMesh
```

Look for:
- Non-orthogonality < 70°
- Skewness < 4
- No negative volume cells

### Validation Strategy

1. **Disk Entry First**: Validate against disk water entry literature
2. **Parameter Sweep**: Vary Fr, We, η systematically
3. **Compare Scaling Laws**: Verify against theoretical predictions in `Theory.md`

### Key Outputs to Monitor

| Output | How to Measure | Purpose |
|--------|---------------|---------|
| Fountain height | Probes at different heights tracking `alpha.water` | Main research question |
| Ring trajectory | `sixDoFRigidBodyMotion` output | Validate motion |
| Cavity shape | α=0.5 isosurface | Validate physics |
| Force on ring | `forces` function object | Validate FSI |

## Git Workflow

### Files to Track

```
# Track these
cases/*/0/*
cases/*/constant/*
cases/*/system/*
cases/*/Allrun
cases/*/Allclean
scripts/**/*.py
docs/*
*.md

# DO NOT track these (add to .gitignore)
*.foam
cases/*/processor*/
cases/*/[0-9]*/
cases/*/[0-9]*.*/
cases/*/log.*
cases/*/postProcessing/
data/*/
venv/
__pycache__/
```

### Recommended .gitignore

Create `.gitignore` with:
```gitignore
# OpenFOAM output
*.foam
[0-9]*/
[0-9]*.*/
processor*/
postProcessing/
log.*

# Python
__pycache__/
*.pyc
venv/

# Data
data/experimental/*
data/simulation/*
!data/.gitkeep
```

## Key References

### Papers

1. **Water entry of small disks, cones, or anything** (arXiv:2510.27622)
   - Unified scaling law for cavity pinch-off modes

2. **Acoustic Signatures of Pinch-Off Cavities** (arXiv:2602.22761)
   - Cavity pinch-off dynamics

3. **Cavity dynamics in water entry at low Froude numbers** (MIT)
   - Classical cavity dynamics theory

### OpenFOAM Resources

- **Tutorials**: `$FOAM_TUTORIALS/multiphase/interFoam/`
- **Recommended cases**: `damBreak`, `damBreakWithObstacle`
- **Documentation**: https://www.openfoam.com/documentation
- **Wiki**: https://openfoamwiki.net/

## Common Issues and Solutions

### Issue: Command not found (foamVersion, blockMesh, etc.)
**Solution**: Environment not sourced. Run:
```bash
source /opt/openfoam12/etc/bashrc
```

### Issue: Mesh check fails
**Solution**: Check `blockMeshDict` for:
- Valid vertex ordering (right-hand rule)
- Proper boundary definitions
- No overlapping cells

### Issue: Solver crashes at start
**Solution**: Check:
- Initial fields are properly set in `0/`
- Boundary conditions match patch names in mesh
- Time step is small enough (adjust `deltaT` in `controlDict`)

### Issue: Ring moves unrealistically
**Solution**: For `overInterDyMFoam`:
- Check `sixDoFRigidBodyMotion` configuration
- Verify mass and inertia tensor
- Ensure forces are calculated on correct patches

## Contact and Updates

- **Project Created**: 2026-03-02
- **Last Updated**: 2026-04-07
- **Language**: Documentation primarily in Chinese, code comments in English

---

*This file should be updated as the project evolves. When adding new cases, scripts, or changing workflows, update this documentation accordingly.*
