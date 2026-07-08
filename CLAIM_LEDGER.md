# Claim Ledger

Companion documentation added 2026-07-08, after publication; it does not
modify the paper. Source locators refer to
`paper/Congruent Dissections of the Regular Tetrahedron.tex` (LaTeX labels
in parentheses). Levels: `theorem-in-paper`, `certified-finite` (exact
finite computation with regenerable certificate), `conditional`
(theorem under explicitly stated finite hypotheses), `open` (explicitly
not claimed).

| ID | Level | Statement (scoped) | Source locator | Evidence in repo |
| --- | --- | --- | --- | --- |
| C1 | theorem-in-paper + certified-finite | Exact atlas of the eight known congruent dissections of the regular tetrahedron, n ∈ {1,2,3,4,6,8,12,24}: canonical-coordinate reconstruction, symbolic Dehn-invariant verification, refinement relations; tetrahedrality of the eight historical representatives. | Abstract; `thm:univ-tet` | `scripts/dissections.py`, `scripts/dehn_verify_n24.py` (not part of `run_all.py`'s phase-26 pipeline; both run individually and verified passing 2026-07-08). |
| C2 | theorem-in-paper | Every atlas dissection is G_diss-transitive; Lagrange forces n dividing 24 FOR THE KNOWN TRANSITIVE FAMILY; full Td-invariance occurs only for n ∈ {1,12,24}. | Abstract; `cor:forward`, `lem:geom-vs-alg-stab` | Proof in paper; screening scripts. |
| C3 | theorem-in-paper | Disproof of the S6 → S12 refinement; cross-pipeline bridge and component structure as stated. | `thm:s6-s12-fail`, `thm:s2-bridge`, `prop:components` | Proof in paper with computational certificates. |
| C4 | theorem-in-paper | Burnside-ring, 24-cell, and IFS-grammar models realize every divisor of 24 and give a tested screening stack for Td-invariant orbit decompositions; slab argument and failure of divisor completeness for the cube as stated. | Abstract; `prop:slab`, `cor:cube-fail` | Proof in paper; model scripts. |
| C5 | conditional | n=16 all-one-face case is EXCLUDED UNDER TWO FINITE MILP HYPOTHESES; the exclusion is automatic (unconditional) in the Coxeter-pure instance. | Abstract; `thm:n16-aof-conditional` (two-hypothesis exclusion), `thm:n16-aof-coxeter` (unconditional Coxeter-pure instance) | Conditional theorem in paper; the two hypotheses are explicit. |
| C6 | certified-finite (reduction) | n=5: exact public certificates reduce any putative face-to-face convex congruent 5-dissection to ONE explicit open metric residual: f(P)=7, t=3, Sym(P)=1, accidental even congruence pattern (4) or (2,2) among the four interior facets. | Abstract; Sec. 12.5 (`sec:prog-n5`), computational certificate 12.16 (`thm:n5`); `docs/n5_residual_status.md` | `scripts/phase26*.py`, `scripts/hqb_*.py`, `scripts/horb_*.py`, `scripts/hcoc_orientation_certificate.py`; 46 tests green via `run_all.py` 2026-07-08; synthesis certificate `results/phase26e_synthesis_theorem_26_1_results.json`. |
| O1 | open | Unconditional n=5 impossibility. EXPLICITLY NOT CLAIMED; the public claim is the C6 reduction only. | Abstract ("No unconditional n=5 impossibility is claimed"); `docs/n5_residual_status.md` | — |
| O2 | open | Unconditional n=16 exclusion (without the two MILP hypotheses, outside the Coxeter-pure instance). Not claimed. | Abstract | — |

Repo history note: the repo already carries an n=5 red-team pass (commits
"Address n=5 red-team audit findings", "Polish n5 residual certificate
wording", 2026-06-30).
