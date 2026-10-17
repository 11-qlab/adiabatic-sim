"""Adiabatic and reversible computing energy analysis.

Compare per-switch energy across:
  - CMOS: (1/2) C V^2
  - Adiabatic: (RC/T) C V^2
  - Reversible: kT ln2 limit (Landauer)

Plus reversible logic gates (Fredkin, Toffoli) and their
bijectivity checks.
"""
from .energy import (
    cmos_energy, adiabatic_energy, landauer_energy,
    efficiency_vs_cmos, energy_delay_product,
    CMOS_PARAMS_7NM, CMOS_PARAMS_45NM,
)
from .reversible import (
    fredkin, toffoli, is_bijective, truth_table,
)

__version__ = "0.1.0"
__all__ = [
    "cmos_energy", "adiabatic_energy", "landauer_energy",
    "efficiency_vs_cmos", "energy_delay_product",
    "CMOS_PARAMS_7NM", "CMOS_PARAMS_45NM",
    "fredkin", "toffoli", "is_bijective", "truth_table",
]
