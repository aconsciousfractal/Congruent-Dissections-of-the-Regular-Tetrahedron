# n = 5 Residual Status

## Active Public Claim

The public certificate stack reduces any putative face-to-face congruent dissection of the regular tetrahedron into 5 convex pieces to one open metric residual:

- `f(P) = 7`
- `t = 3`
- `Sym(P) = 1`
- the four interior facets of `P` are accidentally congruent in an even metric pattern `(4)` or `(2,2)`

This is not a full unconditional n = 5 impossibility theorem. The current theorem-level statement is exactly the reduction to this residual.

## Closed Branches

Closed unconditionally or by exact public certificates:

- `t = 1`: eliminated by the per-face area filter.
- `t = 2`: both residuals closed by canonical-multiset arithmetic.
- `t = 3`, residual `(5,5,3,2)`: closed by canonical-multiset arithmetic.
- `t = 3`, `f = 5`: closed by the quadrilateral-pyramid certificate stack.
- `t = 3`, `f = 7`, odd/singleton metric branches: closed by parity.
- `t = 3`, `f = 7`, genuine `(2,2)` orbit-transport branch: closed by the orientation certificate.
- `t = 4`: full-incidence residual closed unconditionally.

Still open:

- `t = 3`, `f = 7`, `Sym(P) = 1`, accidental even interior-facet congruence pattern `(4)` or `(2,2)`.

## Certificate Audit Map

The old H-labels are retained only as script/result audit labels. They are not the headline theorem statement.

| Audit label | Current status | Script(s) | Result JSON |
|---|---|---|---|
| H-trip | Retired; not a dependency of the public theorem | `phase26e_synthesis_theorem_26_1.py` | `results/phase26e_synthesis_theorem_26_1_results.json` |
| H-coc | Closed by the orientation-bit certificate | `hcoc_orientation_certificate.py` | `results/hcoc_orientation_certificate_results.json` |
| H-Qb | Closed by the quadrilateral-pyramid certificate stack | `hqb_reduction_certificate.py`, `hqb_perface_tiling_certificate.py`, `hqb_asymmetric_caseI_certificate.py`, `hqb_asymmetric_caseII_certificate.py`, `hqb_opp_certificate.py` | `results/hqb_*_results.json` |
| H-orb singleton/odd patterns | Closed by parity; no blanket orbit-detection assumption is used there | `horb_parity_certificate.py` | `results/horb_parity_certificate_results.json` |
| Metric residual scope (H-orb audit) | Narrowed to accidental even metric congruence | `horb_residual_scope.py`, `horb_residual_combinatorial.py` | `results/horb_residual_scope_results.json`, `results/horb_residual_combinatorial_results.json` |

## Reproduction

Run:

```bash
python scripts/run_all.py
```

Expected current synthesis outcome:

```text
N=5 REDUCED TO SINGLE ACCIDENTAL-EVEN METRIC RESIDUAL
```

The synthesis result is written to:

```text
results/phase26e_synthesis_theorem_26_1_results.json
```