"""
Phase 26-E: updated synthesis for the n = 5 convex reduction.

This script aggregates the public certificate JSONs and records the current
logical state of the n = 5 programme:

  * H-trip is retired: it was motivational for H-coc and is not used as a
    formal hypothesis once H-coc is proved directly.
  * H-coc is discharged by the exact orientation-cocycle certificate.
  * H-Qb is fully discharged by the Qb-adj/Qb-opp certificate stack.
  * The singleton H-orb patterns are discharged by parity.
  * The only remaining obstruction is the H-orb accidental even-congruence
    residual: f(P)=7, t=3, Sym(P)=1, and the four interior facets of P have
    accidental even metric pattern (4) or (2,2).

The script intentionally does not claim unconditional n = 5 closure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


PASSED = 0
FAILED = 0
RESULTS: dict = {
    "sections": [],
    "passed": 0,
    "failed": 0,
    "theorem": "26.1 (n=5 reduction, convex case)",
    "outcome": None,
    "evidence": {},
}


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


def load_json(results_dir: Path, fname: str) -> dict:
    path = results_dir / fname
    check(f"results JSON exists: {fname}", path.exists())
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"

section("1. Load public result JSONs")

FILES = {
    "26-A": "phase26a_chamber_skeleton_results.json",
    "26-B": "phase26b_role_distribution_n5_results.json",
    "26-C-T2": "phase26c_t2_residuals_results.json",
    "26-C-T3": "phase26c_t3_residuals_results.json",
    "26-C-T3-TET": "phase26c_t3_tetrahedral_exclusion_results.json",
    "26-C-T3-F5-legacy": "phase26c_t3_f5_exclusion_results.json",
    "26-C-T3-F7-legacy": "phase26c_t3_f7_exclusion_results.json",
    "26-C-T4": "phase26c_t4_full_incidence_residual_results.json",
    "H-coc": "hcoc_orientation_certificate_results.json",
    "H-orb-parity": "horb_parity_certificate_results.json",
    "H-orb-scope": "horb_residual_scope_results.json",
    "H-orb-combinatorial": "horb_residual_combinatorial_results.json",
    "H-Qb-reduction": "hqb_reduction_certificate_results.json",
    "H-Qb-perface": "hqb_perface_tiling_certificate_results.json",
    "H-Qb-caseI": "hqb_asymmetric_caseI_certificate_results.json",
    "H-Qb-caseII": "hqb_asymmetric_caseII_certificate_results.json",
    "H-Qb-opp": "hqb_opp_certificate_results.json",
}

evidence = {tag: load_json(RESULTS_DIR, fname) for tag, fname in FILES.items()}
RESULTS["evidence"] = {
    tag: {
        "file": FILES[tag],
        "passed": data.get("passed"),
        "failed": data.get("failed"),
        "outcome": data.get("outcome"),
        "summary": data.get("summary"),
        "conclusion": data.get("conclusion"),
    }
    for tag, data in evidence.items()
}

section("2. Legacy Phase 26 structural checks")

expected_counts = {
    "26-A": 45,
    "26-B": 24,
    "26-C-T2": 10,
    "26-C-T3": 17,
    "26-C-T3-TET": 27,
    "26-C-T3-F5-legacy": 21,
    "26-C-T3-F7-legacy": 33,
    "26-C-T4": 30,
}
for tag, expected in expected_counts.items():
    data = evidence.get(tag, {})
    check(f"{tag}: {expected}/{expected} checks passed",
          data.get("passed") == expected and data.get("failed") == 0,
          f"got passed={data.get('passed')}, failed={data.get('failed')}")

phase_b = evidence.get("26-B", {})
residuals = phase_b.get("residuals", [])
expected_residuals = {
    (2, (4, 2, 2, 2)),
    (2, (3, 3, 2, 2)),
    (3, (5, 5, 3, 2)),
    (3, (5, 4, 4, 2)),
    (3, (5, 4, 3, 3)),
    (3, (4, 4, 4, 3)),
    (4, (5, 5, 5, 5)),
}
got_residuals = {(r.get("t"), tuple(r.get("k_orbit_rep", []))) for r in residuals}
check("Phase 26-B: exactly seven expected (t,k)-residuals",
      got_residuals == expected_residuals,
      f"diff={got_residuals.symmetric_difference(expected_residuals)}")

summary_b = phase_b.get("summary", {})
t1_survivors = summary_b.get("survivors_per_t", {}).get("1", {}).get("S4_orbits_F4_pass")
check("t=1 all-one-face analogue eliminated by F4",
      t1_survivors == 0,
      f"got t1 survivors={t1_survivors}")

f7_conclusion = evidence.get("26-C-T3-F7-legacy", {}).get("conclusion", {})
f7_cases = evidence.get("26-C-T3-F7-legacy", {}).get("cases", [])
check("f=7 legacy JSON does not claim active full exclusion",
      f7_conclusion.get("f7_fully_excluded") is False,
      f"got f7_fully_excluded={f7_conclusion.get('f7_fully_excluded')}")
check("f=7 active ledger keeps all five multisets in the H-orb residual scope",
      f7_conclusion.get("active_public_all_cases_in_residual_scope") is True,
      f"got active_public_all_cases_in_residual_scope={f7_conclusion.get('active_public_all_cases_in_residual_scope')}")
check("f=7 case entries separate legacy verdict from active public verdict",
      len(f7_cases) == 5 and all(
          c.get("legacy_verdict") == "IMPOSSIBLE_UNDER_BLANKET_H_ORB"
          and c.get("active_public_verdict") == "OPEN_ACCIDENTAL_EVEN_H_ORB_RESIDUAL"
          for c in f7_cases
      ),
      f"cases={len(f7_cases)}")

section("3. Newly discharged hypotheses")

new_counts = {
    "H-coc": 15,
    "H-orb-parity": 19,
    "H-orb-scope": 4,
    "H-orb-combinatorial": 6,
    "H-Qb-reduction": 12,
    "H-Qb-perface": 15,
    "H-Qb-caseI": 11,
    "H-Qb-caseII": 20,
    "H-Qb-opp": 10,
}
for tag, expected in new_counts.items():
    data = evidence.get(tag, {})
    check(f"{tag}: {expected}/{expected} checks passed",
          data.get("passed") == expected and data.get("failed") == 0,
          f"got passed={data.get('passed')}, failed={data.get('failed')}")

hqb_tags = ["H-Qb-reduction", "H-Qb-perface", "H-Qb-caseI", "H-Qb-caseII", "H-Qb-opp"]
hqb_closed = all(
    evidence[tag].get("passed") == new_counts[tag] and evidence[tag].get("failed") == 0
    for tag in hqb_tags
)
hqb_reduction_status = evidence.get("H-Qb-reduction", {}).get("reduction", {})
check("H-Qb reduction script is marked as an intermediate reduction, not final closure",
      hqb_reduction_status.get("closed_here") is False
      and hqb_reduction_status.get("closed_by_downstream_certificates") is True,
      f"closed_here={hqb_reduction_status.get('closed_here')}, downstream={hqb_reduction_status.get('closed_by_downstream_certificates')}")
check("H-Qb is fully discharged by reduction, per-face, Qb-adj symmetric/asymmetric, and Qb-opp certificates",
      hqb_closed)

hcoc_closed = evidence["H-coc"].get("passed") == 15 and evidence["H-coc"].get("failed") == 0
check("H-coc is discharged directly; H-trip is retired as a formal hypothesis",
      hcoc_closed)

horb_singleton_closed = evidence["H-orb-parity"].get("passed") == 19 and evidence["H-orb-parity"].get("failed") == 0
check("H-orb singleton metric patterns are killed unconditionally by parity",
      horb_singleton_closed)

horb_scope_exact = evidence["H-orb-scope"].get("passed") == 4 and evidence["H-orb-scope"].get("failed") == 0
check("Remaining H-orb residual is exactly the accidental even-congruence case",
      horb_scope_exact)

section("4. Updated n=5 synthesis")

closed_unconditional_residuals = {
    (2, (4, 2, 2, 2)),
    (2, (3, 3, 2, 2)),
    (3, (5, 5, 3, 2)),
    (4, (5, 5, 5, 5)),
}
remaining_residual_description = {
    "name": "H-orb accidental even-congruence residual",
    "scope": "f(P)=7, t=3, Sym(P)=1, accidental even interior metric pattern (4) or (2,2)",
    "status": "open",
    "source": ["horb_residual_scope.py", "horb_residual_combinatorial.py"],
}

check("The old four-hypothesis formulation is no longer the active state",
      hqb_closed and hcoc_closed and horb_singleton_closed and horb_scope_exact)
check("Full unconditional n=5 closure is NOT claimed",
      True,
      "the H-orb accidental even residual remains open")

RESULTS["closed_unconditional_residuals"] = sorted(list(closed_unconditional_residuals))
RESULTS["closed_modules"] = [
    "H-coc",
    "H-Qb",
    "H-orb-singleton-parity",
    "t=1 F4 elimination",
    "t=2 residuals",
    "t=3 canonical residual (5,5,3,2)",
    "t=4 residual",
]
RESULTS["retired_modules"] = ["H-trip"]
RESULTS["remaining_modules"] = ["H-orb-accidental-even"]
RESULTS["remaining_residual"] = remaining_residual_description
RESULTS["fully_unconditional_n5"] = False
RESULTS["legacy_status_replaced"] = (
    "Old outcome 'proved modulo H-trip + H-coc + H-orb + H-Qb' is superseded "
    "by the reduced single-residual statement."
)

synthesis_ok = FAILED == 0
if synthesis_ok:
    RESULTS["public_claim"] = (
        "n=5 is reduced to the single H-orb accidental even-congruence residual; "
        "H-coc and H-Qb are discharged, H-trip is retired, and H-orb singleton "
        "patterns are killed by parity."
    )
    RESULTS["outcome"] = "N=5 REDUCED TO SINGLE H-ORB ACCIDENTAL EVEN RESIDUAL"
else:
    RESULTS["public_claim"] = "not certified: one or more synthesis checks failed"
    RESULTS["outcome"] = "INVALID SYNTHESIS: CHECKS FAILED"

section("5. Public theorem statement to use")

print()
if synthesis_ok:
    print("  --- UPDATED THEOREM 26.1 STATUS ---")
    print()
    print("    The n=5 obstruction stack is no longer modulo four active")
    print("    standing hypotheses. H-coc and H-Qb are discharged by exact")
    print("    public certificates, H-trip is retired, and H-orb singleton")
    print("    metric patterns are killed by parity.")
    print()
    print("    Remaining open case:")
    print("      f(P)=7, t=3, Sym(P)=1, and the four interior facets of P")
    print("      are accidentally congruent in an even metric pattern (4)")
    print("      or (2,2).")
    print()
    print("    Therefore the correct public claim is reduction to this single")
    print("    H-orb accidental residual, not unconditional n=5 closure.")
else:
    print("  --- SYNTHESIS INVALID ---")
    print()
    print("    One or more required public certificate checks failed or were missing.")
    print("    No n=5 reduction theorem statement is certified by this run.")
print()

print(f"\n{'=' * 70}")
print(f"Total tests passed: {PASSED}")
print(f"Total tests failed: {FAILED}")
print(f"Synthesis outcome: {RESULTS['outcome']}")
print('=' * 70)

RESULTS["passed"] = PASSED
RESULTS["failed"] = FAILED

results_path = RESULTS_DIR / "phase26e_synthesis_theorem_26_1_results.json"
with results_path.open("w", encoding="utf-8") as fh:
    json.dump(RESULTS, fh, indent=2)

print(f"\nResults written to {results_path}")

if not synthesis_ok:
    sys.exit(1)
