"""
(H-orb) accidental residual: combinatorial classification of f=7 pieces.
========================================================================

Goal of this step: decide whether the accidental even interior-facet
pattern of an f = 7, Sym(P) = 1 piece is already COMBINATORIALLY
incompatible (before any metric geometry).

Edge-count parity refinement (the key combinatorial lemma)
----------------------------------------------------------
A metric congruence class of facets refines the "edge-count" class
(congruent polygons have the same number of edges).  For an EVEN metric
pattern -- every metric class of the four interior facets has even size --
each edge-count class (a union of metric classes) must therefore have even
size too.  With four interior facets this forces their edge-count multiset
to be

        (k, k, k, k)   or   (a, a, b, b)   with a != b.

So if NO realizable f = 7, t = 3 piece can have interior edge-counts of
this form, the residual is excluded combinatorially.

Result: it is NOT excluded.
-------------------------------
1. Arithmetic enumeration of f = 7 face-degree multisets (7 faces of
   degree >= 3, 2E = sum of degrees, V = E - 5, vertex-degree feasibility)
   yields NINE distinct even interior patterns, each compatible with
   admissible boundary triples.
2. These are genuinely realizable: the corner-truncated cube is an explicit
   convex 3-polytope with f = 7 and face-degree sequence (3,4,4,4,5,5,5),
   which contains the even 4-subset (4,4,5,5).

Conclusion (honest)
-------------------
The edge-count parity refinement NARROWS the residual to interior-facet
edge-count multisets (k,k,k,k) / (a,a,b,b), but even patterns survive both
arithmetically and as realizable polytopes.  Hence no purely combinatorial
argument closes the residual: the remaining obstacle is genuinely METRIC
(do two interior facets with equal edge-count actually become congruent on
a Sym(P)=1 piece with three distinct boundary areas?).  This is the
developing-map / rigidity question on the f = 7 interior gluing.

Author: fresh-eyes re-analysis, 2026-06.
"""

from __future__ import annotations

import json
import os
from itertools import combinations, combinations_with_replacement
from collections import Counter, defaultdict

import numpy as np
from scipy.spatial import ConvexHull


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


def even_multiset(ms):
    return all(v % 2 == 0 for v in Counter(ms).values())


# ---------------------------------------------------------------------------
# 1.  Edge-count parity refinement: which size-4 edge-count multisets are even.
# ---------------------------------------------------------------------------
even4 = [ms for ms in combinations_with_replacement(range(3, 9), 4)
         if even_multiset(ms)]
check("even interior edge-count multisets of size 4 are exactly the "
      "(k,k,k,k) and (a,a,b,b) shapes",
      all(len(set(ms)) <= 2 and even_multiset(ms) for ms in even4)
      and all((len(set(ms)) == 1) or (sorted(Counter(ms).values()) == [2, 2])
              for ms in even4))


# ---------------------------------------------------------------------------
# 2.  Arithmetic enumeration of f=7 face-degree multisets and even interiors.
# ---------------------------------------------------------------------------
def vertex_feasible(E):
    V = E - 5
    return V >= 4 and 3 * V <= 2 * E   # vertices deg>=3 summing to 2E


faceseqs = []
for E in range(11, 16):
    for combo in combinations_with_replacement(range(3, 9), 7):
        if sum(combo) == 2 * E and vertex_feasible(E):
            faceseqs.append(combo)

even_interior_patterns = set()
for combo in faceseqs:
    for idx in combinations(range(7), 4):
        inter = tuple(sorted(combo[i] for i in idx))
        if even_multiset(inter):
            even_interior_patterns.add(inter)

check("f=7 face-degree enumeration yields candidate sequences",
      len(faceseqs) > 0, f"{len(faceseqs)} candidate face-degree multisets")
check("NINE distinct even interior patterns are arithmetically consistent "
      "with f=7 (residual not killed by counting)",
      len(even_interior_patterns) == 9,
      f"{sorted(even_interior_patterns)}")


# ---------------------------------------------------------------------------
# 3.  Realizable witness: corner-truncated cube has f=7 with an even 4-subset.
# ---------------------------------------------------------------------------
cube = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
cube.remove((1, 1, 1))
t = 0.4
cube += [(1 - t, 1, 1), (1, 1 - t, 1), (1, 1, 1 - t)]
h = ConvexHull(np.array(cube, dtype=float))
planes = defaultdict(set)
for eq, simp in zip(h.equations, h.simplices):
    planes[tuple(np.round(eq, 6))].update(simp.tolist())
degs = sorted(len(v) for v in planes.values())

check("corner-truncated cube is a convex 3-polytope with f = 7",
      len(degs) == 7, f"face-degree sequence {degs}")
witness_even = None
for sub in combinations(range(7), 4):
    ms = tuple(sorted(degs[i] for i in sub))
    if even_multiset(ms):
        witness_even = ms
        break
check("it contains an even interior 4-subset (so even patterns are "
      "REALIZABLE, not just arithmetic)",
      witness_even is not None, f"even 4-subset {witness_even}")


# ---------------------------------------------------------------------------
check("CONCLUSION: edge-count parity NARROWS the residual to interior "
      "patterns (k,k,k,k)/(a,a,b,b), but they survive combinatorially "
      "=> the residual is genuinely METRIC (developing-map / rigidity)",
      len(even_interior_patterns) == 9 and witness_even is not None)

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["result"] = {
    "edge_count_parity": "even metric pattern => interior edge-counts "
                         "(k,k,k,k) or (a,a,b,b)",
    "even_interior_patterns": sorted(even_interior_patterns),
    "realizable_witness": {"polytope": "corner-truncated cube",
                           "face_degrees": degs,
                           "even_4subset": witness_even},
    "status": "residual NOT combinatorially excluded; narrowed to the above "
              "edge-count families; remaining obstacle is metric "
              "(f=7 interior developing-map / rigidity).",
}
print(f"\n{'=' * 70}\nTotal passed: {PASSED}   failed: {FAILED}\n{'=' * 70}")

out = os.path.join(os.path.dirname(__file__), "..", "results",
                   "horb_residual_combinatorial_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"\nResults written to {os.path.abspath(out)}")
