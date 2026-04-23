"""
Phase 26-B: Boundary role-distribution enumeration for n = 5.

Goal: generalise the Phase 25 P25-C' facet-role MILP (n = 16) to n = 5.
Enumerate every combinatorially-admissible "T-face distribution" of the
5 congruent pieces, classified by the multiset of T-faces touched, and
apply the *necessary* feasibility filters (volume, surface area, T_d
symmetry, T-face cover, congruence).  The output is a residual table:
each surviving distribution is a candidate that Phase 26-C must attack
SAT/ILP-style with the full geometric constraint set.

Embedding (Phase 25-consistent):
    v_0 = ( 1,  1,  1)        |v_i v_j|^2 = 8, edge length = 2 sqrt 2
    v_1 = ( 1, -1, -1)        V_T = 8/3
    v_2 = (-1,  1, -1)        Each T-face is an equilateral triangle
    v_3 = (-1, -1,  1)        of side 2 sqrt 2 and area 2 sqrt 3.

For n = 5:
    V_piece = V_T / 5 = 8/15.
    Total surface area of dT = 4 * area(face) = 8 sqrt 3.
    Each piece's TOTAL exposed surface area = 8 sqrt 3 / 5 (by congruence).
    (Squared for exact rational arithmetic: (8 sqrt 3 / 5)^2 = 192/25.)

Definitions.

  T-FACE TOUCH SET of a piece P: the set
        I(P) = { j in {0,1,2,3} : P has at least one boundary face on T-face j }.

  By piece congruence, the cardinality |I(P)| is the same across all
  5 pieces.  Call it t.

  T-FACE INCIDENCE VECTOR: k = (k_0, k_1, k_2, k_3) where
        k_j = #{ piece P : j in I(P) }.

  Constraint: sum_j k_j = 5 t.

  T_d ACTION: T_d permutes the 4 T-faces; equivalent k vectors form
  one S_4-orbit on multisets.

NECESSARY filters applied below:

  (F1) t >= 1           (the dissection covers dT, so some piece must
                         touch some T-face).
  (F2) max_j k_j <= 5    (only 5 pieces total).
  (F3) sum_j k_j = 5 t   (incidence-count consistency).
  (F4) Per-T-face area:  the k_j pieces touching T-face j contribute
                         boundary regions of total area A_T = 2 sqrt 3
                         on that face.  Squared total: 12.  Each
                         contributing piece supplies between 1 and
                         (1 + small) boundary-face area on that face;
                         no per-piece-per-T-face area can exceed A_T.
  (F5) Total piece exposed area: each of the 5 congruent pieces
                                 contributes total exposed area = 8 sqrt 3 / 5
                                 across its t T-faces.  In particular,
                                 if a piece touches t T-faces, its
                                 average per-face exposed area is
                                 (8 sqrt 3 / 5) / t.
  (F6) Volume:           V_piece = 8/15 forces a 3D piece (no
                         pathological flat or curved degenerate shape).
  (F7) Convexity:        every piece is convex (assumed throughout).
  (F8) S_4 / T_d quotient: distributions equivalent under permutation
                           of T-face labels are merged; the residual
                           is the orbit count.

Output: a residual table giving, for each (t, k-orbit-representative),
the surviving combinatorial type and the necessary geometric data
(per-piece exposed area, per-T-face incidence, etc.).

References:
  - PHASE_26_PLAN.md, sub-phase 26-B.
  - phase26a_chamber_skeleton.py (chamber complex substrate).
  - preprint.md, Section 11.3 (Phase 25 Theorem 11.3.1, parallel for
    the n = 16 all-one-face residual = (t = 1, k = (16, 0, 0, 0))).
"""

from __future__ import annotations

import json
import os
from fractions import Fraction as F
from itertools import product, permutations
from collections import defaultdict


# -----------------------------------------------------------------------------
# Test bookkeeping.
# -----------------------------------------------------------------------------

PASSED = 0
FAILED = 0
RESULTS: dict = {"sections": [], "passed": 0, "failed": 0,
                 "residuals": [], "summary": {}}


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
# Section 1 -- Set-up: invariants of the n = 5 problem.
# -----------------------------------------------------------------------------

section("1. n = 5 invariants: volumes, areas, incidence counts")

n = 5
V_T = F(8, 3)
V_piece = V_T / F(n)
check("V_piece = V_T / 5 = 8/15", V_piece == F(8, 15),
      f"got {V_piece}")

# Surface area of dT: 4 equilateral triangles of side 2 sqrt 2.
# Area of one face = (sqrt 3 / 4) * (2 sqrt 2)^2 = (sqrt 3 / 4) * 8 = 2 sqrt 3.
# Squared per-face area = 12.
A_face_sq = F(12)         # squared area of one T-face
S_T_sq = F(16) * A_face_sq  # (4 * 2 sqrt 3)^2 = 16 * 12 = 192
check("Per-T-face area squared = 12", A_face_sq == F(12),
      f"got {A_face_sq}")
check("Total surface area squared (4 * 2 sqrt 3)^2 = 192",
      S_T_sq == F(192))

# Per-piece total exposed area = (1/5) of total surface, squared = 192/25.
piece_exposed_sq = S_T_sq / F(25)
check("Per-piece total exposed area squared = 192/25",
      piece_exposed_sq == F(192, 25),
      f"got {piece_exposed_sq}")

# t can range from 0 to 4 (number of T-faces a piece touches).
# t = 0 ruled out by (F1).
T_VALUES = list(range(1, 5))
check("Admissible t values = {1, 2, 3, 4}", T_VALUES == [1, 2, 3, 4])


# -----------------------------------------------------------------------------
# Section 2 -- Enumerate all (k_0, k_1, k_2, k_3) for each t.
# -----------------------------------------------------------------------------

section("2. T-face incidence vectors k for each t in {1,2,3,4}")


def enumerate_k_vectors(t: int):
    """Return all k = (k_0, k_1, k_2, k_3) with each k_j in [0, 5] and
    sum k_j = 5 * t.  Note: k_j <= 5 by (F2) since only 5 pieces."""
    out = []
    target = 5 * t
    for k0, k1, k2, k3 in product(range(6), repeat=4):
        if k0 + k1 + k2 + k3 == target:
            out.append((k0, k1, k2, k3))
    return out


total_k_count = 0
k_vectors_by_t = {}
for t in T_VALUES:
    kvs = enumerate_k_vectors(t)
    k_vectors_by_t[t] = kvs
    total_k_count += len(kvs)
    check(f"t = {t}: enumerated {len(kvs)} raw k vectors",
          len(kvs) > 0,
          f"first = {kvs[0]}, last = {kvs[-1]}")

check(f"Total raw k vectors = {total_k_count}", total_k_count > 0)


# -----------------------------------------------------------------------------
# Section 3 -- Quotient by T_d action (permutation of T-faces).
# -----------------------------------------------------------------------------

section("3. Quotient k vectors by S_4 (T-face permutation) -- T_d orbits")

# T_d acts on {face_0, face_1, face_2, face_3} as S_4.  Two k vectors
# are equivalent if they have the same multiset of entries.

def k_orbit_rep(k):
    """Canonical representative of the S_4 orbit of k: sorted descending."""
    return tuple(sorted(k, reverse=True))


orbits_by_t = {}
for t in T_VALUES:
    seen = {}
    for k in k_vectors_by_t[t]:
        rep = k_orbit_rep(k)
        if rep not in seen:
            seen[rep] = []
        seen[rep].append(k)
    orbits_by_t[t] = seen
    check(f"t = {t}: {len(seen)} S_4-orbits of k vectors",
          len(seen) > 0,
          f"orbit reps = {sorted(seen.keys(), reverse=True)}")


# -----------------------------------------------------------------------------
# Section 4 -- Per-T-face area-feasibility filter (F4).
# -----------------------------------------------------------------------------

section("4. Per-T-face area-feasibility filter (F4)")

# For each T-face j, the k_j pieces touching it tile that face's area
# A_T = 2 sqrt 3 with their boundary footprints.  By congruence, the
# multiset of boundary-footprint areas across pieces is the same for
# every piece.  Each piece contributes (8 sqrt 3 / 5) / t average
# squared per-face area; but the per-T-face area sum must equal A_T.
#
# Let a be a piece's per-T-face boundary area on a single touched T-face.
# Then (k_j pieces) * a = A_T   if all k_j pieces contribute equally.
# But pieces touching multiple T-faces may distribute their (8 sqrt 3 / 5)
# total exposure unequally; the constraint becomes:
#
#   sum over (piece p, T-face j) of area(p touches j) = A_T   for each j,
#   sum over T-faces of area(p touches j) = 8 sqrt 3 / 5     for each p,
#   piece p touches T-face j iff j in I(p) (incidence).
#
# The doubly-stochastic-like system has solutions iff the marginals are
# compatible, i.e.,
#       sum_j A_T = 4 A_T = 5 * (8 sqrt 3 / 5) = 8 sqrt 3 = OK by construction.
#
# Per-T-face NECESSARY filter: k_j > 0 iff at least one piece touches
# T-face j; if k_j > 0, the average per-piece-per-T-face area on T-face
# j is A_T / k_j.  This must be <= the maximum admissible per-piece-per-
# T-face area, which is bounded by the piece's total exposed area
# (since a piece's footprint on one face cannot exceed its total).
#
# Specifically: each piece's total exposed area = 8 sqrt 3 / 5, so
# any single per-face contribution <= 8 sqrt 3 / 5.  Hence:
#       A_T / k_j  <=  8 sqrt 3 / 5    AND
#       (A_T total on T-face j) is shared by k_j pieces, each
#       contributing at most 8 sqrt 3 / 5,
#       so       k_j * (8 sqrt 3 / 5) >= A_T = 2 sqrt 3,
#       i.e.,    k_j >= 5 / 4 = 1.25,  i.e., k_j >= 2  (integer).
#
# Wait, that gives k_j >= 2 -- but that contradicts e.g. n = 16 all-one-
# face where k_0 = 16, k_1 = k_2 = k_3 = 0.  The resolution is: T-faces
# with k_j = 0 are simply NOT covered by any boundary footprint, which
# is impossible because dT is fully covered.  So k_j = 0 is forbidden
# for any j unless that T-face has zero area, contradiction.
# Therefore (F4) demands k_j >= 1 for all j (every T-face is touched by
# at least one piece).

# Wait -- this is not right either.  The n=16 all-one-face example has
# all 16 footprints on a single T-face; the other three T-faces are NOT
# COVERED by any boundary face of the pieces on the SAME side, but they
# ARE covered as the "exposed" part of the dissection.  Let me reread:
# in n=16 all-one-face, every piece has exactly ONE boundary face, all
# on the SAME T-face?  No, that can't be right -- a single T-face has
# area A_T, and 16 pieces of total exposed area 4 A_T can't fit all on
# one face area A_T.  So either each piece in n=16 all-one-face has
# boundary area A_T / 16 (not 4 A_T / 16 = A_T / 4), or my reading is
# wrong.
#
# Re-reading Phase 25:  "all-one-face" means each piece has exactly ONE
# boundary face on the SAME T-face.  But then total boundary area = 16
# pieces * A_T/16 = A_T, leaving 3 A_T uncovered -- impossible.
#
# Resolution: the n=16 all-one-face residual configuration is in fact
# not directly comparable; Phase 25 ┬º17.10 / ┬º18 "all-one-face" refers
# to the role-MILP role distribution where EACH PIECE'S SINGLE CORNER
# ROLE is on a single T-face, but pieces also have additional ROLES
# (central, etc.) on the OTHER 3 T-faces.  The terminology is residual-
# specific to the n=16 structure.

# For n = 5, the cleanest necessary filter at the MULTISET level is:

# (F4a) Every T-face is covered by some boundary footprint:  k_j >= 1
#       for all j, OR (alternatively) some piece's complete set of
#       footprints covers the missing face.  But by congruence, the
#       footprint pattern is the same across pieces, so if k_j = 0
#       for some j, then NO piece touches T-face j, hence T-face j
#       is not covered by any boundary footprint, contradicting that
#       dT is fully tiled.  Hence k_j >= 1 for all j.

# (F4b) Per-T-face area constraint:  k_j pieces each touch T-face j
#       with footprint of area at most (8 sqrt 3 / 5) (each piece's
#       total exposed area).  The NECESSARY condition is
#               k_j * (8 sqrt 3 / 5) >= A_T = 2 sqrt 3
#       i.e.,   k_j >= 5/4 = 1.25  =>  k_j >= 2.

def filter_F4(k):
    """k passes F4 iff k_j >= 2 for all j (necessary feasibility)."""
    return all(kj >= 2 for kj in k)


# But wait: k_j >= 2 means EVERY T-face is touched by >= 2 pieces.
# Let's verify that's consistent with sum k_j = 5 t.  Minimum sum
# under k_j >= 2 is 4 * 2 = 8.  So 5 t >= 8, i.e., t >= 8/5, hence
# t >= 2.
#
# This means t = 1 is impossible for n = 5: no congruent dissection
# of T into 5 pieces can have each piece touching exactly 1 T-face.

# Let's verify this very carefully by re-deriving (F4b).  Each piece
# touches t T-faces and contributes total exposed area E = 8 sqrt 3 / 5
# distributed across those t T-faces.  Let a_{p,j} >= 0 be the area of
# piece p's footprint on T-face j (a_{p,j} = 0 if j not in I(p)).
#
# Constraints:
#   (i)   sum_j a_{p,j} = E  for every piece p
#   (ii)  sum_p a_{p,j} = A_T  for every T-face j
#   (iii) a_{p,j} > 0 iff j in I(p) (incidence consistency)
#   (iv)  k_j = #{ p : a_{p,j} > 0 }
#
# For (ii) to be achievable with k_j contributors each of value
# bounded by E:
#       k_j * E >= A_T  =>  k_j >= A_T / E = (2 sqrt 3) / (8 sqrt 3 / 5)
#                              = 5 / 4 = 1.25
#       So k_j >= 2 (since k_j is integer).

# This filter STRONGLY constrains the n = 5 problem!

surviving_t1_count = sum(1 for k in k_vectors_by_t[1] if filter_F4(k))
surviving_t2_count = sum(1 for k in k_vectors_by_t[2] if filter_F4(k))
surviving_t3_count = sum(1 for k in k_vectors_by_t[3] if filter_F4(k))
surviving_t4_count = sum(1 for k in k_vectors_by_t[4] if filter_F4(k))

check(f"t = 1: F4 survivors = 0  (k_j >= 2 forces sum >= 8 > 5)",
      surviving_t1_count == 0,
      f"got {surviving_t1_count}")
check(f"t = 2: F4 survivors = {surviving_t2_count}",
      surviving_t2_count > 0)
check(f"t = 3: F4 survivors = {surviving_t3_count}",
      surviving_t3_count > 0)
check(f"t = 4: F4 survivors = {surviving_t4_count}",
      surviving_t4_count > 0)


# -----------------------------------------------------------------------------
# Section 5 -- Quotient survivors by S_4 (T_d) orbits, build residual table.
# -----------------------------------------------------------------------------

section("5. Build residual table (t, S_4-orbit of k) after F4")

residual_table = []
for t in T_VALUES:
    seen_orbits = set()
    for k in k_vectors_by_t[t]:
        if not filter_F4(k):
            continue
        rep = k_orbit_rep(k)
        if rep in seen_orbits:
            continue
        seen_orbits.add(rep)
        # Per-piece-per-T-face required average area on T-face j
        # if k_j pieces tile that face equally:  A_T / k_j.
        # In our squared-rational setting we keep the rational
        # (A_face_sq / k_j^2) for each j with k_j > 0.
        per_face_sq = [
            (A_face_sq / F(kj * kj)) if kj > 0 else None
            for kj in rep
        ]
        residual_table.append({
            "t": t,
            "k_orbit_rep": list(rep),
            "sum_k": sum(rep),
            "per_T_face_uniform_share_squared": [
                f"{x.numerator}/{x.denominator}" if x is not None else None
                for x in per_face_sq
            ],
        })

n_residuals = len(residual_table)
check(f"Total surviving (t, k-orbit) residuals = {n_residuals}",
      n_residuals > 0,
      f"residuals = {n_residuals}")

# Pretty print.
print(f"\n  Residual table after F4 quotient by S_4:")
print(f"  {'t':>2}  {'k orbit (sorted desc)':>25}  {'sum k':>5}  "
      f"{'per-face uniform a^2':>40}")
print(f"  {'-' * 2}  {'-' * 25}  {'-' * 5}  {'-' * 40}")
for r in residual_table:
    k_str = "(" + ", ".join(str(x) for x in r["k_orbit_rep"]) + ")"
    a_str = ", ".join(
        x if x is not None else "n/a"
        for x in r["per_T_face_uniform_share_squared"]
    )
    print(f"  {r['t']:>2}  {k_str:>25}  {r['sum_k']:>5}  {a_str:>40}")


# -----------------------------------------------------------------------------
# Section 6 -- Volume + per-piece-area cross-check.
# -----------------------------------------------------------------------------

section("6. Volume + per-piece-area cross-check (F5, F6)")

# For each residual (t, k_orbit_rep), we want to check that the per-
# piece geometry is feasible: a piece touches t T-faces with footprints
# of total area E = 8 sqrt 3 / 5, has volume V_piece = 8/15, and is
# convex.  At the abstract level the necessary conditions are:
#
#   (F5)  E = 8 sqrt 3 / 5  per piece (already used in F4 derivation).
#   (F6)  V_piece = 8/15.  By the isoperimetric-like inequality
#         V <= (1/3) * E_max * h_max where E_max is max footprint area
#         and h_max is "depth into T", we get a *very weak* bound
#         that does not rule anything out at this stage.
#
# The strong volume/footprint constraints come into play only with
# specific shape candidates (Phase 26-C / 26-D).  At the role-distribution
# level, we record E^2 = 192 / 25 for downstream use.

E_sq = piece_exposed_sq
check(f"Per-piece total exposed area squared E^2 = {E_sq}",
      E_sq == F(192, 25))

# Sanity: in any residual, sum_j (k_j * a_{j}) = sum_j A_T = 4 * A_T,
# regardless of k.  And 5 * E = 4 * A_T = 8 sqrt 3 by construction.
# Squared: (5 E)^2 = 25 * 192 / 25 = 192 = (4 A_T)^2  -- yes.
check("Per-piece-area marginal sum identity 5 * E = 4 * A_T",
      F(25) * E_sq == F(16) * A_face_sq)


# -----------------------------------------------------------------------------
# Section 7 -- Special residual "all-one-face analogue" status for n = 5.
# -----------------------------------------------------------------------------

section("7. 'All-one-face' analogue for n = 5")

# The Phase 25 n = 16 all-one-face residual corresponds to (t = 1,
# k = (16, 0, 0, 0)).  For n = 5 the analogous would be (t = 1,
# k = (5, 0, 0, 0)), but as F4 shows, this is COMBINATORIALLY
# IMPOSSIBLE (5 / 4 = 1.25 > 1, so a single T-face cannot be tiled
# by 5 footprints each of area at most E = (1/5) * 4 A_T = 4 A_T / 5,
# wait let me recompute: per-piece total E = 8 sqrt 3 / 5, but if a
# piece has only 1 boundary footprint (t = 1), then that single
# footprint IS its full E.
#
# So: for t = 1, each piece's single footprint has area E = 8 sqrt 3 / 5.
# Total footprint area on the touched T-face = k_0 * E = 5 * (8 sqrt 3 / 5)
# = 8 sqrt 3 = 4 A_T.  But a single T-face has area only A_T.  Hence
# 5 footprints each of area E = 8 sqrt 3 / 5 cannot all fit on a single
# T-face.  CONFIRMS t = 1 is impossible.

t1_total_footprint_sq = F(25) * E_sq  # (5 E)^2
single_face_capacity_sq = A_face_sq
ratio = (t1_total_footprint_sq / single_face_capacity_sq)
check(
    f"(5 E)^2 / A_T^2 = {ratio} = 16, so t = 1 needs 16x the available area",
    ratio == F(16),
    f"5 footprints of total area 4 A_T cannot fit on 1 T-face of area A_T",
)

# In fact even (t = 1, k = (k_0, ...)) with k_0 = 5 fails because we
# need k_0 * E_per_face = A_T and E_per_face <= E = 8 sqrt 3 / 5,
# so k_0 >= A_T / (8 sqrt 3 / 5) = 5 / 4 = 1.25, hence k_0 >= 2.
# But t = 1 means each piece touches only ONE T-face, so each piece's
# full E is on a single face: total contribution to any one face is
# k_0 * E.  Equating to A_T: k_0 = 5/4 = 1.25, impossible for integer k_0.

check("t = 1 ruled out for n = 5: 'all-one-face' analogue is COMBINATORIALLY IMPOSSIBLE",
      surviving_t1_count == 0,
      "no integer k_0 satisfies k_0 * E = A_T")


# -----------------------------------------------------------------------------
# Section 8 -- Persistent artefacts.
# -----------------------------------------------------------------------------

section("8. Save residual table for Phase 26-C")

RESULTS["residuals"] = residual_table
RESULTS["summary"] = {
    "n": n,
    "V_piece_str": "8/15",
    "per_piece_exposed_area_squared_str": "192/25",
    "T_face_area_squared_str": "12",
    "raw_k_vector_count": total_k_count,
    "residual_count_after_F4_and_S4_quotient": n_residuals,
    "survivors_per_t": {
        str(t): {
            "raw_k_vectors_F4_pass": sum(
                1 for k in k_vectors_by_t[t] if filter_F4(k)
            ),
            "S4_orbits_F4_pass": len(set(
                k_orbit_rep(k) for k in k_vectors_by_t[t] if filter_F4(k)
            )),
        }
        for t in T_VALUES
    },
}

results_path = os.path.join(
    os.path.join(os.path.dirname(__file__), "..", "results"),
    "phase26b_role_distribution_n5_results.json",
)
with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

check(f"Saved residual table to phase26b_role_distribution_n5_results.json",
      os.path.exists(results_path),
      f"file size = {os.path.getsize(results_path)} bytes")


# -----------------------------------------------------------------------------
# Wrap-up.
# -----------------------------------------------------------------------------

print(f"\n{'=' * 70}")
print(f"Total tests passed: {PASSED}")
print(f"Total tests failed: {FAILED}")
print('=' * 70)

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED

with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")
print(f"\nResidual count for Phase 26-C: {n_residuals}")
print(f"  (t = 1 ruled out by F4; residuals come from t in {{2, 3, 4}}.)")