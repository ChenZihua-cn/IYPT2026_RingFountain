# Ring Sweep Base Case (Prescribed Motion)

OpenFOAM simulation case for ring water entry with **prescribed ring motion** — a simplified variant of `ring_entry` used for scaling-law parameter sweeps.

## Why Prescribed Motion?

The FSI `ring_entry` case is unstable (FPE crashes, tiny timesteps, tuning sensitivity) due to two-way fluid-structure coupling via `rigidBodyMotion`. For a scaling-law sweep, we need consistent, repeatable cavity dynamics across parameter variations — the ring's precise deceleration profile doesn't significantly affect the fountain height at moderate-to-high Fr.

This case eliminates the FSI stability bottleneck by prescribing the ring velocity directly, decoupling the fluid solve from the structural solve.

## Case Overview

- **Solver**: `foamRun -solver incompressibleVoF` (OpenFOAM v12 modular two-phase VOF)
- **Mesh motion**: `solidBody` + `linearMotion` — constant velocity `(0 0 -2.0)` m/s applied to `ringZone` cell zone
- **Physics**: Two-phase (water/air) flow with free surface, surface tension (sigma = 0.07 N/m), gravity
- **Geometry**: Rectangular domain 0.3 x 0.3 x 0.6 m, water depth 0.3 m
- **Ring**: Outer diameter D = 0.05 m, thickness t = 0.0025 m, width w = 0.01 m
- **Initial conditions**: Ring at z = 0.35 m (5 cm above water)
- **Mesh**: ~161K cells (20x20x40 base blocks x 2, snappyHexMesh refinement level 5–6 on ring)

## Key Differences from `ring_entry`

| Aspect | `ring_entry` (FSI) | `ring_sweep/base` (prescribed) |
|--------|-------------------|-------------------------------|
| Mesh motion | `rigidBodyMotion` + Newmark | `solidBody` + `linearMotion` |
| Acceleration relaxation | 0.3 | Not needed |
| maxCo | 0.1 | 0.1 |
| maxDeltaT | 2e-5 | None |
| PIMPLE outer correctors | 5 | 3 |
| moveMeshOuterCorrectors | yes | yes |
| Stability | FPE-prone | Stable |

## Running the Case

```bash
source /opt/openfoam12/etc/bashrc
cd cases/ring_sweep/base
./Allrun
```

The `Allrun` script: clean -> blockMesh -> checkMesh -> snappyHexMesh -> checkMesh -> topoSet -> setFields -> decomposePar -> foamRun -parallel.

## Post-processing

```bash
reconstructPar
paraFoam
```

Probe data at z=0.05-0.50 m and forces on `ringSurface` are in `postProcessing/`.

## References

- `../README.md` — Sweep strategy and parameter space
- `../../ring_entry/README.md` — Original FSI case documentation
- `../../docs/Theory.md` — Theoretical background
- [SOLUTIONS.md](SOLUTIONS.md) — Diagnosis and fix strategy for prescribed motion
