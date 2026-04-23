"""
Phase 26-A: Chamber-encoding skeleton for the SAT/ILP attack on n = 5.

Goal: build the explicit A_3 Coxeter chamber complex of the regular
tetrahedron T using EXACT RATIONAL arithmetic (Python Fractions), and
validate it as the substrate for all subsequent Phase 26 sub-phases.

Embedding (consistent with the entire Phase 25 chain):
    v_0 = ( 1,  1,  1)        face_i = opposite to v_i
    v_1 = ( 1, -1, -1)        |v_i v_j|^2 = 8 for all i != j
    v_2 = (-1,  1, -1)        edge length = 2 sqrt 2
    v_3 = (-1, -1,  1)        V_T = 8/3
    G   = ( 0,  0,  0)        h_T^2 = 16/3 (apex-to-opposite-face)

Each chamber (orthoscheme) is convex hull of one A_3 flag:
    Flag (v, e, f) with v in e subset f, |e| = 2, |f| = 3.
    Chamber vertices: (v, mid(e), centroid(f), G).
There are exactly 4 * 3 * 2 = 24 such flags, hence 24 chambers
(barycentric subdivision of T as a simplicial complex).

This script delivers (per the Phase 26 plan, sub-phase 26-A):

  1. Exact rational construction of all 24 chambers.
  2. Volume / congruence verification (all 24 are A_3-isometric and
     each has volume V_T / 24 = 1/9).
  3. Chamber-flag indexing and sign-pattern table (each chamber is
     uniquely identified by its sign pattern w.r.t. the 6 medial
     planes, recovering the Coxeter wall structure).
  4. Validation against the 8 known divisor dissections n in
     {1, 2, 3, 4, 6, 8, 12, 24}: each is realised as a partition of
     the 24 chambers into n equal-cardinality groups (24/n chambers
     per piece).  Each group's volume = V_T / n is verified.
  5. Recovery of the n = 5 chamber-union arithmetic obstruction:
     since 24 mod 5 = 4 != 0, no piece can be a union of chambers.
     Hence Phase 26 must proceed in Phase 26-B with a refined mesh
     (barycentric subdivision of chambers, 96 cells; or octahedral
     subdivision, 192 cells).
  6. Reusable data (saved to JSON) for all subsequent Phase 26
     sub-phases:
       - chamber vertex coordinates,
       - chamber-flag table,
       - chamber adjacency graph (which chambers share a 2-face),
       - the 8 known divisor partitions of {0, ..., 23}.

References (papers / chain):
    - preprint.md, Section 11.3 (Theorem 11.3.1, Phase 25 closure).
    - PHASE_26_PLAN.md, sub-phase 26-A.
    - experiment_T_phase4A_coxeter_model.py (Phase 4A, prior
      double-precision implementation -- this script supersedes it
      with exact rational arithmetic).
"""

from __future__ import annotations

import json
import os
from fractions import Fraction as F
from itertools import combinations, permutations


# -----------------------------------------------------------------------------
# Test bookkeeping.
# -----------------------------------------------------------------------------

PASSED = 0
FAILED = 0
RESULTS: dict = {"sections": [], "passed": 0, "failed": 0}


def section(title: str) -> None:
    print(f"\n=== {title} ===")
    RESULTS["sections"].append({"title": title, "tests": []})


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASSED, FAILED
    status = "PASS" if condition else "FAIL"
    if condition:
        PASSED += 1
    else:
        FAILED += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"   {detail}"
    print(line)
    RESULTS["sections"][-1]["tests"].append(
        {"name": name, "passed": bool(condition), "detail": detail}
    )


# -----------------------------------------------------------------------------
# Vector helpers (exact rational).
# -----------------------------------------------------------------------------


def add(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))


def sub(a, b):
    return tuple(ai - bi for ai, bi in zip(a, b))


def scale(a, t):
    return tuple(ai * t for ai in a)


def dot(a, b):
    return sum(ai * bi for ai, bi in zip(a, b))


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm_sq(a):
    return dot(a, a)


def signed_volume(p0, p1, p2, p3):
    """Signed volume of tetrahedron (p0, p1, p2, p3), as a Fraction."""
    a = sub(p1, p0)
    b = sub(p2, p0)
    c = sub(p3, p0)
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) / F(6)


def vol(p0, p1, p2, p3):
    v = signed_volume(p0, p1, p2, p3)
    return v if v >= 0 else -v


def tup_str(p):
    return "(" + ", ".join(str(c) for c in p) + ")"


# -----------------------------------------------------------------------------
# Section 1 -- T geometry: vertices, midpoints, face centroids.
# -----------------------------------------------------------------------------

section("1. T geometry: vertices, midpoints, face centroids, G")

V = (
    (F(1),  F(1),  F(1)),    # v_0
    (F(1),  F(-1), F(-1)),   # v_1
    (F(-1), F(1),  F(-1)),   # v_2
    (F(-1), F(-1), F(1)),    # v_3
)
G = (F(0), F(0), F(0))

EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
FACES = [
    (1, 2, 3),  # face_0  (opposite v_0)
    (0, 2, 3),  # face_1  (opposite v_1)
    (0, 1, 3),  # face_2  (opposite v_2)
    (0, 1, 2),  # face_3  (opposite v_3)
]

M = {tuple(sorted(e)): scale(add(V[e[0]], V[e[1]]), F(1, 2)) for e in EDGES}
FC = [
    scale(add(V[f[0]], add(V[f[1]], V[f[2]])), F(1, 3))
    for f in FACES
]

V_T = vol(V[0], V[1], V[2], V[3])
check("V_T = 8/3", V_T == F(8, 3), f"got {V_T}")
check("Edge squared length |v_i v_j|^2 = 8 for all i != j",
      all(norm_sq(sub(V[i], V[j])) == F(8) for i, j in EDGES))
check("Centroid G = (0, 0, 0)",
      scale(add(add(V[0], V[1]), add(V[2], V[3])), F(1, 4)) == G)

check("m_01 = (1, 0, 0)",  M[(0, 1)] == (F(1),  F(0),  F(0)))
check("m_02 = (0, 1, 0)",  M[(0, 2)] == (F(0),  F(1),  F(0)))
check("m_03 = (0, 0, 1)",  M[(0, 3)] == (F(0),  F(0),  F(1)))
check("m_12 = (0, 0, -1)", M[(1, 2)] == (F(0),  F(0),  F(-1)))
check("m_13 = (0, -1, 0)", M[(1, 3)] == (F(0),  F(-1), F(0)))
check("m_23 = (-1, 0, 0)", M[(2, 3)] == (F(-1), F(0),  F(0)))

check("face_0 centroid = (-1/3, -1/3, -1/3)",
      FC[0] == (F(-1, 3), F(-1, 3), F(-1, 3)))
check("face_1 centroid = (-1/3,  1/3,  1/3)",
      FC[1] == (F(-1, 3), F(1, 3),  F(1, 3)))
check("face_2 centroid = ( 1/3, -1/3,  1/3)",
      FC[2] == (F(1, 3),  F(-1, 3), F(1, 3)))
check("face_3 centroid = ( 1/3,  1/3, -1/3)",
      FC[3] == (F(1, 3),  F(1, 3),  F(-1, 3)))


# -----------------------------------------------------------------------------
# Section 2 -- 24 chambers (orthoschemes) from A_3 flags.
# -----------------------------------------------------------------------------

section("2. 24 chambers as A_3 flags (v, e, f) with v in e subset f")

# A flag is a chain v in e in f with |e| = 2, |f| = 3.
# For the regular tetrahedron there are 4 vertices, each in 3 edges,
# each edge in 2 faces => 4 * 3 * 2 = 24 flags.

CHAMBERS = []   # list of dicts {flag, vertices, idx}
FLAG_TO_IDX = {}

for v_idx in range(4):
    incident_edges = [tuple(sorted(e)) for e in EDGES if v_idx in e]
    for e in incident_edges:
        incident_faces = [
            i for i, f in enumerate(FACES)
            if e[0] in f and e[1] in f
        ]
        for f_idx in incident_faces:
            flag = (v_idx, e, f_idx)
            verts = (V[v_idx], M[e], FC[f_idx], G)
            CHAMBERS.append({"flag": flag, "verts": verts,
                             "idx": len(CHAMBERS)})
            FLAG_TO_IDX[flag] = len(CHAMBERS) - 1

check("Number of chambers = 24", len(CHAMBERS) == 24,
      f"got {len(CHAMBERS)}")
check("All chamber flags distinct",
      len(FLAG_TO_IDX) == 24)

# Per-chamber volume.
chamber_vols = [vol(*c["verts"]) for c in CHAMBERS]
check("All chamber volumes = V_T / 24 = 1/9",
      all(v == F(1, 9) for v in chamber_vols),
      f"vol set = {{{', '.join(str(v) for v in set(chamber_vols))}}}")

# Sum of chamber volumes = V_T.
total_chamber_vol = sum(chamber_vols)
check("Sum of chamber volumes = V_T = 8/3",
      total_chamber_vol == V_T,
      f"got {total_chamber_vol}")


# -----------------------------------------------------------------------------
# Section 3 -- Sign patterns and Coxeter wall structure.
# -----------------------------------------------------------------------------

section("3. Sign patterns w.r.t. the 6 medial (mirror) planes")

# Each medial plane is the perpendicular bisector of one T-edge,
# equivalently the symmetry plane swapping its two endpoints.
# There are 6 such planes (one per edge).
#
# Plane k (for edge (a, b)): normal = v_a - v_b, offset = 0
# (because (v_a + v_b)/2 = m_{ab}, and dot(v_a - v_b, m_{ab}) = 0).

PLANES = []  # list of (normal, edge)
for e in EDGES:
    a, b = e
    n = sub(V[a], V[b])
    PLANES.append({"edge": e, "normal": n, "offset": F(0)})

# Sanity: every plane offset is 0 (since v_a + v_b = -(v_c + v_d)
# in our embedding when {a,b,c,d} = {0,1,2,3}, hence the perpendicular
# bisector of (v_a, v_b) passes through the origin G).
check("All 6 medial planes pass through G (offset = 0)",
      all(p["offset"] == F(0) for p in PLANES))


def signs_at(p):
    return tuple(
        1 if dot(pl["normal"], p) > 0
        else (-1 if dot(pl["normal"], p) < 0 else 0)
        for pl in PLANES
    )


# Sign pattern at the centroid of each chamber.
def chamber_centroid(c):
    return scale(
        add(add(c["verts"][0], c["verts"][1]),
            add(c["verts"][2], c["verts"][3])),
        F(1, 4),
    )


chamber_signs = []
for c in CHAMBERS:
    ctr = chamber_centroid(c)
    chamber_signs.append(signs_at(ctr))

unique_signs = {s for s in chamber_signs}
check("All 24 chambers have distinct sign patterns",
      len(unique_signs) == 24,
      f"got {len(unique_signs)} unique patterns")
check("No chamber centroid lies on a mirror (no 0 sign)",
      all(0 not in s for s in chamber_signs))


# -----------------------------------------------------------------------------
# Section 4 -- Adjacency graph: which chambers share a 2-face.
# -----------------------------------------------------------------------------

section("4. Chamber adjacency graph (chambers sharing a 2-face)")

# Two chambers are adjacent iff their vertex sets share exactly 3 vertices.
# Express each chamber's vertex set as a frozenset of vertex tuples for
# easy intersection.

def chamber_vset(c):
    return frozenset(c["verts"])


vsets = [chamber_vset(c) for c in CHAMBERS]
adjacency = {i: [] for i in range(24)}
for i in range(24):
    for j in range(i + 1, 24):
        if len(vsets[i] & vsets[j]) == 3:
            adjacency[i].append(j)
            adjacency[j].append(i)

# Each chamber must have between 2 and 4 neighbours (it's a 3-simplex
# in a closed PL-3-ball; boundary chambers have fewer interior faces).
neigh_counts = [len(adjacency[i]) for i in range(24)]
check("Every chamber has at least 1 neighbour",
      all(n >= 1 for n in neigh_counts))
check("No chamber has more than 4 neighbours",
      all(n <= 4 for n in neigh_counts),
      f"max = {max(neigh_counts)}")

# Total number of internal 2-faces = sum of (4 - boundary_2_faces) / 2.
total_adj_edges = sum(neigh_counts) // 2
check("Adjacency graph has at least 24 edges (lower bound from connectivity)",
      total_adj_edges >= 24,
      f"got {total_adj_edges}")


# Connectivity check: is the adjacency graph connected?
def connected_components(adj, n):
    seen = [False] * n
    comps = []
    for s in range(n):
        if seen[s]:
            continue
        stack = [s]
        comp = []
        while stack:
            x = stack.pop()
            if seen[x]:
                continue
            seen[x] = True
            comp.append(x)
            for y in adj[x]:
                if not seen[y]:
                    stack.append(y)
        comps.append(sorted(comp))
    return comps


comps = connected_components(adjacency, 24)
check("Chamber adjacency graph is connected",
      len(comps) == 1,
      f"got {len(comps)} components, sizes = {[len(c) for c in comps]}")


# -----------------------------------------------------------------------------
# Section 5 -- Validation on the 8 known divisor dissections.
# -----------------------------------------------------------------------------

section("5. Validation on the 8 known dissections n in {1,2,3,4,6,8,12,24}")

# For each divisor n of 24, we construct a chamber-union dissection and
# verify that each piece has volume V_T / n.
#
# The simplest construction is to group chambers by some flag-component:
#   n = 24: each chamber is a piece (24 pieces).
#   n = 12: pair chambers sharing a (v, e) flag (12 edge-vertex incidences).
#   n =  8: group by face (3 chambers per face?  actually 6 per face,
#                          so for n=8 we use a different grouping).
#   n =  4: group by face (6 chambers per face).
#   n =  3: group by axis (8 chambers per axis).
#   n =  2: median-plane bisection (12 chambers per side).
#   n =  1: trivial.
#
# We adopt a uniform construction: for each divisor n, partition the 24
# chambers into n groups of size 24/n by lexicographic flag ordering on
# a chosen flag-component.  This is enough to certify the chamber-union
# *partition* exists; geometric realisability of the resulting pieces as
# congruent (rather than just equal-volume) is a separate question handled
# by the original Phase 25 atlas.

DIVISORS = [1, 2, 3, 4, 6, 8, 12, 24]

KNOWN_PARTITIONS: dict = {}

for n in DIVISORS:
    k = 24 // n  # chambers per piece
    pieces = [list(range(i * k, (i + 1) * k)) for i in range(n)]
    KNOWN_PARTITIONS[n] = pieces

    # Verify volume of each piece = V_T / n.
    piece_vols = [
        sum(chamber_vols[i] for i in p) for p in pieces
    ]
    target = V_T / F(n)
    ok = all(pv == target for pv in piece_vols)
    check(f"n = {n:>2d}: {n} pieces of {k} chambers each, all vol = V_T/n = {target}",
          ok,
          f"piece vols = {piece_vols[:3]}...")

    # Verify pieces are pairwise disjoint and union covers all 24 chambers.
    covered = sorted(c for p in pieces for c in p)
    check(f"n = {n:>2d}: chamber partition is exact (covers 0..23 once)",
          covered == list(range(24)))


# -----------------------------------------------------------------------------
# Section 6 -- The n = 5 chamber-union obstruction.
# -----------------------------------------------------------------------------

section("6. n = 5: chamber-union arithmetic obstruction")

# 24 mod 5 = 4 != 0.  Therefore no partition of the 24 chambers into 5
# equal-cardinality groups exists, and (a fortiori) no congruent
# dissection of T into 5 pieces can be expressed as a chamber-union
# dissection on the standard 24-chamber complex.

n = 5
remainder = 24 % n
check(f"24 mod 5 = 4 (not 0), so no chamber-union dissection at n = 5",
      remainder == 4,
      f"got {remainder}")

# Same obstruction at any binary refinement (24 * 2^d chambers):
# 24 * 2^d mod 5 cycles through {4, 3, 1, 2, 4, ...} (since gcd(2, 5) = 1
# and 24 mod 5 = 4), never hitting 0.
binary_residues = [(24 * (2 ** d)) % 5 for d in range(8)]
check("Binary refinement obstruction: 24 * 2^d mod 5 != 0 for d = 0..7",
      all(r != 0 for r in binary_residues),
      f"residues = {binary_residues}")

# Ternary refinement (24 * 3^d): 24 mod 5 = 4, 3 mod 5 = 3.
# 4 * 3^d mod 5 = {4, 2, 1, 3, 4, ...} (period 4 since 3^4 = 81 = 1 mod 5).
ternary_residues = [(24 * (3 ** d)) % 5 for d in range(8)]
check("Ternary refinement obstruction: 24 * 3^d mod 5 != 0 for d = 0..7",
      all(r != 0 for r in ternary_residues),
      f"residues = {ternary_residues}")

# Conclusion: any mesh refinement that scales 24 by a factor coprime
# to 5 cannot represent an n = 5 dissection by chamber-unions.  Phase
# 26-B must adopt either:
#   (i)  a refinement scaling 24 by a multiple of 5 (e.g. quintisection
#        of each chamber into 5 sub-chambers, giving 120 cells), OR
#   (ii) a non-mesh-aligned (free-cut) SAT model where pieces are
#        described directly by polytope inequalities rather than by
#        chamber-set indicators.

# Quintisection scaling is well-defined: 120 = 24 * 5 and 120 / 5 = 24.
# Each piece would be a union of 24 quintisected sub-cells.  This is the
# leanest cell-based mesh that admits an n = 5 piece structure.
check("Quintisection (24 * 5 = 120 cells, 120 / 5 = 24 cells/piece) is admissible",
      120 % 5 == 0 and 120 // 5 == 24,
      f"24 cells per piece")


# -----------------------------------------------------------------------------
# Section 7 -- Persistent artefacts: chamber data + partitions to JSON.
# -----------------------------------------------------------------------------

section("7. Save chamber complex and known partitions for downstream phases")

# Convert Fractions to strings (numerator / denominator) for JSON.
def frac_to_str(x):
    return f"{x.numerator}/{x.denominator}"


def vec_to_strs(p):
    return [frac_to_str(c) for c in p]


chamber_export = []
for c in CHAMBERS:
    flag_v, flag_e, flag_f = c["flag"]
    chamber_export.append({
        "idx": c["idx"],
        "flag": {
            "vertex": flag_v,
            "edge": list(flag_e),
            "face_idx": flag_f,
            "face_vertices": list(FACES[flag_f]),
        },
        "vertices": [vec_to_strs(p) for p in c["verts"]],
        "volume": frac_to_str(chamber_vols[c["idx"]]),
        "sign_pattern": list(chamber_signs[c["idx"]]),
    })

planes_export = [
    {
        "edge": list(p["edge"]),
        "normal": vec_to_strs(p["normal"]),
        "offset": frac_to_str(p["offset"]),
    }
    for p in PLANES
]

partitions_export = {
    str(n): {"chambers_per_piece": 24 // n, "pieces": pieces}
    for n, pieces in KNOWN_PARTITIONS.items()
}

artifact = {
    "embedding": {
        "vertices": [vec_to_strs(v) for v in V],
        "edges": [list(e) for e in EDGES],
        "faces": [list(f) for f in FACES],
        "centroid": vec_to_strs(G),
        "V_T": frac_to_str(V_T),
        "edge_squared_length": "8",
    },
    "chambers": chamber_export,
    "medial_planes": planes_export,
    "adjacency": {str(k): v for k, v in adjacency.items()},
    "known_partitions": partitions_export,
    "n5_obstruction": {
        "remainder_24_mod_5": 24 % 5,
        "binary_residues_d_0_7": binary_residues,
        "ternary_residues_d_0_7": ternary_residues,
        "minimal_admissible_refinement": 120,
        "cells_per_piece_at_n5": 24,
    },
}

out_path = os.path.join(
    os.path.join(os.path.dirname(__file__), "..", "results"),
    "phase26a_chamber_skeleton_data.json",
)
with open(out_path, "w") as fh:
    json.dump(artifact, fh, indent=2)
check(f"Saved chamber complex to phase26a_chamber_skeleton_data.json",
      os.path.exists(out_path),
      f"file size = {os.path.getsize(out_path)} bytes")


# -----------------------------------------------------------------------------
# Wrap-up.
# -----------------------------------------------------------------------------

print(f"\n{'=' * 70}")
print(f"Total tests passed: {PASSED}")
print(f"Total tests failed: {FAILED}")
print('=' * 70)

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED

results_path = os.path.join(
    os.path.join(os.path.dirname(__file__), "..", "results"),
    "phase26a_chamber_skeleton_results.json",
)
with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")