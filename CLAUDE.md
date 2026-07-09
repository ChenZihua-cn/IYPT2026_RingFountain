# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project

Research on the **Ring Fountain** phenomenon (IYPT 2026 Problem 3): a flat metal ring falling into water generates a fountain. Combines OpenFOAM CFD, theoretical analysis, and experimental validation.

- **Solver**: `foamRun -solver incompressibleVoF` (OpenFOAM Foundation v12 modular framework)
- **Dynamic mesh**: `rigidBodyMotion` (ring_entry) or prescribed `solidBody`/`linearMotion` (ring_sweep)
- **Physics**: Two-phase VOF (water/air), laminar, isothermal, surface tension

AGENTS.md has extended context (papers, conventions, physics background).

## Environment

```bash
source /opt/openfoam12/etc/bashrc   # must be sourced in every shell
foamVersion                          # verify: OpenFOAM-12
```

Python for mesh generation and analysis:
```bash
python3 -m venv venv && source venv/bin/activate
pip install numpy scipy matplotlib pandas
```

## Repo Structure

```
ringfountain/
├── README.md           # Project docs (Chinese/English)
├── CLAUDE.md           # This file
├── AGENTS.md           # Extended agent context
├── cases/
│   ├── ring_entry/     # FSI case (rigidBodyMotion)
│   │   ├── 0/           # Current field files
│   │   ├── 0.orig/      # Clean field backups (restored by Allclean)
│   │   ├── constant/    # dynamicMeshDict, transportProperties, triSurface/
│   │   ├── system/      # controlDict, fvSchemes, fvSolution, ...
│   │   ├── generate_ring.py
│   │   ├── Allrun
│   │   └── Allclean
│   └── ring_sweep/     # Prescribed-motion case (solidBody/linearMotion)
│       ├── README.md    # Sweep strategy
│       └── base/        # Runnable reference case with config + postProcessing data
├── docs/
│   ├── Theory.md       # Theoretical derivation
│   ├── analysis/       # AI-assisted analysis summaries
│   ├── papers/         # Academic PDFs (13 papers)
│   └── references/     # Citation records
└── scripts/
    └── postprocessing/
        └── check_data.py  # Simulation data validation & diagnostics
```

## `ring_entry` Case Workflow

The Allrun script executes these steps in order:

```bash
cd cases/ring_entry
source /opt/openfoam12/etc/bashrc

./Allclean
blockMesh                          # 1. background hex mesh
checkMesh
snappyHexMesh -overwrite           # 2. snap to ring STL, refine near ring
checkMesh
topoSet                            # 3. mark cells inside ring volume
setFields                          # 4. set alpha.water (0 in ring, 1 below waterline)
decomposePar                       # 5. scotch decomposition (8 domains)
mpirun -np 8 foamRun -solver incompressibleVoF -parallel   # 6. run
reconstructPar                     # 7. after completion
```

Key configuration details:

**controlDict**: endTime 5, deltaT 1e-5, adaptive timestep (maxCo 0.1, maxAlphaCo 0.1, maxDeltaT 2e-5). Function objects: `probes` (alpha.water, U, p_rgh at z=0.05–0.50 every 10 steps) and `forces` (on ringSurface patch).

**fvSchemes**: Euler (ddt), Gauss vanLeerV (div(rhoPhi,U)), Gauss interfaceCompression vanLeer 0.5 (div(phi,alpha)), Gauss linear corrected (laplacian).

**fvSolution**: PIMPLE with 5 outer correctors, 2 inner, 1 non-orthogonal, moveMeshOuterCorrectors yes. MULES for alpha (2 corr, 8 sub-cycles, cAlpha 0.5). GAMG for p_rgh (GaussSeidel, faceAreaPair). Relaxation: p_rgh 0.3, U 0.7.

**dynamicMeshDict**: `rigidBodyMotion` solver (Newmark, accelerationRelaxation 0.3, accelerationDamping 0.99). Ring body: rigidBody type (mass=0.117kg, inertias Ixx=Iyy=1.32e-4, Izz=2.64e-4, initial z=0.35m), composite joint Pz-only, patches (ringSurface), innerDistance 0.02, outerDistance 0.10.

## OF12-Specific Notes

- OF12 uses the modular solver framework: `foamRun -solver <name>` replaces legacy binaries. `incompressibleVoF` is the equivalent of old `interFoam`.
- `rigidBodyMotion` (lib `librigidBodyMeshMotion.so`) replaces old `sixDoFRigidBodyMotion`.
- Physical properties: phase definitions in `constant/phaseProperties`, transport coefficients in `constant/transportProperties`.
- Dynamic mesh config lives in `constant/dynamicMeshDict` (not `dynamicMeshDict.rigidBodyMotion`).

## Physical Parameters

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Ring outer diameter | D | 0.05 m |
| Ring mass | m | 0.117 kg |
| Impact velocity | V | √(2gH) |
| Water density | ρ | 1000 kg/m³ |
| Air density | ρ | 1 kg/m³ |
| Surface tension | σ | 0.07 N/m |

Dimensionless: Fr = V/√(gD), We = ρV²D/σ, Bo = ρgD²/σ, η = t/D, α = r/R.

## Git

Track configs (0/, constant/, system/), scripts, docs. Exclude output: `[0-9]*/`, `processor*/`, `postProcessing/`, `log.*`, `*.foam`.
