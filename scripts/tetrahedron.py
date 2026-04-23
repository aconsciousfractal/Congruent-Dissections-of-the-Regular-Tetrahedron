"""
tetrahedron.py — Canonical regular tetrahedron definition and utilities.
"""
import numpy as np


def regular_tetrahedron(edge_length: float = 1.0):
    """
    Return the 4 vertices of a regular tetrahedron with given edge length.
    
    Embedding: edge AB along x-axis, face ABC in the xy-plane.
    
    Returns:
        tuple of 4 numpy arrays (A, B, C, D), each shape (3,).
    """
    a = edge_length
    A = np.array([0.0, 0.0, 0.0])
    B = np.array([a, 0.0, 0.0])
    C = np.array([a / 2, a * np.sqrt(3) / 2, 0.0])
    D = np.array([a / 2, a * np.sqrt(3) / 6, a * np.sqrt(2.0 / 3.0)])
    return A, B, C, D


def volume(edge_length: float = 1.0) -> float:
    """Volume of a regular tetrahedron with given edge length."""
    return (edge_length ** 3) * np.sqrt(2) / 12


def barycentre(A, B, C, D):
    """Barycentre (centroid) of the tetrahedron."""
    return (A + B + C + D) / 4.0


def edge_midpoint(P, Q):
    """Midpoint of edge PQ."""
    return (P + Q) / 2.0


def face_centroid(P, Q, R):
    """Centroid of triangle PQR."""
    return (P + Q + R) / 3.0


def tet_volume_from_vertices(v0, v1, v2, v3) -> float:
    """Volume of tetrahedron given 4 vertices."""
    mat = np.column_stack([v1 - v0, v2 - v0, v3 - v0])
    return abs(np.linalg.det(mat)) / 6.0


def distance_matrix(vertices):
    """
    Compute the sorted pairwise distance multiset for a set of vertices.
    
    Args:
        vertices: list/array of 3D points.
    
    Returns:
        Sorted list of pairwise distances.
    """
    n = len(vertices)
    dists = []
    for i in range(n):
        for j in range(i + 1, n):
            dists.append(np.linalg.norm(np.array(vertices[i]) - np.array(vertices[j])))
    return sorted(dists)
