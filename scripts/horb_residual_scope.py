"""
(H-orb) accidental-congruence residual: precise scoping (honest status).
=========================================================================

After the parity reduction (horb_parity_certificate.py) the ONLY case of
(H-orb) not yet discharged is:

    a piece P with  f(P) = 7,  t = 3,  Sym(P) = 1  (forced by a
    distinct-boundary-area multiset), whose four interior facets are
    ACCIDENTALLY congruent in an even metric pattern -- (4) (all four
    congruent) or (2,2) (two congruent pairs) -- not realised by any
    symmetry of P.

This script documents, with exact computation, WHY the three lightweight
tools that closed every other case do NOT reach this residual, so the
remaining work is correctly scoped (it needs the genuine f = 7 interior
geometry / developing-map rigidity, not another bookkeeping trick).

Tool 1 -- parity (weak CTL).  Forces the interior-facet metric pattern to
          be even.  But (4) and (2,2) ARE even, so parity gives no
          contradiction.  [established in horb_parity_certificate.py]

Tool 2 -- orientation cocycle (the (H-coc) mechanism).  Needs the order-2
          symmetry sigma to define the orbit-transport bit
          1 + s(i) + s(j).  With Sym(P) = 1 there is no sigma, and the
          orientation bit collapses to the pure coboundary s(i) + s(j),
          which is automatically a cocycle (the holonomy around either
          K5 5-cycle is  prod s(i)^2 = 1):  no contradiction.

Tool 3 -- per-face BOUNDARY tiling (the mechanism that closed (H-Qb)).
          For each admissible boundary-area multiset we check whether the
          four T-faces can be tiled by the pieces' boundary faces
          (each piece placing its three areas on three distinct faces,
          missing one).  Below: ALL five multisets admit a boundary
          tiling, so the boundary alone excludes none of them.

Conclusion: the residual is genuinely an INTERIOR f = 7 question and is
the single remaining obstacle to an unconditional n = 5.  It is NOT to be
brute-forced; the natural route is a developing-map / rigidity argument on
the K5 interior gluing of the f = 7 piece.

Author: fresh-eyes re-analysis, 2026-06.
"""

from __future__ import annotations

import json
import os
from fractions import Fraction as Fr
from itertools import permutations, combinations_with_replacement


PASSED = 0
FAILED = 0
RESULTS: dict = {"checks": [], "passed": 0, "failed": 0}


def check(name, condition, detail=""):
    global PASSED, FAILED
    ok = bool(condition)
    PASSED += ok
    FAILED += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    RESULTS["checks"].append({"name": name, "passed": ok, "detail": detail})


# ---------------------------------------------------------------------------
# Tool 1: parity leaves the even patterns (4) and (2,2).
# ---------------------------------------------------------------------------
def integer_partitions(n, mx=None):
    if mx is None:
        mx = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, mx), 0, -1):
        for rest in integer_partitions(n - k, k):
            yield (k,) + rest


even_patterns = [p for p in integer_partitions(4) if all(m % 2 == 0 for m in p)]
check("parity (weak CTL) leaves exactly the even interior-facet patterns "
      "(2,2) and (4)",
      sorted(even_patterns) == sorted([(2, 2), (4,)]),
      f"{even_patterns}")


# ---------------------------------------------------------------------------
# Tool 2: orientation holonomy around a 5-cycle is trivial without sigma.
# ---------------------------------------------------------------------------
# With Sym(P)=1 the only available bit on an A-edge (i,j) is eps(rho_ij) =
# s(i) s(j).  Around the A-cycle 1-2-3-4-5-1 the product is s(1)^2..s(5)^2 = 1
# for EVERY handedness assignment s -> no constraint.
from itertools import product
a_cycle = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
trivial_holonomy = True
for sbits in product([0, 1], repeat=5):
    s = {i + 1: sbits[i] for i in range(5)}
    hol = sum((s[i] + s[j]) for (i, j) in a_cycle) % 2   # additive bits
    if hol != 0:
        trivial_holonomy = False
check("orientation holonomy s(i)+s(j) around the A-cycle is trivial for "
      "every handedness assignment (no sigma => no cocycle contradiction)",
      trivial_holonomy)


# ---------------------------------------------------------------------------
# Tool 3: boundary per-face tiling is FEASIBLE for all five multisets.
# ---------------------------------------------------------------------------
mults = {
    "(6,12,30)": [Fr(1, 10), Fr(1, 5), Fr(1, 2)],
    "(6,15,27)": [Fr(1, 10), Fr(1, 4), Fr(9, 20)],
    "(6,18,24)": [Fr(1, 10), Fr(3, 10), Fr(2, 5)],
    "(12,16,20)": [Fr(1, 5), Fr(4, 15), Fr(1, 3)],
    "(12,12,24)": [Fr(1, 5), Fr(1, 5), Fr(2, 5)],
}
feasible = {}
for name, (al, be, ga) in mults.items():
    types = list(set(permutations([al, be, ga, Fr(0)])))
    ok = False
    for combo in combinations_with_replacement(range(len(types)), 5):
        s = [Fr(0)] * 4
        for idx in combo:
            for j in range(4):
                s[j] += types[idx][j]
        if all(x == Fr(1) for x in s):
            ok = True
            break
    feasible[name] = ok

check("boundary per-face tiling is FEASIBLE for ALL five multisets "
      "(so the boundary alone excludes none of them)",
      all(feasible.values()), f"{feasible}")


# ---------------------------------------------------------------------------
check("RESIDUAL correctly scoped: the only open metric case is the "
      "accidental even interior-facet pattern of an f=7, Sym(P)=1 piece; "
      "it needs the interior f=7 geometry, not a bookkeeping trick",
      sorted(even_patterns) == sorted([(2, 2), (4,)])
      and trivial_holonomy and all(feasible.values()))

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["scope"] = {
    "residual": "f=7, t=3, Sym(P)=1, interior-facet metric pattern (4) or "
                "accidental (2,2)",
    "tool1_parity": "leaves even patterns (2,2),(4)",
    "tool2_orientation": "trivial holonomy without sigma -- no contradiction",
    "tool3_boundary_tiling_feasible": feasible,
    "route": "developing-map / rigidity on the K5 interior gluing of the "
             "f=7 piece -- genuine geometry, do not brute-force",
}
print(f"\n{'=' * 70}\nTotal passed: {PASSED}   failed: {FAILED}\n{'=' * 70}")

out = os.path.join(os.path.dirname(__file__), "..", "results",
                   "horb_residual_scope_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"\nResults written to {os.path.abspath(out)}")
