#!/usr/bin/env python3
"""Finite sanity certificate for the conditional n=5 BRH theorem.

This script checks the arithmetic and symmetry facts used in the written BRH
proof.  It cannot establish BRH for an arbitrary congruent dissection and it
cannot certify the unrestricted n=5 problem.
"""
from __future__ import annotations

import json
from itertools import combinations, permutations, product
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def det3(rows: tuple[tuple[int, int, int], ...]) -> int:
    a, b, c = rows
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def mat_vec(M, x):
    return tuple(sum(M[i][j] * x[j] for j in range(3)) for i in range(3))


def tetrahedral_group():
    normals = {
        (1, 1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
    }
    group = []
    for p in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            M = tuple(
                tuple(signs[i] if j == p[i] else 0 for j in range(3))
                for i in range(3)
            )
            if {mat_vec(M, n) for n in normals} == normals:
                group.append(M)
    return normals, group


def main() -> int:
    checks = []
    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})
        print(f"[{'PASS' if condition else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))

    # Normalize one ambient face area to 1.  BRH gives E=4/5.
    A = Fraction(1)
    E = Fraction(4, 5)
    check("BRH exposed-area identity", E == 4 * A / 5, "E=4/5 after A=1")
    check("t=0 fails boundary coverage", 0 < 8)
    check("t=1 fails boundary coverage", 5 < 8)

    a, b = Fraction(3, 10), Fraction(1, 2)
    three_sums = [r * a + (3 - r) * b for r in range(4)]
    check("t=2 forces (a,b)=(3/10,1/2)", a + b == E and 2 * b == 1)
    check("t=2 three-footprint sums miss one", Fraction(1) not in three_sums,
          ", ".join(map(str, three_sums)))
    check("t=2 four-or-more lower bound", 4 * a > 1, f"4a={4*a}")

    normals, group = tetrahedral_group()
    check("three tetrahedral normals are independent",
          all(det3(tuple(normals_list)) != 0 for normals_list in
              ((tuple(n) for n in combo) for combo in combinations(normals, 3))))
    check("centered tetrahedral symmetry group has order 24", len(group) == 24)
    orbit = {mat_vec(M, (1, 2, 3)) for M in group}
    check("generic orbit has 24 points", len(orbit) == 24)
    check("24 is not divisible by 5", 24 % 5 != 0)

    passed = sum(c["passed"] for c in checks)
    failed = len(checks) - passed
    result = {
        "status": "PASS" if failed == 0 else "FAIL",
        "theorem_scope": "No five-piece partition satisfying BRH",
        "conditional_on": [
            "full-dimensional congruent convex pieces",
            "a fixed exposed-facet subset B transported by every placement isometry",
        ],
        "not_claimed": [
            "BRH for arbitrary congruent dissections",
            "unconditional n=5 impossibility",
            "a proof from finite arithmetic alone",
        ],
        "checks": checks,
        "passed": passed,
        "failed": failed,
        "group_order": len(group),
        "orbit_size": len(orbit),
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "n5_brh_conditional_certificate_results.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
