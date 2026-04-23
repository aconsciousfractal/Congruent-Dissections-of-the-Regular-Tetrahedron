"""
Phase 26-C-T2: SAT/necessary-condition attack on the two t = 2 residuals
                of the n = 5 dissection problem.

Residuals (from Phase 26-B):
    R_T2_1: (t = 2, k = (4, 2, 2, 2))   -- z = (1, 3, 3, 3)
    R_T2_2: (t = 2, k = (3, 3, 2, 2))   -- z = (2, 2, 3, 3)

Strategy -- canonical-multiset enumeration (same as Phase 26-C-T3,
adapted for t = 2).

  By piece congruence, every piece has the SAME multiset of 2 nonzero
  footprint areas (m_1, m_2) on the t = 2 T-faces it touches, with
  m_1 + m_2 = E = 48 (in integer units of sqrt 3 / 30).

  Face j with k_j contributions must sum to A_T = 60.

  For k_j = 2 (face 2 and face 3 in both residuals):
      pair-sum from {m_1, m_2} in {2 m_1, m_1 + m_2 = 48, 2 m_2}.
      Set = 60 -> either 2 m_1 = 60 (m_1 = 30, swap to m_1 = 18, m_2 = 30)
               or 2 m_2 = 60 (m_2 = 30, m_1 = 18).
      Hence canonical multiset is FORCED: (m_1, m_2) = (18, 30).

  For k_j = 4 (face 0 of R_T2_1):
      4 contributions from {18, 30} -> possible sums in {72, 84, 96, 108, 120}.
      60 not in set -> UNSAT.

  For k_j = 3 (face 0 / face 1 of R_T2_2):
      3 contributions from {18, 30} -> possible sums in {54, 66, 78, 90}.
      60 not in set -> UNSAT.

Both residuals fall to the contribution-multiset test alone, before any
assignment-feasibility is even attempted.

References:
  - PHASE_26_PLAN.md, sub-phase 26-C, residuals t = 2.
  - phase26b_role_distribution_n5_results.json (residual table).
  - phase26c_t3_residuals.py (analogous analysis for t = 3).
"""

from __future__ import annotations

import json
import os
from itertools import combinations_with_replacement


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

section("0. Setup: integer scaling + canonical-multiset solver")

A_T_int = 60
E_int = 48
SHARE = {2: 30, 3: 20, 4: 15, 5: 12}

check("Integer-scaled A_T = 60 (units of sqrt 3 / 30)", A_T_int == 60)
check("Integer-scaled E = 48", E_int == 48)


def all_pair_multisets_summing(target):
    """Enumerate all (m_1, m_2) integer pairs with
    1 <= m_1 <= m_2 and m_1 + m_2 = target."""
    out = []
    for m1 in range(1, target // 2 + 1):
        m2 = target - m1
        if m2 >= m1:
            out.append((m1, m2))
    return out


def multiset_size_k_sums_to_target(multiset, k, target):
    """Return all unordered k-subsets (with replacement) of `multiset`
    that sum to `target`."""
    out = []
    for combo in combinations_with_replacement(multiset, k):
        if sum(combo) == target:
            out.append(tuple(sorted(combo)))
    return list(set(out))


# -----------------------------------------------------------------------------
# Section 1 -- Per-residual canonical-multiset enumeration.
# -----------------------------------------------------------------------------

section("1. Per-residual canonical-multiset enumeration")

T2_RESIDUALS = [
    {"name": "R_T2_1",
     "k": (4, 2, 2, 2),
     "z": (1, 3, 3, 3)},
    {"name": "R_T2_2",
     "k": (3, 3, 2, 2),
     "z": (2, 2, 3, 3)},
]


def feasible_pair_multisets_for_residual(k_tuple):
    """Return the set of canonical pair multisets (m_1, m_2) such that
    every nonzero T-face has at least one valid contribution-multisubset."""
    feasible = []
    pairs = all_pair_multisets_summing(E_int)
    for pr in pairs:
        ok = True
        per_face_options = []
        for k_j in k_tuple:
            if k_j == 0:
                per_face_options.append(None)
                continue
            options = multiset_size_k_sums_to_target(pr, k_j, A_T_int)
            if not options:
                ok = False
                break
            per_face_options.append(options)
        if ok:
            feasible.append({"multiset": pr, "per_face_options": per_face_options})
    return feasible


for r in T2_RESIDUALS:
    feas = feasible_pair_multisets_for_residual(r["k"])
    r["feasible_multisets"] = feas
    msg = (f"{r['name']} k = {r['k']}: "
           f"{len(feas)} canonical multisets pass per-T-face contribution test")
    check(msg, len(feas) == 0,
          f"feasible = {[f['multiset'] for f in feas] if feas else 'none'}")


# -----------------------------------------------------------------------------
# Section 2 -- Explicit derivation: forced multiset (18, 30).
# -----------------------------------------------------------------------------

section("2. Forced canonical multiset (18, 30) -- explicit derivation")

# For both residuals, k_2 = k_3 = 2, requiring pair-sum from (m_1, m_2)
# to equal A_T = 60.  The only options are:
#   2 m_1 = 60  ->  m_1 = 30, m_2 = 18 (swap to (18, 30))
#   m_1 + m_2 = 60 = E?  E = 48, so impossible.
#   2 m_2 = 60  ->  m_2 = 30, m_1 = 18.
# Hence canonical multiset is FORCED to (m_1, m_2) = (18, 30).

target_multiset = (18, 30)

# Verify: pair-sum from (18, 30) attaining A_T = 60.
pair_options = multiset_size_k_sums_to_target(target_multiset, 2, A_T_int)
check(
    "Pair-sum 60 from (18, 30): only (30, 30) works",
    pair_options == [(30, 30)],
    f"options = {pair_options}",
)

# Pair-sum 60 NOT from (m_1, m_2) with m_1 + m_2 = 48 unless 2 m_2 = 60.
all_pairs = all_pair_multisets_summing(E_int)
forced_pairs = [pr for pr in all_pairs
                if multiset_size_k_sums_to_target(pr, 2, A_T_int)]
check(
    "Among all (m_1, m_2) with m_1 + m_2 = 48, only (18, 30) gives pair-sum 60",
    forced_pairs == [(18, 30)],
    f"forced_pairs = {forced_pairs}",
)


# -----------------------------------------------------------------------------
# Section 3 -- Face k_j = 3 and k_j = 4 contribution tests.
# -----------------------------------------------------------------------------

section("3. Face k_j = 3 and k_j = 4 contribution tests for multiset (18, 30)")

# For k_j = 3 (face 0 of R_T2_2): 3 contributions from (18, 30) sum to 60.
triplet_options = multiset_size_k_sums_to_target(target_multiset, 3, A_T_int)
check(
    f"Triplet-sum 60 from (18, 30): {len(triplet_options)} options",
    triplet_options == [],
    f"all triplet sums = {[sum(c) for c in combinations_with_replacement(target_multiset, 3)]}",
)

# For k_j = 4 (face 0 of R_T2_1): 4 contributions from (18, 30) sum to 60.
quad_options = multiset_size_k_sums_to_target(target_multiset, 4, A_T_int)
check(
    f"Quadruple-sum 60 from (18, 30): {len(quad_options)} options",
    quad_options == [],
    f"all quadruple sums = {[sum(c) for c in combinations_with_replacement(target_multiset, 4)]}",
)


# -----------------------------------------------------------------------------
# Section 4 -- Synthesis.
# -----------------------------------------------------------------------------

section("4. Synthesis: status of the 2 t = 2 residuals")

for r in T2_RESIDUALS:
    if len(r["feasible_multisets"]) == 0:
        r["status"] = "UNSAT"
        check(f"{r['name']} k = {r['k']}: UNSAT (no canonical multiset survives)",
              True)
    else:
        r["status"] = "OPEN"
        check(f"{r['name']} k = {r['k']}: OPEN ({len(r['feasible_multisets'])} multisets)",
              False, "should not happen for t = 2")
    RESULTS["residuals"][r["name"]] = {
        "k": list(r["k"]),
        "status": r["status"],
        "feasible_multiset_count": len(r["feasible_multisets"]),
    }

unsat_count = sum(1 for r in T2_RESIDUALS if r["status"] == "UNSAT")
print(f"\n  t = 2 residual summary:")
print(f"    UNSAT: {unsat_count} / 2")

RESULTS["summary"] = {
    "total_residuals": 2,
    "unsat_count": unsat_count,
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
    "phase26c_t2_residuals_results.json",
)
with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")