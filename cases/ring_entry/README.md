# Ring Entry Case

OpenFOAM simulation case for ring water entry (IYPT 2026 Problem 3: Ring Fountain).

> **Status**: FSI stability is fragile. The simulation is configured but prone to FPE crashes during water entry impact. See [Known Issues](#1-fpe-crash-gamgsolver-during-water-entry) below. For validated cavity dynamics results, refer to [`ring_sweep/base/`](../ring_sweep/base/) which completed successfully with prescribed motion.

## Case Overview

This case simulates a metal ring falling into water from rest, generating a fountain due to cavity collapse. The simulation uses:

- **Solver**: `foamRun -solver incompressibleVoF` (OpenFOAM v12 modular two-phase VOF)
- **Dynamic mesh**: `rigidBodyMotion` (librigidBodyMeshMotion.so) with composite Pz joint
- **Physics**: Two-phase (water/air) flow with free surface, surface tension (σ = 0.07 N/m), gravity
- **Geometry**: Rectangular domain 0.3×0.3×0.6 m, water depth 0.3 m
- **Ring**: Outer diameter D = 0.05 m, radial wall = 0.0025 m, height = 0.01 m, mass = 0.029 kg (steel)
- **Initial conditions**: Ring at z = 0.50 m (20 cm above water), zero initial velocity
- **Mesh**: 161,206 cells (20×20×40 base blocks × 2, snappyHexMesh refinement level 4 on ring)

## Dimensionless Parameters

- Froude number (Fr): ~2.0
- Weber number (We): ~1400
- Bond number (Bo): ~350
- Thickness ratio (η = t/D): 0.05

## Files and Directories

```
ring_entry/
├── 0/                       # Initial field files
│   ├── alpha.water           # Phase fraction (water = 1, air = 0)
│   ├── p_rgh                 # Dynamic pressure
│   ├── U                     # Velocity
│   ├── pointDisplacement     # Mesh point displacement (dynamic mesh)
│   └── motionScale           # Mesh motion scale field
├── 0.orig/                   # Backup of clean initial fields
├── constant/
│   ├── dynamicMeshDict       # rigidBodyMotion configuration
│   ├── g                     # Gravity: (0 0 -9.81) m/s²
│   ├── transportProperties   # Phase properties (ρ, ν, σ)
│   ├── momentumTransport     # Laminar model
│   ├── phaseProperties       # Phase definitions
│   ├── fvModels              # Finite-volume source models
│   ├── triSurface/           # STL geometry (ring.stl)
│   └── polyMesh/             # Generated mesh (after blockMesh + snappyHexMesh)
├── system/
│   ├── blockMeshDict         # Background mesh (20×20×40 blocks)
│   ├── controlDict            # Time control, adaptive dt, probes, forces
│   ├── fvSchemes              # Discretization schemes
│   ├── fvSolution             # Solver settings, PIMPLE, relaxation
│   ├── snappyHexMeshDict     # Mesh refinement (level 4 on ring surface)
│   ├── setFieldsDict         # Initial water/air phase setup
│   ├── topoSetDict            # Cell set creation for ring region
│   └── decomposeParDict       # Parallel decomposition (8 subdomains, scotch)
├── Allrun                   # Full workflow: mesh → decompose → parallel solve
├── Allclean                 # Clean simulation results
├── generate_ring.py         # Python script to generate ring.stl
└── README.md                # This file
```

## Running the Case

### Prerequisites

- OpenFOAM Foundation edition v12 (`source /opt/openfoam12/etc/bashrc`)
- Python 3 with numpy (for STL generation if needed)
- MPI runtime (for parallel execution)

### Quick Start

```bash
# 1. Activate OpenFOAM
source /opt/openfoam12/etc/bashrc

# 2. Run the full workflow
cd cases/ring_entry
./Allrun
```

The `Allrun` script handles: cleaning → blockMesh → checkMesh → snappyHexMesh → topoSet → setFields → decomposePar → mpirun -np 8 foamRun -parallel.

### Manual Steps (serial, for debugging)

```bash
./Allclean

# Mesh generation
blockMesh
checkMesh
snappyHexMesh -overwrite

# Field initialization
topoSet
setFields

# Run solver
foamRun -solver incompressibleVoF
```

### Parallel Execution

```bash
# After mesh and fields are set up:
decomposePar
mpirun -np 8 foamRun -solver incompressibleVoF -parallel > log.foamRun 2>&1 &

# After solver completes, reconstruct for post-processing:
reconstructPar
paraFoam
```

## Solver Configuration

### Time Stepping (`system/controlDict`)

| Parameter | Value | Notes |
|-----------|-------|-------|
| `startTime` | 0 | |
| `endTime` | 5 | Adjust for testing (0.1–0.5) vs full runs |
| `deltaT` | 1e-05 | Initial time step |
| `maxCo` | 0.1 | Max Courant number for adaptive dt |
| `maxAlphaCo` | 0.1 | Max interface Courant number |
| `maxDeltaT` | 2e-5 | Upper bound to prevent Courant spikes during water entry |

### PIMPLE (`system/fvSolution`)

| Parameter | Value | Notes |
|-----------|-------|-------|
| `nOuterCorrectors` | 5 | Fluid-structure coupling iterations |
| `nCorrectors` | 2 | Pressure correctors per outer iteration |
| `nNonOrthogonalCorrectors` | 1 | Non-orthogonal corrections |
| `moveMeshOuterCorrectors` | yes | Mesh moves each outer iteration |
| `outerCorrectorResidualControl` | p_rgh tol 1e-4 | Exit early when pressure converges |

### Relaxation

| Field/Equation | Factor | Purpose |
|----------------|--------|---------|
| `p_rgh` | 0.3 | Damp pressure oscillations |
| `U.*` | 0.7 | Under-relax momentum |

### Alpha Transport

| Parameter | Value | Notes |
|-----------|-------|-------|
| `cAlpha` | 0.5 | Interface compression coefficient |
| `nAlphaSubCycles` | 8 | Sub-cycles for boundedness |
| `nAlphaCorr` | 2 | MULES correction passes |
| `nLimiterIter` | 5 | Flux limiter iterations |
| `minIter` | 1 | Minimum solver iterations per step |

### Rigid Body Motion (`constant/dynamicMeshDict`)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Solver type | Newmark | Numerical integration |
| `accelerationRelaxation` | 0.3 | Strong damping of force updates (side-effect: reduces reported acceleration below physical free-fall) |
| `accelerationDamping` | 0.99 | Numerical damping |
| Ring mass | 0.029 kg | Steel (ρ=7800 kg/m³) |
| Inertias | Ixx=Iyy=8.47e-6, Izz=1.65e-5 | Must be 9-component tensor format, not vector |
| Joint type | composite / Pz | Translation-only along z |
| `innerDistance` | 0.02 m | Inner morphing zone |
| `outerDistance` | 0.10 m | Outer morphing zone |

## Post-processing

### Visualization

```bash
reconstructPar       # Merge parallel results
paraFoam             # Launch ParaView
```

### Probe Data

Ten probe locations along z-axis (0.05–0.50 m) track `alpha.water`, `U`, and `p_rgh`. Output in `postProcessing/probes/`.

### Forces

Forces on `ringSurface` patch tracked in `postProcessing/forces/`.

## Known Issues and Solutions

### 1. FPE Crash (GAMGSolver during water entry)

**Cause**: When the ring first contacts water, the impact creates large pressure forces on the ring. Without sufficient temporal resolution and relaxation, this triggers a feedback loop: bad forces → divergent rigid body acceleration → extreme mesh motion → Courant spike → corrupted alpha → ill-conditioned pressure matrix → FPE.

**Solution**: The case is configured with conservative settings to prevent this:
- `maxDeltaT 2e-5` limits time step size during impact
- `accelerationRelaxation 0.3` heavily damps rigid body force updates
- `accelerationDamping 0.99` adds numerical damping to the Newmark solver
- `cAlpha 0.5` and `nAlphaSubCycles 8` keep alpha bounded
- `minIter 2` improves GAMG pressure solver stability

### 2. Field File Size Mismatch

**Problem**: `setFields` fails with "size X is not equal to the given value of Y."

**Solution**: The `0/` directory field files must match the current mesh. Run `./Allclean` to regenerate from scratch, or update fields manually:
```bash
mv 0/alpha.water 0/alpha.water.bak
# Copy a known-good field and adjust with setFields
```

### 3. ringSurface Boundary Patch Missing

**Problem**: `rigidBodyMotion` cannot find the `ringSurface` patch.

**Solution**: `snappyHexMeshDict` creates `ringSurface` as a boundary patch from the STL. If missing:
- Check `constant/polyMesh/boundary` for `ringSurface`
- Verify `ring.stl` exists in `constant/triSurface/`

### 4. ParaView Reads Nothing After Parallel Run

**Problem**: `paraFoam` shows no data after a parallel run.

**Solution**: Run `reconstructPar` first. The `processor*/` directories contain partial results that ParaView cannot read directly.

## References

1. IYPT 2026 Problem 3: Ring Fountain
2. Gekle & Gordillo (2010) cavity collapse theory
3. OpenFOAM Foundation v12 documentation
4. `../../README.md` — Project overview
5. `../../docs/Theory.md` — Theoretical background

## Test Configuration

For initial testing:
- `endTime`: 0.1–0.5 s (in `system/controlDict`)
- `writeInterval`: 0.01 s
- Solver runs in background for quick validation

For full simulation, increase `endTime` to 1.0–5.0 s.
