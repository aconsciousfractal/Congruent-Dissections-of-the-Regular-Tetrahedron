# Reviewer Guide

This guide applies to the revised manuscript and repository as of 2026-09-20.

## Ten-minute path

1. Read the abstract in `paper/Congruent Dissections of the Regular
   Tetrahedron.pdf`: the n=5 result is conditional on BRH.
2. Read `CLAIM_LEDGER.md` and `PUBLIC_CLAIM_BOUNDARY.md`.
3. Run `PYTHONUTF8=1 python scripts/run_all.py`.

## Thirty-minute path

4. Read `docs/n5_residual_status.md` for the exact current frontier.
5. Read Definition BRH and `thm:n5` in Section 12.5 of the TeX source.
6. Inspect `scripts/n5_brh_conditional_certificate.py` and
   `scripts/n5_real_area_certificate.py`.
7. Treat `phase26*`, `hqb_*`, `horb_*`, and `hcoc_*` as historical audit
   material, not as an active unrestricted n=5 proof.

## Main claims

- Exact atlas and Dehn/refinement results for the eight historical
  representatives.
- Lagrange/divisor and Coxeter-pure statements with their stated scope.
- n=16 all-one-face exclusion under its explicit hypotheses.
- Conditional n=5 BRH obstruction, corrected area bookkeeping, and the local
  NN identity.

## Known limits

- BRH is not derived from congruence; mixed boundary roles remain open.
- Area incidence is not geometric realizability.
- No replay is independent specialist review or formal verification.
