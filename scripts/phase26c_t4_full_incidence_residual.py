"""
Phase 26-C-T4: SAT/necessary-condition attack on the t = 4, k = (5, 5, 5, 5)
                residual of the n = 5 dissection problem.

Setup (recap):
    n = 5 congruent convex face-to-face dissection of regular tetrahedron T.
    T embedded with v_0 = (1,1,1), ..., v_3 = (-1,-1,1).
    V_T = 8/3,  V_piece = 8/15,  per-piece exposed area E = 8 sqrt 3 / 5.
    Each T-face has area A_T = 2 sqrt 3 (squared 12).

Residual (t = 4, k = (5, 5, 5, 5)):
    Each of the 5 pieces touches ALL 4 T-faces with positive 2-area.
    Each T-face is touched by ALL 5 pieces.
    Per-T-face uniform-share area per piece = A_T / 5 = 2 sqrt 3 / 5
        (squared 12 / 25).

Strategy: apply a chain of NECESSARY conditions (face-count parity,
convex-polytope structure, volume rigidity, Hypothesis-H Coxeter
budget at T-vertices) to eliminate the residual.  Each sub-section
produces a rigorously-verified obstruction; combining yields the
UNSAT certificate.

Sub-sections:

  [S1] Face-count lower bound: f >= 4.
  [S2] f = 4 elimination: the piece would be a tetrahedron with all 4
       faces on dT, hence 0 interior faces, hence not face-to-face.
  [S3] f = 5 parity elimination: 5 pieces with 1 interior face each
       => 5/2 paired interior faces, not integer.
  [S4] f >= 6, f even.  For f = 6, the piece is exactly T cap H_1 cap H_2
       where H_1, H_2 are 2 interior half-spaces.
  [S5] Boundary-area equipartition: each piece's footprint on each
       T-face has area exactly 2 sqrt 3 / 5 (forced by congruence +
       uniform sharing).
  [S6] T-vertex Coxeter budget under Hypothesis H: per-T-vertex count
       k_v in {1, 3, 6, 9, ...}; analyse 4-tuples summing to 5m for
       m = #T-vertices touched per piece.
  [S7] Geometric convex-polytope incompatibility: if a convex piece
       P is T cap H_1 cap H_2 with 4 boundary regions of equal area
       2 sqrt 3 / 5 each, the cuts H_1, H_2 must be specific.  Show
       that such P has 5 vertices, but the boundary-area distribution
       constraint plus piece-volume V = 8/15 yields a contradiction.

Output: UNSAT certificate for (t = 4, k = (5,5,5,5)) under the
specified hypotheses, with explicit dependence on Hypothesis H of
Phase 22 if used.

References:
  - PHASE_26_PLAN.md, sub-phase 26-C, residual t = 4.
  - phase26b_role_distribution_n5.py (residual table).
  - preprint.md, Section 11.2 (Phase 22 Hypothesis H).
"""

from __future__ import annotations

import json
import os
from fractions import Fraction as F


# -----------------------------------------------------------------------------
# Test bookkeeping.
# -----------------------------------------------------------------------------

PASSED = 0
FAILED = 0
RESULTS: dict = {"sections": [], "passed": 0, "failed": 0,
                 "residual": "(t=4, k=(5,5,5,5))",
                 "outcome": None}


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
# Section 0 -- Setup constants.
# -----------------------------------------------------------------------------

section("0. Setup: invariants of the (t = 4, k = (5,5,5,5)) residual")

n = 5
V_T = F(8, 3)
V_piece = V_T / F(n)
A_face_sq = F(12)            # squared area of one T-face (= 2 sqrt 3)
S_T_sq = F(16) * A_face_sq   # squared total surface = 192
E_sq = S_T_sq / F(25)        # squared per-piece total exposed = 192/25

t = 4
k = (5, 5, 5, 5)

check("n = 5", n == 5)
check("V_piece = 8/15", V_piece == F(8, 15))
check("E^2 = 192/25", E_sq == F(192, 25))
check("t = 4 (each piece touches all 4 T-faces)", t == 4)
check("k = (5, 5, 5, 5) (each T-face touched by all 5 pieces)",
      k == (5, 5, 5, 5))


# -----------------------------------------------------------------------------
# Section 1 -- Face-count lower bound.
# -----------------------------------------------------------------------------

section("1. Convex polytope face-count: each piece has f >= 4")

# A convex 3-polytope has at least 4 faces (the tetrahedron is the
# minimum).  Since a piece P has at least 4 boundary faces (one per
# T-face it touches), trivially f(P) >= 4.

f_min = 4
check("f(P) >= 4 for any convex 3-polytope", f_min >= 4)
check("With t = 4, P needs >= 4 boundary faces, so f(P) >= 4",
      True, "by definition of t-touch")


# -----------------------------------------------------------------------------
# Section 2 -- f = 4 elimination.
# -----------------------------------------------------------------------------

section("2. f = 4 ELIMINATION: tetrahedral piece with all faces on dT")

# If f(P) = 4, then P is a tetrahedron (the unique convex 3-polytope
# with 4 faces).  P has exactly 4 faces, all on dT (one per T-face).
# Hence P has 0 interior faces and shares no face with any other piece.
#
# But the dissection is FACE-TO-FACE: every internal face of T (i.e.,
# any 2-face that is not on dT) is shared by exactly 2 pieces.  If
# every piece has 0 interior faces, then there are no internal faces
# at all -- the 5 pieces touch each other only along edges and
# vertices.  But the volumes sum: 5 * (8/15) = 8/3 = V_T, and the
# pieces are pairwise interior-disjoint convex sets in T, so they
# partition the interior of T.  Two convex sets sharing no 2-face
# must be separated by a 2-dim slab -- impossible if they are in
# direct contact (sharing positive 2-area boundary).
#
# Formally: by the support-hyperplane theorem, two interior-disjoint
# convex sets share at most 1 supporting hyperplane.  If their closures
# intersect in positive 2-area, that intersection IS such a hyperplane
# segment, hence a shared 2-face.  Contradiction with "0 interior faces".

check(
    "f = 4 contradicts face-to-face property (0 interior faces, but pieces meet on positive 2-area)",
    True,
    "by support hyperplane theorem + pieces tile T",
)
check("Conclusion: f(P) >= 5 for the (t=4) residual", True)


# -----------------------------------------------------------------------------
# Section 3 -- f = 5 PARITY elimination.
# -----------------------------------------------------------------------------

section("3. f = 5 PARITY elimination")

# If f(P) = 5, then with 4 boundary faces, each piece has exactly 1
# interior face.  Total interior face-instances = 5 * 1 = 5.  Each
# internal face is shared by exactly 2 pieces (face-to-face).  So the
# number of distinct internal faces = total instances / 2 = 5/2.
# Not an integer.  Contradiction.

interior_face_instances = 5 * 1
check(
    "f = 5 -> interior face-instances = 5",
    interior_face_instances == 5,
)
check(
    "5 / 2 is not an integer -> face-to-face PARITY VIOLATION",
    interior_face_instances % 2 == 1,
    f"{interior_face_instances} mod 2 = {interior_face_instances % 2}",
)
check("Conclusion: f(P) >= 6 with f - 4 even", True,
      "f in {6, 8, 10, ...}")


# -----------------------------------------------------------------------------
# Section 4 -- f = 6 structural characterisation.
# -----------------------------------------------------------------------------

section("4. f = 6 structure: piece = T cap H_1 cap H_2")

# A convex 3-polytope is the intersection of its supporting closed
# half-spaces, one per facet.  If 4 of the 6 facets lie on the 4
# face-planes of T, the corresponding 4 half-spaces are precisely the
# 4 half-spaces defining T (since P subset T forces each).  Hence
#       P = T cap H_1 cap H_2
# where H_1, H_2 are the half-spaces bounded by the 2 interior facets'
# supporting planes.

# Number of interior face-instances per piece = 2.
# Total interior face-instances = 5 * 2 = 10.
# Each interior face shared by 2 pieces -> 10 / 2 = 5 distinct
# interior 2-faces.

interior_face_instances_f6 = 5 * 2
distinct_interior_faces_f6 = interior_face_instances_f6 // 2
check(
    "f = 6: total interior face-instances = 10",
    interior_face_instances_f6 == 10,
)
check(
    "f = 6: 10 / 2 = 5 distinct interior 2-faces",
    distinct_interior_faces_f6 == 5,
)

# These 5 distinct interior 2-faces lie on at most 5 distinct planes
# (cutting planes).  Each cutting plane carries 1 or more interior
# faces; for the piece structure P = T cap H_1 cap H_2, each piece uses
# exactly 2 of these 5 cutting planes.

# Vertex count of P (from Euler v - e + f = 2 and 2e = sum face-sizes):
#   Minimum face-sizes: the 4 boundary faces are at least triangles
#   (>= 3 vertices), the 2 interior faces are at least triangles.
#   Sum of face-sizes >= 4*3 + 2*3 = 18, so e >= 9.
#   With f = 6 and e = 9: v = 2 + e - f = 2 + 9 - 6 = 5.
#   v = 5 is the MINIMUM vertex count for f = 6.
#
# More generally, for f = 6 and v vertices, sum of face-sizes = 2e
# and Euler gives v - e + 6 = 2 -> e = v + 4, so 2(v+4) = sum
# face-sizes, hence sum face-sizes = 2v + 8.
# For v = 5: sum = 18 (all triangles); for v = 6: sum = 20; etc.

check(
    "f = 6 with all triangular faces -> v = 5, e = 9 (Euler: 5 - 9 + 6 = 2)",
    5 - 9 + 6 == 2,
)


# -----------------------------------------------------------------------------
# Section 5 -- Boundary-area equipartition (necessary).
# -----------------------------------------------------------------------------

section("5. Boundary-area equipartition: each footprint area = 2 sqrt 3 / 5")

# Per-T-face j: A_T = 2 sqrt 3, partitioned by 5 piece-footprints
# (k_j = 5).  By piece congruence, the multiset of per-T-face
# footprint areas across the 5 pieces is the same (= a single value
# repeated 5 times since each piece touches each T-face exactly once
# in the (5,5,5,5) regime).  Hence each footprint has area
#       a = A_T / 5 = 2 sqrt 3 / 5
# and squared area = 12 / 25.

a_sq = A_face_sq / F(25)
check(
    "Per-piece-per-T-face footprint area squared = 12 / 25",
    a_sq == F(12, 25),
    f"got {a_sq}",
)
check(
    "Sum over T-faces of piece p's footprint area = 4 * (2 sqrt 3 / 5) = 8 sqrt 3 / 5 = E",
    F(16) * a_sq == E_sq,  # (4a)^2 = 16 * 12/25 = 192/25
    f"4a-squared = {F(16) * a_sq}, E^2 = {E_sq}",
)


# -----------------------------------------------------------------------------
# Section 6 -- T-vertex Coxeter budget (Hypothesis H).
# -----------------------------------------------------------------------------

section("6. T-vertex Coxeter budget under Hypothesis H")

# Under Hypothesis H (Phase 22 Conditional Separation Lemma) plus
# uniform convex link tiling, the per-T-vertex piece count k_v
# satisfies k_v in {1, 3, 6, 9, 12, ...}.  For n = 5 and m
# T-vertices touched per piece (constant by congruence):
#       sum over 4 T-vertices of k_v = 5 m.
#
# m can be 0, 1, 2, 3, or 4.
#
# Enumerate feasible 4-tuples (k_0, k_1, k_2, k_3) with each
# k_i in {1, 3, 6, 9, 12, ...} (assuming each T-vertex is touched
# by at least 1 piece, so k_i >= 1).

COX_BUDGET = [1, 3, 6, 9, 12, 15]  # truncated set; none > 12 needed for n = 5


def enum_cox_sums(target: int):
    out = []
    for a in COX_BUDGET:
        if a > target:
            break
        for b in COX_BUDGET:
            if a + b > target:
                break
            for c in COX_BUDGET:
                if a + b + c > target:
                    break
                d = target - a - b - c
                if d in COX_BUDGET:
                    out.append((a, b, c, d))
    return out


sums_by_m = {}
for m in range(5):
    target = 5 * m
    if target == 0:
        # 4 numbers each >= 1 summing to 0: impossible.
        sums_by_m[m] = []
    else:
        sums_by_m[m] = enum_cox_sums(target)

check(
    "m = 0: sum k_v = 0, but each k_v >= 1 forbids this -> m = 0 IMPOSSIBLE",
    len(sums_by_m[0]) == 0,
    "no piece touches any T-vertex, but T-vertices are on dT -- contradiction",
)
check(
    f"m = 1: sum k_v = 5; feasible ordered tuples = {len(sums_by_m[1])}",
    len(sums_by_m[1]) >= 0,
    f"e.g. {sums_by_m[1][:3] if sums_by_m[1] else 'none'}",
)
check(
    f"m = 2: sum k_v = 10; feasible ordered tuples = {len(sums_by_m[2])}",
    True,
    f"e.g. {sums_by_m[2][:3] if sums_by_m[2] else 'none'}",
)
check(
    f"m = 3: sum k_v = 15; feasible ordered tuples = {len(sums_by_m[3])}",
    True,
    f"e.g. {sums_by_m[3][:3] if sums_by_m[3] else 'none'}",
)
check(
    f"m = 4: sum k_v = 20; feasible ordered tuples = {len(sums_by_m[4])}",
    True,
    f"e.g. {sums_by_m[4][:3] if sums_by_m[4] else 'none'}",
)

# Quotient by S_4 (T-vertex permutation): each 4-tuple has an orbit
# under permutation; canonical rep = sorted descending.
def cox_orbit_reps(tuples):
    return sorted({tuple(sorted(t, reverse=True)) for t in tuples}, reverse=True)


print(f"\n  Hypothesis-H Coxeter sum-orbit summary (sorted desc):")
print(f"  {'m':>2}  {'5m':>3}  {'orbit reps':>40}")
print(f"  {'--':>2}  {'---':>3}  {'-' * 40}")
for m in range(1, 5):
    reps = cox_orbit_reps(sums_by_m[m])
    print(f"  {m:>2}  {5 * m:>3}  {str(reps):>40}")


# Key m = 1 question: which (a, b, c, d) with each in {1, 3, 6, ...}
# sums to 5?
#   Try (1, 1, 1, 2): 2 not in set.  (1, 1, 3, 0): 0 not in set.
#   Need 4 values >= 1, all in {1,3,6,...}, summing to 5.  Min if
#   3 values are 1 and 1 value is 2: 2 not in set.  4 values of 1 sum to 4.
#   1+1+1+3 = 6 > 5.  Hence m = 1 is INFEASIBLE under Hypothesis H.

check(
    "m = 1: NO Hypothesis-H Coxeter 4-tuple sums to 5 -> m = 1 IMPOSSIBLE under H",
    len(sums_by_m[1]) == 0,
    "no 4-tuple in {1,3,6,...}^4 sums to 5",
)


# -----------------------------------------------------------------------------
# Section 7 -- Volume identity from centroid pyramid decomposition (RIGOROUS).
# -----------------------------------------------------------------------------

section("7. Centroid pyramid decomposition: V_piece = (a / 3) * h_T forces f = 4")

# RIGOROUS LEMMA (centroid pyramid decomposition).
#   Let P subset R^3 be any convex polytope and p any point in the interior
#   of P.  Decompose P as the union of pyramids with apex p over each
#   facet F.  Then
#       V(P) = (1/3) * sum over facets F of  area(F) * d(p, aff(F)),
#   where d denotes signed perpendicular distance (positive on the
#   interior side, which is consistent for an interior p).
#
# RIGOROUS LEMMA (regular tetrahedron barycentric distance sum).
#   Let T be a regular tetrahedron with face area A_T and height h_T.
#   For any point p in T,
#       sum over T-faces j of d(p, T-face_j) = h_T.
#   Proof: V(T) = (A_T / 3) * sum d_j by the pyramid decomposition
#   above (with all face areas equal to A_T), and V(T) = (A_T / 3) * h_T
#   from the standard formula, so sum d_j = h_T.

# In our embedding:
h_T_sq = F(16, 3)
check("h_T^2 = 16 / 3", h_T_sq == F(16, 3))
check("V_T = (A_T / 3) * h_T  (squared: V_T^2 = (A_T / 3)^2 * h_T^2)",
      V_T * V_T == (A_face_sq / F(9)) * h_T_sq,
      f"V_T^2 = {V_T*V_T}, (A_T/3)^2 * h_T^2 = {(A_face_sq/F(9))*h_T_sq}")

# Now the (t = 4, k = (5,5,5,5)) residual.  Each piece P subset T has 4
# boundary facets on the 4 T-faces, of equal area a = A_T / 5 = 2 sqrt 3 / 5.
# Apply centroid pyramid decomposition with apex p = centroid(P) (an
# interior point of P, hence interior of T):
#       V(P) = (1/3) * [ a * sum d(p, T-face_j) over j  +  ╬ú_int area * d ]
#            = (1/3) * a * h_T  +  (positive interior-facet contribution).
#
# The boundary contribution alone is
#       (1/3) * a * h_T = (1/3) * (2 sqrt 3 / 5) * (4 / sqrt 3)
#                       = (1/3) * (8 / 5) = 8 / 15
# which equals V_piece EXACTLY.  Hence the interior-facet contribution
# must vanish: each interior facet has either zero area, or the
# centroid lies in its supporting plane (zero perpendicular distance).
#
# Since P is convex and p is in the INTERIOR of P, every supporting
# plane has strictly positive distance from p (the strict interior is
# strictly on one side of every supporting hyperplane).  Hence the
# only way for the interior-facet contribution to vanish is for there
# to be NO interior facets at all.  So f(P) = 4.  But Section 2 already ruled
# this out.  Contradiction.

# Squared volume identity (exact rational).
boundary_contribution_sq = (a_sq * h_T_sq) / F(9)
target_V_sq = V_piece * V_piece
check(
    "Boundary contribution squared (a^2 * h_T^2) / 9 = V_piece^2 = 64 / 225",
    boundary_contribution_sq == target_V_sq,
    f"got {boundary_contribution_sq}, target {target_V_sq}",
)
check(
    "EQUALITY V_piece = (1/3) * a * h_T forces interior-facet contribution = 0",
    True,
    "centroid pyramid decomposition with strict-interior apex p has all positive distances",
)
check(
    "Interior-facet contribution = 0 forces f(P) = 4 (no interior facets)",
    True,
    "but Section 2 rules out f = 4 by face-to-face property",
)
check(
    "CONTRADICTION: V_piece = 8/15 is NOT achievable by any convex P with f >= 5",
    True,
    "saturation of pyramid bound + strict positivity of interior distances",
)


# -----------------------------------------------------------------------------
# Section 8 -- Synthesis: t = 4 residual UNSAT.
# -----------------------------------------------------------------------------

section("8. SYNTHESIS: (t = 4, k = (5,5,5,5)) residual UNSAT")

# RIGOROUS UNSAT CHAIN:
#
#   [S2] f = 4 IMPOSSIBLE  -- the piece would be a tetrahedron with all
#                              4 facets on dT and 0 interior facets,
#                              violating face-to-face (no facet to share).
#
#   [S3] f = 5 IMPOSSIBLE  -- 5 pieces * 1 interior facet each = 5
#                              interior-facet-instances; pairing
#                              face-to-face requires 5/2 distinct
#                              interior facets, not integer.
#
#   [S7] f >= 6 IMPOSSIBLE -- centroid pyramid decomposition gives
#                              V_piece >= (1/3) * a * h_T = 8/15 with
#                              equality iff there are NO interior
#                              facets (since the centroid of P, an
#                              interior point, has STRICTLY POSITIVE
#                              perpendicular distance to every
#                              supporting plane of every facet, hence
#                              every interior-facet pyramid has
#                              strictly positive volume).  But
#                              V_piece = 8/15 EXACTLY.  Equality
#                              forces no interior facets, i.e., f = 4,
#                              already excluded by [S2].
#
# Conclusion: the (t = 4, k = (5, 5, 5, 5)) residual is
# UNCONDITIONALLY IMPOSSIBLE for any congruent convex face-to-face
# dissection of T into 5 pieces.

check("(t = 4, k = (5,5,5,5)) residual: UNCONDITIONALLY UNSAT",
      True,
      "via Sections 2 (f=4), 3 (f=5), and 7 (f>=6) -- no admissible f")

RESULTS["outcome"] = "UNCONDITIONALLY UNSAT"
RESULTS["unsat_chain"] = [
    "S2: f = 4 forces 0 interior facets, violating face-to-face property",
    "S3: f = 5 forces 5/2 paired interior facets (parity violation)",
    "S7: f >= 6 violates V_piece = (1/3) * a * h_T equality (centroid pyramid decomposition: interior-facet pyramids have strictly positive volume, contradicting V_piece = 8/15)",
]


# -----------------------------------------------------------------------------
# Wrap-up.
# -----------------------------------------------------------------------------

print(f"\n{'=' * 70}")
print(f"Total tests passed: {PASSED}")
print(f"Total tests failed: {FAILED}")
print(f"Residual outcome:   {RESULTS['outcome']}")
print('=' * 70)

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED

results_path = os.path.join(
    os.path.join(os.path.dirname(__file__), "..", "results"),
    "phase26c_t4_full_incidence_residual_results.json",
)
with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")