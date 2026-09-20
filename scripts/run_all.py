"""One-command reproducer for the active public checks.

The historical phase-26 n=5 reduction scripts remain in this repository for
auditability, but they are retired from the active proof chain because their
boundary-role and metric-prism steps were not established.  The active runner
therefore executes the conditional BRH certificate, the corrected exact
real-area enumeration, the local NN identity, and the two independent atlas
checks.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PIPELINE = [
    "n5_brh_conditional_certificate.py",
    "n5_real_area_certificate.py",
    "n5_nn_identity_certificate.py",
    "dehn_verify_n24.py",
    "independent_verifier.py",
]


def run_script(name: str) -> tuple[bool, float]:
    script = SCRIPTS / name
    print(f"\n{'=' * 70}\n>>> {name}\n{'=' * 70}")
    t0 = time.perf_counter()
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    dt = time.perf_counter() - t0
    sys.stdout.write(proc.stdout)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        return False, dt
    return True, dt


def main() -> int:
    total = 0.0
    for name in PIPELINE:
        ok, dt = run_script(name)
        total += dt
        if not ok:
            print(f"\n[FAIL] {name} exited non-zero")
            return 1
        print(f"[ok] {name} ({dt:.2f}s)")
    print(f"\n{'=' * 70}")
    print(f"All {len(PIPELINE)} active checks passed in {total:.2f}s")
    print("Scope: conditional BRH theorem support plus atlas/area diagnostics;")
    print("unrestricted n=5 impossibility is not claimed.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
