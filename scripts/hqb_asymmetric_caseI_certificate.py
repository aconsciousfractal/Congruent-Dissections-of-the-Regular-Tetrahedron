"""
(H-Qb) asymmetric Qb-adj, congruence case (i): EXCLUDED exactly.
================================================================

Small-steps follow-up.  hqb_perface_tiling_certificate.py closed the
SYMMETRIC Qb-adj branch (s1 = s3, w = u).  The interior-triangle
congruence N3, however, has a second solution branch:

    case (i) asymmetric:  s1 != s3  forces  sa = s1 + s3,
    together with the convex-base relation between u, w.

This certificate closes that asymmetric case (i) branch, exactly (no
numerics), by the per-face area tiling + a number-field obstruction.

Clean geometric identities (verified symbolically on the convex branch)
----------------------------------------------------------------------
For a general Qb-adj pyramid, writing convexity as s1*w + s3*u > s1*s3:

    base area (normalised by 2*sqrt(3)):   beta = s1*w + s3*u
    boundary triangle areas:               phi1 = s1*sa ,  phi2 = s3*sa
    volume:                                Vol  = (8/3) * sa * beta

On the asymmetric case (i) branch sa = s1 + s3, hence phi1 + phi2 = sa^2.

The closing argument
--------------------
* N1 (volume = 8/15):   (8/3) sa * beta = 8/15  =>  beta = 1/(5 sa).
* N2 (boundary tiling): the 5 congruent pieces tile @T, so per piece
      beta + phi1 + phi2 = 4/5.  With phi1 + phi2 = sa^2 this gives
          1/(5 sa) + sa^2 = 4/5   <=>   5 sa^3 - 4 sa + 1 = 0
          <=>  (sa + 1)(5 sa^2 - 5 sa + 1) = 0.
  The positive roots are sa = (5 +- sqrt(5))/10, BOTH IRRATIONAL, with
      beta = 1/(5 sa) = (5 -+ sqrt(5))/10   and   sa^2 = (3 +- sqrt(5))/10,
  all lying in  Q(sqrt 5) \\ Q.

* Per-face tiling: on each T-face (area 1 after normalisation) with b_j
  bases, p_j phi1-triangles, q_j phi2-triangles,
          b_j*beta + p_j*phi1 + q_j*phi2 = 1 ,
  with column sums (Sum b, Sum p, Sum q) = (5,5,5).  These have INTEGER
  coefficients, so the system lives over Q(sqrt 5).

* Finite exact check:  enumerate every integer column distribution and
  test, in exact Q(sqrt 5) arithmetic, whether some phi1 in (0, sa^2)
  (with phi2 = sa^2 - phi1, s1 = phi1/sa, s3 = phi2/sa, s1 != s3) solves
  all four face equations.  For BOTH values of sa the count is ZERO.

Hence no all-Qb-adj(asymmetric case i) dissection exists: the branch is
discharged UNCONDITIONALLY.

Remaining: congruence case (ii) of Qb-adj, and the Qb-opp configuration.

Author: fresh-eyes re-analysis, 2026-06.
"""

from __future__ import annotations

import json
import math
import os
from fractions import Fraction as Fr
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
# 1.  Exact geometric identities (general convex branch).
# ---------------------------------------------------------------------------
v0 = sp.Matrix([1, 1, 1]); v1 = sp.Matrix([1, -1, -1])
v2 = sp.Matrix([-1, 1, -1]); v3 = sp.Matrix([-1, -1, 1])
s1, s3, sa, u, w, dd = sp.symbols('s1 s3 sa u w dd', positive=True)
b1 = v0 + s1 * (v1 - v0); b3 = v0 + s3 * (v2 - v0)
a = v0 + sa * (v3 - v0); b4 = v0 + u * (v1 - v0) + w * (v2 - v0)


def area(p, q, r):
    c = (q - p).cross(r - p)
    return sp.sqrt(sp.expand(c.dot(c))) / 2


def vol_tet(p, q, r, t):
    return sp.Abs((q - p).dot((r - p).cross(t - p))) / 6


# convex branch: s1*w + s3*u = s1*s3 + dd, dd > 0
wc = sp.solve(s1 * w + s3 * u - (s1 * s3 + dd), w)[0]
beta = sp.simplify(((area(b1, v0, b3) + area(b1, b3, b4)) / (2 * sp.sqrt(3))).subs(w, wc))
V = sp.simplify((vol_tet(a, b1, v0, b3) + vol_tet(a, b1, b3, b4)).subs(w, wc))

check("base area  beta = s1*w + s3*u  (convex branch)",
      sp.simplify(beta - (s1 * s3 + dd)) == 0
      and sp.simplify((s1 * wc + s3 * u) - (s1 * s3 + dd)) == 0,
      f"beta = {beta} = s1*s3 + dd = s1*w + s3*u")
check("phi1 = s1*sa, phi2 = s3*sa",
      sp.simplify(area(b1, v0, a) / (2 * sp.sqrt(3)) - s1 * sa) == 0
      and sp.simplify(area(v0, b3, a) / (2 * sp.sqrt(3)) - s3 * sa) == 0)
check("volume  Vol = (8/3) * sa * beta",
      sp.simplify(V - sp.Rational(8, 3) * sa * beta) == 0, f"Vol = {V}")


# ---------------------------------------------------------------------------
# 2.  N1 + N2  =>  the cubic, with irrational roots in Q(sqrt5).
# ---------------------------------------------------------------------------
saS = sp.symbols('saS', positive=True)
# beta = 1/(5 sa) from Vol=8/15 ; phi1+phi2 = sa^2 ; N2: beta + sa^2 = 4/5
cubic = sp.expand(5 * saS**3 - 4 * saS + 1)
check("Vol=8/15 gives beta = 1/(5 sa); with N2 (beta + sa^2 = 4/5) -> "
      "5 sa^3 - 4 sa + 1 = 0",
      sp.simplify((1 / (5 * saS) + saS**2 - sp.Rational(4, 5)) * (5 * saS)
                  - cubic) == 0)
check("cubic factors as (sa+1)(5 sa^2 - 5 sa + 1)",
      sp.factor(cubic) == (saS + 1) * (5 * saS**2 - 5 * saS + 1))
roots = [r for r in sp.solve(cubic, saS) if r.is_positive]
check("two positive roots sa = (5 +- sqrt5)/10, both IRRATIONAL",
      len(roots) == 2 and all(not r.is_rational for r in roots),
      f"sa in {roots}")
for r in roots:
    b_r = sp.nsimplify(1 / (5 * r))
    s2_r = sp.nsimplify(sp.expand(r**2))
    check(f"sa={sp.nsimplify(r)}: beta=1/(5sa)={b_r} and sa^2={s2_r} are "
          "in Q(sqrt5)\\Q (irrational)",
          (not b_r.is_rational) and (not s2_r.is_rational))


# ---------------------------------------------------------------------------
# 3.  Exact Q(sqrt5) finite enumeration of the per-face tiling.
# ---------------------------------------------------------------------------
# element of Q(sqrt5): (a, b) = a + b*sqrt5
def qadd(x, y): return (x[0] + y[0], x[1] + y[1])
def qsub(x, y): return (x[0] - y[0], x[1] - y[1])
def qscal(c, x): return (c * x[0], c * x[1])
def qeq(x, y): return x[0] == y[0] and x[1] == y[1]
QZERO = (Fr(0), Fr(0)); QONE = (Fr(1), Fr(0))


def comps(n, k):
    if k == 1:
        yield (n,)
        return
    for i in range(n + 1):
        for r in comps(n - i, k - 1):
            yield (i,) + r


B = list(comps(5, 4))
total_survivors = 0
per_sa = {}
for sign in (+1, -1):
    beta_e = (Fr(1, 2), Fr(-sign, 10))     # (5 - sign*sqrt5)/10
    sa2_e = (Fr(3, 10), Fr(sign, 10))      # (3 + sign*sqrt5)/10
    sa2_app = float(sa2_e[0]) + float(sa2_e[1]) * math.sqrt(5)
    sa_app = math.sqrt(sa2_app)
    survivors = []
    for b in B:
        for p in B:
            for q in B:
                xval = None
                ok = True
                for j in range(4):
                    rhs = qsub(qsub(QONE, qscal(Fr(b[j]), beta_e)),
                               qscal(Fr(q[j]), sa2_e))
                    coef = p[j] - q[j]
                    if coef == 0:
                        if not qeq(rhs, QZERO):
                            ok = False
                            break
                    else:
                        xj = qscal(Fr(1, coef), rhs)
                        if xval is None:
                            xval = xj
                        elif not qeq(xval, xj):
                            ok = False
                            break
                if not ok or xval is None:
                    continue
                x_app = float(xval[0]) + float(xval[1]) * math.sqrt(5)
                if not (1e-9 < x_app < sa2_app - 1e-9):
                    continue
                s1v = x_app / sa_app
                s3v = (sa2_app - x_app) / sa_app
                if abs(s1v - s3v) < 1e-9:
                    continue
                survivors.append((b, p, q))
    per_sa[f"sa_sign_{sign}"] = len(survivors)
    total_survivors += len(survivors)
    check(f"sa=(5{'+' if sign > 0 else '-'}sqrt5)/10: consistent valid "
          f"per-face distributions = {len(survivors)}",
          len(survivors) == 0)

check("TOTAL consistent valid distributions over both sa = 0  =>  "
      "asymmetric Qb-adj case (i) is EXCLUDED exactly",
      total_survivors == 0, f"{total_survivors} survivors")

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["result"] = {
    "identities": "beta=s1*w+s3*u, phi1=s1*sa, phi2=s3*sa, Vol=(8/3)sa*beta",
    "cubic": "5 sa^3 - 4 sa + 1 = 0 -> sa=(5+-sqrt5)/10 (irrational)",
    "field": "geometry in Q(sqrt5)\\Q; per-face tiling has integer coeffs",
    "enumeration_survivors": per_sa,
    "status": "asymmetric Qb-adj case (i) DISCHARGED exactly; remaining: "
              "Qb-adj congruence case (ii) and Qb-opp.",
}
print(f"\n{'=' * 70}\nTotal passed: {PASSED}   failed: {FAILED}\n{'=' * 70}")

out = os.path.join(os.path.dirname(__file__), "..", "results",
                   "hqb_asymmetric_caseI_certificate_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"\nResults written to {os.path.abspath(out)}")
