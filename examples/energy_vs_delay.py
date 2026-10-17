"""Plot energy vs switching time for CMOS, adiabatic, Landauer."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from adiabatic_sim import (
    cmos_energy, adiabatic_energy, landauer_energy,
    CMOS_PARAMS_7NM,
)

p = CMOS_PARAMS_7NM
C, V, R = p["C_load"], p["V_dd"], p["R_on"]
tau = R * C

E_cmos = cmos_energy(C, V)
E_land = landauer_energy()

T = np.logspace(-13, -5, 300)   # 0.1 ps to 10 us
E_ad = np.array([adiabatic_energy(C, V, R, t) for t in T])

fig, ax = plt.subplots(figsize=(9, 5))
ax.loglog(T * 1e12, np.full_like(T, E_cmos * 1e18),
          'r--', lw=2, label=r"CMOS: $\frac{1}{2}CV^2$")
ax.loglog(T * 1e12, E_ad * 1e18, 'b-', lw=2,
          label=r"Adiabatic: $\frac{RC}{T}\cdot\frac{1}{2}CV^2$")
ax.loglog(T * 1e12, np.full_like(T, E_land * 1e18),
          'g:', lw=2, label=r"Landauer: $k_BT\ln 2$")
ax.axvline(tau * 1e12, color='gray', ls=':', lw=1, label=r"$\tau=RC$")

ax.set_xlabel("Switching time (ps)")
ax.set_ylabel("Energy per switch (aJ)")
ax.set_title(f"Energy per switch: CMOS vs adiabatic\n"
             f"C={C*1e15:.0f} fF, V={V} V, R={R:.0f} $\\Omega$")
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="lower left", fontsize=9)
ax.set_ylim(1e-8, 1e3)

out = os.path.join(os.path.dirname(__file__), "energy_vs_delay.png")
plt.tight_layout()
plt.savefig(out, dpi=140)
print(f"wrote {out}")
print()
print(f"CMOS energy       : {E_cmos*1e18:.3f} aJ")
print(f"Landauer limit    : {E_land*1e18:.8f} aJ")
print(f"CMOS / Landauer   : {E_cmos/E_land:.0f}x")
print()
for T_val in (1e-9, 1e-6):
    E = adiabatic_energy(C, V, R, T_val)
    print(f"Adiabatic at T={T_val*1e12:>6.0f} ps: "
          f"{E*1e18:.8f} aJ  ({E_cmos/E:.0f}x below CMOS)")
