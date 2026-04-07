# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains research on the **Ring Fountain** phenomenon (IYPT 2026 Problem 3), investigating how a flat metal ring falling into water generates a fountain. The project combines theoretical analysis, OpenFOAM CFD simulations, and experimental validation.

**Key characteristics**:
- Physics: Two-phase (water/air) flow with free surface, rigid body motion, cavity dynamics
- Methodology: OpenFOAM Foundation v12 for CFD, Python for pre/post-processing
- Current state: Documentation and theory established; simulation cases and scripts to be developed

## Environment Setup

### OpenFOAM Foundation v12
The project requires OpenFOAM Foundation edition v12. Setup steps:

```bash
# Install (WSL/Ubuntu)
sudo apt-get update
sudo apt-get install -y openfoam12

# Add to ~/.bashrc
echo "source /opt/openfoam12/etc/bashrc" >> ~/.bashrc
source ~/.bashrc

# Verify
foamVersion  # Should output "OpenFOAM-12"
echo $WM_PROJECT_DIR  # Should be /opt/openfoam12
```

### Python Environment
Python scripts will be used for mesh generation, data analysis, and visualization. Recommended setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install common scientific packages
pip install numpy scipy matplotlib pandas
```

## Common Commands

### OpenFOAM Workflow
Typical simulation workflow for a case in `cases/`:

```bash
# Activate OpenFOAM environment
openfoam12  # or: source /opt/openfoam12/etc/bashrc

# Navigate to case directory
cd cases/ring_entry

# Generate mesh
blockMesh

# Optional: decompose for parallel run
decomposePar

# Run solver (example with interFoam)
interFoam  # or: mpirun -np 4 interFoam -parallel

# Optional: reconstruct parallel results
reconstructPar

# Post-process with ParaView
paraFoam
```

### Case Management
- `./Allrun`: Standard OpenFOAM script to run entire case (mesh → solver → post-process)
- `./Allclean`: Clean case results while preserving configuration
- `checkMesh`: Validate mesh quality before simulation

### Development Commands
- **Mesh generation**: `blockMesh`, `snappyHexMesh` (for complex geometries)
- **Field initialization**: `setFields` for initial phase distribution
- **Solver execution**: `interFoam`, `overInterDyMFoam`, `multiphaseInterFoam`
- **Post-processing**: `postProcess` for function objects, `sample` for probe data

## Directory Structure

The repository follows this organization (some directories may not yet exist):

```
ringfountain/
├── README.md              # Project overview and setup instructions
├── Theory.md             # Detailed theoretical derivation and equations
├── cases/                # OpenFOAM simulation cases (to be created)
│   ├── disk_impact/      # Disk impact validation case
│   ├── disk_entry/       # Disk water entry case  
│   └── ring_entry/       # Main ring entry case (with fountain)
├── scripts/              # Python utilities (to be created)
│   ├── preprocessing/    # Mesh generation, parameter sweep
│   ├── postprocessing/   # Data extraction, visualization
│   └── utilities/        # Common functions, unit conversion
├── docs/                 # Documentation
│   ├── theory.md         # Theoretical background
│   └── openfoam_guide.md # OpenFOAM-specific guidance
└── data/                 # Experimental and simulation data (to be created)
    ├── experimental/     # High-speed camera measurements
    └── simulation/       # CFD output data
```

## Solver Selection

Choose solver based on simulation requirements:

| Solver | Application | Command |
|--------|-------------|---------|
| `interFoam` | Basic two-phase VOF, stationary mesh | `interFoam` |
| `overInterDyMFoam` | Moving objects with overset grid | `overInterDyMFoam` |
| `multiphaseInterFoam` | Three or more phases | `multiphaseInterFoam` |

**Recommendation**: Start with `interFoam` for simplified validation, then use `overInterDyMFoam` for full ring entry with rigid body motion.

## Key Simulation Parameters

### Dimensionless Numbers
- **Froude number**: `Fr = V/√(gD)` (inertia vs. gravity)
- **Weber number**: `We = ρV²D/σ` (inertia vs. surface tension)  
- **Bond number**: `Bo = ρgD²/σ` (gravity vs. surface tension)
- **Thickness ratio**: `η = t/D` (ring geometry)
- **Inner radius ratio**: `α = r/R` (ring geometry)

### Physical Parameters (Typical values)
- Ring diameter (D): 0.01–0.1 m
- Thickness (t): 0.001–0.01 m  
- Drop height (H): 0.1–1.0 m
- Impact velocity: `V = √(2gH)`
- Water density: 1000 kg/m³
- Air density: 1 kg/m³
- Surface tension: 0.07 N/m

## Workflow Guidelines

### Creating a New Case
1. Copy an existing case template from `cases/template/` (when available)
2. Modify `constant/polyMesh/blockMeshDict` for geometry
3. Set physical properties in `constant/transportProperties`
4. Configure boundary conditions in `0/` directory files
5. Adjust solver settings in `system/fvSchemes` and `system/fvSolution`
6. Set output controls in `system/controlDict`

### Running Simulations
```bash
# 1. Activate OpenFOAM
openfoam12

# 2. Generate mesh
cd cases/ring_entry
blockMesh
checkMesh  # Verify mesh quality

# 3. Set initial conditions (if needed)
setFields

# 4. Run solver
interFoam > log.interFoam 2>&1 &

# 5. Monitor progress
tail -f log.interFoam
```

### Post-processing
- **Probe data**: Configure `system/probes` to track α at heights
- **Surface extraction**: Extract α=0.5 isosurface for fountain height
- **Force coefficients**: Use `forces` function object for drag/lift
- **Visualization**: `paraFoam` or export to VTK for ParaView

## Important Files

- `README.md`: Comprehensive project documentation in Chinese/English
- `Theory.md`: Detailed governing equations and solver strategies  
- `docs/OpenFOAM Foundation v12 进阶教程.pdf`: Advanced OpenFOAM tutorial (Chinese)

## Notes for Development

1. **Parallel execution**: Use `decomposePar` and `mpirun` for large cases
2. **Restart capability**: Simulations can be restarted from latest time step
3. **Version control**: Exclude large simulation data from git (use `.gitignore`)
4. **Validation**: Compare with theoretical scaling laws in `Theory.md`
5. **Parameter studies**: Use Python scripts to automate case variations

## Resources

- **OpenFOAM tutorials**: `$FOAM_TUTORIALS/multiphase/interFoam/`
- **Key papers**: References in README.md (arXiv:2510.27622, arXiv:2602.22761)
- **Community**: CFD Online Forums, OpenFOAM Wiki