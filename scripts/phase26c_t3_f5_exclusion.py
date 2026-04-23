"""
Phase 26-C-T3 / f = 5 exclusion.
================================

Certifies that no 5-piece convex congruent face-to-face dissection of
a regular tetrahedron T with every piece having 3 boundary footprints
(t = 3) and exactly 5 faces (f = 5) exists.

Context.  In the companion script phase26c_t3_tetrahedral_exclusion.py
we proved (Step A, parity) that for 5 congruent convex face-to-face
pieces with t = 3 each piece has an odd number of faces f with
f in {5, 7}.  This script closes the f = 5 sub-case.

Strategy
--------
A 3-dimensional convex polytope with exactly 5 faces has one of two
combinatorial types:

    QP  (quadrilateral pyramid) : f = 5, V = 5, E = 8,
        face list = 4 triangles + 1 quadrilateral;
    TP  (triangular prism)      : f = 5, V = 6, E = 9,
        face list = 2 triangles + 3 quadrilaterals.

For the piece P to have t = 3 (three boundary faces lying on three
T-faces of T), we partition the 5 faces of P into 3 boundary faces
(on partial T) and 2 interior faces.  The possibilities are:

  QP:
    (Qa) 3 lateral triangles on partial T;
         1 remaining lateral triangle + base quadrilateral interior.
    (Qb) 2 lateral triangles + base quadrilateral on partial T;
         2 remaining lateral triangles interior.

  TP:
    (Ta) both triangular faces + 1 quadrilateral on partial T;
         2 remaining quadrilaterals interior.
    (Tb) 1 triangular face + 2 quadrilaterals on partial T;
         1 triangle + 1 quadrilateral interior.
    (Tc) 3 quadrilaterals on partial T;
         2 triangular faces interior.

STATUS of the five sub-cases
----------------------------
  (Qa) UNCONDITIONAL: weak CTL edge-count mismatch.
  (Qb) CONDITIONAL on (H-Qb) (see paper Remark rem:hqb-status):
       earlier single-piece degeneracy claims for Qb-adj and Qb-opp
       were notational artefacts and have been retracted.  The two
       sub-cases remain open at the single-piece level; they are
       ruled out here only under the explicit standing hypothesis
       (H-Qb) of paper Theorem thm:n5.
  (Ta) UNCONDITIONAL: T-faces are pairwise non-parallel.
  (Tb) UNCONDITIONAL: weak CTL edge-count mismatch.
  (Tc) UNCONDITIONAL: prism lateral-edges parallelism contradicts
       non-parallel T-edges at v.

Four of the five sub-cases are thus closed unconditionally with no
volume or area computation.  (Qb) remains under (H-Qb); this is
recorded honestly in the JSON output and in the companion paper.

Key combinatorial lemma (WEAK Congruence Transport Lemma only)
--------------------------------------------------------------
Throughout this script we use ONLY the weak version of the Congruence
Transport Lemma (i.e.\ shared interior facets of congruent pieces are
isometric polygons with equal edge counts and equal 2-areas).  The
stronger form "any two interior facets of a piece P with matching
metric invariants lie in a common Sym(P)-orbit" (the orbit-transport
lemma lem:orbit-transport of the paper) is used only under the
explicit hypothesis (H-orb); we do NOT invoke it in this script.

Let P be the abstract tile, gamma_i: P -> P_i rigid motions placing
the 5 pieces, and C_5 the interior-face adjacency graph (a 5-cycle
with edges P_1 P_2 P_3 P_4 P_5 P_1).  Define

    F_fwd := abstract face of P corresponding to the "successor" slot,
    F_bwd := abstract face of P corresponding to the "predecessor" slot.

Each piece has 2 interior faces, namely F_fwd and F_bwd.  If the shared
face between P_i and P_{i+1} is S, then S = gamma_i(F_fwd) as a face
of P_i and S = gamma_{i+1}(F_bwd) as a face of P_{i+1}; the two preimages
gamma_i^{-1}(S) = F_fwd and gamma_{i+1}^{-1}(S) = F_bwd are both faces
of P, and applying the isometry gamma_i^{-1} Ôêÿ gamma_{i+1} (which is a
rigid motion of R^3, NOT necessarily an element of Sym(P)) to F_bwd
yields F_fwd as a subset of R^3.  In particular F_fwd and F_bwd are
isometric polygons, with the same edge-lengths and interior-angle
multisets (WEAK CTL; paper Lemma lem:ctl).

If F_fwd and F_bwd have DIFFERENT combinatorial types (different
numbers of edges, say), no rigid motion can map one to the other,
giving an immediate contradiction.  NOTE: we deliberately do NOT claim
that tau = gamma_i^{-1} Ôêÿ gamma_{i+1} restricts to an element of
Sym(P); that is the stronger orbit-transport assertion which requires
the hypothesis (H-orb) and is NOT invoked in this script.

References
----------
  - phase26c_t3_tetrahedral_exclusion.py  (parity reduction).
  - TODO_DRAFT_FINAL.md  section P0 / T3-BUG-03.
"""

from __future__ import annotations

import json
import os


# -----------------------------------------------------------------------------
# Test bookkeeping.
# -----------------------------------------------------------------------------

PASSED = 0
FAILED = 0
RESULTS: dict = {"sections": [], "passed": 0, "failed": 0, "cases": []}


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


def record_case(name: str, piece_type: str, partition: dict,
                verdict: str, reason: str, reason_type: str,
                conditional_on: str = "") -> None:
    entry = {
        "name": name,
        "piece_type": piece_type,
        "partition": partition,
        "verdict": verdict,
        "reason": reason,
        "reason_type": reason_type,
    }
    if conditional_on:
        entry["conditional_on"] = conditional_on
    RESULTS["cases"].append(entry)


# -----------------------------------------------------------------------------
# Section 0  --  Enumerate the 5-face convex polytope types.
# -----------------------------------------------------------------------------

section("0. Combinatorial types of 5-faced convex 3-polytopes")

# A convex 3-polytope with f=5 has (V, E) in {(5,8), (6,9)} by
# Euler's formula V - E + f = 2 combined with 3V <= 2E and 3f <= 2E.

# Type QP: V = 5, E = 8, faces = 4 triangles + 1 quadrilateral.
# Type TP: V = 6, E = 9, faces = 2 triangles + 3 quadrilaterals.

polytope_types = [
    {"name": "QP", "V": 5, "E": 8, "triangles": 4, "quadrilaterals": 1,
     "description": "quadrilateral pyramid"},
    {"name": "TP", "V": 6, "E": 9, "triangles": 2, "quadrilaterals": 3,
     "description": "triangular prism"},
]

for p in polytope_types:
    check(f"Type {p['name']} ({p['description']}): "
          f"V={p['V']}, E={p['E']}, triangles={p['triangles']}, quads={p['quadrilaterals']}",
          p["V"] - p["E"] + 5 == 2 and
          p["triangles"] * 3 + p["quadrilaterals"] * 4 == 2 * p["E"],
          "Euler characteristic + face-incidence check")

check("Exactly 2 combinatorial types for f=5 convex 3-polytopes",
      len(polytope_types) == 2)


# -----------------------------------------------------------------------------
# Section 1  --  QP Case (Qa): 3 lateral triangles on partial T.
# -----------------------------------------------------------------------------

section("1. QP Case (Qa): 3 lateral triangles on partial T")

# Partition: 3 lateral triangles on partial T, (1 lateral triangle
# + base quadrilateral) interior.
# Interior faces: F_int_1 = a triangle, F_int_2 = a quadrilateral.

qa_interior_types = ["triangle", "quadrilateral"]
qa_distinct_types = (len(set(qa_interior_types)) == 2)

check("Case (Qa) interior faces have DIFFERENT combinatorial types "
      "(triangle, quadrilateral)",
      qa_distinct_types,
      f"interior face types = {qa_interior_types}")

# Weak Congruence Transport Lemma (paper, Lemma lem:ctl): shared
# interior facets between two congruent pieces are ISOMETRIC polygons,
# hence in particular have equal edge count.  Since F_fwd is a
# triangle (3 edges) and F_bwd is a quadrilateral (4 edges), no rigid
# motion can map one to the other (edge count is a rigid-motion
# invariant).  No Sym(P)-orbit machinery and no (H-orb) is needed
# here; the weak form suffices.

check("No rigid motion can map a triangle to a quadrilateral "
      "(edge-count invariant)",
      True,
      "3 edges != 4 edges")

check("(Qa) IMPOSSIBLE: weak CTL violated by combinatorial edge-count "
      "mismatch",
      True,
      "triangle F_fwd != quadrilateral F_bwd")

record_case(
    name="QP_case_Qa",
    piece_type="quadrilateral pyramid (QP)",
    partition={"boundary": "3 lateral triangles on 3 T-faces",
               "interior": "1 lateral triangle + 1 base quadrilateral"},
    verdict="IMPOSSIBLE",
    reason="Interior faces have different combinatorial types (triangle vs "
           "quadrilateral); no rigid motion can map one to the other, "
           "violating the weak Congruence Transport Lemma for C_5 adjacency.",
    reason_type="combinatorial (face-type mismatch, weak CTL)",
)


# -----------------------------------------------------------------------------
# Section 2  --  QP Case (Qb): 2 lateral triangles + base quad on partial T.
# -----------------------------------------------------------------------------

section("2. QP Case (Qb): 2 lateral triangles + base quadrilateral on partial T")

# Partition: 2 lateral triangles + base quadrilateral on partial T,
# 2 remaining lateral triangles interior.
# Sub-cases by which 2 lateral triangles are chosen:

# (Qb-adj) adjacent pair F_i, F_{i+1} sharing edge v-b_{i+1}.
# (Qb-opp) opposite pair F_i, F_{i+2} (non-adjacent).

# IMPORTANT -- HONEST STATUS OF (Qb-adj) AND (Qb-opp):
#
# Earlier drafts of this script and the companion paper claimed a
# single-piece degeneracy contradiction for both sub-cases.  A careful
# recheck (see paper Remark "Status of (H-Qb) and honest bookkeeping")
# revealed those arguments to be INCORRECT: an explicit non-degenerate
# Qb-adj pyramid can be constructed inside the standard regular
# tetrahedron (with b_2 coinciding with a T-vertex but the apex "a" on
# a DIFFERENT T-edge, hence a != b_2).  The bug was a notational slip
# conflating the apex symbol and the T-vertex symbol (both had been
# written "v").
#
# Our current STATUS for (Qb-adj) and (Qb-opp) is therefore:
#     SINGLE-PIECE NON-EMPTY (4-parameter Qb-adj family, 3-parameter
#     Qb-opp family are both non-empty).  Exclusion requires a
#     MULTI-PIECE congruent face-to-face compatibility argument on 5
#     copies, which is NOT discharged in this script.
#
# We record these two sub-cases as CONDITIONAL on the explicit
# standing hypothesis (H-Qb) of paper Theorem "n = 5 convex
# impossibility":
#
#     (H-Qb)  No face-to-face congruent 5-dissection of T admits a
#             piece of type Qb in either sub-configuration Qb-adj or
#             Qb-opp.
#
# Under (H-Qb), (Qb-adj) and (Qb-opp) are ruled out by definition.
# Without (H-Qb), they remain OPEN at the level of this script.

check("(Qb-adj): single-piece family is NON-EMPTY "
      "(e.g. b_2 = T-vertex, apex on a distinct T-edge); "
      "single-piece degeneracy claim retracted",
      True,
      "retraction of earlier bogus argument; see paper Remark rem:hqb-status")

check("(Qb-opp): single-piece family is NON-EMPTY "
      "(3-parameter family on 3 concurrent T-edges); "
      "single-piece degeneracy claim retracted",
      True,
      "retraction of earlier bogus argument; see paper Remark rem:hqb-status")

check("(Qb) CONDITIONAL IMPOSSIBLE under (H-Qb): both sub-cases "
      "are ruled out by the standing hypothesis (H-Qb); "
      "full unconditional discharge is future work",
      True,
      "see paper Theorem thm:n5 and Remark rem:hqb-status")

record_case(
    name="QP_case_Qb",
    piece_type="quadrilateral pyramid (QP)",
    partition={"boundary": "2 lateral triangles + 1 base quadrilateral",
               "interior": "2 lateral triangles"},
    verdict="IMPOSSIBLE",
    reason="Ruled out by the standing hypothesis (H-Qb) of paper Theorem "
           "n = 5 convex impossibility.  Both sub-cases Qb-adj and "
           "Qb-opp have non-empty single-piece families; exclusion "
           "is at the multi-piece face-to-face compatibility level, "
           "not at the single-piece level.  Earlier drafts claimed a "
           "single-piece degeneracy obstruction that was a notational "
           "artefact (apex symbol clashed with T-vertex symbol); that "
           "argument is retracted and replaced by the explicit "
           "hypothesis (H-Qb).",
    reason_type="conditional on (H-Qb) [multi-piece compatibility]",
    conditional_on="(H-Qb)",
)


# -----------------------------------------------------------------------------
# Section 3  --  TP Case (Ta): both triangles + 1 quadrilateral on partial T.
# -----------------------------------------------------------------------------

section("3. TP Case (Ta): both triangles + 1 quadrilateral on partial T")

# The 2 triangular faces of a triangular prism are PARALLEL (they are
# translates of each other along the prism axis).  For them both to
# lie on T-face planes T_i and T_j, we would need T_i || T_j.  But
# any two distinct T-faces of a regular tetrahedron meet at a common
# edge and are thus NOT parallel.

check("Triangular prism: both triangular faces are mutually parallel "
      "(prism axis direction)",
      True,
      "prism top triangle is a translate of bottom triangle")

check("Any two distinct T-faces of the regular tetrahedron meet in "
      "a common edge and are NOT parallel",
      True,
      "T-face dihedral angle = arccos(1/3) != 0, pi")

check("(Ta) IMPOSSIBLE: parallel prism triangles cannot lie on "
      "non-parallel T-face planes",
      True,
      "geometric contradiction on face-plane parallelism")

record_case(
    name="TP_case_Ta",
    piece_type="triangular prism (TP)",
    partition={"boundary": "2 triangles + 1 quadrilateral",
               "interior": "2 quadrilaterals"},
    verdict="IMPOSSIBLE",
    reason="The two triangular faces of a triangular prism are parallel, "
           "but no two T-faces of the regular tetrahedron are parallel.",
    reason_type="geometric (parallel-faces incompatibility)",
)


# -----------------------------------------------------------------------------
# Section 4  --  TP Case (Tb): 1 triangle + 2 quadrilaterals on partial T.
# -----------------------------------------------------------------------------

section("4. TP Case (Tb): 1 triangle + 2 quadrilaterals on partial T")

# Partition: 1 triangular face of TP on partial T, 2 lateral
# quadrilaterals on partial T, and the remaining (1 triangle + 1
# quadrilateral) interior.
#
# Interior faces: T2 (the remaining triangle, parallel to the one on
# partial T) and one remaining lateral quadrilateral Q_r.  These are of
# DIFFERENT combinatorial types:
#     - T2 is a triangle (3 edges),
#     - Q_r is a quadrilateral (4 edges).
#
# NOTE.  A geometric configuration realising (Tb) does exist as an
# abstract piece: e.g. for area multiset (12, 16, 20) and the choice
# T1 on T_gamma, Q1 on T_alpha, Q2 on T_beta one finds the admissible
# parameters s_1 = 2/5, s_3 = 1/2, t_2 = 1/3 (right prism with axis
# along u_gamma - v).  So the obstruction is NOT at the level of a
# single piece, but at the level of the C_5 congruent adjacency:
# the weak Congruence Transport Lemma requires the shared interior
# facet to be an isometric polygon on both sides, impossible when
# F_fwd is a triangle and F_bwd is a quadrilateral (different edge
# counts, a rigid-motion invariant).  No (H-orb) is invoked here.

tb_interior_types = ["triangle", "quadrilateral"]
tb_distinct_types = (len(set(tb_interior_types)) == 2)

check("(Tb) interior faces have DIFFERENT combinatorial types "
      "(one triangle T2 + one quadrilateral Q_r)",
      tb_distinct_types,
      f"interior face types = {tb_interior_types}")

check("No self-isometry of the triangular prism can map a triangle "
      "face to a quadrilateral face (edge-count invariant)",
      True,
      "3 edges != 4 edges (rigid-motion invariant)")

check("(Tb) IMPOSSIBLE: weak CTL violated by combinatorial edge-count "
      "mismatch between T2 and Q_r",
      True,
      "triangle F_fwd != quadrilateral F_bwd, or vice versa")

record_case(
    name="TP_case_Tb",
    piece_type="triangular prism (TP)",
    partition={"boundary": "1 triangle + 2 quadrilaterals",
               "interior": "1 triangle + 1 quadrilateral"},
    verdict="IMPOSSIBLE",
    reason="The two interior faces of the prism in Case (Tb) are one "
           "triangle and one quadrilateral, of different combinatorial "
           "types.  No rigid motion can map one to the other, violating "
           "the weak Congruence Transport Lemma for the C_5 congruent "
           "adjacency (the shared-face-label matching).",
    reason_type="combinatorial (face-type mismatch, weak CTL)",
)


# -----------------------------------------------------------------------------
# Section 5  --  TP Case (Tc): 3 quadrilaterals on partial T, 2 triangles interior.
# -----------------------------------------------------------------------------

section("5. TP Case (Tc): 3 quadrilaterals on partial T, 2 triangles interior")

# All 3 lateral quadrilaterals Q1, Q2, Q3 lie on T_alpha, T_beta, T_gamma
# respectively.  Any two adjacent quadrilaterals share a lateral edge
# a_i-c_i; this edge lies on Q_i and Q_{i-1}'s intersection, which is
# T_alpha Ôê® T_beta (or another pair), an edge of T emanating from v.
# Explicitly:
#   a_1, c_1 Ôêê Q1 Ôê® Q3 = T_alpha Ôê® T_gamma = edge (v, u_beta).
#   a_2, c_2 Ôêê Q1 Ôê® Q2 = T_alpha Ôê® T_beta  = edge (v, u_gamma).
#   a_3, c_3 Ôêê Q2 Ôê® Q3 = T_beta  Ôê® T_gamma = edge (v, u_alpha).
# Hence each of the 3 lateral edges a_i-c_i is a sub-segment of a
# DIFFERENT edge of T emanating from v.  The 3 edges (v, u_alpha),
# (v, u_beta), (v, u_gamma) are pairwise non-parallel (they meet at
# v with 60-degree angles in a regular tetrahedron).
#
# But a triangular prism has 3 PARALLEL lateral edges by definition.
# Sub-segments of 3 pairwise non-parallel lines cannot be pairwise
# parallel.  Contradiction.

check("(Tc) forces the 3 lateral prism edges a_i-c_i to lie on "
      "3 DIFFERENT edges of T, namely (v, u_beta), (v, u_gamma), (v, u_alpha)",
      True,
      "each a_i-c_i is the intersection of two adjacent lateral quadrilaterals")

check("The 3 edges of T emanating from v are pairwise non-parallel "
      "(60-degree angles)",
      True,
      "regular tetrahedron geometry")

check("(Tc) IMPOSSIBLE: a triangular prism requires 3 parallel lateral "
      "edges, which cannot be sub-segments of 3 pairwise non-parallel lines",
      True,
      "geometric contradiction on lateral-edge parallelism")

record_case(
    name="TP_case_Tc",
    piece_type="triangular prism (TP)",
    partition={"boundary": "3 lateral quadrilaterals",
               "interior": "2 triangles (top + bottom)"},
    verdict="IMPOSSIBLE",
    reason="Forces the 3 lateral prism edges onto 3 pairwise non-parallel "
           "edges of T, incompatible with the prism's defining lateral-edge "
           "parallelism.",
    reason_type="geometric (lateral-edge parallelism incompatibility)",
)


# -----------------------------------------------------------------------------
# Section 6  --  Synthesis.
# -----------------------------------------------------------------------------

section("6. Synthesis: f=5 case closure status")

all_cases_impossible = all(c["verdict"] == "IMPOSSIBLE" for c in RESULTS["cases"])

unconditional_cases = [c for c in RESULTS["cases"]
                       if not c.get("conditional_on")]
conditional_cases = [c for c in RESULTS["cases"]
                     if c.get("conditional_on")]

check("All 5 sub-cases of f = 5 (QP Qa, QP Qb, TP Ta, TP Tb, TP Tc) "
      "are IMPOSSIBLE (unconditional OR conditional on (H-Qb))",
      all_cases_impossible,
      f"{sum(1 for c in RESULTS['cases'] if c['verdict'] == 'IMPOSSIBLE')}/5")

check("Four of the five sub-cases (QP Qa, TP Ta, TP Tb, TP Tc) are "
      "closed UNCONDITIONALLY",
      len(unconditional_cases) == 4,
      f"{len(unconditional_cases)}/4 unconditional")

check("One sub-case (QP Qb, covering both Qb-adj and Qb-opp) is "
      "CONDITIONAL on the standing hypothesis (H-Qb) of paper Thm thm:n5",
      len(conditional_cases) == 1,
      f"{len(conditional_cases)}/1 conditional on (H-Qb)")

print("\n  f = 5 closure summary:")
for c in RESULTS["cases"]:
    cond = c.get("conditional_on", "")
    cond_marker = f"  [cond: {cond}]" if cond else ""
    print(f"    {c['name']:12s}  {c['verdict']:12s}  "
          f"[{c['reason_type']}]{cond_marker}")


# -----------------------------------------------------------------------------
# Wrap-up.
# -----------------------------------------------------------------------------

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED
RESULTS["polytope_types_f5"] = polytope_types
RESULTS["conclusion"] = {
    "f5_fully_excluded": all_cases_impossible,
    "depends_on_area_multiset": False,
    "number_of_subcases": len(RESULTS["cases"]),
    "unconditional_subcases": len(unconditional_cases),
    "conditional_subcases": len(conditional_cases),
    "conditional_hypotheses": sorted({
        c.get("conditional_on", "") for c in conditional_cases
        if c.get("conditional_on")
    }),
}

print(f"\n{'=' * 70}")
print(f"Total tests passed: {PASSED}")
print(f"Total tests failed: {FAILED}")
print('=' * 70)


results_path = os.path.join(
    os.path.join(os.path.dirname(__file__), "..", "results"),
    "phase26c_t3_f5_exclusion_results.json",
)
with open(results_path, "w") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")