# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Research on the **Ring Fountain** phenomenon (IYPT 2026 Problem 3): a flat metal ring falling into water generates a fountain. Combines OpenFOAM CFD, theoretical analysis, and experimental validation.

- **Solver**: `foamRun -solver incompressibleVoF` (OpenFOAM Foundation v12 modular framework)
- **Dynamic mesh**: `rigidBodyMotion` (ring_entry) or prescribed `solidBody`/`linearMotion` (ring_sweep)
- **Physics**: Two-phase VOF (water/air), laminar, isothermal, surface tension (σ=0.07 N/m)

AGENTS.md has extended context (papers, conventions, physics background, development conventions).

## Current Status

- **ring_entry** (FSI via rigidBodyMotion): Configured but FSI stability is fragile. The solver is prone to FPE crashes during water entry impact due to force-divergence feedback loop. Conservative settings (maxDeltaT 2e-5, accelerationRelaxation 0.3, accelerationDamping 0.99) mitigate but haven't eliminated the issue.
- **ring_sweep/base** (prescribed motion): Ran successfully to completion. Results in `postProcessing/` — use as the validated reference for cavity dynamics. This decoupled approach is the recommended path for parameter sweeps.
- Dynamic mesh debugging artifacts: `constant/dynamicMeshDict.bak2` and other backup files exist in ring_entry — these are from stabilization attempts and should not be committed or used.

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

## Essential Commands

### Run ring_entry case (FSI)

```bash
cd cases/ring_entry
./Allclean && ./Allrun          # full workflow: mesh → fields → parallel solve
```

The solver runs in background. Monitor with:
```bash
tail -f cases/ring_entry/log.foamRun
```

After solver completes:
```bash
cd cases/ring_entry
reconstructPar                  # merge parallel results
paraFoam                        # visualize
```

### Run in serial (for debugging)

```bash
cd cases/ring_entry
./Allclean
blockMesh && snappyHexMesh -overwrite
topoSet && setFields
foamRun -solver incompressibleVoF
```

### Generate ring STL geometry

```bash
cd cases/ring_entry
python3 generate_ring.py   # generates constant/triSurface/ring.stl
# Edit generate_ring.py to change D, t, w parameters
```

### Validate simulation data

```bash
python3 scripts/postprocessing/check_data.py                          # checks ring_entry
python3 scripts/postprocessing/check_data.py -c ring_sweep/base       # check another case
python3 scripts/postprocessing/check_data.py --no-plot                # text-only report
```

Checks: NaN/Inf in ring kinematics, hydrostatic pressure validation, force oscillations, sudden jumps in velocity/force, monotonicity of ring descent. Plots saved to `postProcessing/checks/`.

### Mesh quality

```bash
checkMesh   # key metrics: non-orthogonality < 70, skewness < 4, no negative volumes
```

## `ring_entry` Case Workflow

The Allrun script executes: Allclean → blockMesh → checkMesh → snappyHexMesh -overwrite → checkMesh → topoSet → setFields → decomposePar (scotch, 8 domains) → mpirun -np 8 foamRun -solver incompressibleVoF -parallel.

**Allclean restores `0/` from `0.orig/` and removes polyMesh/**, so mesh must be regenerated each run.

### Key configuration details

**controlDict**: endTime 5, deltaT 1e-5, adaptive timestep (maxCo 0.1, maxAlphaCo 0.1, maxDeltaT 2e-5). Function objects: `probes` (alpha.water, U, p_rgh at z=0.05–0.50 every 10 steps) and `forces` (on ringSurface patch).

**fvSchemes**: Euler (ddt), Gauss vanLeerV (div(rhoPhi,U)), Gauss interfaceCompression vanLeer 0.5 (div(phi,alpha)), Gauss linear corrected (laplacian).

**fvSolution**: PIMPLE with 5 outer correctors, 2 inner, 1 non-orthogonal, `moveMeshOuterCorrectors yes`, `outerCorrectorResidualControl` on p_rgh (tol 1e-4). MULES: 2 alphaCorr, 8 sub-cycles, cAlpha 0.5, nLimiterIter 5. Relaxation: p_rgh 0.3, U 0.7. GAMG for p_rgh (GaussSeidel, faceAreaPair, minIter 2 for stability).

**dynamicMeshDict**: `rigidBodyMotion` solver (Newmark, accelerationRelaxation 0.3, accelerationDamping 0.99). Ring: rigidBody type, mass 0.029 kg (steel), inertias Ixx=Iyy=8.47e-6, Izz=1.65e-5 (9-component tensor format), initial z=0.50 m. Composite joint with Pz-only constraint. Patches (ringSurface), innerDistance 0.02, outerDistance 0.10.

### Known issues

1. **FPE crash at water entry**: The force-divergence feedback loop (bad forces → divergent acceleration → extreme mesh motion → Courant spike → corrupted alpha → ill-conditioned pressure matrix → FPE). Conservative settings above mitigate but don't eliminate. See [ring_entry README](cases/ring_entry/README.md#1-fpe-crash-gamgsolver-during-water-entry) for full diagnosis.

2. **field size mismatch**: If `setFields` fails with size mismatch, run `./Allclean` to regenerate from scratch (mesh changed but 0/ fields weren't updated).

3. **missing ringSurface patch**: Verify `constant/polyMesh/boundary` contains `ringSurface` after snappyHexMesh. If missing, STL may not have been found.

4. **dynamicMeshDict inertia format**: Must be 9-component tensor, not vector. Wrong format causes silent failure at solver start.

5. **`accelerationRelaxation` side-effect**: Values below 0.9 artificially reduce reported acceleration (ring falls slower than physical free-fall). The current 0.3 makes the ring kinematics non-physical but is needed for stability.

## OF12-Specific Notes

- OF12 uses modular solver framework: `foamRun -solver <name>`. `incompressibleVoF` ≡ legacy `interFoam`.
- `rigidBodyMotion` (lib `librigidBodyMeshMotion.so`) replaces old `sixDoFRigidBodyMotion`.
- Dynamic mesh config in `constant/dynamicMeshDict` (not `dynamicMeshDict.rigidBodyMotion`).
- Phase definitions in `constant/phaseProperties`, transport in `constant/transportProperties`.

## Physical Parameters

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Ring outer diameter | D | 0.05 m |
| Ring thickness | t | 0.0025 m |
| Ring width | w | 0.01 m |
| Ring mass | m | 0.029 kg |
| Impact velocity | V | √(2gH) |
| Water density | ρ_w | 1000 kg/m³ |
| Air density | ρ_a | 1 kg/m³ |
| Surface tension | σ | 0.07 N/m |
| Water depth | h_w | 0.3 m |
| Domain size | L×W×H | 0.3×0.3×0.6 m |

Dimensionless: Fr = V/√(gD), We = ρV²D/σ, Bo = ρgD²/σ, η = t/D, α = r/R.

## Git

Track configs (0/, constant/, system/), scripts, docs, case READMEs. Exclude output: `[0-9]*/`, `processor*/`, `postProcessing/`, `log.*`, `*.foam`, `constant/polyMesh/`, backup files (`*.bak*`).
