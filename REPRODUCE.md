# Reproduce

Companion documentation added 2026-07-08, after publication; it does not
modify the paper.

## Environment

- Python 3.11+ with `numpy`, `sympy` (`pip install -r requirements.txt`).
- On Windows, set `PYTHONUTF8=1` (scripts print Unicode symbols).
- Exact rational/symbolic arithmetic throughout; no floating-point
  tolerance decisions in certificates.

## One-Command Replay (verified 2026-07-08)

```bash
PYTHONUTF8=1 python scripts/run_all.py
```

Runs every public phase-26 / n=5 certificate script in dependency order and
regenerates the JSON certificates under `results/`. Observed output
(2026-07-08, excerpt):

```text
Total tests passed: 46
Total tests failed: 0
Synthesis outcome: N=5 REDUCED TO SINGLE ACCIDENTAL-EVEN METRIC RESIDUAL
All 18 scripts passed in 39.45s
```

The regenerated JSON certificates were byte-identical to the tracked files
in `results/` on the 2026-07-08 run (deterministic reproducer; verified via
clean `git status` after the run).

## Selected Individual Checks

```bash
PYTHONUTF8=1 python scripts/dehn_verify_n24.py        # Listing 1 of Appendix A (Dehn scaling at n=24)
PYTHONUTF8=1 python scripts/independent_verifier.py   # Coxeter-pure S4-orbit verifier (15-family scope)
PYTHONUTF8=1 python -m pytest scripts/tests -q        # unit tests for geometry primitives
```

These three commands are NOT part of `run_all.py`'s pipeline (which
covers the phase-26 / n=5 certificate set). All three were run separately
and verified passing on 2026-07-08.
