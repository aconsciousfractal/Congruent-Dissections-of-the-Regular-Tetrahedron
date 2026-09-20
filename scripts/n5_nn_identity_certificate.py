#!/usr/bin/env python3
"""Verify the local class-6 NN first-factor polynomial identity."""
from __future__ import annotations

import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def main() -> int:
    x, y, z, L = sp.symbols("x y z L")
    Qp = x**2 - x*y + y**2
    Qr = z**2 - z + 1
    B = x**2 + x*y + y**2 - (z**2 + z + 1)
    D = x*y - z
    A_floor = D + 2 * L * Qp + Qr / (6 * L)
    A_total = A_floor + B + D
    E_lambda = Qr - 12 * L**2 * Qp
    E_axis = Qp * (4 - (6 * L - 1)**2) - 12 * B
    identity = sp.factor(
        24 * L * (A_floor - sp.Rational(3, 4) * A_total)
        - (2 * L * E_axis + (1 - 6 * L) * E_lambda)
    )
    passed = identity == 0
    result = {
        "status": "PASS" if passed else "FAIL",
        "identity_zero": passed,
        "identity_remainder": str(identity),
        "scope": "class-6 NN 012/021 coordinate chart only",
        "not_claimed": ["global n=5 closure", "all class-6 branches", "mixed boundary roles"],
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / "n5_nn_identity_certificate_results.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"[{'PASS' if passed else 'FAIL'}] polynomial identity remainder = {identity}")
    print(f"Wrote {out}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
