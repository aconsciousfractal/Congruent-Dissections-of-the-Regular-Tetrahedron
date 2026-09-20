# Reproduce

This guide describes the revised public source, PDF, active scripts, and
results as of 2026-09-20.

## Environment

Python 3.10+ with `numpy`, `sympy`, `scipy`, and `pytest`:

```bash
pip install -r requirements.txt
```

Set `PYTHONUTF8=1` on Windows if the console does not display the symbols in
the atlas scripts.

## Active replay

```bash
PYTHONUTF8=1 python scripts/run_all.py
```

The active runner executes:

- `n5_brh_conditional_certificate.py` — finite BRH arithmetic and symmetry
  sanity checks;
- `n5_real_area_certificate.py` — corrected exact common-role area census;
- `n5_nn_identity_certificate.py` — local polynomial identity;
- `dehn_verify_n24.py` — orthoscheme volume/Dehn scaling skeleton;
- `independent_verifier.py` — independent Coxeter-pure S4-orbit check.

The runner intentionally excludes the historical phase-26/H-Qb/H-orb/H-coc
reduction chain.  Those files remain for auditability, but their former
unrestricted n=5 synthesis is retired.  Running the former synthesis script
produces a `RETIRED_HISTORICAL` marker; its pre-rewrite JSON is kept under
`results/historical/`.

## Expected observations

The BRH script reports 10 finite checks and group/orbit data
`|H|=24`, `|Hx|=24`, `24 mod 5 != 0`.  The area script reports 3,461 incidence
matrices, no free positive families, and six distinct positive multisets.  The
NN script reports zero polynomial remainder.  The atlas scripts finish with
`OK` and 15 Coxeter-pure orbit families.

These observations support the stated conditional theorem and bookkeeping
only.  They do not prove BRH for arbitrary placements, geometric realizability
of an area matrix, or the unrestricted n=5 problem.

## Unit tests

```bash
PYTHONUTF8=1 python -m pytest scripts/tests -q
```

The tests cover the canonical tetrahedron primitives and the eight historical
atlas constructors.  They are separate from the active n=5 proof-support
runner.
