#!/usr/bin/env python3
"""
Generate STL file for ring geometry with new parameters.
"""

import numpy as np
import math

def generate_ring_stl(D, t, w, center=(0, 0, 0), resolution=60, filename="ring.stl"):
    """
    Generate an STL file for a ring geometry.
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

    # Create top and bottom faces (annular rings)
    # Top face: outer ring to inner ring
    for i in range(resolution):
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

    print(f"Generated ring STL: {filename}")
    print(f"  Outer diameter: {D} m, Thickness: {t} m, Width: {w} m")
    print(f"  Outer radius: {R} m, Inner radius: {r} m")
    print(f"  Center: {center}")
    print(f"  Resolution: {resolution} facets")
    print(f"  Total vertices: {len(vertices)}, Total faces: {len(faces)}")

if __name__ == "__main__":
    # New parameters based on theory.md analysis
    D = 0.05       # Outer diameter: 5 cm
    t = 0.0025     # Thickness: 2.5 mm
    w = 0.01       # Width: 1 cm
    center = (0, 0, 0.50)  # Initial position: 20 cm above water surface (z=0.3)

    filename = "constant/triSurface/ring.stl"
    generate_ring_stl(D, t, w, center, resolution=60, filename=filename)