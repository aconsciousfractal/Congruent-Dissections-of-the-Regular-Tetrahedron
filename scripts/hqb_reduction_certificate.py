"""
(H-Qb) REDUCTION CERTIFICATE  --  exact, lightweight (no heavy search).
=======================================================================

Goal.  Pin down honestly what the Qb sub-case of the f = 5 closure really
costs.  (H-Qb) excludes a piece of type Qb (quadrilateral pyramid with base
+ two lateral triangles on the boundary of T) in a 5-piece convex congruent
face-to-face dissection.  Earlier drafts rated this intermediate reduction
as L1+ and deferred the remaining assembly problem; the current public ledger
closes that assembly problem with the downstream hqb_perface / hqb_asymmetric /
hqb_opp certificates.

Approach.  Instead of a heavy numeric / SAT search over the placement space
(the dead end of the earlier Colab attempts), we set up the EXACT placement
family and impose the clean NECESSARY conditions that any such piece must
satisfy, then read off the residual locus in closed form.

The clean necessary conditions (all unconditional)
--------------------------------------------------
  N1 (volume).      A congruent 5-dissection of T (V_T = 8/3) has every
                    piece of volume V_T/5 = 8/15.
  N2 (boundary).    The 5 congruent pieces tile @T (total area 8*sqrt(3)),
                    so each piece's boundary-face areas sum to 8*sqrt(3)/5.
  N3 (interior      f = 5 gives C_5 interior adjacency: each piece has 2
      congruence).  interior faces, glued to congruent faces of neighbours.
                    By the same parity used for (H-orb), the 2 interior
                    triangles of the piece must be CONGRUENT to each other.
  N4 (convexity).   The base must be a non-degenerate convex quadrilateral.

Model.  Regular tetrahedron T = conv{(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)},
V_T = 8/3, face area 2*sqrt(3), edge 2*sqrt(2).  Qb-adj placement
(paper rem:hqb-status): base on face T_alpha = (v0,v1,v2), apex a on the
T-edge [v0,v3]; b2 = v0, b1 on [v0,v1], b3 on [v0,v2], b4 interior to
T_alpha.  N3 is satisfied identically on the symmetric sub-family
s1 = s3 = s, w = u (the role-swap symmetry of the two boundary triangles),
which is where any solution must localise once N3 is imposed.

Exact reduction (this script verifies it symbolically)
------------------------------------------------------
On the convex branch (u > s/2, so sqrt((s-2u)^2) = 2u - s):

    Vol     = 16 * s * u * sa / 3,         A_base = 4*sqrt(3)*s*u,
    A_F1    = A_F2 = 2*sqrt(3)*s*sa,
    A_sum   = 4*sqrt(3) * s * (u + sa).

Imposing N1, N2:

        s * u * sa = 1/10        (volume)
        s * (u + sa) = 2/5       (boundary area)

so u, sa are the two roots of  x^2 - (2/(5s)) x + 1/(10s) = 0, which are
REAL and positive iff  s <= 2/5.  Hence the Qb-adj locus surviving
N1..N4 is a NON-EMPTY one-parameter family (parameter s in (0, 2/5]).

Conclusion (honest)
-------------------
(H-Qb) is NOT dischargeable by single-piece + first-order global
constraints: an explicit exact Qb-adj pyramid (witness below) satisfies
volume, boundary-area balance, interior-triangle congruence and convexity
simultaneously.  This matches the paper's L1+ rating.  The genuine
remaining obstruction is purely a 5-PIECE ASSEMBLY question -- per-face
tiling of the four T-faces and the solid-angle closure at the T-vertex v0
-- which is the real research content, NOT something to brute-force.

This certificate therefore REDUCES (H-Qb) to that explicit assembly
problem and records the exact candidate locus, rather than over-claiming a
closure.

Author: fresh-eyes re-analysis, 2026-06.
"""

from __future__ import annotations

import json
import os
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
# Exact model.
# ---------------------------------------------------------------------------
v0 = sp.Matrix([1, 1, 1])
v1 = sp.Matrix([1, -1, -1])
v2 = sp.Matrix([-1, 1, -1])
v3 = sp.Matrix([-1, -1, 1])

VT = sp.Rational(8, 3)
check("V_T = 8/3 for this regular tetrahedron",
      sp.Abs((v1 - v0).dot((v2 - v0).cross(v3 - v0))) / 6 == VT)

s, sa, u = sp.symbols('s sa u', positive=True)
b1 = v0 + s * (v1 - v0)
b3 = v0 + s * (v2 - v0)
a = v0 + sa * (v3 - v0)
b4 = v0 + u * (v1 - v0) + u * (v2 - v0)


def tri_area(p, q, r):
    c = (q - p).cross(r - p)
    return sp.sqrt(sp.expand(c.dot(c))) / 2


def vol_tet(p, q, r, t):
    return sp.Abs((q - p).dot((r - p).cross(t - p))) / 6


# ---------------------------------------------------------------------------
# Verify the closed-form reduction on the convex branch u > s/2.
# ---------------------------------------------------------------------------
# Convex base means u > s/2.  Substitute u = (s + d)/2 with d > 0; then
# |s - 2u| = d and sqrt((s-2u)^2) = d exactly, so the branch is rigorous.
d = sp.symbols('d', positive=True)
sub_conv = {u: (s + d) / 2}

V = (vol_tet(a, b1, v0, b3) + vol_tet(a, b1, b3, b4)).subs(sub_conv)
A_base = (tri_area(b1, v0, b3) + tri_area(b1, b3, b4)).subs(sub_conv)
A_F1 = tri_area(b1, v0, a).subs(sub_conv)
A_F2 = tri_area(v0, b3, a).subs(sub_conv)

V_c = sp.simplify(V)
Ab_c = sp.simplify(A_base)
Asum_c = sp.simplify(A_base + A_F1 + A_F2)

# expected forms, also written with u = (s + d)/2
exp_V = (sp.Rational(16, 3) * s * u * sa).subs(sub_conv)
exp_Ab = (4 * sp.sqrt(3) * s * u).subs(sub_conv)
exp_As = (4 * sp.sqrt(3) * s * (u + sa)).subs(sub_conv)

check("Vol = 16*s*u*sa/3 on the convex branch (u = (s+d)/2, d>0)",
      sp.simplify(V_c - exp_V) == 0, f"Vol = {V_c}")
check("A_base = 4*sqrt(3)*s*u on the convex branch",
      sp.simplify(Ab_c - exp_Ab) == 0, f"A_base = {Ab_c}")
check("A_F1 = A_F2 = 2*sqrt(3)*s*sa",
      sp.simplify(A_F1 - 2 * sp.sqrt(3) * s * sa) == 0
      and sp.simplify(A_F2 - 2 * sp.sqrt(3) * s * sa) == 0)
check("A_sum = 4*sqrt(3)*s*(u + sa) on the convex branch",
      sp.simplify(Asum_c - exp_As) == 0, f"A_sum = {sp.factor(Asum_c)}")

# ---------------------------------------------------------------------------
# Reduced system N1 & N2 and its 1-parameter solution.
# ---------------------------------------------------------------------------
eq_vol = sp.Eq(sp.Rational(16, 3) * s * u * sa, sp.Rational(8, 15))   # -> s u sa = 1/10
eq_area = sp.Eq(4 * sp.sqrt(3) * s * (u + sa), 8 * sp.sqrt(3) / 5)     # -> s(u+sa)=2/5
red_vol = sp.simplify(sp.solve(eq_vol, u * sa)[0])
red_area = sp.simplify(sp.solve(eq_area, u + sa)[0])
check("N1 reduces to  s*u*sa = 1/10",
      sp.simplify(red_vol - 1 / (10 * s)) == 0, f"u*sa = {red_vol}")
check("N2 reduces to  s*(u+sa) = 2/5",
      sp.simplify(red_area - 2 / (5 * s)) == 0, f"u+sa = {red_area}")

# u, sa are roots of x^2 - (2/(5s)) x + 1/(10s); real iff discriminant >= 0.
disc = (2 / (5 * s)) ** 2 - 4 * (1 / (10 * s))
disc = sp.simplify(disc)
# disc >= 0  <=>  s <= 2/5
s_bound = sp.solve(sp.Eq(disc, 0), s)
check("u, sa real  <=>  s <= 2/5 (discriminant vanishes at s = 2/5)",
      sp.Rational(2, 5) in s_bound, f"disc = {sp.factor(disc)}, roots s = {s_bound}")

# ---------------------------------------------------------------------------
# Explicit exact witness (so the locus is provably NON-empty).
# ---------------------------------------------------------------------------
s0 = sp.Rational(1, 3)
u0 = (6 - sp.sqrt(6)) / 10
sa0 = (6 + sp.sqrt(6)) / 10
w_vol = sp.simplify(s0 * u0 * sa0)
w_area = sp.simplify(s0 * (u0 + sa0))
check("witness (s,u,sa) = (1/3, (6-sqrt6)/10, (6+sqrt6)/10): s*u*sa = 1/10",
      w_vol == sp.Rational(1, 10), f"s*u*sa = {w_vol}")
check("witness: s*(u+sa) = 2/5",
      w_area == sp.Rational(2, 5), f"s*(u+sa) = {w_area}")
check("witness is convex & inside: s/2 < u < 1/2 and 0 < sa < 1",
      (s0 / 2 < u0) and (u0 < sp.Rational(1, 2)) and (0 < sa0) and (sa0 < 1),
      f"u={sp.nsimplify(u0)}~{float(u0):.4f}, sa~{float(sa0):.4f}")

check("=> N1..N4 leave a NON-EMPTY 1-parameter Qb-adj family: (H-Qb) is "
      "NOT closed by single-piece + first-order global constraints",
      w_vol == sp.Rational(1, 10) and w_area == sp.Rational(2, 5))

# ---------------------------------------------------------------------------
RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["reduction"] = {
    "volume_constraint": "s*u*sa = 1/10",
    "boundary_area_constraint": "s*(u+sa) = 2/5",
    "residual_locus": "1-parameter family, s in (0, 2/5]",
    "witness": "(s,u,sa) = (1/3, (6-sqrt6)/10, (6+sqrt6)/10)",
    "status": "intermediate reduction only: this script reduces H-Qb to the "
              "5-piece assembly problem (per-face tiling + solid-angle "
              "closure at v0).  The current public quadrilateral-pyramid ledger is closed by "
              "the downstream hqb_perface, hqb_asymmetric_caseI/II, and "
              "hqb_opp certificates.",
    "closed_here": False,
    "closed_by_downstream_certificates": True,
}
print(f"\n{'=' * 70}\nTotal passed: {PASSED}   failed: {FAILED}\n{'=' * 70}")

out = os.path.join(os.path.dirname(__file__), "..", "results",
                   "hqb_reduction_certificate_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"\nResults written to {os.path.abspath(out)}")
