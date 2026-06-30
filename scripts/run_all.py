"""
run_all.py - One-command reproducer for the paper

    "Congruent Dissections of the Regular Tetrahedron"
    Babanskyy, 2026.

Runs every public phase-26 / n=5 certificate script in dependency order.
Each script regenerates its JSON certificate under results/; this runner
fails if any script exits non-zero. It is a deterministic reproducer, not a
separate committed-baseline diff checker.

Usage:
    python scripts/run_all.py
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
RESULTS = ROOT / "results"

# Dependency order: 26-A (chamber skeleton) -> 26-B (role census)
# -> 26-C (all residuals) -> 26-E (synthesis, reads all prior JSONs).
PIPELINE = [
    "phase26a_chamber_skeleton.py",
    "phase26b_role_distribution_n5.py",
    "phase26c_t2_residuals.py",
    "phase26c_t3_residuals.py",
    "phase26c_t3_tetrahedral_exclusion.py",
    "phase26c_t3_f5_exclusion.py",
    "hqb_reduction_certificate.py",
    "hqb_perface_tiling_certificate.py",
    "hqb_asymmetric_caseI_certificate.py",
    "hqb_asymmetric_caseII_certificate.py",
    "hqb_opp_certificate.py",
    "phase26c_t3_f7_exclusion.py",
    "hcoc_orientation_certificate.py",
    "horb_parity_certificate.py",
    "horb_residual_scope.py",
    "horb_residual_combinatorial.py",
    "phase26c_t4_full_incidence_residual.py",
    "phase26e_synthesis_theorem_26_1.py",
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
    if not RESULTS.exists():
        RESULTS.mkdir(parents=True, exist_ok=True)
    total = 0.0
    for name in PIPELINE:
        ok, dt = run_script(name)
        total += dt
        if not ok:
            print(f"\n[FAIL] {name} exited non-zero")
            return 1
        print(f"[ok] {name}  ({dt:.2f}s)")
    print(f"\n{'=' * 70}\nAll {len(PIPELINE)} scripts passed in {total:.2f}s\n{'=' * 70}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
