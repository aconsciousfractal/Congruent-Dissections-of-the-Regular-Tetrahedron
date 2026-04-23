"""
tests/test_tetrahedron.py — Basic tests for the canonical tetrahedron and known dissections.
"""
import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tetrahedron import (
    regular_tetrahedron, volume, tet_volume_from_vertices, distance_matrix
)
from dissections import dissect_n1, dissect_n2, dissect_n3, dissect_n24


def test_regular_tetrahedron_edge_lengths():
    """All 6 edges should have length 1."""
    A, B, C, D = regular_tetrahedron(1.0)
    dists = distance_matrix([A, B, C, D])
    assert all(abs(d - 1.0) < 1e-12 for d in dists), f"Edge lengths: {dists}"


def test_volume_unit():
    """Volume of unit-edge regular tetrahedron = sqrt(2)/12."""
    expected = np.sqrt(2) / 12
    assert abs(volume(1.0) - expected) < 1e-12


def test_volume_from_vertices():
    A, B, C, D = regular_tetrahedron(1.0)
    v = tet_volume_from_vertices(A, B, C, D)
    assert abs(v - volume(1.0)) < 1e-12


def test_dissect_n1():
    """n=1 produces 1 piece equal to T."""
    A, B, C, D = regular_tetrahedron()
    pieces = dissect_n1(A, B, C, D)
    assert len(pieces) == 1
    v = tet_volume_from_vertices(*pieces[0])
    assert abs(v - volume()) < 1e-12


def test_dissect_n2_volume():
    """n=2: two pieces, each with half the volume."""
    A, B, C, D = regular_tetrahedron()
    pieces = dissect_n2(A, B, C, D)
    assert len(pieces) == 2
    total = sum(tet_volume_from_vertices(*p) for p in pieces)
    assert abs(total - volume()) < 1e-12
    for p in pieces:
        v = tet_volume_from_vertices(*p)
        assert abs(v - volume() / 2) < 1e-10


def test_dissect_n2_congruence():
    """n=2: two pieces should be congruent (same sorted distance multiset)."""
    A, B, C, D = regular_tetrahedron()
    pieces = dissect_n2(A, B, C, D)
    d1 = distance_matrix(pieces[0])
    d2 = distance_matrix(pieces[1])
    assert np.allclose(d1, d2, atol=1e-12), f"Distance mismatch:\n{d1}\n{d2}"


def test_dissect_n3_volume():
    """n=3: three pieces summing to full volume."""
    A, B, C, D = regular_tetrahedron()
    pieces = dissect_n3(A, B, C, D)
    assert len(pieces) == 3
    total = sum(tet_volume_from_vertices(*p) for p in pieces)
    assert abs(total - volume()) < 1e-10


def test_dissect_n24_count():
    """n=24: should produce exactly 24 pieces."""
    A, B, C, D = regular_tetrahedron()
    pieces = dissect_n24(A, B, C, D)
    assert len(pieces) == 24


def test_dissect_n24_volume():
    """n=24: 24 pieces summing to full volume, each = Vol(T)/24."""
    A, B, C, D = regular_tetrahedron()
    pieces = dissect_n24(A, B, C, D)
    total = sum(tet_volume_from_vertices(*p) for p in pieces)
    assert abs(total - volume()) < 1e-10
    for i, p in enumerate(pieces):
        v = tet_volume_from_vertices(*p)
        assert abs(v - volume() / 24) < 1e-10, f"Piece {i}: vol={v}, expected={volume()/24}"


def test_dissect_n24_congruence():
    """n=24: all 24 orthoschemes should be congruent."""
    A, B, C, D = regular_tetrahedron()
    pieces = dissect_n24(A, B, C, D)
    ref = distance_matrix(pieces[0])
    for i, p in enumerate(pieces[1:], 1):
        dm = distance_matrix(p)
        assert np.allclose(ref, dm, atol=1e-10), \
            f"Piece {i} not congruent to piece 0:\n{dm}\nvs\n{ref}"
