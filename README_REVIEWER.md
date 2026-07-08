# Reviewer Guide

Companion documentation added 2026-07-08, after publication; it does not
modify the paper.

## Ten-Minute Path

1. Read the abstract in
   `paper/Congruent Dissections of the Regular Tetrahedron.pdf` — note the
   last paragraph: the n=5 result is a certificate-backed REDUCTION, not an
   impossibility claim.
2. Read `CLAIM_LEDGER.md` (C1-C6 plus the two explicitly-open rows O1/O2).
3. Run the one-command replay:
   `PYTHONUTF8=1 python scripts/run_all.py`
   (~40 s; expects "Total tests passed: 46", "All 18 scripts passed").

## Thirty-Minute Path

4. Read `docs/n5_residual_status.md` — the exact statement of the open
   metric residual (f(P)=7, t=3, Sym(P)=1, accidental even pattern).
5. Compare the synthesis certificate
   `results/phase26e_synthesis_theorem_26_1_results.json` with
   computational certificate 12.16 (`thm:n5`) in Sec. 12.5 of the paper.
6. Spot-check one certificate chain, e.g.
   `scripts/hqb_reduction_certificate.py` →
   `results/` JSON → the corresponding paper lemma.
7. Read `PUBLIC_CLAIM_BOUNDARY.md` for what may and may not be quoted.

## Main Claims

- Exact atlas of the 8 known dissections with Dehn verification (C1).
- Lagrange n | 24 for the known transitive family; Td-invariance only for
  n ∈ {1,12,24} (C2).
- S6 → S12 refinement disproved (C3).
- n=16 all-one-face excluded under two finite MILP hypotheses (C5,
  conditional).
- n=5 reduced to a single explicit open metric residual (C6) — and
  explicitly NOT closed (O1).

## Known Limits

- The n=5 residual is open; no impossibility statement exists.
- The n=16 exclusion is conditional outside the Coxeter-pure instance.
- Certificates regenerate deterministically; the 2026-07-08 replay
  reproduced tracked JSONs byte-identically.
