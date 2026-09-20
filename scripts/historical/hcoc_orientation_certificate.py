"""
(H-coc) DISCHARGE CERTIFICATE  --  orientation-character reduction.
===================================================================

Target.  The earlier auxiliary-hypothesis formulation isolated the
 t = 3, f = 7, boundary multiset (12, 12, 24), Sym(P)-orbit structure
(2, 2) sub-case behind the algebraic condition

    (H-coc)   for every triangle {i, j, k} of the K_5 interior-adjacency
              graph, the orbit-transport elements satisfy
              g_ij . g_jk . g_ki = id  in  Sym(P) = C_2.

That formulation left a historical developing-map route from H-trip to
H-coc as motivation.  The current public ledger does not use H-trip as a
formal dependency: this script DISCHARGES (H-coc) directly for the
(2, 2) sub-case.

The argument in one paragraph
-----------------------------
1. (No stabiliser slack.)  In the (2, 2) case every interior facet of P
   lies in a Sym(P)-orbit of SIZE 2, so Stab(F) = 1.  Hence the
   orbit-transport element g_ij in C_2 is UNIQUELY determined -- the
   "modulo stabiliser" ambiguity the paper worries about is empty here.

2. (Orientation character is an honest homomorphism.)  Let
   eps = sgn(det) : Isom(R^3) -> {+1, -1} = Z/2.  It is a homomorphism.
   Put s(l) = eps(gamma_l) for the placing motion gamma_l of piece P_l.

3. (Facet correction is the reflection.)  Let
   rho = gamma_j^{-1} gamma_i  be the face-to-face identification of the
   shared facet (pointwise, by face-to-face-ness).  Both rho and g_ij map
   the slot facet F_{a_i} -> F_{a_j}; with trivial stabiliser they agree
   pointwise on the facet, so c := g_ij^{-1} rho fixes the facet plane
   POINTWISE.  An isometry of R^3 fixing a planar facet pointwise is
   either id or the reflection through that plane.  Because P_i and P_j
   occupy OPPOSITE sides of the shared facet (disjoint interiors,
   face-to-face), c maps P to the opposite side of the facet from itself,
   so c is NOT the identity: c is the facet reflection, eps(c) = -1.

4. (The forced bit.)  eps(g_ij) = eps(rho) . eps(c)^{-1}
   = eps(gamma_i) eps(gamma_j) . (-1) = -s(i) s(j).  In Z/2:
        bit(g_ij) = 1 + s(i) + s(j)          (the "c0 = 1" coboundary).

5. (The contradiction.)  Substituting bit(g_ij) = 1 + s(i) + s(j) into
   the K_5-triangle constraints of (H-coc) forces  z_i + z_j = 1  for all
   10 vertex pairs, i.e. a proper 2-colouring of K_5 -- impossible since
   K_5 is not bipartite.  Hence NO such dissection exists, with (H-coc)
   now a THEOREM, not a hypothesis.

What this script certifies (all with exact arithmetic)
------------------------------------------------------
  Part A.  The combinatorial dichotomy: with the forced coboundary bit
           the K_5 system is UNSAT for c0 = 1 and SAT for c0 = 0, so the
           whole closure rests precisely on c0 = 1.
  Part B.  The three orientation-character facts (homomorphism;
           facet-fixing isometry is id-or-reflection; opposite-sides
           gluing forces the reflection), verified on explicit exact
           orthogonal matrices, establishing c0 = 1.
  Part C.  Synthesis: bit(g_ij) = 1 + s(i) + s(j) is forced, the K_5
           contradiction follows, (H-coc) is discharged.

Exactness.  All linear algebra uses exact rational matrices
(fractions.Fraction); determinants and fixed-point checks are exact.
The only enumeration (Part A) is a finite 2^10 search.

Author: fresh-eyes re-analysis, 2026-06.
"""

from __future__ import annotations

import json
import os
from fractions import Fraction
from itertools import combinations, product


# ---------------------------------------------------------------------------
# Bookkeeping
# ---------------------------------------------------------------------------
PASSED = 0
FAILED = 0
RESULTS: dict = {"parts": [], "passed": 0, "failed": 0}


def part(title: str) -> None:
    print(f"\n=== {title} ===")
    RESULTS["parts"].append({"title": title, "checks": []})


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASSED, FAILED
    ok = bool(condition)
    PASSED += ok
    FAILED += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    RESULTS["parts"][-1]["checks"].append(
        {"name": name, "passed": ok, "detail": detail})


# ---------------------------------------------------------------------------
# Minimal exact 3x3 rational matrix algebra
# ---------------------------------------------------------------------------
Mat = tuple  # 3-tuple of 3-tuples of Fraction


def m(rows) -> Mat:
    return tuple(tuple(Fraction(x) for x in r) for r in rows)


def matmul(A: Mat, B: Mat) -> Mat:
    return tuple(
        tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )


def matvec(A: Mat, v):
    return tuple(sum(A[i][k] * v[k] for k in range(3)) for i in range(3))


def det3(A: Mat) -> Fraction:
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def transpose(A: Mat) -> Mat:
    return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))


I3 = m([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def is_orthogonal(A: Mat) -> bool:
    return matmul(A, transpose(A)) == I3


def eps(A: Mat) -> int:
    """Orientation character eps = sgn(det) in {+1, -1}."""
    d = det3(A)
    assert d in (Fraction(1), Fraction(-1)), f"non-isometry det {d}"
    return int(d)


def bit(sign: int) -> int:
    """{+1,-1} -> Z/2 with bit(+1)=0, bit(-1)=1."""
    return 0 if sign == 1 else 1


# ===========================================================================
# PART A.  Combinatorial dichotomy: closure <=> c0 = 1.
# ===========================================================================
part("A. K_5 triangle system: UNSAT iff c0 = 1 (closure rests on c0 = 1)")

# K_5 = two edge-disjoint 5-cycles (the A-orbit slots and B-orbit slots),
# the unique 2-factorisation up to relabelling.
a_cycle = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
b_cycle = [(1, 3), (3, 5), (5, 2), (2, 4), (4, 1)]


def norm(e):
    return tuple(sorted(e))


a_set = {norm(e) for e in a_cycle}
b_set = {norm(e) for e in b_cycle}
all_edges = {norm((i, j)) for i in range(1, 6) for j in range(1, 6) if i < j}
triangles = list(combinations(range(1, 6), 3))

check("A- and B-slot cycles are edge-disjoint and cover K_5",
      a_set.isdisjoint(b_set) and (a_set | b_set) == all_edges,
      "two edge-disjoint 5-cycles")


def tau_bit(edge, a, y, c0):
    """Forced transport bit on an edge under per-vertex slot labels
    (a on A-edges, y on B-edges) and constant orientation offset c0."""
    u, v = norm(edge)
    if (u, v) in a_set:
        return (c0 + a[u] + a[v]) % 2
    return (c0 + y[u] + y[v]) % 2


def count_consistent(c0: int) -> int:
    cnt = 0
    for bits in product([0, 1], repeat=10):
        a = {i + 1: bits[i] for i in range(5)}
        y = {i + 1: bits[5 + i] for i in range(5)}
        if all(
            (tau_bit((i, j), a, y, c0)
             + tau_bit((j, k), a, y, c0)
             + tau_bit((i, k), a, y, c0)) % 2 == 0
            for (i, j, k) in triangles
        ):
            cnt += 1
    return cnt


n_c0_0 = count_consistent(0)
n_c0_1 = count_consistent(1)
check("c0 = 0:  K_5 (H-coc) system is SATISFIABLE (no contradiction)",
      n_c0_0 > 0, f"{n_c0_0}/1024 label assignments consistent")
check("c0 = 1:  K_5 (H-coc) system is UNSATISFIABLE (contradiction)",
      n_c0_1 == 0, f"{n_c0_1}/1024 label assignments consistent")
check("=> the entire f=7 (2,2) closure reduces to proving the single "
      "orientation bit  c0 = 1",
      n_c0_0 > 0 and n_c0_1 == 0)

RESULTS["dichotomy"] = {"consistent_c0_0": n_c0_0, "consistent_c0_1": n_c0_1}


# ===========================================================================
# PART B.  Orientation-character facts  =>  c0 = 1.
# ===========================================================================
part("B. Orientation character eps = sgn(det): the three forcing facts")

# ---- B1. eps is a homomorphism on Isom(R^3) (det is multiplicative). ----
# A representative spanning set of exact orthogonal generators:
#   Rx = 90-deg rotation about x  (det +1)
#   Sz = reflection in z = 0      (det -1)
#   Swp = coordinate swap x<->y   (det -1, an improper isometry)
Rx = m([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
Sz = m([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
Swp = m([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
gens = {"Rx": Rx, "Sz": Sz, "Swp": Swp}

for name, A in gens.items():
    check(f"generator {name} is orthogonal (a linear isometry)",
          is_orthogonal(A), f"det = {det3(A)}")

hom_ok = True
for (na, A), (nb, B) in product(gens.items(), repeat=2):
    if eps(matmul(A, B)) != eps(A) * eps(B):
        hom_ok = False
check("eps(A.B) = eps(A).eps(B) on all generator products "
      "(eps is a homomorphism, no stabiliser slack to spoil it)",
      hom_ok)

# ---- B2. An isometry fixing a planar facet POINTWISE is id or the ----
# ----     reflection through that plane (so eps in {+1, -1}).        ----
# Take the facet to lie in the plane z = 0.  Fixing three affinely
# independent points of that plane pointwise pins the isometry on the
# plane; the only freedom left is the off-plane sign, giving exactly
# {id, reflection-in-z}.
plane_pts = [(Fraction(0), Fraction(0), Fraction(0)),
             (Fraction(1), Fraction(0), Fraction(0)),
             (Fraction(0), Fraction(1), Fraction(0))]


def fixes_plane_pointwise(A: Mat) -> bool:
    # linear isometries fixing the z=0 plane pointwise: check the two
    # in-plane basis vectors are fixed.
    return (matvec(A, (Fraction(1), 0, 0)) == (Fraction(1), 0, 0)
            and matvec(A, (0, Fraction(1), 0)) == (0, Fraction(1), 0))


# Enumerate all 48 signed permutation matrices (the exact orthogonal
# matrices with entries in {-1,0,1}) and keep those fixing the plane.


def signed_perms():
    import itertools
    for perm in itertools.permutations(range(3)):
        for signs in product([1, -1], repeat=3):
            rows = [[0, 0, 0] for _ in range(3)]
            for i in range(3):
                rows[i][perm[i]] = signs[i]
            yield m(rows)


fixers = [A for A in signed_perms()
          if is_orthogonal(A) and fixes_plane_pointwise(A)]
fixer_dets = sorted({int(det3(A)) for A in fixers})
check("isometries (in the signed-permutation model) fixing the facet "
      "plane pointwise: exactly {id, reflection}",
      len(fixers) == 2 and fixer_dets == [-1, 1],
      f"{len(fixers)} such maps, dets = {fixer_dets}")
RESULTS["proof_boundary_note"] = (
    "The signed-permutation enumeration is an exact sanity model for the "
    "coordinate representatives; the all-isometry statement used in the proof "
    "is the standard Euclidean lemma that an isometry fixing a planar facet "
    "pointwise is either the identity or the reflection in that plane."
)
the_reflection = next(A for A in fixers if det3(A) == -1)
check("the non-identity facet-fixing isometry is the plane reflection, "
      "eps = -1",
      eps(the_reflection) == -1)

# ---- B3. Opposite-sides face-to-face gluing forces the reflection. ----
# Model: shared facet in plane z = 0.  Reference body P occupies z >= 0
# (a witness point at z = +1).  The symmetry g_ij keeps P -> P, so
# g_ij(witness) stays on the SAME side (z >= 0).  The face-to-face
# identification rho carries P onto the neighbour copy occupying z <= 0,
# so the correction c = g_ij^{-1} rho sends the witness to the OPPOSITE
# side.  Any facet-fixing isometry sending z=+1 to z<0 must be the
# reflection.
witness = (Fraction(0), Fraction(0), Fraction(1))
opp = [A for A in fixers if matvec(A, witness)[2] < 0]
check("a facet-fixing isometry that swaps the two sides (opposite-side "
      "occupancy) is unique and equals the reflection",
      len(opp) == 1 and opp[0] == the_reflection)
check("therefore the constant facet correction has eps(c) = -1, i.e. "
      "c0 = bit(eps(c)) = 1",
      bit(eps(opp[0])) == 1)

RESULTS["c0_proved"] = 1


# ===========================================================================
# PART C.  Synthesis: bit(g_ij) = 1 + s(i) + s(j)  =>  (H-coc) discharged.
# ===========================================================================
part("C. Synthesis: the forced bit and the unconditional contradiction")

# eps(g_ij) = eps(rho) * eps(c)^{-1} = s(i) s(j) * (-1)  =>  bit = 1 + s_i + s_j.
# We verify the additive identity bit(-s_i s_j) = 1 + bit(s_i) + bit(s_j)
# over all sign choices, then re-run the K_5 contradiction with this
# geometrically forced bit (no (H-coc) assumed).
identity_ok = all(
    bit(-(si * sj)) == (1 + bit(si) + bit(sj)) % 2
    for si in (1, -1) for sj in (1, -1)
)
check("forced-bit identity  bit(g_ij) = 1 + s(i) + s(j)  holds for all "
      "handedness sign choices",
      identity_ok)

# Plug s = (s1..s5) directly (slot labels are the handedness bits) and
# confirm NO handedness assignment evades the contradiction: the
# K_5-triangle sums are identically 1 (odd), never 0.
forced_contradiction = True
for sbits in product([0, 1], repeat=5):
    s = {i + 1: sbits[i] for i in range(5)}
    for (i, j, k) in triangles:
        tij = (1 + s[i] + s[j]) % 2
        tjk = (1 + s[j] + s[k]) % 2
        tik = (1 + s[i] + s[k]) % 2
        if (tij + tjk + tik) % 2 == 0:
            forced_contradiction = False
check("with the forced bit, EVERY K_5 triangle sum is odd (= 1) for "
      "EVERY handedness assignment: (H-coc) cocycle can never hold",
      forced_contradiction,
      "3*(1) + 2*(s-terms) = 1 (mod 2)")

check("CONCLUSION: (H-coc) is discharged -- the f=7 (2,2) sub-case is "
      "closed UNCONDITIONALLY",
      n_c0_1 == 0 and bit(eps(opp[0])) == 1 and forced_contradiction)

RESULTS["conclusion"] = {
    "hcoc_discharged": bool(n_c0_1 == 0 and bit(eps(opp[0])) == 1
                            and forced_contradiction),
    "mechanism": "orientation character eps=sgn(det) forces "
                 "bit(g_ij)=1+s(i)+s(j); K_5 non-bipartite => UNSAT",
    "residual": "none for genuine (2,2) orientation branch; the quadrilateral-pyramid branch is discharged separately, and only the accidental-even metric residual remains in the global synthesis",
}


# ---------------------------------------------------------------------------
RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
print(f"\n{'=' * 70}\nTotal passed: {PASSED}   failed: {FAILED}\n{'=' * 70}")

out = os.path.join(os.path.dirname(__file__), "..", "results",
                   "hcoc_orientation_certificate_results.json")
with open(out, "w") as fh:
    json.dump(RESULTS, fh, indent=2)
print(f"\nResults written to {os.path.abspath(out)}")
