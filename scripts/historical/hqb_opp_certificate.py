"""
(H-Qb) the Qb-opp configuration: EXCLUDED exactly  ->  (H-Qb) FULLY discharged.
===============================================================================

Last sub-case of (H-Qb).  Qb-opp is the quadrilateral pyramid whose base is
on a T-face T_alpha and whose two boundary lateral triangles sit on the two
T-faces OPPOSITE across the base, with all five pyramid vertices on the
three T-edges concurrent at the T-vertex v0:

    b1, b2 on edge [v0,v1] ,   b3, b4 on edge [v0,v2] ,   apex a on [v0,v3].

Interior faces (C5 adjacency, f=5): F2 = tri(b2,b3,a), F4 = tri(b4,b1,a);
N3 requires F2 ~= F4 (congruent).  Boundary faces: base quad b1b2b3b4 on
T_alpha, F1 = tri(b1,b2,a) on T_beta, F3 = tri(b3,b4,a) on T_gamma.

Universal identities (convex branch t1<t2, t4<t3; verified symbolically)
-----------------------------------------------------------------------
    phiF1 = ta*(t2 - t1) ,   phiF3 = ta*(t3 - t4) ,
    beta  = t2*t3 - t1*t4 ,   Vol = (8/3) * ta * beta .

Reduction
---------
* N1 (Vol = 8/15):  beta = 1/(5 ta).
* N2 (boundary tiling): beta + phiF1 + phiF3 = 4/5, so
        ta = 1/(4 - 5*(phiF1 + phiF3)).
* Writing t2 = t1 + phiF1/ta, t3 = t4 + phiF3/ta, the volume relation
  beta = 1/(5 ta) becomes the LINEAR equation
        E1:  t1*phiF3 + t4*phiF1 + phiF1*phiF3/ta = 1/5 .
* Congruence F2 ~= F4 <=> the two triples
        {A2,P2,P3} = {b2b3, b3a, b2a}  and  {A4,P1,P4} = {b4b1, b1a, b4a}
  (squared lengths /8) have equal elementary symmetric functions
  e1, e2, e3.  The e1-difference is also LINEAR in (t1, t4).

Per-face tiling distributions (column sums (5,5,5)):
  * rank 2 (89 points): per-face fixes rational (phiF1, phiF3), hence
    rational ta.  E1 and (e1-difference = 0) are two linear equations ->
    a unique rational (t1, t4); we then test (e2-diff = e3-diff = 0) and
    validity.  0 survivors (exact).
  * rank 1 (12 lines): each forces phiF1=1, phiF3=1, phiF1+phiF3 >= 4/5
    (=> beta <= 0), or a negative phi -- outside the feasibility box
    {0<phiF1, 0<phiF3, phiF1+phiF3 < 4/5}.  Excluded elementarily.
  * rank 0: forces b_j = 5/4, impossible.

Hence Qb-opp admits no per-face tiling.  Together with Qb-adj (symmetric +
case i + case ii) this discharges (H-Qb) ENTIRELY.

Author: fresh-eyes re-analysis, 2026-06.
"""

from __future__ import annotations

import json
import os
from fractions import Fraction as Fr
import sympy as sp


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
# 1.  Universal identities (convex branch t1<t2, t4<t3).
# ---------------------------------------------------------------------------
v0 = sp.Matrix([1, 1, 1]); v1 = sp.Matrix([1, -1, -1])
v2 = sp.Matrix([-1, 1, -1]); v3 = sp.Matrix([-1, -1, 1])
t1, t2, t3, t4, ta = sp.symbols('t1 t2 t3 t4 ta', positive=True)
d21, d34 = sp.symbols('d21 d34', positive=True)  # t2-t1, t3-t4
b1 = v0 + t1 * (v1 - v0); b2 = v0 + t2 * (v1 - v0)
b3 = v0 + t3 * (v2 - v0); b4 = v0 + t4 * (v2 - v0); a = v0 + ta * (v3 - v0)


def ar(p, q, r):
    c = (q - p).cross(r - p)
    return sp.sqrt(sp.expand(c.dot(c))) / 2


def vol(p, q, r, s):
    return sp.Abs((q - p).dot((r - p).cross(s - p))) / 6


sub = {t2: t1 + d21, t3: t4 + d34}      # convex branch makes the sqrt's resolve
phiF1 = sp.simplify((ar(b1, b2, a) / (2 * sp.sqrt(3))).subs(sub))
phiF3 = sp.simplify((ar(b3, b4, a) / (2 * sp.sqrt(3))).subs(sub))
beta = sp.simplify(((ar(b1, b2, b3) + ar(b1, b3, b4)) / (2 * sp.sqrt(3))).subs(sub))
V = sp.simplify((vol(a, b1, b2, b3) + vol(a, b1, b3, b4)).subs(sub))

check("phiF1 = ta*(t2-t1)", sp.simplify(phiF1 - ta * d21) == 0, f"{phiF1}")
check("phiF3 = ta*(t3-t4)", sp.simplify(phiF3 - ta * d34) == 0, f"{phiF3}")
check("beta = t2*t3 - t1*t4",
      sp.simplify(beta - ((t1 + d21) * (t4 + d34) - t1 * t4)) == 0, f"{beta}")
check("Vol = (8/3)*ta*beta", sp.simplify(V - sp.Rational(8, 3) * ta * beta) == 0,
      f"Vol = {V}")


# ---------------------------------------------------------------------------
# 2.  Per-face tiling: rank-2 / rank-1 / rank-0 classification.
# ---------------------------------------------------------------------------
def comps(n, k):
    if k == 1:
        yield (n,)
        return
    for i in range(n + 1):
        for r in comps(n - i, k - 1):
            yield (i,) + r


B = list(comps(5, 4))
rank2_points = set()
rank1_lines = set()
rank0 = 0
for b in B:
    for p in B:
        for q in B:
            rows = [(p[j] - b[j], q[j] - b[j], Fr(5 - 4 * b[j], 5)) for j in range(4)]
            nz = [(r[0], r[1]) for r in rows if (r[0], r[1]) != (0, 0)]
            if not nz:
                rank0 += 1
                continue
            c0 = nz[0]
            rank = 1
            for c in nz:
                if c0[0] * c[1] - c0[1] * c[0] != 0:
                    rank = 2
                    break
            if rank == 2:
                for i in range(4):
                    hit = False
                    for k2 in range(i + 1, 4):
                        a1, a2, r1 = rows[i]
                        e1c, e2c, r2 = rows[k2]
                        det = a1 * e2c - a2 * e1c
                        if det != 0:
                            x = (r1 * e2c - a2 * r2) / det
                            y = (a1 * r2 - r1 * e1c) / det
                            if all(rows[m][0] * x + rows[m][1] * y == rows[m][2]
                                   for m in range(4)) and 0 < x < 1 and 0 < y < 1:
                                rank2_points.add((x, y))
                            hit = True
                            break
                    if hit:
                        break
            else:
                base = next(r for r in rows if (r[0], r[1]) != (0, 0))
                cons = True
                for r in rows:
                    if (r[0], r[1]) == (0, 0):
                        if r[2] != 0:
                            cons = False
                            break
                        continue
                    tt = Fr(r[0], base[0]) if base[0] != 0 else Fr(r[1], base[1])
                    if r[0] != tt * base[0] or r[1] != tt * base[1] or r[2] != tt * base[2]:
                        cons = False
                        break
                if cons:
                    rank1_lines.add((base[0], base[1], base[2]))

check("rank-2 -> 89 candidate (phiF1,phiF3) points", len(rank2_points) == 89)
check("rank-1 -> 12 consistent solution lines", len(rank1_lines) == 12)
check("rank-0 -> 56 distributions, all forcing b_j=5/4 (impossible)", rank0 == 56)


# ---------------------------------------------------------------------------
# 3.  rank-2 exact congruence test: 0 survivors.
# ---------------------------------------------------------------------------
T1 = sp.symbols('T1')
survivors = []
checked = 0
for (pa, pb) in rank2_points:
    for (f1, f3) in {(pa, pb), (pb, pa)}:
        den = 4 - 5 * f1 - 5 * f3
        if den <= 0:
            continue
        TA = Fr(1, 1) / den
        if not (0 < TA < 1) or f1 == 0:
            continue
        D21 = f1 / TA
        D34 = f3 / TA
        t4e = (Fr(1, 5) - T1 * f3 - f1 * f3 / TA) / f1      # from E1
        t1e, t2e, t3e = T1, T1 + D21, t4e + D34
        A2 = t2e**2 - t2e * t3e + t3e**2
        P2 = t2e**2 - t2e * TA + TA**2
        P3 = t3e**2 - t3e * TA + TA**2
        A4 = t1e**2 - t1e * t4e + t4e**2
        P1 = t1e**2 - t1e * TA + TA**2
        P4 = t4e**2 - t4e * TA + TA**2
        e1 = sp.expand((A2 + P2 + P3) - (A4 + P1 + P4))     # linear in T1
        e2 = sp.expand((A2 * P2 + A2 * P3 + P2 * P3) - (A4 * P1 + A4 * P4 + P1 * P4))
        e3 = sp.expand((A2 * P2 * P3) - (A4 * P1 * P4))
        checked += 1
        for r in sp.solve(e1, T1):
            if not r.is_rational:
                continue
            if sp.expand(e2.subs(T1, r)) == 0 and sp.expand(e3.subs(T1, r)) == 0:
                t1v, t4v = r, t4e.subs(T1, r)
                t2v, t3v = t1v + D21, t4v + D34
                if 0 < t1v < t2v < 1 and 0 < t4v < t3v < 1:
                    survivors.append((float(f1), float(f3)))

check("rank-2: 0 survivors of (E1, e1-diff) linear solve + e2/e3 consistency "
      "+ validity",
      len(survivors) == 0, f"checked {checked} assignments, {len(survivors)} survivors")


# ---------------------------------------------------------------------------
# 4.  rank-1: every line leaves the feasibility box.
# ---------------------------------------------------------------------------
def infeasible(a, b, c):
    if a == 0 and b != 0:
        return not (0 < Fr(c, b) < Fr(4, 5))
    if b == 0 and a != 0:
        return not (0 < Fr(c, a) < Fr(4, 5))
    if a == b and a != 0:
        return not (0 < Fr(c, a) < Fr(4, 5))
    return False


bad = [ln for ln in rank1_lines if infeasible(*ln)]
check("all 12 rank-1 lines infeasible (phiF1, phiF3, or their sum outside "
      "(0,4/5))", len(bad) == 12, f"{len(bad)}/12")

check("CONCLUSION: Qb-opp EXCLUDED  =>  (H-Qb) is FULLY discharged "
      "(Qb-adj + Qb-opp)",
      len(survivors) == 0 and len(bad) == 12 and rank0 == 56)

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["result"] = {
    "rank2_checked": checked, "rank2_survivors": len(survivors),
    "rank1_lines": 12, "rank1_infeasible": len(bad), "rank0": rank0,
    "status": "Qb-opp DISCHARGED exactly; (H-Qb) FULLY discharged. "
              "Only the accidental-even metric residual remains.",
}
print(f"\n{'=' * 70}\nTotal passed: {PASSED}   failed: {FAILED}\n{'=' * 70}")

out = os.path.join(os.path.dirname(__file__), "..", "results",
                   "hqb_opp_certificate_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"\nResults written to {os.path.abspath(out)}")
