"""
dissections.py — Constructors for each known congruent dissection of the regular tetrahedron.

Each function returns a list of pieces, where each piece is a list of vertex arrays.
"""
import numpy as np
from tetrahedron import (
    regular_tetrahedron, edge_midpoint, face_centroid, barycentre
)


def dissect_n1(A, B, C, D):
    """n=1: trivial (the whole tetrahedron)."""
    return [[A, B, C, D]]


def dissect_n2(A, B, C, D):
    """
    n=2: Median bisection.
    Cut through edge AB and midpoint of opposite edge CD.
    """
    M_CD = edge_midpoint(C, D)
    piece1 = [A, B, C, M_CD]
    piece2 = [A, B, D, M_CD]
    return [piece1, piece2]


def dissect_n3(A, B, C, D):
    """
    n=3: Axial trisection.
    Three planes through vertex D and axis D→centroid(ABC),
    each passing through one base vertex. Pieces are tetrahedra.
    """
    G_ABC = face_centroid(A, B, C)
    piece1 = [D, G_ABC, A, B]
    piece2 = [D, G_ABC, B, C]
    piece3 = [D, G_ABC, C, A]
    return [piece1, piece2, piece3]


def dissect_n24(A, B, C, D):
    """
    n=24: Full barycentric subdivision (orthoschemes).
    Each piece = conv(vertex, edge_midpoint, face_centroid, barycentre).
    One piece per flag (vertex, edge, face).
    """
    G = barycentre(A, B, C, D)
    vertices = {'A': A, 'B': B, 'C': C, 'D': D}
    vnames = ['A', 'B', 'C', 'D']
    
    # All edges as ordered pairs
    edges = []
    for i in range(4):
        for j in range(i+1, 4):
            edges.append((vnames[i], vnames[j]))
    
    # All faces as triples
    faces = []
    for i in range(4):
        for j in range(i+1, 4):
            for k in range(j+1, 4):
                faces.append((vnames[i], vnames[j], vnames[k]))
    
    pieces = []
    for face in faces:
        fc = face_centroid(vertices[face[0]], vertices[face[1]], vertices[face[2]])
        # Each face has 3 edges, each edge has 2 vertices → 6 flags per face
        face_edges = []
        for i in range(3):
            for j in range(i+1, 3):
                face_edges.append((face[i], face[j]))
        
        for edge in face_edges:
            em = edge_midpoint(vertices[edge[0]], vertices[edge[1]])
            # Each edge in this face has 2 vertices
            for v in edge:
                piece = [vertices[v], em, fc, G]
                pieces.append(piece)
    
    return pieces


# Placeholder functions for cases not yet fully reconstructed

def dissect_n4(A, B, C, D):
    """
    n=4: Two orthogonal median planes.
    Planes through (AB, M_CD) and (CD, M_AB).
    """
    M_AB = edge_midpoint(A, B)
    M_CD = edge_midpoint(C, D)
    piece1 = [A, M_AB, C, M_CD]
    piece2 = [A, M_AB, D, M_CD]
    piece3 = [B, M_AB, C, M_CD]
    piece4 = [B, M_AB, D, M_CD]
    return [piece1, piece2, piece3, piece4]


def dissect_n6(A, B, C, D):
    """
    n=6: Hexasection via 3 median-of-base planes through the altitude axis.
    Each S3 piece is bisected by the median from G_ABC through the opposite edge midpoint.
    """
    G_ABC = face_centroid(A, B, C)
    M_AB = edge_midpoint(A, B)
    M_BC = edge_midpoint(B, C)
    M_CA = edge_midpoint(C, A)
    return [
        [D, G_ABC, A, M_AB],
        [D, G_ABC, M_AB, B],
        [D, G_ABC, B, M_BC],
        [D, G_ABC, M_BC, C],
        [D, G_ABC, C, M_CA],
        [D, G_ABC, M_CA, A],
    ]


def dissect_n8(A, B, C, D):
    """
    n=8: 8T-LE partition (Padrón-Plaza-Suárez).
    Bisect each n=4 piece along its longest edge (the original T-edge).

    n=4 pieces (from two orthogonal median planes):
      P1=[A,M_AB,C,M_CD], P2=[A,M_AB,D,M_CD],
      P3=[B,M_AB,C,M_CD], P4=[B,M_AB,D,M_CD].
    Longest edges: A-C, A-D, B-C, B-D (all length 1).
    Bisect each at the midpoint of that edge.
    """
    M_AB = edge_midpoint(A, B)
    M_CD = edge_midpoint(C, D)
    M_AC = edge_midpoint(A, C)
    M_BC = edge_midpoint(B, C)
    M_AD = edge_midpoint(A, D)
    M_BD = edge_midpoint(B, D)
    return [
        # P1=[A,M_AB,C,M_CD] bisected at M_AC
        [A,  M_AB, M_AC, M_CD],
        [M_AC, M_AB, C, M_CD],
        # P2=[A,M_AB,D,M_CD] bisected at M_AD
        [A,  M_AB, M_AD, M_CD],
        [M_AD, M_AB, D, M_CD],
        # P3=[B,M_AB,C,M_CD] bisected at M_BC
        [B,  M_AB, M_BC, M_CD],
        [M_BC, M_AB, C, M_CD],
        # P4=[B,M_AB,D,M_CD] bisected at M_BD
        [B,  M_AB, M_BD, M_CD],
        [M_BD, M_AB, D, M_CD],
    ]


def dissect_n12(A, B, C, D):
    """
    n=12: Fundamental domain of A4 ⊂ Td.
    Each piece = merge of 2 adjacent S24 orthoschemes with opposite flag parity.
    """
    from .tetra_axial import build_S12_pieces
    return build_S12_pieces()
