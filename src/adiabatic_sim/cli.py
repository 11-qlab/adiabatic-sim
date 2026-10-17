"""Command-line interface for adiabatic-sim."""
import argparse
import json
import sys
from .energy import (
    cmos_energy, adiabatic_energy, landauer_energy,
    efficiency_vs_cmos, CMOS_PARAMS_7NM, CMOS_PARAMS_45NM,
)
from .reversible import fredkin, toffoli, is_bijective


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="adiabatic-sim",
        description="Compare CMOS, adiabatic, and reversible energy",
    )
    p.add_argument("--C", type=float, default=1e-15, help="Load capacitance (F)")
    p.add_argument("--V", type=float, default=0.7, help="Supply voltage (V)")
    p.add_argument("--R", type=float, default=1e3, help="On-resistance (Ohm)")
    p.add_argument("--T", type=float, default=1e-10,
                   help="Switching time (s)")
    p.add_argument("--sweep", action="store_true",
                   help="Sweep switching time and print EDP curve")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args(argv)

    E_cmos = cmos_energy(args.C, args.V)
    E_ad = adiabatic_energy(args.C, args.V, args.R, args.T)
    E_land = landauer_energy()
    ratio = efficiency_vs_cmos(args.C, args.V, args.R, args.T)

    result = {
        "C_F": args.C,
        "V_V": args.V,
        "R_Ohm": args.R,
        "T_s": args.T,
        "cmos_energy_J": E_cmos,
        "adiabatic_energy_J": E_ad,
        "landauer_J": E_land,
        "ratio_ad_cmos": ratio,
        "cmos_over_landauer": E_cmos / E_land,
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"CMOS energy       : {E_cmos*1e18:.3f} aJ")
    print(f"Adiabatic energy  : {E_ad*1e18:.3f} aJ")
    print(f"Landauer limit    : {E_land*1e21:.3f} zJ")
    print(f"Ratio (ad/CMOS)   : {ratio:.4f}")
    print(f"CMOS / Landauer   : {E_cmos/E_land:.0f}x")

    if args.sweep:
        print("\nSwitching time sweep:")
        print(f"{'T (ps)':>10} {'E_ad (aJ)':>12} {'ratio':>8} {'EDP (J*s)':>14}")
        for T_mult in (0.1, 1, 10, 100, 1000, 1e4):
            T_new = args.T * T_mult
            E_ad = adiabatic_energy(args.C, args.V, args.R, T_new)
            edp = E_ad * T_new
            print(f"{T_new*1e12:>10.1f} {E_ad*1e18:>12.3f} "
                  f"{E_ad/E_cmos:>8.4f} {edp:>14.3e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
