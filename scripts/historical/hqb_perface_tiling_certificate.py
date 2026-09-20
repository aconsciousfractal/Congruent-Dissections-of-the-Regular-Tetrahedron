"""
(H-Qb) per-face tiling: the SYMMETRIC Qb-adj branch is EXCLUDED.
===============================================================

Small-steps follow-up to hqb_reduction_certificate.py.  That certificate
reduced the Qb-adj closure (symmetric branch s1=s3=s, w=u, forced by the
interior-triangle congruence N3) to a non-empty 1-parameter family

        s*u*sa = 1/10 ,     s*(u+sa) = 2/5 ,     valid for s in (3/10, 2/5).

Here we add ONE more clean, unconditional necessary condition -- the
per-face area tiling -- and it CLOSES that branch.

Per-face tiling
---------------
All 5 pieces are congruent Qb pyramids.  Each T-face (area 2*sqrt(3)) is
tiled exactly by the boundary faces lying on it.  On the symmetric branch a
piece contributes A_base = 4*sqrt(3)*s*u to its base-face and
A_F = 2*sqrt(3)*s*sa to each of its two triangle-faces.  If T-face j carries
b_j bases and t_j triangles then

        b_j*A_base + t_j*A_F = 2*sqrt(3)
   <=>  s*(2*b_j*u + t_j*sa) = 1 .

Using s*(u+sa) = 2/5 (so 1/s = 5(u+sa)/2) this rearranges, for every face, to

        u/sa = (5 - 2*t_j) / (4*b_j - 5)  =:  r ,

the SAME rational value r on all four faces.

The contradiction
-----------------
* A valid (non-degenerate, convex, inside-T) Qb-adj piece has
  r = u/sa strictly in the OPEN interval (1/3, 1): the endpoints are the
  degenerate limits sa = 1 (apex at a T-vertex, s = 3/10) and u = 1/2
  (base collapses, s = 2/5).  r is monotone in s, so the image is exactly
  (1/3, 1).
* Every rational value r in (1/3, 1) of the form (5-2t)/(4b-5) with
  integers b,t >= 0, 1 <= b+t <= 5, is realised by a UNIQUE pair (b,t).
  (The only r with two or more pairs are r = 1/3 and r = 1 -- the excluded
  degenerate endpoints.)
* Hence all four faces must share the SAME (b_j, t_j) = (b, t), forcing
  Sum_j b_j = 4b = 5  and  Sum_j t_j = 4t = 10 -- neither 5/4 nor 10/4 is
  an integer.  CONTRADICTION.

Therefore no 5-piece convex congruent face-to-face dissection of T has all
pieces of symmetric Qb-adj type.  The symmetric branch of (H-Qb) for Qb-adj
is discharged UNCONDITIONALLY.

Remaining (next small steps): the asymmetric N3 branch (s1 + s3 = sa, or the
cross-congruence case) and the Qb-opp configuration, each via the same
per-face tiling bookkeeping with the appropriate boundary areas.

Author: fresh-eyes re-analysis, 2026-06.
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
import sympy as sp


PASSED = 0
FAILED = 0
RESULTS: dict = {"checks": [], "passed": 0, "failed": 0}


def check(name: str, condition, detail: str = "") -> None:
    global PASSED, FAILED
    ok = bool(condition)
    PASSED += ok
    FAILED += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    RESULTS["checks"].append({"name": name, "passed": ok, "detail": detail})


# ---------------------------------------------------------------------------
# 1.  Valid-piece range  =>  r = u/sa in the open interval (1/3, 1).
# ---------------------------------------------------------------------------
s = sp.symbols('s', positive=True)
w = sp.sqrt(4 - 10 * s)                       # w = sqrt(4 - 10 s) in (0,1)
u = (2 - w) / (10 * s)
sa = (2 + w) / (10 * s)

# the family identities
check("family identity  s*u*sa = 1/10",
      sp.simplify(s * u * sa - sp.Rational(1, 10)) == 0)
check("family identity  s*(u+sa) = 2/5",
      sp.simplify(s * (u + sa) - sp.Rational(2, 5)) == 0)

# nondegeneracy boundaries
val_lo = sp.Rational(3, 10)   # sa = 1  (apex at T-vertex v3)
val_hi = sp.Rational(2, 5)    # u = sa = 1/2 (base degenerates)
check("at s = 3/10: sa = 1 (apex degenerate)  ->  excluded endpoint",
      sp.simplify(sa.subs(s, val_lo) - 1) == 0)
check("at s = 2/5: u = 1/2 (base degenerate)  ->  excluded endpoint",
      sp.simplify(u.subs(s, val_hi) - sp.Rational(1, 2)) == 0)

r = sp.simplify(u / sa)
r_lo = sp.nsimplify(r.subs(s, val_lo))
r_hi = sp.nsimplify(r.subs(s, val_hi))
check("r = u/sa -> 1/3 as s -> 3/10  and  -> 1 as s -> 2/5",
      r_lo == sp.Rational(1, 3) and r_hi == 1, f"r in {{{r_lo} .. {r_hi}}}")

# monotone increasing on (3/10, 2/5): r = (2-w)/(2+w), w decreasing in s
mono = sp.simplify(sp.diff(r, s))
# check sign numerically across the interval (exact sign is positive)
pos = all(mono.subs(s, sp.Rational(k, 100)) > 0 for k in range(31, 40))
check("r is strictly increasing on (3/10, 2/5): image is exactly (1/3, 1) "
      "open, and every VALID piece has r in (1/3, 1)",
      pos)

# convexity u > s/2 and u<1/2, sa<1 all hold on the open interval (sanity)
for ss in [sp.Rational(31, 100), sp.Rational(7, 20), sp.Rational(39, 100)]:
    uu = u.subs(s, ss); ss_a = sa.subs(s, ss)
    ok = (uu > ss / 2) and (uu < sp.Rational(1, 2)) and (0 < ss_a < 1)
    check(f"sample s={ss}: convex & inside (s/2<u<1/2, 0<sa<1)", ok,
          f"u~{float(uu):.4f}, sa~{float(ss_a):.4f}")


# ---------------------------------------------------------------------------
# 2.  Per-face ratio enumeration: every r in (1/3,1) has a UNIQUE (b,t).
# ---------------------------------------------------------------------------
groups = defaultdict(list)
for b in range(0, 6):
    for t in range(0, 6):
        if not (1 <= b + t <= 5):
            continue
        if 4 * b - 5 == 0:
            continue
        groups[sp.Rational(5 - 2 * t, 4 * b - 5)].append((b, t))

inside = {rr: ps for rr, ps in groups.items() if sp.Rational(1, 3) < rr < 1}
multi_inside = {rr: ps for rr, ps in inside.items() if len(ps) >= 2}
multi_all = {rr: ps for rr, ps in groups.items() if len(ps) >= 2}

check("every per-face ratio r in (1/3,1) is hit by a UNIQUE (b,t) pair",
      all(len(ps) == 1 for ps in inside.values()),
      f"{ {str(rr): ps for rr, ps in sorted(inside.items())} }")
check("the only ratios with >= 2 pairs are r = 1/3 and r = 1 "
      "(the excluded degenerate endpoints)",
      set(multi_all.keys()) == {sp.Rational(1, 3), sp.Integer(1)},
      f"multi-pair r: { {str(k): v for k, v in multi_all.items()} }")
check("=> no admissible r in (1/3,1) supports two distinct faces",
      len(multi_inside) == 0)


# ---------------------------------------------------------------------------
# 3.  The contradiction: equal (b,t) on all faces forces 4b = 5.
# ---------------------------------------------------------------------------
# Sum_j b_j = 5 (one base per piece), Sum_j t_j = 10 (two triangles per piece).
total_b, total_t, n_faces = 5, 10, 4
check("all 4 faces share the same (b,t) (forced by uniqueness) => "
      "4*b = 5 has no integer solution",
      (total_b % n_faces) != 0,
      f"4*b = {total_b}  ->  b = 5/4 not an integer")
check("likewise 4*t = 10 has no integer solution",
      (total_t % n_faces) != 0,
      f"4*t = {total_t}  ->  t = 5/2 not an integer")

check("CONCLUSION: symmetric Qb-adj branch is EXCLUDED unconditionally by "
      "per-face tiling -- a genuine closure beyond the earlier reduction",
      all(len(ps) == 1 for ps in inside.values())
      and (total_b % n_faces != 0))

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["result"] = {
    "valid_piece_ratio_range": "u/sa in (1/3, 1) open",
    "per_face_unique_ratio": {str(rr): ps for rr, ps in sorted(inside.items())},
    "multi_pair_ratios": {str(k): v for k, v in multi_all.items()},
    "contradiction": "4*b = 5 and 4*t = 10 have no integer solution",
    "status": "symmetric Qb-adj branch DISCHARGED; remaining: asymmetric N3 "
              "branch (s1+s3=sa) and Qb-opp, via the same per-face tiling.",
}
print(f"\n{'=' * 70}\nTotal passed: {PASSED}   failed: {FAILED}\n{'=' * 70}")

out = os.path.join(os.path.dirname(__file__), "..", "results",
                   "hqb_perface_tiling_certificate_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"\nResults written to {os.path.abspath(out)}")
