# Claim Ledger

This ledger applies to the revised public manuscript and companion artifacts
as of 2026-09-20.  Levels are `theorem-in-paper`, `certified-finite`,
`conditional`, and `open`.

| ID | Level | Statement (scoped) | Source locator | Evidence in repo |
| --- | --- | --- | --- | --- |
| C1 | theorem-in-paper + certified-finite | Exact atlas of the eight known congruent dissections of the regular tetrahedron, with canonical reconstruction, symbolic Dehn checks, and refinement relations. | Abstract; `thm:univ-tet` | `scripts/dissections.py`, `scripts/dehn_verify_n24.py` |
| C2 | theorem-in-paper | Every atlas dissection is `G_diss`-transitive; the Lagrange and full-`Td` statements have the scope stated in the paper. | Abstract; `cor:forward`, `lem:geom-vs-alg-stab` | Paper proof and atlas scripts |
| C3 | theorem-in-paper | The S6 -> S12 refinement is disproved, with the stated component structure. | `thm:s6-s12-fail`, `thm:s2-bridge`, `prop:components` | Paper proof and certificates |
| C4 | theorem-in-paper | Burnside-ring, 24-cell, and IFS models give the stated divisor/screening results within their declared scopes. | Abstract; `prop:slab`, `cor:cube-fail` | Paper proof and model scripts |
| C5 | conditional | The n=16 all-one-face case is excluded under the two named MILP hypotheses and unconditionally in the Coxeter-pure instance. | `thm:n16-aof-conditional`, `thm:n16-aof-coxeter` | Conditional theorem in paper |
| C6 | conditional | Under BRH, no five-piece partition exists. BRH fixes one set of reference facets whose images are exposed in every congruent copy. | `def:brh`, `thm:n5` | `scripts/n5_brh_conditional_certificate.py`; written proof |
| C7 | certified-finite + diagnostic | Under the common-role area model, the corrected real-area enumeration has six distinct positive multisets; the local NN identity holds in its specified coordinate chart. | Sec. 12.5; `n5_real_area_certificate.py`, `n5_nn_identity_certificate.py` | JSON results in `results/` |
| R1 | retired | The earlier claim that arbitrary five-piece dissections reduce to one accidental-even metric residual is withdrawn. Its boundary-role and metric-prism steps are not established. | Historical phase-26 section and results | `scripts/historical/` and `results/historical/`, excluded from `run_all.py` |
| O1 | open | Unconditional impossibility for five congruent convex face-to-face pieces, including mixed boundary roles. | `docs/n5_residual_status.md` | — |
| O2 | open | Unconditional n=16 exclusion outside the stated hypotheses. | Abstract; Section 12 | — |

Finite replay checks files and arithmetic.  It does not prove BRH, geometric
realizability of an area matrix, novelty, or independent review.
