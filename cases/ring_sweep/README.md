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
| Mesh motion | `rigidBodyMotion` + Newmark solver | `solidBody` + `linearMotion` |
| Timestep control | `maxCo 0.1`, `maxDeltaT 2e-5` | `maxCo 0.1`, no `maxDeltaT` |
| PIMPLE outer correctors | 5 | 3 |
| Acceleration relaxation | 0.3 | Not needed |
| Stability | FPE-prone | Stable |
| Runtime per case | Long (small deltaT) | Shorter |

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

## Current Status (2026-07-09)

The `base/` case now has complete configuration files (system/, constant/) and the core issues identified earlier (empty cellZone, missing motionScale, missing moveMeshOuterCorrectors) have been resolved. See [SOLUTIONS.md](base/SOLUTIONS.md) for the full diagnosis and fix strategy.

Key fixes applied:
- **cellZone**: Switched from `snappyHexMesh cellZoneInside` to `topoSet cylinderToCell` subtraction — robustly populates `ringZone` regardless of wall thinness (Problem 1)
- **motionScale**: Field now present in `0/` (Problem 2)
- **moveMeshOuterCorrectors**: Now set to `yes` in fvSolution (Problem 3)
- **Forces**: `ringSurface` created as boundary patch (not internal faceZone) for force measurements
- **Refinement**: Increased from (4 4) to (5 6) for better surface representation

### Remaining work

- [ ] Verify prescribed-motion run completes with ring moving downward at -2.0 m/s
- [ ] Fix `ring_entry` FSI stability (separate issue, see ring_entry/README.md)
- [ ] Extract ring velocity profile from one successful FSI run
- [ ] Write `sweep.py` to automate parameter sweep
- [ ] Run sweep and fit scaling law exponents

## Validation Checkpoints

- [ ] ring_sweep base case: ring moves downward at prescribed velocity (cellZone has cells, mesh deforms)
- [ ] Prescribed motion run produces cavity/fountain dynamics comparable to FSI within ~10%
- [ ] Parameter sweep produces monotonic trends (no random scatter)
- [ ] Scaling law exponents are physically reasonable (e.g., h_max/D grows with Fr)
