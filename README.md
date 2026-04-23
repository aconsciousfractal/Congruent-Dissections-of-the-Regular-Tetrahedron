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
├── paper/                       # LaTeX source (.tex) and compiled PDF
├── scripts/                     # Self-contained Python scripts
│   ├── tetrahedron.py           #   canonical geometry primitives
│   ├── tetra_geom.py            #   dihedral-angle / Dehn helpers
│   ├── dissections.py           #   constructors for the 8 known dissections S_n
│   ├── independent_verifier.py  #   cross-verifier for Thm 5.5 (transitivity)
│   ├── dehn_verify_n24.py       #   Listing 1 of Appendix A (Dehn scaling at n=24)
│   ├── phase26a_chamber_skeleton.py
│   ├── phase26b_role_distribution_n5.py
│   ├── phase26c_t2_residuals.py
│   ├── phase26c_t3_residuals.py
│   ├── phase26c_t3_tetrahedral_exclusion.py
│   ├── phase26c_t3_f5_exclusion.py
│   ├── phase26c_t3_f7_exclusion.py
│   ├── phase26c_t4_full_incidence_residual.py
│   ├── phase26e_synthesis_theorem_26_1.py
│   ├── run_all.py               #   one-command reproducer
│   └── tests/
│       └── test_tetrahedron.py
├── results/                     # Pre-generated certificates (JSON)
│   ├── S6_to_S12_edge_spectrum.json          # Thm 7.1 (S_6 → S_12 disproof)
│   ├── phase26a_chamber_skeleton_results.json
│   ├── phase26b_role_distribution_n5_results.json
│   ├── phase26c_t2_residuals_results.json
│   ├── phase26c_t3_residuals_results.json
│   ├── phase26c_t3_tetrahedral_exclusion_results.json
│   ├── phase26c_t3_f5_exclusion_results.json
│   ├── phase26c_t3_f7_exclusion_results.json
│   ├── phase26c_t4_full_incidence_residual_results.json
│   └── phase26e_synthesis_theorem_26_1_results.json
├── LICENSE                      # MIT
├── requirements.txt
└── .gitignore
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
Each `phase26*` script writes a `*_results.json` certificate into `results/`
using exact rational arithmetic (`fractions.Fraction`).

### One-command reproduction

```bash
python scripts/run_all.py
```

Runs every phase-26 verification script in dependency order and reports
pass/fail per step.  Total runtime ≈ 1–2 minutes on commodity hardware.

### Individual scripts

| Script | Role | Runtime |
|---|---|---|
| `phase26a_chamber_skeleton.py` | chamber-complex skeleton | < 5 s |
| `phase26b_role_distribution_n5.py` | role-distribution census for n = 5 (7 residuals) | < 5 s |
| `phase26c_t2_residuals.py` | both t = 2 residuals closed unconditionally | < 2 s |
| `phase26c_t3_residuals.py` | t = 3 parity reduction | < 5 s |
| `phase26c_t3_tetrahedral_exclusion.py` | t = 3 tetrahedral-component exclusion | < 5 s |
| `phase26c_t3_f5_exclusion.py` | t = 3, f = 5 sub-case (21 / 21 passing) | < 10 s |
| `phase26c_t3_f7_exclusion.py` | t = 3, f = 7 sub-case, cocycle check (33 / 33 passing) | < 30 s |
| `phase26c_t4_full_incidence_residual.py` | t = 4 closed unconditionally | < 5 s |
| `phase26e_synthesis_theorem_26_1.py` | final synthesis (40 / 40 aggregated) | < 10 s |

### Auxiliary verification

```bash
python scripts/dehn_verify_n24.py          # Listing 1 (orthoscheme volume and edge spectrum)
python scripts/independent_verifier.py     # transitivity cross-check (Thm 5.5)
pytest scripts/tests/                       # geometric primitives sanity
```

## Key paper results

- **Theorem 4.2** (edge spectrum) — the squared-edge multisets of the eight canonical pieces S_n fully determine n up to congruence.
- **Theorem 5.5** (transitivity of known dissections) — each S_n admits a congruence group acting transitively on pieces.
- **Conditional theorem 12.8** (n = 16 all-one-face) — L3 in the Coxeter-pure case; L2 under (H_roles) + (H_slot) in the general convex case.
- **Conditional theorem 12.16** (n = 5) — the first non-divisor of 24 is conditionally reduced in the convex category, modulo four explicit finite standing hypotheses (H-trip), (H-coc), (H-orb), (H-Qb).  Four of the seven (t, k)-residuals close unconditionally; three invoke (H-orb) and (H-Qb) uniformly and (H-coc) on a single sub-case.
- **Lemma 12.2** (Stabiliser Transport, L2) — rigorous implication under a named auxiliary hypothesis.
- **Screening stack (§10)** — non-G_diss-transitive configurations for n ∤ 24 are ruled out up to an explicit T_d-maximality caveat (L1+).

See `paper/Congruent Dissections of the Regular Tetrahedron.pdf` for full statements, proofs, and the **Evidence-level glossary** (Appendix B) defining the six-level L0 / L1 / L1+ / L2 / L2+ / L3 tagging scheme used throughout.

## Citation

Babanskyy, O. (2026). *Congruent Dissections of the Regular Tetrahedron*.

## License

MIT — see [LICENSE](LICENSE).

## Contact

Issues and pull requests welcome.
