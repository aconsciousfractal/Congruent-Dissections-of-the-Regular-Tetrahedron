#!/usr/bin/env python3
"""Retired phase-26 synthesis marker.

The former phase-26 stack claimed an unrestricted n=5 reduction to one
accidental-even metric residual.  That wording is withdrawn: its boundary-role
and metric-prism steps were not established.  The old JSON is retained under
``results/historical/`` for auditability.  The active n=5 runner is
``scripts/run_all.py``.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results/phase26e_synthesis_theorem_26_1_results.json"
RESULT = {
    "status": "RETIRED_HISTORICAL",
    "theorem": "26.1 (former unrestricted n=5 residual reduction)",
    "outcome": "WITHDRAWN",
    "reason": [
        "the boundary-role homogeneity step was not established from congruence",
        "the triangular-prism metric shortcut was not established",
        "the setwise-to-pointwise facet-fixing step was not established",
    ],
    "active_replacement": "n5_brh_conditional_certificate.py",
    "public_claim": (
        "The former unrestricted single-residual reduction is retired. "
        "The active result is the conditional BRH obstruction."
    ),
}
OUT.write_text(json.dumps(RESULT, indent=2) + "\n", encoding="utf-8")
print("[RETIRED] The former unrestricted n=5 synthesis is withdrawn.")
print(f"Wrote {OUT}")
print("Use scripts/run_all.py for the active BRH-scoped checks.")
