#!/usr/bin/env python3
"""
Generate a non-watertight ring STL for the ring_sweep prescribed-motion case.

The STL is deliberately punctured (a few top-cap facets omitted) so that
snappyHexMesh can populate the `ringZone` cellZone correctly.

Why: A watertight torus causes snappyHexMesh to split the domain into two
disconnected regions (ring interior vs. exterior). With a single
`locationInMesh` outside the ring, interior cells are removed, and
`cellZoneInside inside` yields zero cells. The solidBody motion solver
then has nothing to move.

Fix: Omit 2 adjacent top-cap segments (4 facets) to connect ring interior
to exterior through a small hole. snappyHexMesh then keeps all cells and
populates ringZone correctly.
"""

import numpy as np
import math
import argparse
import os


def generate_ring_stl(D, t, w, center=(0, 0, 0), resolution=60,
                      puncture_segments=2, filename="ring.stl"):
    """
    Generate an STL file for a ring geometry.

    Parameters
    ----------
    puncture_segments : int
        Number of adjacent top-cap segments to omit. Default 2 (4 facets)
        makes the STL non-watertight so snappyHexMesh populates the
        cellZone. Set to 0 for a fully closed surface.
    """
    R = D / 2.0
    r = (D - 2*t) / 2.0

    cx, cy, cz = center

    # Create vertices for outer and inner cylinders
    vertices = []
    faces = []

    # Generate vertices for outer cylinder (top and bottom)
    for i in range(resolution):
        angle = 2 * math.pi * i / resolution
        x_outer = R * math.cos(angle)
        y_outer = R * math.sin(angle)

        # Bottom vertices (z = -w/2)
        vertices.append((x_outer + cx, y_outer + cy, cz - w/2))
        # Top vertices (z = w/2)
        vertices.append((x_outer + cx, y_outer + cy, cz + w/2))

    # Generate vertices for inner cylinder (top and bottom)
    inner_start = 2 * resolution
    for i in range(resolution):
        angle = 2 * math.pi * i / resolution
        x_inner = r * math.cos(angle)
        y_inner = r * math.sin(angle)

        # Bottom vertices (z = -w/2)
        vertices.append((x_inner + cx, y_inner + cy, cz - w/2))
        # Top vertices (z = w/2)
        vertices.append((x_inner + cx, y_inner + cy, cz + w/2))

    # Create faces for outer cylinder side
    for i in range(resolution):
        next_i = (i + 1) % resolution

        # Outer cylinder side faces (quads as two triangles)
        v0 = i * 2          # outer bottom current
        v1 = next_i * 2     # outer bottom next
        v2 = i * 2 + 1      # outer top current
        v3 = next_i * 2 + 1 # outer top next

        # First triangle
        faces.append((v0, v1, v2))
        # Second triangle
        faces.append((v1, v3, v2))

    # Create faces for inner cylinder side
    for i in range(resolution):
        next_i = (i + 1) % resolution

        # Inner cylinder side faces
        v0 = inner_start + i * 2          # inner bottom current
        v1 = inner_start + next_i * 2     # inner bottom next
        v2 = inner_start + i * 2 + 1      # inner top current
        v3 = inner_start + next_i * 2 + 1 # inner top next

        # Note: inner faces need opposite orientation (facing inward)
        faces.append((v0, v2, v1))
        faces.append((v1, v2, v3))

    # Build set of segments to skip in top cap (deliberate puncture)
    skip_segments = set(range(puncture_segments))

    # Create top and bottom faces (annular rings)
    # Top face: outer ring to inner ring (with deliberate puncture)
    for i in range(resolution):
        if i in skip_segments:
            continue
        next_i = (i + 1) % resolution

        # Top face triangles (outer -> inner)
        v0_outer = i * 2 + 1          # outer top current
        v1_outer = next_i * 2 + 1     # outer top next
        v0_inner = inner_start + i * 2 + 1      # inner top current
        v1_inner = inner_start + next_i * 2 + 1 # inner top next

        # First triangle (outer current -> outer next -> inner current)
        faces.append((v0_outer, v1_outer, v0_inner))
        # Second triangle (outer next -> inner next -> inner current)
        faces.append((v1_outer, v1_inner, v0_inner))

    # Bottom face: outer ring to inner ring
    for i in range(resolution):
        next_i = (i + 1) % resolution

        # Bottom face triangles (outer -> inner)
        v0_outer = i * 2              # outer bottom current
        v1_outer = next_i * 2         # outer bottom next
        v0_inner = inner_start + i * 2          # inner bottom current
        v1_inner = inner_start + next_i * 2     # inner bottom next

        # Note: bottom faces need opposite orientation (facing downward)
        faces.append((v0_outer, v0_inner, v1_outer))
        faces.append((v1_outer, v0_inner, v1_inner))

    # Write STL file
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, 'w') as f:
        f.write("solid ring\n")

        for face in faces:
            # Get triangle vertices
            v0 = vertices[face[0]]
            v1 = vertices[face[1]]
            v2 = vertices[face[2]]

            # Calculate normal (cross product of edges)
            edge1 = np.array(v1) - np.array(v0)
            edge2 = np.array(v2) - np.array(v0)
            normal = np.cross(edge1, edge2)
            norm = np.linalg.norm(normal)
            if norm > 0:
                normal = normal / norm
            else:
                normal = np.array([0, 0, 1])

            # Write facet
            f.write(f"  facet normal {normal[0]:.6e} {normal[1]:.6e} {normal[2]:.6e}\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {v0[0]:.6e} {v0[1]:.6e} {v0[2]:.6e}\n")
            f.write(f"      vertex {v1[0]:.6e} {v1[1]:.6e} {v1[2]:.6e}\n")
            f.write(f"      vertex {v2[0]:.6e} {v2[1]:.6e} {v2[2]:.6e}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")

        f.write("endsolid ring\n")

    n_facets = len(faces)
    n_removed = 2 * puncture_segments
    print(f"Generated ring STL: {filename}")
    print(f"  D={D:.4f} m, t={t:.4f} m, w={w:.4f} m, center=({cx},{cy},{cz})")
    print(f"  resolution={resolution}, total facets={n_facets}")
    if puncture_segments > 0:
        print(f"  PUNCTURED: {n_removed} top-cap facets removed "
              f"({puncture_segments} segments)")
        print(f"  STL is NON-WATERTIGHT (deliberate) for cellZone compatibility")
    else:
        print(f"  STL is watertight")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate ring STL for ring_sweep prescribed-motion case")
    parser.add_argument("-D", type=float, default=0.05,
                        help="Outer diameter [m] (default: 0.05)")
    parser.add_argument("-t", type=float, default=0.0025,
                        help="Wall thickness [m] (default: 0.0025)")
    parser.add_argument("-w", type=float, default=0.01,
                        help="Ring width/height [m] (default: 0.01)")
    parser.add_argument("--cz", type=float, default=0.35,
                        help="Initial z-centre [m] (default: 0.35)")
    parser.add_argument("--resolution", type=int, default=60,
                        help="Angular segments (default: 60)")
    parser.add_argument("--puncture-segments", type=int, default=2,
                        help="Top-cap segments to omit for non-watertight STL "
                             "(default: 2, set 0 for closed)")
    parser.add_argument("-o", "--output", default="constant/triSurface/ring.stl",
                        help="Output path (default: constant/triSurface/ring.stl)")
    args = parser.parse_args()

    generate_ring_stl(
        D=args.D, t=args.t, w=args.w,
        center=(0, 0, args.cz),
        resolution=args.resolution,
        puncture_segments=args.puncture_segments,
        filename=args.output)