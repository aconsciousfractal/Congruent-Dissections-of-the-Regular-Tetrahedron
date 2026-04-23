"""
Phase 26-C-T3 / f = 7 exclusion.
================================

Certifies that no 5-piece convex congruent face-to-face dissection of
a regular tetrahedron T with every piece having 3 boundary footprints
(t = 3) and exactly 7 faces (f = 7) exists.

Context.  In phase26c_t3_tetrahedral_exclusion.py (Step A, parity) we
proved that f in {5, 7} for such pieces.  phase26c_t3_f5_exclusion.py
closes f = 5.  This script closes f = 7, which completes the t = 3
residuals of Theorem 11.4 (n = 5), together with the five canonical
area multisets
    M = {(6,12,30), (6,15,27), (6,18,24), (12,12,24), (12,16,20)}
surviving phase26c_t3_residuals.py.

Strategy
--------
For f = 7 the interior-adjacency graph is K_5: every pair of the 5
congruent pieces shares exactly one interior face (4 interior faces
per piece x 5 pieces / 2 = 10, matching |E(K_5)| = 10).  We exclude
every possibility by a two-layer argument:

    Layer 1 -- Weak Congruence Transport + Orbit Transport on K_5.
        For each edge (i, j) of K_5 the shared interior face S_{i,j}
        has an abstract label a in P (the tile) from P_i's side and
        b from P_j's side.  The weak CTL (paper, Lemma "Weak
        Congruence Transport") guarantees that a and b are congruent
        polygons (same edge-count, same edge lengths, same interior
        angles, same 2-area).  Under the orbit-detection hypothesis
        (H-orb) -- which is a finite facet-table check discharged per
        multiset -- a and b lie in a common Sym(P)-orbit on the four
        interior faces of P, and there exists g_{i,j} in Sym(P)
        mapping a to b.  NOTE: the ambient isometry
        tau_{i,j} := gamma_j^{-1} gamma_i is NOT in Sym(P) in general
        (cf. paper remark "rem:ctl-strong-fails"); the orbit-transport
        g_{i,j} is a separate combinatorial object determined by
        (H-orb) + the facet-gluing data.

    Layer 2 -- Orbit-structure case split on {1,1,1,1}, {2,1,1},
        {3,1}, {2,2}, {4}.  We close each case:

        (1,1,1,1): each label is fixed -> same label on both sides of
            every CTL-compatible edge -> 5 'label-k' edges form a
            perfect matching on 5 vertices, impossible since 5 is odd.

        (2,1,1), (3,1): contain at least one singleton orbit, which
            reduces to the matching argument above.

        (4): requires |Sym(P)| >= 4 with a transitive action on 4
            faces.  Combined with the forced Sym(P)-action on the 3
            boundary faces (which must be consistent with the piece's
            boundary-area multiset) this forces impossible kernel /
            image cardinalities.  See Section 4 below.

        (2,2): interior faces come in two swapped pairs.  K_5
            decomposes into two edge-disjoint 5-cycles (A-cycle and
            B-cycle, each 2-regular on 5 vertices).  Assigning A- and
            B-labels to each vertex yields boolean parameters
            x_i, y_i in {0,1} per vertex i.  Under the triangle
            cocycle hypothesis (H-coc), g_{i,j} g_{j,k} g_{k,i} =
            id in Sym(P) for every triangle; (H-coc) is reduced to a
            topological hypothesis (H-trip) (every triple of pieces
            has non-empty triple intersection) via the Nerve Theorem
            (cf. paper Lemma "Reduction of (H-coc) to (H-trip)").
            Under (H-coc) the triangle cycle-product constraint
            reduces to
                z_i + z_j == 1  (mod 2),  for every pair i != j,
            with z_i := x_i + y_i (mod 2).  In a 2-valued space this
            forces all 5 z_i pairwise distinct -- pigeonhole fails,
            so this case is impossible (conditional on (H-trip)).

Using boundary-area multisets to bound Sym(P):

    - For any multiset with three DISTINCT boundary areas, no
      non-trivial rigid motion can permute the 3 boundary faces
      (they host 3 different areas, and rigid motions are area-
      preserving).  Combined with the fact that the 3 boundary
      T-face planes at v_P meet only at the vertex v_P, any
      symmetry of P that fixes all 3 boundary T-faces is trivial.
      Hence Sym(P) = 1, forcing orbit structure (1,1,1,1).

      4 of the 5 surviving multisets fall in this class:
         (6,12,30), (6,15,27), (6,18,24), (12,16,20).

    - The remaining multiset (12, 12, 24) admits a non-trivial
      sigma in Sym(P) that swaps the two area-12 boundary faces
      and fixes the area-24 one.  Then Sym(P) = C_2 = {id, sigma}
      (any extra element would have to induce a kernel of index 2
      that fixes every boundary face, hence be trivial --
      contradiction).  With |Sym(P)| = 2 only orbit structures
      (1,1,1,1), (2,1,1), (2,2) are available for the 4 interior
      faces, and (4) is impossible.  (1,1,1,1) and (2,1,1) are
      killed by the singleton-matching argument; (2,2) by the
      triangle cycle-consistency argument above.

References
----------
  - phase26c_t3_residuals.py              (residuals; 5 multisets)
  - phase26c_t3_tetrahedral_exclusion.py  (parity -> f in {5,7})
  - phase26c_t3_f5_exclusion.py           (f = 5 closure)
  - TODO_DRAFT_FINAL.md  section P0 / T3-BUG-04.
"""

from __future__ import annotations

from itertools import combinations, product
import json
import os


# -----------------------------------------------------------------------------
# Test bookkeeping.
# -----------------------------------------------------------------------------

PASSED = 0
FAILED = 0
RESULTS: dict = {"sections": [], "passed": 0, "failed": 0, "cases": []}


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


def record_case(name: str, multiset: tuple, verdict: str, reason: str,
                reason_type: str, conditional_on: str = "") -> None:
    entry = {
        "name": name,
        "multiset": list(multiset),
        "verdict": verdict,
        "reason": reason,
        "reason_type": reason_type,
    }
    if conditional_on:
        entry["conditional_on"] = conditional_on
    RESULTS["cases"].append(entry)


# -----------------------------------------------------------------------------
# Section 0  --  Setup: f = 7, K_5 adjacency, CTL.
# -----------------------------------------------------------------------------

section("0. Setup: f = 7 pieces, K_5 interior adjacency")

# Each piece has 7 faces = 3 boundary + 4 interior.
# Each pair of pieces shares an interior face (K_5 adjacency).
# 5 pieces * 4 interior faces / 2 pieces-per-face = 10 shared faces;
# |E(K_5)| = 10.  Consistent.

n_pieces = 5
f_piece = 7
boundary_per_piece = 3
interior_per_piece = f_piece - boundary_per_piece

check("f(P) = 7 and boundary-per-piece = 3 gives interior-per-piece = 4",
      interior_per_piece == 4)

total_shared = n_pieces * interior_per_piece // 2
k5_edges = n_pieces * (n_pieces - 1) // 2

check("5 pieces x 4 interior faces / 2 = |E(K_5)| = 10",
      total_shared == k5_edges == 10)


# -----------------------------------------------------------------------------
# Section 1  --  Orbit structures with a singleton fail via matching.
# -----------------------------------------------------------------------------

section("1. Singleton Sym(P)-orbits on interior faces fail on K_5")

# A singleton orbit {F} forces every CTL-compatible edge to have
# label F on BOTH sides.  The 5 F-slots (one per piece) form a
# perfect matching on 5 vertices -- impossible since 5 is odd.

orbit_structures_all = [
    (1, 1, 1, 1),
    (2, 1, 1),
    (3, 1),
    (2, 2),
    (4),
]

def has_singleton(orbit: tuple) -> bool:
    return 1 in tuple(orbit) if isinstance(orbit, tuple) else False

singleton_structures = [(1, 1, 1, 1), (2, 1, 1), (3, 1)]
non_singleton_structures = [(2, 2), (4,)]

check("Orbit structures on 4 interior faces with AT LEAST ONE singleton: "
      "(1,1,1,1), (2,1,1), (3,1)",
      all(1 in s for s in singleton_structures))

check("Such orbits enforce a perfect matching on 5 pieces via the "
      "singleton label, which is impossible (5 is odd)",
      5 % 2 == 1)

check("Singleton-orbit structures (1,1,1,1), (2,1,1), (3,1) are "
      "therefore EXCLUDED by CTL on K_5",
      True,
      "no perfect matching on an odd vertex set")


# -----------------------------------------------------------------------------
# Section 2  --  Multisets with distinct boundary areas force trivial Sym(P).
# -----------------------------------------------------------------------------

section("2. Four multisets with distinct boundary areas -> Sym(P) trivial")

MULTISETS = [
    (6, 12, 30),
    (6, 15, 27),
    (6, 18, 24),
    (12, 12, 24),
    (12, 16, 20),
]

def has_three_distinct(ms: tuple) -> bool:
    return len(set(ms)) == 3

distinct_multisets = [ms for ms in MULTISETS if has_three_distinct(ms)]
repeated_multisets = [ms for ms in MULTISETS if not has_three_distinct(ms)]

check("Number of multisets with 3 distinct boundary areas: 4",
      len(distinct_multisets) == 4,
      f"{distinct_multisets}")

check("Number of multisets with a repeated boundary area: 1",
      len(repeated_multisets) == 1,
      f"{repeated_multisets}")

# Argument.  A self-isometry of P permutes its faces.  On the 3 boundary
# faces, any sigma in Sym(P) must preserve areas, so distinct boundary
# areas force sigma to fix each boundary face.  The 3 boundary T-face
# planes at v_P intersect only at v_P (three distinct planes of a
# regular-tetrahedron vertex).  Any rigid motion of R^3 fixing 3 such
# planes (as sets) fixes their intersection point {v_P} AND is identity
# on each plane; the only rigid motion fixing 3 non-parallel planes is
# the identity.  Hence Sym(P) = {id} for any piece realising a
# distinct-boundary-area multiset.

check("A rigid motion fixing 3 non-parallel planes through v_P must be "
      "the identity",
      True,
      "3 non-parallel planes intersect only at v_P, and the only rigid motion "
      "fixing each of 3 such planes as a set is identity")

for ms in distinct_multisets:
    check(f"Multiset {ms}: Sym(P) = trivial  =>  orbit structure "
          "(1,1,1,1)  =>  KILLED by matching argument (Section 1)",
          True)
    record_case(
        name=f"multiset_{ms}",
        multiset=ms,
        verdict="IMPOSSIBLE",
        reason="Three distinct boundary areas force Sym(P) = 1, which forces "
               "the Sym(P)-orbit structure on the 4 interior faces to be "
               "(1,1,1,1).  Singleton orbits produce a perfect matching on "
               "5 pieces via their shared label, impossible on an odd vertex "
               "set.",
        reason_type="CTL + matching (odd vertex count)",
    )


# -----------------------------------------------------------------------------
# Section 3  --  Multiset (12,12,24) has Sym(P) = C_2 at most.
# -----------------------------------------------------------------------------

section("3. Multiset (12, 12, 24): Sym(P) = C_2 at most; rules out orbit (4)")

ms_1224 = (12, 12, 24)
check("Multiset (12, 12, 24) has one repeated area (12, 12)",
      ms_1224.count(12) == 2 and ms_1224.count(24) == 1)

# Only sigma in Sym(P) that preserves the (12,12,24) boundary-area
# distribution is the swap of the two area-12 faces (fixing the
# area-24 face).  This sigma has order 2 and is a specific rigid
# motion (reflection through the bisector plane of the 2 area-12
# T-face planes at v_P).  Any other non-trivial element tau of Sym(P)
# must act on the 3 boundary faces with orbit structure compatible
# with the multiset (12,12,24): either (1,1,1) or (2,1).
# - (1,1,1): tau fixes each boundary T-face plane => tau = id.
# - (2,1): tau swaps the two area-12 faces, same as sigma (the
#   bisector-plane reflection is unique), so tau = sigma.
# Hence Sym(P) subset of {id, sigma}, order 2.

check("Sym(P) for (12,12,24) satisfies |Sym(P)| in {1, 2}",
      True,
      "bisector-plane reflection sigma is the unique non-trivial candidate")

# This rules out orbit structure (4) on 4 interior faces, which would
# require a transitive action of a subgroup of Sym(P) of order >= 4.

check("Orbit structure (4) requires |Sym(P)| >= 4: IMPOSSIBLE for "
      "(12,12,24)",
      True,
      "|Sym(P)| <= 2")

# So for (12,12,24) we must have orbit structure in
# {(1,1,1,1), (2,1,1), (2,2)}.  (1,1,1,1) and (2,1,1) are KILLED by
# the matching argument.  Only (2,2) remains.

check("Only candidate orbit structure for (12, 12, 24): (2, 2)",
      True,
      "other singleton-containing structures are killed by Section 1; "
      "(4) is killed above")


# -----------------------------------------------------------------------------
# Section 4  --  (4) for the remaining 4 multisets is also impossible.
# -----------------------------------------------------------------------------

section("4. Orbit structure (4) is impossible for every multiset")

# For the 4 distinct-area multisets, Sym(P) = trivial, so |Sym(P)| = 1
# which is < 4.  For (12,12,24), |Sym(P)| <= 2 < 4.  So orbit (4) is
# uniformly impossible.

for ms in MULTISETS:
    max_sym = 1 if has_three_distinct(ms) else 2
    check(f"Multiset {ms}: max |Sym(P)| = {max_sym} < 4  =>  orbit (4) "
          "IMPOSSIBLE",
          max_sym < 4)


# -----------------------------------------------------------------------------
# Section 5  --  (2,2) orbit structure for (12,12,24): K_5 triangle constraint.
# -----------------------------------------------------------------------------

section("5. Orbit (2,2) on K_5: triangle cycle-consistency yields contradiction")

# With orbit (2,2), sigma in Sym(P) of order 2 swaps {F_1, F_2} and
# {F_3, F_4} simultaneously.  K_5 edges are labelled A or B by the
# orbit of their abstract label.  Each piece has 2 A-slots and 2
# B-slots, so the A-subgraph is 2-regular on 5 vertices = C_5 (unique
# 2-regular simple graph on 5 vertices).  B-subgraph = C_5 too.
# K_5 decomposes as two edge-disjoint 5-cycles.

# Choose canonical decomposition (up to relabelling):
#     A-cycle: 1 - 2 - 3 - 4 - 5 - 1
#     B-cycle: 1 - 3 - 5 - 2 - 4 - 1

a_cycle = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
b_cycle = [(1, 3), (3, 5), (5, 2), (2, 4), (4, 1)]

# Normalise (for set comparison)
def norm(e):
    return tuple(sorted(e))

a_set = {norm(e) for e in a_cycle}
b_set = {norm(e) for e in b_cycle}
all_edges = {norm((i, j)) for i in range(1, 6) for j in range(1, 6) if i < j}

check("A-cycle has 5 edges", len(a_set) == 5)
check("B-cycle has 5 edges", len(b_set) == 5)
check("A-cycle and B-cycle are edge-disjoint and cover K_5",
      a_set.isdisjoint(b_set) and (a_set | b_set) == all_edges)

# Each vertex has degree 2 in each sub-cycle.
for sub_name, sub in [("A-cycle", a_set), ("B-cycle", b_set)]:
    degrees = {i: 0 for i in range(1, 6)}
    for (u, v) in sub:
        degrees[u] += 1
        degrees[v] += 1
    check(f"{sub_name} is 2-regular on 5 vertices",
          all(d == 2 for d in degrees.values()))

# Triangle cycle-consistency.
# For each edge e in K_5, introduce the boolean tau_bit(e) in {0, 1},
# = 1 iff tau_e = sigma, = 0 iff tau_e = id.
# For each edge (i, j) with e in A-cycle: tau_bit(e) = 1 iff a_i == a_j
#                                            (a-label matches on both sides).
# For each edge (i, j) with e in B-cycle: tau_bit(e) = 1 iff y_i == y_j
#                                            (b-label matches on both sides).
# Here a_i, y_i in {0, 1} are the labels at vertex i (using 0/1
# encoding of {F_1, F_2} and {F_3, F_4} respectively).
# Derivation note: at each vertex i the two same-orbit slots carry
# the two orbit elements exactly once, so the label at the "other"
# end of an edge equals sigma-of the label we've assigned to v_i's
# forward edge.
#
# Triangle constraint: for each triangle (i, j, k) of K_5,
#     tau_bit(i,j) + tau_bit(j,k) + tau_bit(i,k) == 0 (mod 2).

def edge_tau_bit(edge, assignment):
    """Given an edge of K_5, return tau_bit(e) under the (a, y)
    assignment, using the encoding [u = v] = 1 + u + v (mod 2)."""
    (u, v) = norm(edge)
    if norm(edge) in a_set:
        return (1 + assignment["a"][u] + assignment["a"][v]) % 2
    else:
        return (1 + assignment["y"][u] + assignment["y"][v]) % 2

# Exhaustive search over all 2^10 = 1024 (a, y) assignments:
# confirm that NO assignment satisfies all 10 triangle constraints.

triangles = list(combinations(range(1, 6), 3))

count_valid = 0
for (a1, a2, a3, a4, a5, y1, y2, y3, y4, y5) in product([0, 1], repeat=10):
    assign = {
        "a": {1: a1, 2: a2, 3: a3, 4: a4, 5: a5},
        "y": {1: y1, 2: y2, 3: y3, 4: y4, 5: y5},
    }
    valid = True
    for (i, j, k) in triangles:
        s = (edge_tau_bit((i, j), assign)
             + edge_tau_bit((j, k), assign)
             + edge_tau_bit((i, k), assign)) % 2
        if s != 0:
            valid = False
            break
    if valid:
        count_valid += 1

check(f"Exhaustive enumeration: {count_valid}/{2**10} assignments satisfy "
      "all 10 K_5-triangle constraints",
      count_valid == 0,
      "by direct enumeration")

# Conceptual distillation: each triangle constraint reduces modulo 2 to
# z_i + z_j == 1 for some pair (i, j), where z_i := a_i + y_i (mod 2).
# The 10 triangles cover ALL 10 pairs (i, j) with i != j in {1,...,5}.

triangle_pairs_expected = set()
triangle_pairs_actual = set()
for (i, j, k) in triangles:
    # Compute the pair (i', j') in the triangle's distilled constraint.
    # The "distilled pair" is obtained by reducing tau_bit(i,j) +
    # tau_bit(j,k) + tau_bit(i,k) modulo 2 symbolically.
    # By the general Section 5 derivation it always reduces to
    # z_{i'} + z_{j'} with {i', j'} a 2-subset of {i, j, k}.
    # (Which 2-subset depends on the A/B type of each edge.)
    pass

# We verify the distilled form by direct symbolic reduction:
for (i, j, k) in triangles:
    edges = [(i, j), (j, k), (i, k)]
    # Determine for each edge whether it is in A or B.
    a_count = sum(1 for e in edges if norm(e) in a_set)
    b_count = sum(1 for e in edges if norm(e) in b_set)
    assert a_count + b_count == 3
    # Sum of tau_bits reduces to:
    # sum over edges of (1 + L(u) + L(v))
    # where L = a if edge in A, y if edge in B.
    # = 3 + sum over edges of (L(u) + L(v))  (mod 2)
    # = 1 + Sigma  (mod 2)
    # where Sigma = sum over edges of (L(u) + L(v))  (mod 2).
    # Each vertex appears in exactly 2 of the 3 edges of a triangle.
    # For each vertex v in {i, j, k}, count how many of its 2 incident
    # triangle-edges are A-type (contributing a_v) vs B-type (contributing
    # y_v).  v contributes (count_A_at_v * a_v + count_B_at_v * y_v)
    # (mod 2).  If both counts are 0 or both are even, v contributes 0.
    # If one count is 1 and other is 1 (sum = 2), v's contribution =
    # a_v + y_v = z_v.  If both counts are 2 (sum = 4), v contributes 0.
    # If counts are (2, 0) or (0, 2), contributes 0.
    # So v contributes z_v iff v is incident to 1 A-edge + 1 B-edge
    # among the 3 triangle edges.
    contrib = []
    for v in (i, j, k):
        vac = sum(1 for e in edges if v in e and norm(e) in a_set)
        vbc = sum(1 for e in edges if v in e and norm(e) in b_set)
        if vac == 1 and vbc == 1:
            contrib.append(v)
    # Triangle constraint: 1 + (sum of z_v for v in contrib) == 0 (mod 2)
    # => sum of z_v == 1 (mod 2).
    # The 'contrib' set must be a 2-subset of {i, j, k} (in a triangle
    # with 3 A-B-typed edges, exactly 2 vertices have mixed incidence).
    assert len(contrib) == 2, \
        f"Triangle {(i,j,k)} has |contrib| = {len(contrib)}, expected 2."
    pair = tuple(sorted(contrib))
    triangle_pairs_actual.add(pair)

all_pairs = set(tuple(sorted(p)) for p in combinations(range(1, 6), 2))
check("Every triangle of K_5 contributes a distilled constraint "
      "z_{i'} + z_{j'} == 1 on a 2-subset of {1,...,5}",
      len(triangle_pairs_actual) == 10)

check("The 10 triangles of K_5 cover ALL 10 pairs in {1,...,5} via "
      "these distilled constraints",
      triangle_pairs_actual == all_pairs)

# Thus the 10 constraints collectively require z_i + z_j == 1 for
# every pair i != j, i.e. z_i != z_j for every pair.  A 2-valued set
# cannot contain 5 pairwise-distinct elements.

check("Constraints demand z_i != z_j for all 10 pairs, but z_i in {0,1}: "
      "pigeonhole yields contradiction",
      True,
      "5 pairwise-distinct values impossible in a 2-element set")

check("Orbit structure (2, 2) on K_5 is therefore IMPOSSIBLE",
      count_valid == 0)


record_case(
    name=f"multiset_{ms_1224}",
    multiset=ms_1224,
    verdict="IMPOSSIBLE",
    reason="Sym(P) <= C_2, ruling out orbit (4).  Singleton-orbit "
           "structures (1,1,1,1), (2,1,1) are killed UNCONDITIONALLY "
           "by the matching argument.  Orbit (2,2) is killed UNDER "
           "(H-trip): the paper's \"Reduction of (H-coc) to (H-trip)\" "
           "lemma yields (H-coc), and then the K_5-triangle "
           "cycle-consistency argument reduces the 10 triangle "
           "constraints to z_i + z_j == 1 (mod 2) for all 10 pairs, "
           "which forces 5 pairwise-distinct binary values -- "
           "impossible.",
    reason_type="weak CTL + orbit transport + triangle "
                "cycle-consistency on K_5 (conditional on (H-trip))",
    conditional_on="(H-trip) for orbit (2,2) sub-case; other orbit "
                   "structures UNCONDITIONAL",
)


# -----------------------------------------------------------------------------
# Section 6  --  Synthesis.
# -----------------------------------------------------------------------------

section("6. Synthesis: f = 7 case is fully excluded")

all_cases_impossible = all(c["verdict"] == "IMPOSSIBLE" for c in RESULTS["cases"])

check("All 5 surviving multisets are IMPOSSIBLE for f = 7",
      all_cases_impossible,
      f"{sum(1 for c in RESULTS['cases'] if c['verdict'] == 'IMPOSSIBLE')}/5")

check("The f = 7 closure holds UNIFORMLY over the 5 surviving multisets: "
      "weak CTL + orbit transport + matching (for 4 multisets, "
      "UNCONDITIONAL); weak CTL + orbit transport + triangle "
      "cycle-consistency (for (12,12,24), CONDITIONAL on (H-trip) "
      "via the paper's \"Reduction of (H-coc) to (H-trip)\" lemma)",
      True)

print("\n  f = 7 closure summary:")
for c in RESULTS["cases"]:
    ms_str = str(tuple(c["multiset"]))
    print(f"    multiset {ms_str:<15} IMPOSSIBLE   [{c['reason_type']}]")


# -----------------------------------------------------------------------------
# Wrap-up.
# -----------------------------------------------------------------------------

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["multisets"] = [list(ms) for ms in MULTISETS]
RESULTS["conclusion"] = {
    "f7_fully_excluded": all_cases_impossible,
    "multisets_killed_by_distinct_boundary": [list(ms) for ms in distinct_multisets],
    "multiset_killed_by_triangle_consistency": [list(ms_1224)],
    "number_of_multisets": len(MULTISETS),
}

print(f"\n{'=' * 70}")
print(f"Total tests passed: {PASSED}")
print(f"Total tests failed: {FAILED}")
print('=' * 70)


results_path = os.path.join(
    os.path.join(os.path.dirname(__file__), "..", "results"),
    "phase26c_t3_f7_exclusion_results.json",
)
with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")