"""Energy dissipation models: CMOS vs adiabatic switching.

Conventional CMOS inverter:
    E_CMOS = (1/2) C V^2       per switch (irreversible, dissipated)

Adiabatic charging (slow ramp):
    E_adiabatic = (RC / T) C V^2    (dissipated during ramp)

The adiabatic energy scales as 1/T and vanishes as the switching
time T becomes long compared to the RC time constant.  This is
the entire argument for reversible computing: slow = efficient.

Adiabaticity factor alpha (from the literature):
    alpha = 128  -> irreversible (fast switching)
    alpha = 0    -> fully reversible (infinitely slow)
"""
from __future__ import annotations
import numpy as np


# Physical constants
k_B = 1.380649e-23       # J/K
hbar = 1.054571817e-34   # J·s
e = 1.602176634e-19      # C
T_room = 300.0           # K


def cmos_energy(C, V):
    """Conventional CMOS switching energy: (1/2) C V^2."""
    return 0.5 * C * V ** 2


def adiabatic_energy(C, V, R, T_switch):
    """Adiabatic charging energy: (RC/T) C V^2.

    Valid when T_switch >> RC.  In the fast-switching limit
    (T_switch << RC), energy approaches the CMOS value.
    """
    tau = R * C
    if T_switch < tau:
        return cmos_energy(C, V)
    return (tau / T_switch) * 0.5 * C * V ** 2


def landauer_energy(T=T_room):
    """Landauer limit: k_B T ln 2 per bit erased."""
    return k_B * T * np.log(2)


def energy_delay_product(C, V, R, T_switch):
    """Return (energy, delay, EDP) for a given technology."""
    E = adiabatic_energy(C, V, R, T_switch)
    return E, T_switch, E * T_switch


def optimal_switch_time(C, V, R, E_min=None):
    """Find the switching time that minimizes EDP for adiabatic logic.

    EDP(T) = (RC/T) C V^2 * T = RC^2 V^2   -- constant!
    The EDP is independent of T in the adiabatic regime.
    Below RC, the EDP grows as T decreases.
    """
    tau = R * C
    # EDP is flat above tau, so any T >= tau gives the same EDP.
    return tau


def efficiency_vs_cmos(C, V, R, T_switch):
    """Ratio of adiabatic energy to CMOS energy."""
    E_cmos = cmos_energy(C, V)
    E_ad = adiabatic_energy(C, V, R, T_switch)
    return E_ad / E_cmos


# ============================================================
# Concrete parameter set from modern CMOS
# ============================================================
CMOS_PARAMS_7NM = {
    "C_load": 1e-15,         # 1 fF gate capacitance
    "V_dd": 0.7,             # 0.7 V supply
    "R_on": 1e3,             # 1 kOhm on-resistance
    "T_switch_ns": 0.1,      # 100 ps typical gate delay
}

CMOS_PARAMS_45NM = {
    "C_load": 2e-15,         # 2 fF
    "V_dd": 1.0,
    "R_on": 2e3,
    "T_switch_ns": 0.2,
}


if __name__ == "__main__":
    print("=== Energy per switch: CMOS vs adiabatic ===\n")

    p = CMOS_PARAMS_7NM
    C, V, R = p["C_load"], p["V_dd"], p["R_on"]
    T = p["T_switch_ns"] * 1e-9

    E_cmos = cmos_energy(C, V)
    E_ad = adiabatic_energy(C, V, R, T)

    print(f"Parameters: C={C*1e15:.1f} fF, V={V} V, R={R} Ohm, T={T*1e12:.0f} ps")
    print(f"CMOS energy       : {E_cmos*1e18:.2f} aJ")
    print(f"Adiabatic energy  : {E_ad*1e18:.2f} aJ")
    print(f"Ratio (ad/CMOS)   : {E_ad/E_cmos:.4f}")
    print(f"Landauer limit    : {landauer_energy()*1e21:.2f} zJ")
    print(f"CMOS / Landauer   : {E_cmos/landauer_energy():.0f}x")
    print()
    print("Slower switching:")
    for T_mult in (1, 10, 100, 1000):
        T_new = T * T_mult
        E_new = adiabatic_energy(C, V, R, T_new)
        print(f"  T={T_new*1e12:>8.1f} ps : E = {E_new*1e18:>8.3f} aJ  "
              f"(ratio {E_new/E_cmos:.4f})")
