"""Tests for energy and reversible gate models."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import numpy as np


def test_cmos_energy_basic():
    """CMOS energy = 1/2 C V^2."""
    from adiabatic_sim import cmos_energy
    assert abs(cmos_energy(1e-15, 1.0) - 0.5e-15) < 1e-30
    assert abs(cmos_energy(2e-15, 0.7) - 0.5 * 2e-15 * 0.49) < 1e-30


def test_adiabatic_scales_with_T():
    """Adiabatic energy decreases as 1/T above RC."""
    from adiabatic_sim import adiabatic_energy
    C, V, R = 1e-15, 0.7, 1e3
    E1 = adiabatic_energy(C, V, R, 1e-9)
    E2 = adiabatic_energy(C, V, R, 1e-8)
    assert E2 < E1
    assert abs(E2 / E1 - 0.1) < 1e-6


def test_adiabatic_floor_below_RC():
    """Below RC, adiabatic energy drops to CMOS level."""
    from adiabatic_sim import adiabatic_energy, cmos_energy
    C, V, R = 1e-15, 0.7, 1e3
    E_fast = adiabatic_energy(C, V, R, 1e-14)   # below RC = 1e-12
    E_cmos = cmos_energy(C, V)
    assert abs(E_fast - E_cmos) < 1e-30


def test_landauer_value():
    """Landauer limit at 300 K is ~2.87 zJ."""
    from adiabatic_sim import landauer_energy
    E = landauer_energy(300.0)
    assert 2.8e-21 < E < 2.9e-21


def test_landauer_scales_with_T():
    """Landauer = kT ln2."""
    from adiabatic_sim import landauer_energy
    assert abs(landauer_energy(600.0) / landauer_energy(300.0) - 2.0) < 1e-9


def test_fredkin_bijective():
    from adiabatic_sim import fredkin, is_bijective
    assert is_bijective(fredkin)


def test_toffoli_bijective():
    from adiabatic_sim import toffoli, is_bijective
    assert is_bijective(toffoli)


def test_fredkin_truth_table():
    from adiabatic_sim import fredkin
    # Fredkin with control=1 swaps
    assert fredkin((1, 0, 1)) == (1, 1, 0)
    assert fredkin((1, 1, 0)) == (1, 0, 1)
    # Control=0 does nothing
    assert fredkin((0, 1, 0)) == (0, 1, 0)


def test_toffoli_truth_table():
    from adiabatic_sim import toffoli
    # Both controls 1 -> flip target
    assert toffoli((1, 1, 0)) == (1, 1, 1)
    assert toffoli((1, 1, 1)) == (1, 1, 0)
    # Otherwise no-op
    assert toffoli((1, 0, 0)) == (1, 0, 0)
    assert toffoli((0, 1, 1)) == (0, 1, 1)
