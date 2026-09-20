# n = 5 status

## Active public result

The previous public claim that every arbitrary five-piece congruent dissection
reduces to one accidental-even metric residual is withdrawn.  Its first step
quietly required the same exposed facet roles in every congruent copy, and its
triangular-prism and setwise-facet shortcuts did not establish the needed
metric statements.

The active theorem is instead conditional:

> If a reference polytope has a fixed facet subset `B` whose images are exactly
the boundary facets of every one of the five copies (BRH), then no such
partition exists.

The proof uses:

- boundary area to exclude `t=0,1,2` exposed facets;
- transport of three tetrahedral face normals and zero translation for `t=3,4`;
- a generic 24-point orbit of the centered tetrahedral symmetry group, giving
  `24 = 5m`, a contradiction.

No face-to-face hypothesis is needed for this conditional obstruction, although
face-to-face remains part of the ambient programme elsewhere.

## Corrected finite bookkeeping

Under the weaker common-role area model (`A=60`, `E=48`), exact rational
enumeration gives six distinct positive multisets:

- `t=2`: none for `(4,2,2,2)` and `(3,3,2,2)`;
- `t=3`, `(5,5,3,2)`: none;
- `t=3`, `(5,4,4,2)`: `(6,12,30)`;
- `t=3`, `(5,4,3,3)`: `(6,15,27)`, `(6,18,24)`,
  `(48/5,84/5,108/5)`, `(12,12,24)`;
- `t=3`, `(4,4,4,3)`: `(6,18,24)`, `(12,12,24)`, `(12,16,20)`.

The rational list is valid at the incidence level.  The aligned matrix in the
paper is a bookkeeping witness, not a geometric tiling.

## Local result

The class-6 NN 012/021 chart satisfies an exact polynomial identity forcing
`A_floor/A_total=3/4` for positive-area solutions.  Since the common-role list
has maximum ratio `30/48=5/8`, that chart is locally excluded.  The chart does
not cover all class-6 branches or mixed boundary roles.

## Open frontier

The unrestricted convex five-piece problem, including the face-to-face case,
remains open.  The
next structural task is to classify variable boundary-role subsets `B_i` and
show either that a class of mixed roles is impossible or that some class
forces BRH.  The historical phase-26 scripts and JSON files are retained as
an audit trail but are not active evidence for this frontier.
