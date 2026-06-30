# n = 5 Hypothesis Discharge Status

This repository no longer uses the old four-hypothesis statement as the active public status for the n = 5 convex programme.

## Active Public Claim

The n = 5 obstruction stack is reduced to one open residual:

- `f(P) = 7`
- `t = 3`
- `Sym(P) = 1`
- the four interior facets of `P` are accidentally congruent in an even metric pattern `(4)` or `(2,2)`

This is not a full unconditional n = 5 impossibility theorem. The correct statement is a reduction to the H-orb accidental-even residual.

## Closed Or Retired Modules

| Module | Public status | Script(s) | Result JSON |
|---|---|---|---|
| H-trip | Retired; no longer an active formal hypothesis | `phase26e_synthesis_theorem_26_1.py` | `results/phase26e_synthesis_theorem_26_1_results.json` |
| H-coc | Closed directly by the orientation-bit certificate | `hcoc_orientation_certificate.py` | `results/hcoc_orientation_certificate_results.json` |
| H-Qb | Closed by the Qb reduction/per-face/asymmetric/opposite certificate stack | `hqb_reduction_certificate.py`, `hqb_perface_tiling_certificate.py`, `hqb_asymmetric_caseI_certificate.py`, `hqb_asymmetric_caseII_certificate.py`, `hqb_opp_certificate.py` | `results/hqb_*_results.json` |
| H-orb singleton/odd patterns | Closed by parity, without blanket H-orb | `horb_parity_certificate.py` | `results/horb_parity_certificate_results.json` |
| H-orb residual scope | Narrowed exactly to accidental even patterns | `horb_residual_scope.py`, `horb_residual_combinatorial.py` | `results/horb_residual_scope_results.json`, `results/horb_residual_combinatorial_results.json` |

## Residual Ledger

Closed unconditionally or by discharged certificates:

- `t = 1`: eliminated by the per-face area filter.
- `t = 2`: both residuals closed by canonical-multiset arithmetic.
- `t = 3`, residual `(5,5,3,2)`: closed by canonical-multiset arithmetic.
- `t = 3`, `f = 5`: Qb is no longer a standing hypothesis; the `hqb_*` stack discharges it.
- `t = 3`, `f = 7`, genuine orbit/odd-singleton branches: H-coc and parity close the previous named branches.
- `t = 4`: full-incidence residual closed unconditionally.

Still open:

- `t = 3`, `f = 7`, `Sym(P) = 1`, accidental even interior-facet congruence pattern `(4)` or `(2,2)`.

## Reproduction

Run:

```bash
python scripts/run_all.py
```

Expected current synthesis outcome:

```text
N=5 REDUCED TO SINGLE H-ORB ACCIDENTAL EVEN RESIDUAL
```

The synthesis result is written to:

```text
results/phase26e_synthesis_theorem_26_1_results.json
```
