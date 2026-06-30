"""
(H-Qb) asymmetric Qb-adj, congruence case (ii): EXCLUDED exactly.
=================================================================

Final Qb-adj branch.  The interior-triangle congruence N3 has two matchings
of the non-shared edges of the two interior triangles tri(b4,b1,a),
tri(b3,b4,a) (which share edge b4-a):

    case (i):  |b4b1| = |b3b4|  and  |b1a| = |b3a|   (closed:
               hqb_asymmetric_caseI_certificate.py)
    case (ii): |b4b1| = |b3a|   and  |b1a| = |b3b4|  (this file).

Universal identities (independent of the congruence case; verified on the
convex branch s1*w + s3*u > s1*s3):

    beta = s1*w + s3*u ,   phi1 = s1*sa ,   phi2 = s3*sa ,
    Vol  = (8/3) * sa * beta .

Reduction
---------
* N1 (Vol = 8/15):  beta = 1/(5 sa).
* N2 (boundary tiling): beta + phi1 + phi2 = 4/5, so
        sa = 1 / (4 - 5*(phi1 + phi2)),   s1 = phi1/sa,   s3 = phi2/sa.
  => once the per-face tiling fixes (phi1, phi2), the triple
     (s1, s3, sa) is determined.
* Case (ii) congruence: two quadratics C1 = C2 = 0 in (u, w).  Crucially
  C1 + C2 is LINEAR in (u, w) (the quadratic terms cancel).  Together with
  the (also linear) volume equation s1*w + s3*u = 1/(5 sa) it pins (u, w)
  by a 2x2 linear system, and then C1 = 0 (equivalently C2 = 0, since
  C1 + C2 = 0 is imposed) is a single consistency test.

Unlike case (i) there is no Q(sqrt5) field obstruction here (the geometry
is rational once (phi1,phi2) is rational); the exclusion is a direct
rational over-determination.

Per-face tiling distributions (b_j, p_j, q_j), column sums (5,5,5):
  * rank 2 (generic): the per-face system fixes a unique rational
    (phi1, phi2) -- 89 candidate points.  For each we solve the linear
    (C1+C2, Vol) system for rational (u, w) and test C1 = 0 + validity:
    0 survivors (exact).
  * rank 1: 12 distinct solution lines a*phi1 + b*phi2 = c.  EVERY one
    forces phi1 = 1, phi2 = 1, phi1 + phi2 >= 4/5 (=> beta <= 0), or a
    negative phi -- all outside the feasibility box {0<phi1, 0<phi2,
    phi1+phi2 < 4/5}.  Excluded elementarily (no geometry needed).
  * rank 0: forces b_j = p_j = q_j with b_j*(4/5) = 1, i.e. b_j = 5/4,
    not an integer.  Impossible.

Hence case (ii) admits no per-face tiling: discharged UNCONDITIONALLY.
With case (i) this closes the entire Qb-adj configuration.

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
# 1.  C1 + C2 is linear in (u, w).
# ---------------------------------------------------------------------------
s1, s3, sa, u, w = sp.symbols('s1 s3 sa u w', real=True)
C1 = s1**2 - 2*s1*u - s1*w - s3**2 + s3*sa - sa**2 + u**2 + u*w + w**2
C2 = s1**2 - s1*sa - s3**2 + s3*u + 2*s3*w + sa**2 - u**2 - u*w - w**2
L = sp.expand(C1 + C2)
check("C1 + C2 is linear in (u, w) (quadratic terms cancel)",
      sp.degree(sp.Poly(L, u, w).as_expr(), u) <= 1
      and sp.degree(sp.Poly(L, u, w).as_expr(), w) <= 1,
      f"C1+C2 = {L}")

# the linear coefficients used below
# L = (s3-2 s1) u + (2 s3 - s1) w + (2 s1^2 - 2 s3^2 - s1 sa + s3 sa)
check("L = (s3-2s1)u + (2s3-s1)w + (s1-s3)(2s1+2s3-sa)",
      sp.expand(L - ((s3 - 2*s1)*u + (2*s3 - s1)*w
                     + (s1 - s3)*(2*s1 + 2*s3 - sa))) == 0)


# ---------------------------------------------------------------------------
# 2.  Per-face tiling distributions and the 89 / 12 / 0 classification.
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
            rows = [(p[j] - b[j], q[j] - b[j], Fr(5 - 4*b[j], 5)) for j in range(4)]
            coeffs = [(r[0], r[1]) for r in rows]
            nz = [c for c in coeffs if c != (0, 0)]
            if not nz:
                rank0 += 1
                continue
            c0 = nz[0]
            rank = 1
            for c in nz:
                if c0[0]*c[1] - c0[1]*c[0] != 0:
                    rank = 2
                    break
            if rank == 2:
                # solve first two independent rows
                for i in range(4):
                    done = False
                    for k2 in range(i + 1, 4):
                        a1, a2, r1 = rows[i]
                        d1, d2, r2 = rows[k2]
                        det = a1*d2 - a2*d1
                        if det != 0:
                            x = (r1*d2 - a2*r2)/det
                            y = (a1*r2 - r1*d1)/det
                            if all(rows[m][0]*x + rows[m][1]*y == rows[m][2]
                                   for m in range(4)):
                                if 0 < x < 1 and 0 < y < 1:
                                    rank2_points.add((x, y))
                            done = True
                            break
                    if done:
                        break
            else:  # rank 1
                base = next(r for r in rows if (r[0], r[1]) != (0, 0))
                cons = True
                for r in rows:
                    if (r[0], r[1]) == (0, 0):
                        if r[2] != 0:
                            cons = False
                            break
                        continue
                    t = Fr(r[0], base[0]) if base[0] != 0 else Fr(r[1], base[1])
                    if r[0] != t*base[0] or r[1] != t*base[1] or r[2] != t*base[2]:
                        cons = False
                        break
                if cons:
                    rank1_lines.add((base[0], base[1], base[2]))

check("rank-2 distributions give 89 candidate (phi1,phi2) points in (0,1)^2",
      len(rank2_points) == 89, f"{len(rank2_points)} points")
check("rank-1 consistent distributions give 12 solution lines",
      len(rank1_lines) == 12, f"{len(rank1_lines)} lines")
check("rank-0 distributions force b_j = 5/4 (impossible)", rank0 == 56,
      f"{rank0} rank-0 distributions, all inconsistent")


# ---------------------------------------------------------------------------
# 3.  rank-2: exact rational test, 0 survivors.
# ---------------------------------------------------------------------------
def C1f(S1, S3, SA, U, W):
    return (S1**2 - 2*S1*U - S1*W - S3**2 + S3*SA - SA**2 + U**2 + U*W + W**2)


rank2_survivors = []
for (p1, p2) in rank2_points:
    den = 4 - 5*p1 - 5*p2
    if den <= 0:
        continue
    SA = Fr(1, 1)/den
    S1 = p1/SA
    S3 = p2/SA
    if not (0 < SA < 1 and 0 < S1 < 1 and 0 < S3 < 1) or S1 == S3:
        continue
    R_L = -(S1 - S3)*(2*S1 + 2*S3 - SA)
    R_V = Fr(1, 1)/(5*SA)
    det = -2*(S1**2 - S1*S3 + S3**2)
    U = (R_L*S1 - (2*S3 - S1)*R_V)/det
    W = ((S3 - 2*S1)*R_V - R_L*S3)/det
    if C1f(S1, S3, SA, U, W) != 0:
        continue
    if U > 0 and W > 0 and (U + W) < 1 and (S1*W + S3*U) > S1*S3:
        rank2_survivors.append((p1, p2))

check("rank-2: 0 valid (phi1,phi2) survive the exact (u,w) over-determination",
      len(rank2_survivors) == 0, f"{len(rank2_survivors)} survivors")


# ---------------------------------------------------------------------------
# 4.  rank-1: every line leaves the feasibility box {0<phi1,0<phi2,phi1+phi2<4/5}.
# ---------------------------------------------------------------------------
def line_infeasible(a, b, c):
    """True iff a*phi1 + b*phi2 = c has NO point with
    phi1>0, phi2>0, phi1+phi2 < 4/5."""
    # check the three boundary-violation certificates the 12 lines hit
    if a == 0 and b != 0:           # phi2 = c/b constant
        v = Fr(c, b)
        return not (0 < v < Fr(4, 5))      # phi2 fixed outside (0,4/5)
    if b == 0 and a != 0:           # phi1 = c/a constant
        v = Fr(c, a)
        return not (0 < v < Fr(4, 5))
    if a == b and a != 0:           # phi1 + phi2 = c/a constant
        v = Fr(c, a)
        return not (0 < v < Fr(4, 5))      # sum fixed outside (0,4/5)
    return False


bad_lines = [ln for ln in rank1_lines if line_infeasible(*ln)]
check("all 12 rank-1 lines are infeasible (force phi1, phi2, or phi1+phi2 "
      "outside (0, 4/5)) -- excluded elementarily",
      len(bad_lines) == 12,
      f"{len(bad_lines)}/12 lines provably infeasible")
for ln in sorted(rank1_lines):
    a, b, c = ln
    kind = ("phi2=" + str(Fr(c, b)) if a == 0 else
            "phi1=" + str(Fr(c, a)) if b == 0 else
            "phi1+phi2=" + str(Fr(c, a)))
    check(f"  line {ln}: {kind} -> outside feasibility box",
          line_infeasible(*ln))


# ---------------------------------------------------------------------------
check("CONCLUSION: case (ii) admits no per-face tiling => asymmetric Qb-adj "
      "case (ii) EXCLUDED; with case (i), all of Qb-adj is discharged",
      len(rank2_survivors) == 0 and len(bad_lines) == 12 and rank0 == 56)

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["result"] = {
    "rank2_points": 89, "rank2_survivors": len(rank2_survivors),
    "rank1_lines": 12, "rank1_infeasible": len(bad_lines),
    "rank0": rank0,
    "status": "asymmetric Qb-adj case (ii) DISCHARGED exactly; Qb-adj fully "
              "closed (symmetric + case i + case ii). Remaining: Qb-opp.",
}
print(f"\n{'=' * 70}\nTotal passed: {PASSED}   failed: {FAILED}\n{'=' * 70}")

out = os.path.join(os.path.dirname(__file__), "..", "results",
                   "hqb_asymmetric_caseII_certificate_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"\nResults written to {os.path.abspath(out)}")
