import sympy as sp
from sympy import Point3D, sqrt, Rational, Plane
from itertools import combinations

def norm_sq(p1, p2):
    return sp.simplify((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def dist(p1, p2):
    return sp.simplify(sqrt(norm_sq(p1, p2)))

def edge_lengths(vertices):
    return [dist(u, v) for u, v in combinations(vertices, 2)]

def volume_tetrahedron(A, B, C, D):
    # Volume = 1/6 * |(A-D) dot ((B-D) x (C-D))|
    M = sp.Matrix([
        [A.x - D.x, A.y - D.y, A.z - D.z],
        [B.x - D.x, B.y - D.y, B.z - D.z],
        [C.x - D.x, C.y - D.y, C.z - D.z]
    ])
    return sp.simplify(abs(M.det()) / 6)

def print_stats(name, vertices, T_vol):
    print(f"\n--- Case: {name} ---")
    
    vol = volume_tetrahedron(*vertices)
    print(f"Volume: {vol} (Ratio to T: {sp.simplify(vol/T_vol)})")
    
    edges = edge_lengths(vertices)
    edges.sort(key=lambda x: x.evalf())
    print("Edge lengths (sorted):")
    for e in edges:
        sq = sp.simplify(e**2)
        print(f"  {e}  [squared: {sq}]")
    
    # Quick sanity check for 8T-LE proportions if n=8
    if name == "n=8 (8T-LE partition piece)":
        sq_edges = [sp.simplify(e**2) for e in edges]
        min_sq = min(sq_edges)
        proportions = [sp.simplify(sq / min_sq) for sq in sq_edges]
        print(f"Squared edge proportions: {proportions}")

def main():
    # Regular Tetrahedron T coordinates (edge length 1)
    A = Point3D(0, 0, 0)
    B = Point3D(1, 0, 0)
    C = Point3D(Rational(1,2), sqrt(3)/2, 0)
    D = Point3D(Rational(1,2), sqrt(3)/6, sqrt(6)/3)
    
    T_vol = volume_tetrahedron(A, B, C, D)
    print(f"Volume of regular tetrahedron T: {T_vol}")
    
    # --- Case n=2: Median Bisection ---
    # Plane through AB and midpoint of CD
    M_CD = (C + D) / 2
    piece_n2 = [A, B, C, M_CD]
    print_stats("n=2 (Median bisection)", piece_n2, T_vol)
    
    # --- Case n=4: Two Orthogonal Median Planes ---
    # Planes through (AB, M_CD) and (CD, M_AB)
    M_AB = (A + B) / 2
    # The piece vertices are defined by cutting T with these two planes.
    # The two planes intersect along the line connecting M_AB and M_CD.
    # The resulting 4 pieces are tetrahedra with vertices like (A, M_AB, C, M_CD)
    piece_n4 = [A, M_AB, C, M_CD]
    print_stats("n=4 (Quadrisection)", piece_n4, T_vol)
    
    # --- Case n=24: Full Barycentric Subdivision (Orthoscheme) ---
    G_ABC = (A + B + C) / 3
    G_T = (A + B + C + D) / 4
    piece_n24 = [A, M_AB, G_ABC, G_T]
    print_stats("n=24 (Orthoscheme)", piece_n24, T_vol)

    # --- Case n=8: 8T-LE Sub-piece ---
    # According to PPS23, the 8T-LE pieces form exactly 8 congruent tetrahedra 
    # of squared edge ratio [3, 2, 1, 1, 1, 1].
    # By dissecting the n=4 piece appropriately (bisecting its longest edge), we get the n=8 piece.
    # The longest edge of the $n=4$ piece is AC = 1. Its midpoint is M_AC.
    M_AC = (A + C) / 2
    piece_n8 = [A, M_AB, M_AC, M_CD]
    print_stats("n=8 (8T-LE partition piece)", piece_n8, T_vol)

if __name__ == "__main__":
    main()
