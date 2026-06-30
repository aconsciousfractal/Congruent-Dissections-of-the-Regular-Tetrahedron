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
|   `-- n5_hypothesis_discharge_status.md
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

Runs every public phase-26 / n=5 certificate script in dependency order and
reports pass/fail per step.  Total runtime ≈ 1–2 minutes on commodity hardware.

### Individual scripts

| Script | Role | Runtime |
|---|---|---|
| `phase26a_chamber_skeleton.py` | chamber-complex skeleton | < 5 s |
| `phase26b_role_distribution_n5.py` | role-distribution census for n = 5 (7 residuals) | < 5 s |
| `phase26c_t2_residuals.py` | both t = 2 residuals closed unconditionally | < 2 s |
| `phase26c_t3_residuals.py` | t = 3 parity reduction | < 5 s |
| `phase26c_t3_tetrahedral_exclusion.py` | t = 3 tetrahedral-component exclusion | < 5 s |
| `phase26c_t3_f5_exclusion.py` | legacy f = 5 decomposition; Qb now discharged by `hqb_*` certificates | < 10 s |
| `hqb_reduction_certificate.py` | H-Qb reduction ledger | < 5 s |
| `hqb_perface_tiling_certificate.py` | H-Qb per-face tiling certificate | < 5 s |
| `hqb_asymmetric_caseI_certificate.py` | H-Qb asymmetric case I certificate | < 5 s |
| `hqb_asymmetric_caseII_certificate.py` | H-Qb asymmetric case II certificate | < 5 s |
| `hqb_opp_certificate.py` | H-Qb opposite-edge certificate | < 5 s |
| `phase26c_t3_f7_exclusion.py` | legacy f = 7 closure under blanket H-orb/H-coc assumptions | < 30 s |
| `hcoc_orientation_certificate.py` | direct H-coc orientation-bit discharge | < 5 s |
| `horb_parity_certificate.py` | H-orb singleton/odd-pattern parity discharge | < 5 s |
| `horb_residual_scope.py` | exact remaining H-orb accidental-even scope | < 5 s |
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

- **Theorem 4.2** (edge spectrum) — the squared-edge multisets of the eight canonical pieces S_n fully determine n up to congruence.
- **Theorem 5.5** (transitivity of known dissections) — each S_n admits a congruence group acting transitively on pieces.
- **Conditional theorem 12.8** (n = 16 all-one-face) — L3 in the Coxeter-pure case; L2 under (H_roles) + (H_slot) in the general convex case.
- **Conditional Theorem 12.16 (`thm:n5`) / phase26e synthesis status** (n = 5) - the public certificate stack now reduces the first non-divisor of 24 to one open H-orb accidental-even residual. H-coc and H-Qb are discharged by exact scripts, H-trip is retired, and H-orb singleton/odd patterns are killed by parity. Full unconditional n = 5 closure is not claimed; see `docs/n5_hypothesis_discharge_status.md`.
- **Lemma 12.2** (Stabiliser Transport, L2) — rigorous implication under a named auxiliary hypothesis.
- **Screening stack (§10)** — non-G_diss-transitive configurations for n ∤ 24 are ruled out up to an explicit T_d-maximality caveat (L1+).

The updated n = 5 status is in the TeX source `paper/Congruent Dissections of the Regular Tetrahedron.tex`, the regenerated checked-in PDF, and `docs/n5_hypothesis_discharge_status.md`. If the TeX changes again, regenerate the PDF before merging or publishing this branch.

## Citation

Babanskyy, O. (2026). *Congruent Dissections of the Regular Tetrahedron*.

## License

MIT — see [LICENSE](LICENSE).

## Contact

Issues and pull requests welcome.
