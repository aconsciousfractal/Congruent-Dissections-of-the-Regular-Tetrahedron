# Congruent Dissections of the Regular Tetrahedron

Companion repository for the paper

> **Congruent Dissections of the Regular Tetrahedron**
> Oleksiy Babanskyy, 2026.

This repository contains the canonical manuscript source and PDF, the public
atlas checks, and a deliberately scoped set of n=5 certificates.  The current
n=5 theorem is conditional on boundary-role homogeneity (BRH).  The
unrestricted five-piece problem remains open.

## Layout

```
.
|-- paper/                       # LaTeX source and checked-in PDF
|-- docs/
|   `-- n5_residual_status.md    # current public n=5 boundary
|-- scripts/
|   |-- n5_brh_conditional_certificate.py
|   |-- n5_real_area_certificate.py
|   |-- n5_nn_identity_certificate.py
|   |-- dehn_verify_n24.py
|   |-- independent_verifier.py
|   |-- run_all.py                # active one-command reproducer
|   |-- tetrahedron.py, tetra_geom.py, dissections.py
|   |-- tests/                    # atlas geometry tests
|   `-- historical/              # retired n=5 audit scripts
|-- results/                     # deterministic JSON certificates
|   |-- n5_brh_conditional_certificate_results.json
|   |-- n5_real_area_certificate_results.json
|   |-- n5_nn_identity_certificate_results.json
|   `-- historical/              # former results, retained inactive
|-- CLAIM_LEDGER.md
|-- PUBLIC_CLAIM_BOUNDARY.md
|-- REPRODUCE.md
|-- LICENSE
`-- requirements.txt
```

The former phase-26, H-Qb, H-orb and H-coc scripts are retained under
`scripts/historical/` so that the previous n=5 programme remains auditable.
They are explicitly retired from the active proof chain; their old
single-residual synthesis must not be quoted as a theorem.  The guard
`scripts/phase26e_synthesis_theorem_26_1.py` writes a
`RETIRED_HISTORICAL` marker, and all former result JSONs are under
`results/historical/`.

## Dependencies

Python >= 3.10, `numpy >= 1.24`, `sympy >= 1.12`, `scipy >= 1.10`, and
`pytest >= 8.0`.

```bash
python -m venv .venv
.venv\Scripts\activate              # Windows
source .venv/bin/activate              # Linux / macOS
pip install -r requirements.txt
```

## Current n=5 result

Under BRH, the paper proves that no five-piece partition exists.  BRH means
that one fixed subset of facets of a reference piece has images equal to the
facets exposed on the boundary in every copy.  The proof is an area argument
for one or two exposed facets and a tetrahedral-symmetry orbit argument for
three or four.  BRH is an additional hypothesis; congruence alone does not
supply it.

Files under `scripts/historical/` and `results/historical/` are audit material,
not active evidence.  Only the checks listed in `scripts/run_all.py` support
the current public claim.

The exact real-area certificate records the six positive common-role area
multisets, including the rational witness
`(48/5, 84/5, 108/5)`.  These are incidence-level necessary data, not geometric
dissections.  The NN script verifies one local polynomial identity in a
specified coordinate chart.  Neither computation settles the unrestricted
case.

## Reproducing the active checks

```bash
PYTHONUTF8=1 python scripts/run_all.py
```

The runner executes five active checks:

1. the finite arithmetic and symmetry checks used by the BRH proof;
2. the corrected exact real-area enumeration (3,461 incidence matrices);
3. the local NN polynomial identity;
4. the $n=24$ orthoscheme volume/Dehn skeleton;
5. the independent Coxeter-pure S4-orbit verifier.

It does not run the historical phase-26 reduction chain.  Run the atlas unit
tests separately:

```bash
PYTHONUTF8=1 python -m pytest scripts/tests -q
```

## Main paper results

- **Dehn-invariant certificate** (Section 4, `thm:dehn-values`) for the eight
  historical pieces.
- **Transitivity certificate** (Section 7, `thm:transitivity`) for the atlas
  family, with its stated scope.
- **S6 -> S12 disproof** and the refinement relations in the atlas.
- **n=16 all-one-face exclusion** under the two named hypotheses, and
  unconditionally in the Coxeter-pure instance.
- **n=5 BRH conditional theorem** (`thm:n5`), with exact area bookkeeping and
  a local chart check.  Unrestricted n=5 remains open.

## Claim boundary and review path

- `CLAIM_LEDGER.md` records every public claim and its level.
- `PUBLIC_CLAIM_BOUNDARY.md` states what may and may not be quoted.
- `README_REVIEWER.md` gives a short reader path.
- `REPRODUCE.md` records the active commands and their limits.

No script, replay, or local audit is an independent specialist review or a
formal verification of the geometric BRH implication.

## Citation

Babanskyy, O. (2026). *Congruent Dissections of the Regular Tetrahedron*.

## License

MIT — see [LICENSE](LICENSE).

## Contact

Issues and pull requests welcome.
