# Congruent Dissections of the Regular Tetrahedron

Companion repository for the paper

> **Congruent Dissections of the Regular Tetrahedron**
> Oleksiy Babanskyy, 2026.

Contains the manuscript source, the experimental scripts used to produce
and cross-check every empirical claim, and the datasets those scripts
generated during the research phase.

## Layout

```
.
|-- paper/                       # LaTeX source (.tex) and checked-in PDF
|-- docs/
|   `-- n5_residual_status.md
|-- scripts/                     # Self-contained Python scripts
|   |-- tetrahedron.py           # canonical geometry primitives
|   |-- tetra_geom.py            # dihedral-angle / Dehn helpers
|   |-- dissections.py           # constructors for the 8 known dissections S_n
|   |-- independent_verifier.py  # Coxeter-pure S4-orbit verifier (15-family scope)
|   |-- dehn_verify_n24.py       # Listing 1 of Appendix A (Dehn scaling at n=24)
|   |-- phase26a_chamber_skeleton.py
|   |-- phase26b_role_distribution_n5.py
|   |-- phase26c_t2_residuals.py
|   |-- phase26c_t3_residuals.py
|   |-- phase26c_t3_tetrahedral_exclusion.py
|   |-- phase26c_t3_f5_exclusion.py
|   |-- hqb_reduction_certificate.py
|   |-- hqb_perface_tiling_certificate.py
|   |-- hqb_asymmetric_caseI_certificate.py
|   |-- hqb_asymmetric_caseII_certificate.py
|   |-- hqb_opp_certificate.py
|   |-- phase26c_t3_f7_exclusion.py
|   |-- hcoc_orientation_certificate.py
|   |-- horb_parity_certificate.py
|   |-- horb_residual_scope.py
|   |-- horb_residual_combinatorial.py
|   |-- phase26c_t4_full_incidence_residual.py
|   |-- phase26e_synthesis_theorem_26_1.py
|   |-- run_all.py               # one-command reproducer
|   `-- tests/
|       `-- test_tetrahedron.py
|-- results/                     # Pre-generated certificates (JSON)
|   |-- S6_to_S12_edge_spectrum.json
|   |-- phase26a_chamber_skeleton_results.json
|   |-- phase26b_role_distribution_n5_results.json
|   |-- phase26c_t2_residuals_results.json
|   |-- phase26c_t3_residuals_results.json
|   |-- phase26c_t3_tetrahedral_exclusion_results.json
|   |-- phase26c_t3_f5_exclusion_results.json
|   |-- hqb_reduction_certificate_results.json
|   |-- hqb_perface_tiling_certificate_results.json
|   |-- hqb_asymmetric_caseI_certificate_results.json
|   |-- hqb_asymmetric_caseII_certificate_results.json
|   |-- hqb_opp_certificate_results.json
|   |-- phase26c_t3_f7_exclusion_results.json
|   |-- hcoc_orientation_certificate_results.json
|   |-- horb_parity_certificate_results.json
|   |-- horb_residual_scope_results.json
|   |-- horb_residual_combinatorial_results.json
|   |-- phase26c_t4_full_incidence_residual_results.json
|   `-- phase26e_synthesis_theorem_26_1_results.json
|-- LICENSE                      # MIT
|-- requirements.txt
`-- .gitignore
```

## Dependencies

Python ≥ 3.10, `numpy ≥ 1.24`, `sympy ≥ 1.12`, `scipy ≥ 1.10`.

```bash
python -m venv .venv
.venv\Scripts\activate              # Windows
source .venv/bin/activate           # Linux / macOS
pip install -r requirements.txt
```

## Reproducing the paper

All scripts under `scripts/` are standalone (stdlib + numpy + sympy + scipy).
Each phase-26 / n=5 certificate script writes a `*_results.json` certificate
into `results/`, using exact rational arithmetic (`fractions.Fraction`) where
applicable.

### One-command reproduction

```bash
python scripts/run_all.py
```

Runs every active phase-26 / n=5 certificate and audit script in dependency order and
reports pass/fail per step. Total runtime is about 1-2 minutes on commodity hardware.

### Individual scripts

| Script | Role | Runtime |
|---|---|---|
| `phase26a_chamber_skeleton.py` | chamber-complex skeleton | < 5 s |
| `phase26b_role_distribution_n5.py` | role-distribution census for n = 5 (7 residuals) | < 5 s |
| `phase26c_t2_residuals.py` | both t = 2 residuals closed unconditionally | < 2 s |
| `phase26c_t3_residuals.py` | t = 3 parity reduction | < 5 s |
| `phase26c_t3_tetrahedral_exclusion.py` | t = 3 tetrahedral-component exclusion | < 5 s |
| `phase26c_t3_f5_exclusion.py` | f = 5 decomposition; quadrilateral-pyramid branch is discharged by `hqb_*` certificates | < 10 s |
| `hqb_reduction_certificate.py` | quadrilateral-pyramid reduction ledger | < 5 s |
| `hqb_perface_tiling_certificate.py` | quadrilateral-pyramid per-face tiling certificate | < 5 s |
| `hqb_asymmetric_caseI_certificate.py` | quadrilateral-pyramid asymmetric case I certificate | < 5 s |
| `hqb_asymmetric_caseII_certificate.py` | quadrilateral-pyramid asymmetric case II certificate | < 5 s |
| `hqb_opp_certificate.py` | quadrilateral-pyramid opposite-edge certificate | < 5 s |
| `phase26c_t3_f7_exclusion.py` | f = 7 audit ledger; active synthesis leaves accidental-even metric residual open | < 30 s |
| `hcoc_orientation_certificate.py` | orientation-bit certificate for the K5 transport branch | < 5 s |
| `horb_parity_certificate.py` | parity certificate for singleton/odd metric patterns | < 5 s |
| `horb_residual_scope.py` | exact remaining accidental-even metric scope | < 5 s |
| `horb_residual_combinatorial.py` | combinatorial non-closure of the residual | < 5 s |
| `phase26c_t4_full_incidence_residual.py` | t = 4 closed unconditionally | < 5 s |
| `phase26e_synthesis_theorem_26_1.py` | final synthesis (46 / 46 aggregated) | < 10 s |

### Auxiliary verification

```bash
python scripts/dehn_verify_n24.py          # Listing 1 (orthoscheme volume and edge spectrum)
python scripts/independent_verifier.py     # Coxeter-pure S4-orbit check (15-family scope)
pytest scripts/tests/                       # geometric primitives sanity
```

## Key paper results

- **Theorem 4.2** (edge spectrum) - the squared-edge multisets of the eight canonical pieces S_n fully determine n up to congruence.
- **Theorem 5.5** (transitivity of known dissections) - each S_n admits a congruence group acting transitively on pieces.
- **Conditional theorem 12.8** (n = 16 all-one-face) - L3 in the Coxeter-pure case; L2 under (H_roles) + (H_slot) in the general convex case.
- **Computational Certificate 12.16 (`thm:n5`) / phase26e synthesis status** (n = 5) - the public certificate stack reduces the first non-divisor of 24 to one open accidental-even metric residual. Full unconditional n = 5 closure is not claimed; see `docs/n5_residual_status.md`.
- **Lemma 12.2** (Stabiliser Transport, L2) - rigorous implication under a named auxiliary hypothesis.
- **Screening stack (Section 10)** - non-G_diss-transitive configurations for n not dividing 24 are ruled out up to an explicit T_d-maximality caveat (L1+).

The updated n = 5 status is in the TeX source `paper/Congruent Dissections of the Regular Tetrahedron.tex`, the regenerated checked-in PDF, and `docs/n5_residual_status.md`. If the TeX changes again, regenerate the PDF before merging or publishing this branch.

## Claim Boundary

Companion claim-discipline docs were added on 2026-07-08 (after
publication; the paper is unchanged):

- `CLAIM_LEDGER.md` — every claim with its level (theorem-in-paper,
  certified-finite, conditional, open) and paper locator.
- `PUBLIC_CLAIM_BOUNDARY.md` — what may and may not be quoted; in
  particular, n=5 is a certificate-backed REDUCTION to one open metric
  residual, never an impossibility claim.
- `README_REVIEWER.md` — 10/30-minute reviewer paths.
- `REPRODUCE.md` — one-command replay (`scripts/run_all.py`, ~40 s,
  46 tests, byte-identical certificate regeneration verified 2026-07-08).

## Citation

Babanskyy, O. (2026). *Congruent Dissections of the Regular Tetrahedron*.

## License

MIT — see [LICENSE](LICENSE).

## Contact

Issues and pull requests welcome.
