#!/usr/bin/env python3
"""Exact real-area incidence enumeration for the revised n=5 section.

The output is necessary area bookkeeping under a common-role model.  It is not
an enumeration of geometric dissections and is not used to claim unrestricted
n=5 impossibility.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESIDUALS = {
    "t2_(4,2,2,2)": (2, (4, 2, 2, 2)),
    "t2_(3,3,2,2)": (2, (3, 3, 2, 2)),
    "t3_(5,5,3,2)": (3, (5, 5, 3, 2)),
    "t3_(5,4,4,2)": (3, (5, 4, 4, 2)),
    "t3_(5,4,3,3)": (3, (5, 4, 3, 3)),
    "t3_(4,4,4,3)": (3, (4, 4, 4, 3)),
}
EXPECTED = {
    "t2_(4,2,2,2)": (),
    "t2_(3,3,2,2)": (),
    "t3_(5,5,3,2)": (),
    "t3_(5,4,4,2)": ((F(6), F(12), F(30)),),
    "t3_(5,4,3,3)": (
        (F(6), F(15), F(27)), (F(6), F(18), F(24)),
        (F(48, 5), F(84, 5), F(108, 5)), (F(12), F(12), F(24)),
    ),
    "t3_(4,4,4,3)": (
        (F(6), F(18), F(24)), (F(12), F(12), F(24)), (F(12), F(16), F(20)),
    ),
}


def compositions(total: int, length: int):
    if length == 1:
        return [(total,)]
    out = []
    def rec(rem, prefix):
        if len(prefix) == length - 1:
            out.append(tuple(prefix + [rem]))
            return
        for value in range(rem + 1):
            rec(rem - value, prefix + [value])
    rec(total, [])
    return out


def matrices_with_margins(k, t):
    options = [compositions(value, t) for value in k]
    for rows in product(*options):
        if all(sum(rows[row][col] for row in range(4)) == 5 for col in range(t)):
            yield rows


def rref_solve(A, b, nvars):
    M = [[F(x) for x in row] + [F(rhs)] for row, rhs in zip(A, b)]
    row = 0
    pivots = []
    for col in range(nvars):
        pivot = next((i for i in range(row, len(M)) if M[i][col]), None)
        if pivot is None:
            continue
        M[row], M[pivot] = M[pivot], M[row]
        q = M[row][col]
        M[row] = [x / q for x in M[row]]
        for i in range(len(M)):
            if i != row and M[i][col]:
                q = M[i][col]
                M[i] = [M[i][j] - q * M[row][j] for j in range(nvars + 1)]
        pivots.append(col)
        row += 1
    if any(all(M[i][j] == 0 for j in range(nvars)) and M[i][-1] for i in range(len(M))):
        return "none", None
    if len(pivots) < nvars:
        return "free", None
    sol = [F(0)] * nvars
    for i, col in enumerate(pivots):
        sol[col] = M[i][-1]
    return "unique", tuple(sol)


def main() -> int:
    result = {"status": "PASS", "model": "common-role real-area incidence", "residuals": {}}
    total_matrices = 0
    total_free = 0
    for name, (t, k) in RESIDUALS.items():
        counts = {"count_matrices": 0, "unique_solved_matrices": 0, "free_solution_families": 0}
        positive = set()
        for matrix in matrices_with_margins(k, t):
            counts["count_matrices"] += 1
            status, solution = rref_solve(list(matrix) + [[1] * t], [60] * 4 + [48], t)
            if status == "free":
                counts["free_solution_families"] += 1
            elif status == "unique":
                counts["unique_solved_matrices"] += 1
                if all(value > 0 for value in solution):
                    positive.add(tuple(sorted(solution)))
        total_matrices += counts["count_matrices"]
        total_free += counts["free_solution_families"]
        expected = EXPECTED[name]
        observed = tuple(sorted(positive))
        ok = observed == tuple(sorted(expected)) and counts["free_solution_families"] == 0
        result["residuals"][name] = {
            **counts,
            "positive_area_multisets": [[str(v) for v in values] for values in observed],
            "expected_match": ok,
        }
        print(f"[{ 'PASS' if ok else 'FAIL'}] {name}: {len(observed)} positive multisets")
        if not ok:
            result["status"] = "FAIL"
    result["total_matrices"] = total_matrices
    result["total_free_solution_families"] = total_free
    result["distinct_positive_multisets"] = len({tuple(v) for item in result["residuals"].values() for v in item["positive_area_multisets"]})
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "n5_real_area_certificate_results.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Total matrices: {total_matrices}; free families: {total_free}")
    print(f"Wrote {out}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
