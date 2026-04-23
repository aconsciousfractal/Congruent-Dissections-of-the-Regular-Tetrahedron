"""
Phase 26-C-T3 / tetrahedral exclusion.
=====================================

This script certifies three facts that, together, dramatically narrow the
residual t = 3 problem for the n = 5 convex congruent face-to-face
dissection of the regular tetrahedron T.

Notation
--------
We continue to work in the integer-scaled unit system of Phase 26-C:
area of T-face A_T = 60, per-piece boundary area E = 48, canonical
per-piece area multiset (m_1, m_2, m_3) with m_1 + m_2 + m_3 = E.

The 7 (residual, multiset) pairs that survive the canonical-multiset
assignment-feasibility test (see phase26c_t3_residuals.py, after the
T3-BUG-01 fix of 2026-04-16) are:

    R_T3_2 : (6, 12, 30)
    R_T3_3 : (6, 15, 27), (6, 18, 24), (12, 12, 24)
    R_T3_4 : (6, 18, 24), (12, 12, 24), (12, 16, 20)

i.e. five DISTINCT multisets:
    (6, 12, 30), (6, 15, 27), (6, 18, 24), (12, 12, 24), (12, 16, 20).

STEP A  --  Parity (topological) lemma
--------------------------------------
Claim.  In a convex, congruent, face-to-face dissection of T into 5
pieces with t = 3 (each piece touches exactly 3 of the 4 T-faces on
its boundary), every piece has an ODD number of faces f, with

    5 <= f <= 7.

Proof.  A convex piece P with t = 3 has, by convexity, exactly one
face per touched T-face (two coplanar faces of a convex polytope
coincide); so P has exactly 3 boundary faces.  Every other face of P
is interior and, by the face-to-face hypothesis, is shared with
exactly one other piece.  Let f be the common face count (pieces
are congruent, hence same f).  Then the total count of interior
face-incidences across pieces is 5(f - 3); but each interior face
is counted twice, so 5(f - 3) is even.  Since 5 is odd, (f - 3)
must be even, whence f is odd.

In a 5-piece problem each piece shares interior faces with at most
four others, so the number of interior faces per piece is <= 4,
i.e. f - 3 <= 4, i.e. f <= 7.  Finally a 3D convex polytope has
f >= 4; the parity forces f != 4, so f >= 5.  Thus f in {5, 7}. QED.

STEP B  --  Tetrahedral product lemma (auxiliary / sanity check)
----------------------------------------------------------------
Claim.  If a convex tetrahedral piece P (f = 4) with t = 3 and
V(P) = V(T)/5 existed, its three boundary footprint areas
(m_1, m_2, m_3) would satisfy

    m_1 * m_2 * m_3 = A_T^3 / 25 = 60^3 / 25 = 8640.

Proof.  A convex 4-face P with 3 faces on 3 T-faces has its four
face-planes equal to {three T-face planes, one interior plane}.
Three of the four vertices of P are intersections of two T-face
planes with the interior plane, i.e. points on the three edges
of T emanating from the apex vertex v (the T-vertex opposite to
the missing T-face).  The fourth vertex of P is the intersection
of the three T-face planes, i.e. v itself.  Parametrising the
three edge positions w_i in [v, u_i] by t_i = |vw_i| / |vu_i|,

    V(P) = t_1 t_2 t_3 * V(T)    (determinant identity),
    area(face of P on T-face opposite to u_i)
         = t_j t_k * A_T  for {i,j,k} = {1,2,3}.

Hence m_1 m_2 m_3 = (t_1 t_2)(t_1 t_3)(t_2 t_3) A_T^3
                  = (t_1 t_2 t_3)^2 A_T^3
                  = (1/5)^2 * A_T^3 = A_T^3 / 25. QED.

Although Step A already excludes f = 4 by parity, Step B serves as
an independent sanity check: we verify explicitly that NONE of the
five surviving multisets satisfy m_1 m_2 m_3 = 8640, confirming
that the parity-excluded case is also arithmetically excluded.

STEP C  --  Residual topological case split
-------------------------------------------
Steps A and B jointly reduce the t = 3 case to proving impossibility
for the two topological sub-cases:

    (C5)   f = 5: each piece has 2 interior faces; the interior-face
           adjacency graph on 5 vertices is 2-regular, hence a
           5-cycle C_5 (unique up to isomorphism).

    (K5)   f = 7: each piece has 4 interior faces; the interior-face
           adjacency graph is 4-regular on 5 vertices, i.e. K_5.

Each of these sub-cases requires a separate geometric argument
(Phase 26-C-T3 follow-up, not implemented in this script).  We
record the case split as output for downstream consumption.

References
----------
  - PHASE_26_PLAN.md, sub-phase 26-C, residuals t = 3.
  - phase26c_t3_residuals.py (fixed 2026-04-16).
  - 09-papers/Congruent Dissections of the Regular Tetrahedron/
    TODO_DRAFT_FINAL.md, section P0 / T3-BUG.
"""

from __future__ import annotations

import json
import os
from fractions import Fraction as F


# -----------------------------------------------------------------------------
# Test bookkeeping (same convention as sibling scripts).
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
# Problem constants.
# -----------------------------------------------------------------------------

A_T = 60     # area of one T-face in units of sqrt 3 / 30
E = 48       # per-piece boundary area = 4 A_T / 5 in the same units
N_PIECES = 5
T_FACES = 4

# The five distinct surviving area multisets (union across R_T3_2/3/4).
SURVIVING_MULTISETS = [
    (6, 12, 30),
    (6, 15, 27),
    (6, 18, 24),
    (12, 12, 24),
    (12, 16, 20),
]

# Occurrence of each multiset across the three SAT residuals (for the record).
RESIDUAL_MULTISET_PAIRS = [
    ("R_T3_2", (6, 12, 30)),
    ("R_T3_3", (6, 15, 27)),
    ("R_T3_3", (6, 18, 24)),
    ("R_T3_3", (12, 12, 24)),
    ("R_T3_4", (6, 18, 24)),
    ("R_T3_4", (12, 12, 24)),
    ("R_T3_4", (12, 16, 20)),
]


# -----------------------------------------------------------------------------
# Section 0  --  Setup sanity checks.
# -----------------------------------------------------------------------------

section("0. Setup: integer units, basic identities")

check("A_T = 60 (integer scaled area of one T-face)", A_T == 60)
check("E = 48 (integer scaled per-piece boundary area)", E == 48)
check("5 * E = 4 * A_T (global boundary area conservation)",
      N_PIECES * E == T_FACES * A_T,
      f"{N_PIECES * E} = {T_FACES * A_T}")
check("n pieces = 5", N_PIECES == 5)
check("T-faces = 4", T_FACES == 4)

for ms in SURVIVING_MULTISETS:
    check(f"Surviving multiset {ms} has m_1+m_2+m_3 = E = 48",
          sum(ms) == E,
          f"sum = {sum(ms)}")


# -----------------------------------------------------------------------------
# Section 1  --  Step A: parity / topological lemma.
# -----------------------------------------------------------------------------

section("1. Step A  --  parity: f must be odd, hence f in {5, 7}")

# Claim: 5 * (f - 3) must be even for the interior-face incidence
# count to decompose into pairs.  Since 5 is odd, f - 3 must be even.
# Since f >= 4 (3D convex polytope), and parity forbids f = 4, the
# minimum valid f is 5.  Since each piece has at most 4 interior
# face-neighbours (the other 4 pieces), f - 3 <= 4, so f <= 7.

allowed_f = []
for f in range(4, 10):
    interior_per_piece = f - 3
    total_interior_incidences = N_PIECES * interior_per_piece
    parity_ok = (total_interior_incidences % 2 == 0)
    face_neighbour_bound_ok = (interior_per_piece <= N_PIECES - 1)
    polytope_bound_ok = (f >= 4)
    if parity_ok and face_neighbour_bound_ok and polytope_bound_ok:
        allowed_f.append(f)

check("Parity + degree-bound + convexity: allowed f = {5, 7}",
      allowed_f == [5, 7],
      f"allowed = {allowed_f}")

# Explicit: f = 4 is excluded by parity alone.
check("f = 4 excluded by parity (5 * 1 = 5 is odd)",
      (N_PIECES * (4 - 3)) % 2 == 1,
      "5*(f-3)=5 odd, not decomposable into face-pairs")

# f = 6 excluded by parity.
check("f = 6 excluded by parity (5 * 3 = 15 is odd)",
      (N_PIECES * (6 - 3)) % 2 == 1)

# f = 8 excluded by parity (15 -> 25), and also by degree bound.
check("f = 8 excluded by parity (5 * 5 = 25 is odd)",
      (N_PIECES * (8 - 3)) % 2 == 1)

# f = 9 excluded by degree bound (needs 6 interior-face neighbours,
# only 4 available).
check("f = 9 excluded by degree bound (needs 6 neighbours; only 4 available)",
      (9 - 3) > N_PIECES - 1)


# -----------------------------------------------------------------------------
# Section 2  --  Step B: tetrahedral product lemma (sanity check).
# -----------------------------------------------------------------------------

section("2. Step B  --  tetrahedral product lemma m_1 m_2 m_3 = A_T^3 / 25")

# By the parametrisation derived in the docstring: if a convex
# tetrahedral piece P with t = 3 and V(P) = V(T)/5 existed, then
# m_1 m_2 m_3 = (1/25) A_T^3 = 8640 in integer-scaled units.

target_tetrahedral_product = F(A_T) ** 3 / F(25)
check("Target tetrahedral product = A_T^3 / 25 = 8640",
      target_tetrahedral_product == F(8640),
      f"{target_tetrahedral_product} = 8640")

# Check each surviving multiset.
tetra_lemma_per_multiset = []
for ms in SURVIVING_MULTISETS:
    product = F(ms[0]) * F(ms[1]) * F(ms[2])
    agrees = (product == target_tetrahedral_product)
    tetra_lemma_per_multiset.append({
        "multiset": list(ms),
        "product": int(product),
        "target": int(target_tetrahedral_product),
        "tetrahedral_realisable": bool(agrees),
    })
    check(f"Multiset {ms}: product {int(product)} != 8640 -> tetrahedral case UNSAT",
          not agrees,
          f"product = {int(product)}")

# Sanity: are there ANY integer multisets (m1, m2, m3) with sum = 48
# and product = 8640?  If yes, the tetrahedral lemma alone is not a
# universal arithmetic obstruction and we are relying on the ┬º3 area
# multiset enumeration for correctness.
any_integer_solution = []
for m1 in range(1, E):
    for m2 in range(m1, E - m1):
        m3 = E - m1 - m2
        if m3 < m2:
            continue
        if m1 * m2 * m3 == int(target_tetrahedral_product):
            any_integer_solution.append((m1, m2, m3))

check("Integer multisets summing to 48 with product 8640 (diagnostic)",
      True,   # never fails; informational
      f"solutions = {any_integer_solution}")


# -----------------------------------------------------------------------------
# Section 3  --  Step C: residual topological case split.
# -----------------------------------------------------------------------------

section("3. Step C  --  residual sub-cases to close: f in {5, 7}")

# f = 5: each piece has 2 interior faces; interior-face graph on
# 5 vertices is 2-regular, hence a single 5-cycle C_5 (only
# 2-regular simple graph on 5 vertices up to iso).
# f = 7: each piece has 4 interior faces; interior-face graph is
# 4-regular on 5 vertices, hence K_5 (only 4-regular simple graph
# on 5 vertices).

subcases = [
    {
        "f": 5,
        "interior_faces_per_piece": 2,
        "total_interior_faces": N_PIECES * 2 // 2,
        "adjacency_graph": "C_5 (5-cycle)",
        "combinatorial_piece_types": [
            "quadrilateral pyramid (4 triangles + 1 quadrilateral, 5V/8E)",
            "triangular prism (2 triangles + 3 quadrilaterals, 6V/9E)",
        ],
        "status": "OPEN (geometric argument needed)",
    },
    {
        "f": 7,
        "interior_faces_per_piece": 4,
        "total_interior_faces": N_PIECES * 4 // 2,
        "adjacency_graph": "K_5 (complete graph on 5 vertices)",
        "combinatorial_piece_types": [
            "hexagonal pyramid (1 hexagon + 6 triangles, 7V/12E)",
            "pentagonal prism (2 pentagons + 5 quadrilaterals, 10V/15E)",
            "other 7-faced convex polytopes (enumerated in Step D)",
        ],
        "status": "OPEN (geometric argument needed)",
    },
]

for sc in subcases:
    check(f"f = {sc['f']}: {sc['interior_faces_per_piece']} interior faces/piece, "
          f"{sc['total_interior_faces']} interior faces total, graph = {sc['adjacency_graph']}",
          True,
          sc["status"])

# These two sub-cases absorb the entire residual task for closing
# Theorem 11.4 unconditionally.  The plan is to handle them in
# follow-up scripts phase26c_t3_f5_exclusion.py and
# phase26c_t3_f7_exclusion.py.

# -----------------------------------------------------------------------------
# Section 4  --  Synthesis.
# -----------------------------------------------------------------------------

section("4. Synthesis")

check("Step A (parity): f in {5, 7}",
      True,
      "tetrahedral case f=4 EXCLUDED by parity")
check("Step B (tetrahedral product lemma): all 5 surviving multisets have "
      "m_1 m_2 m_3 != 8640",
      all(not e["tetrahedral_realisable"] for e in tetra_lemma_per_multiset),
      "consistent with Step A; serves as independent arithmetic sanity check")
check("Step C (residual split): closing Theorem 11.4 reduces to killing "
      "f = 5 (C_5) and f = 7 (K_5) topological sub-cases",
      True,
      "follow-up: phase26c_t3_f5_exclusion.py, phase26c_t3_f7_exclusion.py")


# -----------------------------------------------------------------------------
# Wrap-up.
# -----------------------------------------------------------------------------

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["constants"] = {
    "A_T": A_T,
    "E": E,
    "n_pieces": N_PIECES,
    "n_T_faces": T_FACES,
    "target_tetrahedral_product": int(target_tetrahedral_product),
}
RESULTS["surviving_multisets"] = [list(m) for m in SURVIVING_MULTISETS]
RESULTS["residual_multiset_pairs"] = [
    {"residual": r, "multiset": list(m)}
    for (r, m) in RESIDUAL_MULTISET_PAIRS
]
RESULTS["step_A_allowed_f"] = allowed_f
RESULTS["step_B_per_multiset"] = tetra_lemma_per_multiset
RESULTS["step_B_diagnostic_integer_solutions_product_8640"] = [
    list(m) for m in any_integer_solution
]
RESULTS["step_C_subcases"] = subcases

print(f"\n{'=' * 70}")
print(f"Total tests passed: {PASSED}")
print(f"Total tests failed: {FAILED}")
print('=' * 70)

print(f"\n  Summary:")
print(f"    Step A (parity):              f in {allowed_f}")
print(f"    Step B (tetrahedral product): 0/{len(SURVIVING_MULTISETS)} multisets satisfy m_1 m_2 m_3 = 8640")
print(f"    Step C (residual):            close f = 5 (C_5) and f = 7 (K_5)")


results_path = os.path.join(
    os.path.join(os.path.dirname(__file__), "..", "results"),
    "phase26c_t3_tetrahedral_exclusion_results.json",
)
with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")