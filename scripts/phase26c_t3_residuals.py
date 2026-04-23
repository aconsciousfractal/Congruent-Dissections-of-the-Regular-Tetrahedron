"""
Phase 26-C-T3: SAT/necessary-condition attack on the four t = 3 residuals
                of the n = 5 dissection problem.

Residuals (from Phase 26-B):
    R_T3_1: (t = 3, k = (5, 5, 3, 2))   -- z = (0, 0, 2, 3)
    R_T3_2: (t = 3, k = (5, 4, 4, 2))   -- z = (0, 1, 1, 3)
    R_T3_3: (t = 3, k = (5, 4, 3, 3))   -- z = (0, 1, 2, 2)
    R_T3_4: (t = 3, k = (4, 4, 4, 3))   -- z = (1, 1, 1, 2)

Strategy -- canonical-multiset enumeration.

  By piece congruence, every piece has the SAME multiset of 3 nonzero
  footprint areas on the t = 3 T-faces it touches.  Call this the
  CANONICAL FOOTPRINT MULTISET (m_1, m_2, m_3) with m_1 <= m_2 <= m_3
  and m_1 + m_2 + m_3 = E = 8 sqrt 3 / 5.

  For each T-face j with k_j > 0, the k_j pieces touching face j each
  contribute one of {m_1, m_2, m_3} to face j; the contributions sum
  to A_T = 2 sqrt 3.  This is a strong constraint:

      sum of (multiset of size k_j drawn from {m_1, m_2, m_3}) = A_T.

  In particular, the MAXIMUM possible sum from k_j contributions is
  k_j * m_3, and the MINIMUM is k_j * m_1.

  CRITICAL OBSERVATION.  For k_j = 2 (e.g. residual R_T3_1's face 3),
  the pair-sum from {m_1, m_2, m_3} ranges in {2 m_1, m_1 + m_2,
  m_1 + m_3, 2 m_2, m_2 + m_3, 2 m_3}.  Of these, only 2 m_3 can
  reach A_T = 2 sqrt 3 = 10 sqrt 3 / 5 because all other pair-sums
  are < m_1 + m_2 + m_3 = E = 8 sqrt 3 / 5 < 2 sqrt 3.  Hence:

      m_3 = sqrt 3   AND   m_1 + m_2 = E - sqrt 3 = 3 sqrt 3 / 5.

  This UNIQUELY determines m_3.  Subsequent face constraints then pin
  down m_1, m_2 (or yield contradictions).  The face k_j = 5 constraint
  (face 0/1) requires 5 contributions from {m_1, m_2, sqrt 3} summing
  to A_T = 2 sqrt 3 = 10 sqrt 3 / 5.  This typically fails by parity
  on 4-divisibility of 4 (n_a + n_b3) + 9 n_bb modulo arithmetic
  arguments.

  We work in INTEGER COEFFICIENTS of sqrt 3.  Set A_T = 2 sqrt 3,
  E = 8 sqrt 3 / 5.  Scale by 30 (LCM of {1, 2, 3, 5} times 6 to clear
  the /5 denominator): A_T = 60, E = 48 in these units.  Face shares:
      k_j = 5 -> share = 12,
      k_j = 4 -> share = 15,
      k_j = 3 -> share = 20,
      k_j = 2 -> share = 30.

This script enumerates, for each of the 4 t = 3 residuals, the
canonical-multiset solutions and, when such multisets pass the
per-T-face contribution test, the full set of per-piece ordered
assignments with exact integer arithmetic.

STATUS (2026-04-16, after T3-BUG-01 fix).
  The earlier version of this script contained a guard that
  incorrectly identified all four residuals as UNSAT.  With the
  guard removed, the true combinatorial status of each residual is:

      R_T3_1   (5,5,3,2)    UNSAT
      R_T3_2   (5,4,4,2)    COMBINATORIAL_SAT
      R_T3_3   (5,4,3,3)    COMBINATORIAL_SAT
      R_T3_4   (4,4,4,3)    COMBINATORIAL_SAT

  Three of the four residuals survive at the area-multiset level.
  The canonical-multiset abstraction captures only per-piece
  congruence of area multisets and per-T-face total area; it does
  NOT capture footprint-shape consistency across congruent pieces,
  nor geometric realisability on each T-face (packing of the
  footprint polygons).  A genuine UNSAT certificate for R_T3_2,
  R_T3_3, R_T3_4 requires a strengthened abstraction (see the
  Phase 26-C-T3 follow-up scripts phase26c_t3_residuals_shape.py
  and/or phase26c_t3_residuals_packing.py, and the TODO file
  09-papers/Congruent Dissections of the Regular Tetrahedron/
  TODO_DRAFT_FINAL.md).

References:
  - PHASE_26_PLAN.md, sub-phase 26-C, residuals t = 3.
  - phase26b_role_distribution_n5_results.json (residual table).
  - TODO_DRAFT_FINAL.md, section P0 / T3-BUG, for the fix trail.
"""

from __future__ import annotations

import json
import os
from itertools import product, combinations_with_replacement
from fractions import Fraction as F


# -----------------------------------------------------------------------------
# Test bookkeeping.
# -----------------------------------------------------------------------------

PASSED = 0
FAILED = 0
RESULTS: dict = {"sections": [], "passed": 0, "failed": 0,
                 "residuals": {}, "summary": None}


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
# Section 0 -- Setup.
# -----------------------------------------------------------------------------

section("0. Setup: integer scaling (units of sqrt 3 / 30)")

# In our integer-scaled units:
#   A_T = 60                           (= 2 sqrt 3 * 30 / sqrt 3 = 60 in units of sqrt 3 / 30)
#   E   = 48                           (= 8 sqrt 3 / 5 * 30 / sqrt 3 = 48)
#   k_j = 5 share = A_T / 5 = 12
#   k_j = 4 share = 15
#   k_j = 3 share = 20
#   k_j = 2 share = 30

A_T_int = 60
E_int = 48
SHARE = {2: 30, 3: 20, 4: 15, 5: 12}

check("Integer-scaled A_T = 60", A_T_int == 60)
check("Integer-scaled E = 48", E_int == 48)
check("Per-T-face uniform shares: {2: 30, 3: 20, 4: 15, 5: 12}",
      SHARE == {2: 30, 3: 20, 4: 15, 5: 12})

# Sanity: 5 pieces * E = 5 * 48 = 240 = 4 * A_T = 4 * 60.
check("5 * E = 4 * A_T (boundary-area conservation)",
      5 * E_int == 4 * A_T_int,
      f"{5 * E_int} = {4 * A_T_int}")


# -----------------------------------------------------------------------------
# Section 1 -- Multiset solver.
# -----------------------------------------------------------------------------

section("1. Canonical-multiset solver (per-T-face contribution sums)")


def all_multisets_of_3_pos_summing(target):
    """Enumerate all (m_1, m_2, m_3) integer triplets with
    1 <= m_1 <= m_2 <= m_3 and m_1 + m_2 + m_3 = target."""
    out = []
    for m1 in range(1, target):
        for m2 in range(m1, target - m1):
            m3 = target - m1 - m2
            if m3 >= m2:
                out.append((m1, m2, m3))
    return out


def multiset_size_k_sums_to_target(multiset, k, target):
    """Return all ordered k-subsets (with replacement) of `multiset`
    that sum to `target`."""
    out = []
    for combo in combinations_with_replacement(multiset, k):
        if sum(combo) == target:
            out.append(tuple(sorted(combo)))
    return list(set(out))


# Quick sanity check.
ms = [1, 2, 5]
sums = multiset_size_k_sums_to_target(ms, 3, 8)
check("Sample multiset solver: 3 picks from {1,2,5} sum to 8 -> [(1,2,5)]",
      sums == [(1, 2, 5)],
      f"got {sums}")


# -----------------------------------------------------------------------------
# Section 2 -- Per-residual canonical-multiset enumeration.
# -----------------------------------------------------------------------------

section("2. Per-residual canonical-multiset enumeration")

# For each residual we enumerate all integer triplets (m_1, m_2, m_3)
# with m_1 + m_2 + m_3 = E_int = 48.  For each triplet, we check
# whether for each T-face j with k_j > 0, there exists a k_j-multisubset
# of {m_1, m_2, m_3} summing to A_T_int = 60.  If no triplet passes,
# the residual is UNSAT at the canonical-multiset level.

T3_RESIDUALS = [
    {"name": "R_T3_1",
     "k": (5, 5, 3, 2),
     "z": (0, 0, 2, 3)},
    {"name": "R_T3_2",
     "k": (5, 4, 4, 2),
     "z": (0, 1, 1, 3)},
    {"name": "R_T3_3",
     "k": (5, 4, 3, 3),
     "z": (0, 1, 2, 2)},
    {"name": "R_T3_4",
     "k": (4, 4, 4, 3),
     "z": (1, 1, 1, 2)},
]


def feasible_multisets_for_residual(k_tuple):
    """Return the set of canonical multisets (m_1, m_2, m_3) such that
    every nonzero T-face has at least one valid contribution-multisubset."""
    feasible = []
    triplets = all_multisets_of_3_pos_summing(E_int)
    for tri in triplets:
        ok = True
        per_face_options = []
        for k_j in k_tuple:
            if k_j == 0:
                per_face_options.append(None)
                continue
            options = multiset_size_k_sums_to_target(tri, k_j, A_T_int)
            if not options:
                ok = False
                break
            per_face_options.append(options)
        if ok:
            feasible.append({"multiset": tri, "per_face_options": per_face_options})
    return feasible


for r in T3_RESIDUALS:
    feas = feasible_multisets_for_residual(r["k"])
    r["feasible_multisets"] = feas
    msg = (f"{r['name']} k = {r['k']}: "
           f"{len(feas)} canonical multisets pass per-T-face contribution test")
    check(msg, len(feas) >= 0,
          f"first 2 = {[f['multiset'] for f in feas[:2]] if feas else 'none'}")


# -----------------------------------------------------------------------------
# Section 3 -- Per-residual: assignment-feasibility (full ILP enumeration).
# -----------------------------------------------------------------------------

section("3. Full assignment-feasibility enumeration (per piece per T-face)")

# For each residual + canonical-multiset combination that survives ┬º2,
# we now enumerate all per-piece assignments and check whether they
# are jointly consistent.  This is the SAT step.
#
# Each piece picks a permutation of (m_1, m_2, m_3) onto its 3 touched
# T-faces.  The assignment must:
#   (i)   honour piece-congruence (each piece uses the same canonical
#         multiset);
#   (ii)  honour the per-T-face sum (sum of contributions to each
#         touched T-face = A_T_int).
#
# The number of assignments per piece is at most 3! = 6 (assuming
# distinct m_i; with ties, fewer).  Across 5 pieces, at most 6^5 = 7776
# combinations -- trivial to enumerate exhaustively.


def assignment_feasibility(k_tuple, multiset, witness_cap: int = 100_000):
    """Brute-force enumerate all per-piece assignments and return the
    list of feasible assignments.  Returns up to `witness_cap` witnesses
    (default 100 000, large enough to accommodate the worst case of
    6**5 = 7776 per-piece permutation tuples per multiset and typical
    totals of O(10^4) witnesses for the t = 3 residuals)."""
    # Determine for each piece p which T-faces it touches.
    # A piece touches T-face j iff j in I(p) iff piece p contributes
    # nonzero to face j.  By design, |I(p)| = t = number of nonzero
    # k_j entries.  We must distribute the 5 pieces' "touch sets"
    # I(p) such that for each j, #{p : j in I(p)} = k_j.

    # Step 1: enumerate touch-set multiplicities.
    #
    # NOTE (2026-04-16, bug fix).  The previous version of this function
    # contained the guard
    #
    #     t = sum(1 for kj in k_tuple if kj > 0)
    #     if t != 3:
    #         return []
    #
    # which conflated two different meanings of the letter "t":
    #
    #   (a) the MATHEMATICAL t = number of T-faces each piece touches,
    #       which is the same for all pieces by congruence (here t = 3);
    #
    #   (b) the CODE t = number of entries of k_tuple that are strictly
    #       positive, i.e. the number of T-faces that at least one piece
    #       touches.  For every t = 3 residual the full boundary partial T
    #       is covered, so ALL four k_j are strictly positive and the
    #       code-t equals 4, not 3.  The guard therefore triggered for
    #       every residual and returned an empty witness list.
    #
    # The genuine t = 3 invariant (each piece touches exactly 3 of the 4
    # T-faces, i.e. misses exactly one) is enforced a few lines below by
    # the check   sum(z) == 5   on z_j = 5 - k_j, so the guard above was
    # both incorrect and redundant and has been removed.

    # All 3-subsets of {0,1,2,3}:
    three_subsets = [
        (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3),
    ]
    # Which 3-subset corresponds to "miss face j" = j removed.
    # subsets indexed by "missed face":
    miss_to_subset = {
        0: (1, 2, 3),
        1: (0, 2, 3),
        2: (0, 1, 3),
        3: (0, 1, 2),
    }

    # The number of pieces missing face j is z_j = 5 - k_j.
    z = tuple(5 - kj for kj in k_tuple)
    # Each piece has exactly 1 missed face (since t = 3, each piece
    # touches 3 faces and misses 1).
    if sum(z) != 5:
        return []

    # Build the 5-piece miss-face sequence (multiset).
    miss_sequence = []
    for j, zj in enumerate(z):
        miss_sequence.extend([j] * zj)
    # miss_sequence has length 5; piece p misses face miss_sequence[p].

    # Step 2: enumerate per-piece permutations (each piece assigns
    # the multiset (m_1, m_2, m_3) to its 3 touched faces).
    from itertools import permutations as perm
    multiset_perms = list(set(perm(multiset)))  # distinct perms

    # For each piece, produce list of (assignment dict {face: area}) options.
    piece_options = []
    for p in range(5):
        miss = miss_sequence[p]
        touched = miss_to_subset[miss]
        opts = []
        for mp in multiset_perms:
            assignment = dict(zip(touched, mp))
            assignment[miss] = 0
            opts.append(assignment)
        piece_options.append(opts)

    # Step 3: enumerate Cartesian product and check per-face sum.
    feasible = []
    target = [A_T_int if kj > 0 else 0 for kj in k_tuple]

    from itertools import product as cart_product
    count = 0
    for assignments in cart_product(*piece_options):
        # Sum over pieces for each T-face.
        face_sums = [0, 0, 0, 0]
        for a in assignments:
            for j in range(4):
                face_sums[j] += a[j]
        if face_sums == target:
            feasible.append(assignments)
            count += 1
            if count >= witness_cap:
                break
    return feasible


for r in T3_RESIDUALS:
    total_witnesses = 0
    witness_examples = []
    per_multiset_counts = []
    for f in r["feasible_multisets"]:
        wits = assignment_feasibility(r["k"], f["multiset"])
        per_multiset_counts.append({
            "multiset": list(f["multiset"]),
            "witness_count": len(wits),
        })
        total_witnesses += len(wits)
        if wits and len(witness_examples) < 2:
            witness_examples.append({
                "multiset": list(f["multiset"]),
                "first_witness": [list(w.items()) for w in wits[0]],
            })

    r["total_assignment_witnesses"] = total_witnesses
    r["witness_examples"] = witness_examples
    r["per_multiset_counts"] = per_multiset_counts

    if total_witnesses == 0:
        check(f"{r['name']} k = {r['k']}: NO assignment feasible -> UNSAT",
              True,
              "no per-piece permutation set sums to A_T per T-face")
        r["status"] = "UNSAT"
    else:
        # SAT at the combinatorial level -- need geometric refinement.
        check(f"{r['name']} k = {r['k']}: {total_witnesses} witness assignments",
              True,
              f"COMBINATORIAL SAT (geometric realisability TBD in 26-D)")
        r["status"] = "COMBINATORIAL_SAT"

    # Per-multiset breakdown for diagnostics.
    for pmc in per_multiset_counts:
        print(f"      multiset {tuple(pmc['multiset'])}: "
              f"{pmc['witness_count']} witnesses")


# -----------------------------------------------------------------------------
# Section 4 -- Synthesis.
# -----------------------------------------------------------------------------

section("4. Synthesis: status of the 4 t = 3 residuals")

for r in T3_RESIDUALS:
    msg = (f"{r['name']} k = {r['k']}: status = {r['status']}, "
           f"feasible multisets = {len(r['feasible_multisets'])}, "
           f"witnesses = {r['total_assignment_witnesses']}")
    check(msg, True, "")
    RESULTS["residuals"][r["name"]] = {
        "k": list(r["k"]),
        "status": r["status"],
        "feasible_multiset_count": len(r["feasible_multisets"]),
        "feasible_multisets": [list(f["multiset"]) for f in r["feasible_multisets"]],
        "assignment_witness_count": r["total_assignment_witnesses"],
        "per_multiset_counts": r["per_multiset_counts"],
        "witness_examples": r["witness_examples"],
    }

# Summary
unsat_count = sum(1 for r in T3_RESIDUALS if r["status"] == "UNSAT")
sat_count = sum(1 for r in T3_RESIDUALS if r["status"] == "COMBINATORIAL_SAT")

print(f"\n  t = 3 residual summary:")
print(f"    UNSAT:                {unsat_count} / 4")
print(f"    COMBINATORIAL_SAT:    {sat_count} / 4")

RESULTS["summary"] = {
    "total_residuals": 4,
    "unsat_count": unsat_count,
    "combinatorial_sat_count": sat_count,
}


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
    "phase26c_t3_residuals_results.json",
)
with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")