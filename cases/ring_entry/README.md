# Ring Entry Case

OpenFOAM simulation case for ring water entry (IYPT 2026 Problem 3: Ring Fountain).

## Case Overview

This case simulates a metal ring falling into water from rest, generating a fountain due to cavity collapse. The simulation uses:

- **Solver**: `overInterDyMFoam` (overset grid + VOF + 6-DoF rigid body motion)
- **Physics**: Two-phase (water/air) flow with free surface, surface tension, gravity
- **Geometry**: Rectangular domain 0.3×0.3×0.6m, water depth 0.3m
- **Ring**: Outer diameter D=0.05m, thickness t=0.0025m, width w=0.01m
- **Initial conditions**: Ring at z=0.35m (5cm above water), zero initial velocity

## Case Setup

### Geometric Parameters
- Domain: 0.3m × 0.3m × 0.6m (x × y × z)
- Water depth: 0.3m (bottom half)
- Ring outer diameter: 0.05m (5cm)
- Ring thickness: 0.0025m (2.5mm)
- Ring width: 0.01m (1cm)
- Ring initial position: (0, 0, 0.35)m
- Ring initial velocity: (0, 0, 0)m/s (free fall under gravity)

### Dimensionless Parameters
- Froude number (Fr): ~2.0
- Weber number (We): ~1400
- Bond number (Bo): ~350
- Thickness ratio (η = t/D): 0.05

### Mesh Configuration
- Background mesh: 10×10×20 cells (4,000 cells)
- Surface refinement: Level (4 4) on ring surface
- Local refinement: Small box around ring, level 1
- Expected total cells: < 100,000

## Files and Directories

```
ring_entry/
├── 0/                    # Initial field files (from disk_impact)
├── 0.orig/              # Backup of clean initial fields
├── constant/
│   ├── dynamicMeshDict  # 6-DoF motion configuration
│   ├── g                # Gravity acceleration
│   ├── transportProperties # Phase properties
│   ├── physicalProperties.* # Material properties
│   ├── triSurface/      # STL geometry
│   └── turbulenceProperties # Turbulence model
├── system/
│   ├── blockMeshDict    # Background mesh
│   ├── controlDict      # Time control, output
│   ├── fvSchemes        # Discretization schemes
│   ├── fvSolution       # Solver settings
│   ├── snappyHexMeshDict # Mesh refinement
│   ├── setFieldsDict    # Initial field setup
│   ├── topoSetDict      # Cell set creation
│   └── decomposeParDict # Parallel decomposition
├── Allrun              # Run script
├── Allclean            # Clean script
├── generate_ring.py    # STL generation script
└── README.md           # This file
```

## Running the Case

### Prerequisites
- OpenFOAM Foundation edition v12
- Python3 with numpy (for STL generation if needed)

### Quick Start
```bash
# 1. Source OpenFOAM
source /opt/openfoam12/etc/bashrc

# 2. Run the case
cd /root/ringfountain/cases/ring_entry
./Allrun
```

### Manual Steps
```bash
# Clean previous results
./Allclean

# Generate background mesh
blockMesh

# Refine mesh around ring
snappyHexMesh -overwrite

# Create cell set for ring
topoSet

# Set initial fields (water phase)
setFields

# Run solver (test with short endTime)
overInterDyMFoam
```

## Key Configuration Details

### Dynamic Mesh (`constant/dynamicMeshDict`)
- `sixDoFRigidBodyMotion` solver
- `patches (ringSurface)` for force calculation
- Initial velocity: (0, 0, 0) - free fall under gravity
- Centre of mass: (0, 0, 0.35)m
- Soft wall restraint at bottom

### Overset Interpolation (`system/fvSchemes`)
- `oversetInterpolation` with `inverseDistance` method
- `oversetInterpolationSuppressed` for pressure gradient

### Initial Conditions
- Water phase: α=1 for z < 0.3m
- Air phase: α=0 for z > 0.3m
- Velocity field: uniform (0, 0, 0)
- Pressure: hydrostatic

### Boundary Conditions
- `bottom`: wall, no-slip
- `walls`: wall, no-slip
- `atmosphere`: patch, pressure inlet/outlet
- `ringSurface`: wall, moving wall velocity (for 6-DoF)

## Known Issues and Solutions

### 1. Field File Size Mismatch
**Problem**: `setFields` fails with "size X is not equal to the given value of Y" error.
**Solution**: Clean 0 directory completely:
```bash
rm -rf 0 && cp -r /root/RingFountain/disk_impact/0 .
cp /root/RingFountain/ring_fountain/base_case/0/{pointDisplacement,motionScale} 0/
```

### 2. ringSurface Boundary Patch Missing
**Problem**: `sixDoFRigidBodyMotion` cannot find `ringSurface` patch.
**Solution**: The case configures `snappyHexMesh` to create `ringSurface` as boundary patch. If missing:
- Check `constant/polyMesh/boundary` for `ringSurface`
- Try running `createBaffles` to create patch from faceZone

### 3. Mesh Explosion
**Problem**: Too many cells (>1M) causing memory issues.
**Solution**: Already addressed by:
- Reduced background mesh (10×10×20 vs 20×20×40)
- Smaller refinement box around ring
- Lower refinement level in box (level 1 vs level 3)

### 4. Solver Compatibility
**Problem**: `overInterDyMFoam` not found or fails.
**Solution**: Ensure OpenFOAM Foundation v12 is sourced:
```bash
source /opt/openfoam12/etc/bashrc
```

## Post-processing

### Visualization
```bash
paraFoam
```

### Probe Data
- Probe locations at various heights in `system/controlDict`
- Data in `postProcessing/probes/`

### Force Coefficients
- Forces on ring in `postProcessing/forces/`
- Ring state in `postProcessing/sixDoFRigidBodyState/`

### Fountain Surface
- α=0.5 isosurface in `postProcessing/fountainSurface/`

## References

1. IYPT 2026 Problem 3: Ring Fountain
2. Gekle & Gordillo (2010) cavity collapse theory
3. OpenFOAM Foundation v12 documentation
4. `/root/ringfountain/README.md` - Project overview
5. `/root/ringfountain/Theory.md` - Theoretical background

## Test Configuration

For initial testing:
- `endTime`: 0.1s (in `system/controlDict`)
- `writeInterval`: 0.01s
- Solver runs in background for quick validation

For full simulation, increase `endTime` to 1.0-2.0s in `system/controlDict`.