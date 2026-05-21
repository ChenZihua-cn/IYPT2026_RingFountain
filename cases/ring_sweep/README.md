# Ring Sweep — Scaling Law Verification

> **Status**: Plan document. Only the `base/` reference case is implemented (constant-velocity prescribed motion). The full sweep infrastructure (sweep.py, parameter matrix, automated post-processing) is not yet built.

Parametric sweep case to verify the fountain height scaling law:

```
h_max/D = f(Fr, We, Bo, η, α)
```

## Strategy

**Prescribe ring motion** instead of solving FSI. The current `ring_entry` case uses `rigidBodyMotion` to couple flow and ring acceleration — this is the main source of instability (FPE crashes, tiny timesteps, tuning sensitivity). For a scaling law sweep, we don't need the exact ring deceleration; we need consistent, repeatable cavity dynamics across parameter variations.

### Why prescribed motion works

- The fountain is driven by **cavity pinch-off and bubble rise**, which happen well after the ring has passed through the water surface
- The ring's precise deceleration profile during the first few milliseconds doesn't change the cavity shape enough to affect h_max — especially at moderate-to-high Fr where inertia dominates
- Prescribed motion decouples the fluid solve from the structural solve, eliminating the FSI stability bottleneck

### Velocity prescription

Two options, in order of preference:

1. **Extract from FSI run**: Get one successful FSI run at a reference point (D=0.05m, V≈2 m/s), extract the ring's z-velocity vs time, and fit a curve. Reuse this profile (scaled by impact velocity) for all sweep points.
2. **Simple model**: `V(t) = V₀·exp(-t/τ)` with τ calibrated from the reference FSI run, or constant velocity at high Fr.

## Case Design

### What changes from `ring_entry`

| Aspect | `ring_entry` (FSI) | `ring_sweep` (prescribed) |
|--------|-------------------|--------------------------|
| Mesh motion | `rigidBodyMotion` + Newmark solver | Prescribed solid-body motion |
| Timestep control | `maxDeltaT 5e-6`, `maxCo 0.02` | Larger: `maxCo 0.1`, no `maxDeltaT` |
| PIMPLE outer correctors | 15 (for FSI coupling) | 3–5 |
| Acceleration relaxation | 0.001 | Not needed |
| Stability | FPE-prone | Stable |
| Runtime per case | Long (small Δt + many correctors) | Shorter |

### What stays the same

- Domain: 0.3×0.3×0.6m (20×20×40 per block hex mesh)
- fvSchemes: Euler ddt, vanLeerV div, interfaceCompression div(phi,alpha)
- fvSolution: MULES alpha (2 corr, 4 sub-cycles), GAMG pressure
- Function objects: probes at z=0.05–0.50m, forces on ring patch
- Ring geometry via STL, snappyHexMesh refinement, topoSet/setFields for init

### Parameter space

| Parameter | Symbol | Range | Step | Default |
|-----------|--------|-------|------|---------|
| Ring diameter | D | 0.03–0.08 m | varies | 0.05 m |
| Ring thickness | t | 0.001–0.005 m | varies | 0.0025 m |
| Impact velocity | V₀ | 0.5–3.0 m/s | varies | 2.0 m/s |
| Water depth | h_w | 0.2–0.4 m | fixed first | 0.3 m |
| Inner/outer radius ratio | α = r/R | 0.3–0.8 | varies | geometry-dependent |

### Sweep script workflow

```
sweep.py
  1. Read parameter matrix (CSV or YAML)
  2. For each parameter set:
     a. Call generate_ring.py with {D, t, α}
     b. Copy base case template
     c. Template-replace values in:
        - system/controlDict (endTime)
        - constant/dynamicMeshDict (prescribed velocity)
        - constant/physicalProperties.* (if varying fluids)
        - 0/U (initial velocity on ring patch)
     d. Run ./Allrun
     e. Post-process: extract h_max from probe data
     f. Log result: params → h_max
  3. Fit scaling law: h_max/D = C·Fr^a·We^b·η^c·α^d
```

### Post-processing

For each run, extract fountain height:

1. Parse `postProcessing/probes/` time series
2. For each probe height z_i, find when `alpha.water` exceeds threshold (0.5)
3. Max z with water presence → h_max
4. Store in results CSV: `D, t, V0, Fr, We, Bo, η, α, h_max, h_max/D`

## Current Issues & Diagnosis (2026-05-19)

The `base/` case is implemented but the ring does not move. Three problems identified:

### Problem 1: `ringZone` cellZone is empty (0 cells) — PRIMARY

The `solidBody` motion solver moves cells in `ringZone` at the prescribed velocity. But `ringZone` contains **zero cells** — proved by [cellZones](base/constant/polyMesh/cellZones#L22) (`cellLabels List<label> 0()`) and [log.topoSet](base/log.topoSet#L33-L36) (`Cannot find any cellZone named ringZone`).

**Root cause**: The ring STL is a closed torus surface. During the castellated mesh phase, `snappyHexMesh` splits the mesh at the surface into two regions — the ring interior and the exterior. Then it keeps only the region containing `insidePoint (0 0 0.5)`, which is *outside* the ring. The ~8600 cells inside the ring solid are disconnected from the `insidePoint` and get **removed**. Since no cells survive on the "inside" side of the surface, the `cellZone ringZone` (added in the most recent uncommitted diff to `snappyHexMeshDict`) ends up with zero cells.

OF12's `snappyHexMesh` supports only a single `insidePoint` (no `locationsInMesh` plural form), so you cannot keep both the ring interior and the exterior simultaneously.

**Why `ring_entry` isn't affected**: `ring_entry` uses `rigidBodyMotion` which moves the `ringSurface` *patch* (boundary) based on fluid forces — it does not use a cellZone. The empty `ringZone` in `ring_entry` is irrelevant (the uncommitted addition of `cellZone ringZone` to ring_entry's `snappyHexMeshDict` has no effect on FSI).

**Solution**: Make the ring STL **non-watertight** by removing 2–4 adjacent facets at the top of the torus (near z=0.355). This connects the ring interior to the exterior, so snappyHexMesh no longer sees them as disconnected regions. `cellZoneInside inside` will then correctly populate `ringZone` with cells, and `solidBody` will move them. The small opening also means a tiny gap in the `ringSurface` patch, but for a prescribed-motion sweep this is negligible.

Steps:
1. Edit `constant/triSurface/ring.stl` — locate facets near z=0.355, delete 2–4 adjacent ones (a contiguous block of ~10–20 lines in the ASCII STL)
2. Re-run `./Allrun` from scratch
3. Verify with `checkMesh` that `ringZone` has cells

### Problem 2: Missing `motionScale` field in `0/`

`ring_entry` has [0/motionScale](../ring_entry/0/motionScale) — a `pointScalarField` that controls mesh deformation distribution. `ring_sweep/base/0/` does not have this field. OF12's `solidBody` solver may create it automatically, but if not, the mesh deformation around the moving cellZone may fail.

**Solution**: Copy `motionScale` from `ring_entry/0/` into `ring_sweep/base/0/`:
```bash
cp ../ring_entry/0/motionScale base/0/
```

### Problem 3: Missing `moveMeshOuterCorrectors yes` in `fvSolution`

[ring_entry fvSolution](../ring_entry/system/fvSolution#L89) has `moveMeshOuterCorrectors yes` in the PIMPLE block. Without this, the mesh motion is only applied *between* PIMPLE loops, not *during* them — the fluid is solved on a stationary mesh, then the mesh jumps to the new position. For prescribed motion this is less critical than for FSI, but it still causes a first-order lag in the fluid response.

**Solution**: Add to `base/system/fvSolution` in the `PIMPLE` block:
```
moveMeshOuterCorrectors yes;
```

### Problem 4 (ring_entry only): FSI instability → FPE crash

The `ring_entry` FSI simulation crashes with a Floating Point Exception in the GAMG pressure solver. The ring falls from z=0.35 to z=0.325, then velocities and accelerations blow up (1e73 m/s, 1e157 m/s²). The GAMG solver receives NaN/Inf pressure values and crashes.

This is a separate issue from the ring_sweep problems and does not block the sweep case (prescribed motion eliminates FSI entirely). Fixing it is deferred to the FSI reference run milestone.

## Implementation Steps

1. ~~Get one clean FSI run~~ → **Fix `ring_sweep/base/` first** (Problems 1–3 above), since prescribed motion avoids FSI entirely
2. **Fix ring STL** — make non-watertight (Problem 1)
3. **Fix missing fields/settings** — add `motionScale`, add `moveMeshOuterCorrectors` (Problems 2–3)
4. **Verify**: prescribed-motion run completes with ring moving downward at -2.0 m/s
5. Extract ring velocity profile (for non-constant-velocity sweeps) once FSI is stable
6. Write `sweep.py` to automate the parameter sweep
7. Run sweep and fit the scaling law exponents

## Validation Checkpoints

- [ ] ring_sweep base case: ring moves downward at prescribed velocity (cellZone has cells, mesh deforms)
- [ ] Prescribed motion run produces cavity/fountain dynamics comparable to FSI within ~10%
- [ ] FSI reference run completes without FPE (deferred)
- [ ] Parameter sweep produces monotonic trends (no random scatter)
- [ ] Scaling law exponents are physically reasonable (e.g., h_max/D grows with Fr)
