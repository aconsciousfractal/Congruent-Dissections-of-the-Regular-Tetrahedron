#!/usr/bin/env python3
"""
INDEPENDENT VERIFIER — Congruent Coxeter-pure partitions of the regular tetrahedron
===================================================================================

Zero-dependency on historical labels (S0..S16), merge maps, or identify() functions.
Only uses: chambers, adjacency, convexity, S₄ action, tiling test.

Question: how many S₄-orbit families of congruent-tiling-admissible convex 
connected chamber-unions exist?

Expected: 15 S4-orbit families in the Coxeter-pure companion scope.
This is not the count of the eight historical representative dissections in
the main atlas.
"""

import sys

import numpy as np
from itertools import permutations, combinations
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ══════════════════════════════════════════════════════════════
#  1. BUILD THE COXETER COMPLEX (24 chambers of the regular tetrahedron)
# ══════════════════════════════════════════════════════════════

A = np.array([0.0, 0.0, 0.0])
B = np.array([1.0, 0.0, 0.0])
C = np.array([0.5, np.sqrt(3)/2, 0.0])
D = np.array([0.5, np.sqrt(3)/6, np.sqrt(2.0/3.0)])
VERTS = [A, B, C, D]
GT = sum(VERTS) / 4

FACES = [(0,1,2), (0,1,3), (0,2,3), (1,2,3)]

# Each chamber = orthoscheme (vertex, edge_midpoint, face_centroid, body_centroid)
# Flag = (vertex_index, edge_as_sorted_pair, face_as_sorted_triple)
chamber_pts = []
flags = []
for face in FACES:
    Gf = (VERTS[face[0]] + VERTS[face[1]] + VERTS[face[2]]) / 3
    for edge in combinations(face, 2):
        Me = (VERTS[edge[0]] + VERTS[edge[1]]) / 2
        for v in edge:
            chamber_pts.append([VERTS[v], Me, Gf, GT])
            flags.append((v, tuple(sorted(edge)), tuple(sorted(face))))

N = len(flags)
assert N == 24, f"Expected 24 chambers, got {N}"
flag_to_idx = {flags[i]: i for i in range(N)}

# ══════════════════════════════════════════════════════════════
#  2. S₄ ACTION ON CHAMBERS (the geometric action via vertex permutation)
# ══════════════════════════════════════════════════════════════

S4_elements = list(permutations(range(4)))
# For each σ ∈ S₄, σ sends flag (v, e, f) to (σ(v), σ(e), σ(f))
chamber_perm = {}
for sigma in S4_elements:
    perm = []
    for i in range(N):
        v, e, f = flags[i]
        new_flag = (sigma[v],
                    tuple(sorted(sigma[x] for x in e)),
                    tuple(sorted(sigma[x] for x in f)))
        perm.append(flag_to_idx[new_flag])
    chamber_perm[sigma] = tuple(perm)

# Verify: action is faithful (24 distinct permutations)
assert len(set(chamber_perm.values())) == 24, "S₄ action is not faithful!"

# ══════════════════════════════════════════════════════════════
#  3. SIGN-PATTERN ENCODING & ADJACENCY
# ══════════════════════════════════════════════════════════════

EDGES = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
plane_normals = []
plane_offsets = []
for a, b in EDGES:
    opp = sorted(set(range(4)) - {a, b})
    M = (VERTS[opp[0]] + VERTS[opp[1]]) / 2
    n = np.cross(VERTS[b] - VERTS[a], M - VERTS[a])
    n = n / np.linalg.norm(n)
    # Canonical sign
    for i in range(3):
        if abs(n[i]) > 1e-8:
            if n[i] < 0: n = -n
            break
    plane_normals.append(n)
    plane_offsets.append(n @ VERTS[a])

centroids = [np.mean(pts, axis=0) for pts in chamber_pts]
sign_patterns = [
    tuple(1 if c @ plane_normals[j] - plane_offsets[j] >= 0 else -1 for j in range(6))
    for c in centroids
]
sign_to_idx = {s: i for i, s in enumerate(sign_patterns)}

# Adjacency: Hamming distance 1 in sign space
adj = [[] for _ in range(N)]
for i in range(N):
    for j in range(i+1, N):
        if sum(a != b for a, b in zip(sign_patterns[i], sign_patterns[j])) == 1:
            adj[i].append(j)
            adj[j].append(i)

# Verify: chamber graph is 3-regular with 36 edges
total_edges = sum(len(a) for a in adj) // 2
assert all(len(a) == 3 for a in adj), "Chamber graph is not 3-regular!"
assert total_edges == 36, f"Expected 36 edges, got {total_edges}"

# ══════════════════════════════════════════════════════════════
#  4. CONVEXITY AND CONNECTIVITY TESTS
# ══════════════════════════════════════════════════════════════

def is_connected(subset):
    """BFS connectivity test on the chamber adjacency graph."""
    if len(subset) <= 1:
        return True
    s = set(subset)
    start = next(iter(s))
    visited = {start}
    queue = [start]
    while queue:
        u = queue.pop(0)
        for v in adj[u]:
            if v in s and v not in visited:
                visited.add(v)
                queue.append(v)
    return len(visited) == len(subset)

def is_convex(subset):
    """Halfspace-convexity: subset = intersection of reflecting halfspaces."""
    s = set(subset)
    active = []
    for j in range(6):
        vals = {sign_patterns[i][j] for i in subset}
        if len(vals) == 1:
            active.append((j, vals.pop()))
    # Intersection of active halfspaces
    closure = set()
    for i in range(N):
        if all(sign_patterns[i][j] == sv for j, sv in active):
            closure.add(i)
    return closure == s

# ══════════════════════════════════════════════════════════════
#  5. S₄-ORBIT COMPUTATION (pure, no historical labels)
# ══════════════════════════════════════════════════════════════

def s4_orbit(subset_frozenset):
    """Compute the full S₄-orbit of a chamber-subset."""
    orbit = set()
    for sigma in S4_elements:
        perm = chamber_perm[sigma]
        image = frozenset(perm[c] for c in subset_frozenset)
        orbit.add(image)
    return orbit

def orbit_canonical(subset_frozenset):
    """Return the lexicographically smallest member of the S₄-orbit."""
    best = None
    for sigma in S4_elements:
        perm = chamber_perm[sigma]
        image = tuple(sorted(perm[c] for c in subset_frozenset))
        if best is None or image < best:
            best = image
    return best

# ══════════════════════════════════════════════════════════════
#  6. CONGRUENT TILING TEST (does subset tile the tetrahedron?)
# ══════════════════════════════════════════════════════════════

def tiles_tetrahedron(subset_frozenset):
    """
    Test if there exist n = 24/k translates (by S₄ elements) that 
    partition all 24 chambers with no overlap.
    Uses bitmask backtracking.
    """
    k = len(subset_frozenset)
    if 24 % k != 0:
        return False
    n_pieces = 24 // k
    
    # Precompute all distinct translates as bitmasks
    unique_masks = {}
    for sigma in S4_elements:
        perm = chamber_perm[sigma]
        mask = 0
        for c in subset_frozenset:
            mask |= (1 << perm[c])
        if mask not in unique_masks:
            unique_masks[mask] = sigma
    masks = list(unique_masks.keys())
    full = (1 << 24) - 1
    
    def backtrack(covered, depth):
        if depth == n_pieces:
            return covered == full
        # Find first uncovered bit
        bit = 0
        tmp = covered
        while tmp & 1:
            tmp >>= 1
            bit += 1
        for mask in masks:
            if not (mask & (1 << bit)):
                continue
            if mask & covered:
                continue
            if backtrack(covered | mask, depth + 1):
                return True
        return False
    
    return backtrack(0, 0)

# ══════════════════════════════════════════════════════════════
#  7. MAIN ENUMERATION
# ══════════════════════════════════════════════════════════════

print("=" * 72)
print("  INDEPENDENT VERIFIER — S₄-orbit families of Coxeter partitions")
print("  No historical labels. Pure computation from chambers + S₄ action.")
print("=" * 72)

# Enumerate all convex connected k-subsets for each divisor of 24
# (plus k=5 as control)
K_VALUES = [1, 2, 3, 4, 5, 6, 8, 12, 24]

all_families = []  # (k, canonical_rep, orbit_size, tiles)

for k in K_VALUES:
    print(f"\n{'─'*60}")
    print(f"  k = {k}  (n = {24//k if 24 % k == 0 else 'N/A'})")
    print(f"{'─'*60}")
    
    # Enumerate convex connected subsets
    convex_subsets = set()
    if k == 24:
        convex_subsets.add(frozenset(range(24)))
    else:
        for combo in combinations(range(24), k):
            fs = frozenset(combo)
            if is_connected(combo) and is_convex(combo):
                convex_subsets.add(fs)
    
    print(f"  Convex connected subsets: {len(convex_subsets)}")
    
    # Group by S₄-orbit
    seen_canonicals = set()
    orbits = []
    for subset in convex_subsets:
        canon = orbit_canonical(subset)
        if canon not in seen_canonicals:
            orb = s4_orbit(subset)
            for member in orb:
                seen_canonicals.add(orbit_canonical(member))
            
            # Tiling test
            can_tile = tiles_tetrahedron(subset)
            
            orbits.append({
                'canonical': canon,
                'orbit_size': len(orb),
                'tiles': can_tile,
            })
    
    # Sort orbits
    orbits.sort(key=lambda o: (not o['tiles'], -o['orbit_size']))
    
    tiling_count = sum(1 for o in orbits if o['tiles'])
    non_tiling = sum(1 for o in orbits if not o['tiles'])
    
    print(f"  S₄-orbits: {len(orbits)} total")
    print(f"    Tiling-admissible: {tiling_count}")
    if non_tiling:
        print(f"    Non-tiling:        {non_tiling}")
    
    for i, o in enumerate(orbits):
        tile_str = "✓ TILES" if o['tiles'] else "✗ no tiling"
        print(f"    [{i}] orbit_size={o['orbit_size']:2d}, {tile_str}, rep={o['canonical']}")
        all_families.append((k, o['canonical'], o['orbit_size'], o['tiles']))

# ══════════════════════════════════════════════════════════════
#  8. SUMMARY
# ══════════════════════════════════════════════════════════════

print(f"\n{'═'*72}")
print(f"  SUMMARY")
print(f"{'═'*72}")

tiling_families = [(k, c, s, t) for k, c, s, t in all_families if t]
non_tiling = [(k, c, s, t) for k, c, s, t in all_families if not t]

print(f"\n  TILING-ADMISSIBLE S₄-ORBIT FAMILIES: {len(tiling_families)}")
print(f"  {'k':>3}  {'orbit_size':>10}  representative")
for k, canon, sz, _ in sorted(tiling_families):
    print(f"  {k:3d}  {sz:10d}  {canon}")

if non_tiling:
    print(f"\n  NON-TILING CONVEX ORBITS: {len(non_tiling)}")
    for k, canon, sz, _ in sorted(non_tiling):
        print(f"  {k:3d}  {sz:10d}  {canon} (k∤24)" if 24 % k != 0 else f"  {k:3d}  {sz:10d}  {canon}")

# Current-scope comparison
expected_coxeter_pure = 15
historical_atlas_representatives = 8
status = "match" if len(tiling_families) == expected_coxeter_pure else "DIFF"
print("\n  CURRENT-SCOPE CHECK")
print(f"    Coxeter-pure companion target: {expected_coxeter_pure} S4-orbit families")
print(f"    This run:                       {len(tiling_families)} S4-orbit families")
print(f"    Status:                         {status}")
print(f"    Main-paper historical atlas:    {historical_atlas_representatives} representative n-values")
print("    Scope note: this script verifies Coxeter-pure chamber-union families;")
print("    it is not a count of the historical atlas representatives.")

# ------------------------------------------------------------------------
#  9. CONTACT VECTORS (independent of historical labels)
# ══════════════════════════════════════════════════════════════

print(f"\n{'═'*72}")
print(f"  CONTACT VECTORS FOR ALL TILING FAMILIES")
print(f"{'═'*72}")

def contact_vector(subset):
    """Compute (n_V, n_M, n_F) contact with tetrahedron boundary."""
    pts = set()
    for ci in subset:
        for v in chamber_pts[ci]:
            pts.add(tuple(np.round(v, 10)))
    nV = nM = nF = 0
    for p in pts:
        pa = np.array(p)
        if min(np.linalg.norm(pa - v) for v in VERTS) < 1e-8:
            nV += 1
        elif np.linalg.norm(pa - GT) < 1e-8:
            continue  # body centroid
        else:
            is_mid = any(np.linalg.norm(pa - (VERTS[i]+VERTS[j])/2) < 1e-8
                        for i in range(4) for j in range(i+1, 4))
            if is_mid:
                nM += 1
            else:
                nF += 1
    return (nV, nM, nF)

print(f"\n  {'#':>2}  {'k':>2}  {'|Orb|':>5}  {'(nV,nM,nF)':>10}  representative")
idx = 0
for k, canon, sz, tiles in sorted(all_families):
    if not tiles:
        continue
    idx += 1
    cv = contact_vector(frozenset(canon))
    print(f"  {idx:2d}  {k:2d}  {sz:5d}  ({cv[0]},{cv[1]},{cv[2]}){' ':>5}  {canon}")

# ══════════════════════════════════════════════════════════════
#  10. ORDER-DUALITY TEST (which pairs are related by P ↔ P*?)
# ══════════════════════════════════════════════════════════════

print(f"\n{'═'*72}")
print(f"  ORDER-DUALITY ANALYSIS (w₀-conjugation)")
print(f"{'═'*72}")

# The longest element w₀ of S₄ is the reverse permutation (3,2,1,0)
w0 = (3, 2, 1, 0)
w0_perm = chamber_perm[w0]

print(f"\n  w₀ = {w0} (longest element of S₄)")
print(f"  w₀ acts on chambers by: chamber_perm[w₀]")

# For each tiling family, compute w₀ * orbit_canonical
# If it maps to the same orbit → self-dual
# If it maps to a different orbit → dual pair
tiling_canons = {}
for k, canon, sz, tiles in all_families:
    if tiles:
        tiling_canons[canon] = (k, sz)

print(f"\n  Duality mapping:")
dual_pairs = []
self_dual = []
seen = set()

for canon, (k, sz) in sorted(tiling_canons.items()):
    if canon in seen:
        continue
    # Apply w₀
    w0_image = frozenset(w0_perm[c] for c in canon)
    w0_canon = orbit_canonical(w0_image)
    
    if w0_canon == canon:
        self_dual.append((k, canon, sz))
        seen.add(canon)
        print(f"    k={k:2d}  {canon}  →  SELF-DUAL")
    elif w0_canon in tiling_canons:
        dual_pairs.append((k, canon, w0_canon, sz))
        seen.add(canon)
        seen.add(w0_canon)
        print(f"    k={k:2d}  {canon}  ↔  {w0_canon}  (DUAL PAIR)")
    else:
        print(f"    k={k:2d}  {canon}  →  {w0_canon}  (w₀-image NOT in tiling families!?)")
        seen.add(canon)

print(f"\n  Self-dual families:  {len(self_dual)}")
print(f"  Dual pairs:          {len(dual_pairs)}")
print(f"  Extended families (modulo duality): {len(self_dual) + len(dual_pairs)}")
print(f"  (= {len(self_dual)} self-dual + {len(dual_pairs)} pairs = "
      f"{len(self_dual) + len(dual_pairs)} total)")

print(f"\n{'═'*72}")
print(f"  VERDICT")
print(f"{'═'*72}")
print(f"\n  True S₄-orbit families:              {len(tiling_families)}")
print(f"  Extended families (mod w₀-duality):   {len(self_dual) + len(dual_pairs)}")
print(f"  Coxeter-pure companion target:        15")
print(f"  Main-paper historical atlas values:   8")
if len(tiling_families) != expected_coxeter_pure:
    sys.exit(1)
