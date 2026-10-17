"""Reversible computing primitives.

Fredkin gate: controlled-SWAP, 3-input 3-output, bijective.
Toffoli gate: doubly-controlled-NOT, 3-input 3-output, bijective.

Both are logically reversible: every output configuration
corresponds to exactly one input.  Information is never erased,
so no Landauer kT ln2 penalty per gate.

Energy advantage: reversible gates can in principle be run
arbitrarily slowly with arbitrarily small dissipation (only
leakage remains).
"""
from __future__ import annotations
import numpy as np


def fredkin(inputs):
    """Fredkin gate: if inputs[0] == 1, swap inputs[1] and inputs[2]."""
    a, b, c = inputs
    if a:
        return (a, c, b)
    return (a, b, c)


def toffoli(inputs):
    """Toffoli gate: if inputs[0] and inputs[1] are 1, flip inputs[2]."""
    a, b, c = inputs
    if a and b:
        return (a, b, 1 - c)
    return (a, b, c)


def is_bijective(gate_fn, n_inputs=3):
    """Check if a 3-input gate is bijective."""
    seen = set()
    for i in range(2 ** n_inputs):
        bits = tuple((i >> k) & 1 for k in range(n_inputs))
        out = gate_fn(bits)
        if out in seen:
            return False
        seen.add(out)
    return len(seen) == 2 ** n_inputs


def truth_table(gate_fn, n_inputs=3):
    """Print truth table as a list of (input, output) tuples."""
    rows = []
    for i in range(2 ** n_inputs):
        bits = tuple((i >> k) & 1 for k in range(n_inputs))
        rows.append((bits, gate_fn(bits)))
    return rows


def reversible_energy(T_room=300.0):
    """Per-gate energy in the reversible limit.

    In principle, reversible gates can dissipate arbitrarily
    little.  In practice, leakage through the gate's energy
    landscape sets a floor.  We use the Landauer limit as a
    lower bound and note that real devices are 10-1000x above it.
    """
    k_B = 1.380649e-23
    return k_B * T_room * np.log(2)


if __name__ == "__main__":
    print("=== Reversible gates ===\n")

    print("Fredkin truth table:")
    for inp, out in truth_table(fredkin):
        print(f"  {inp} -> {out}")
    print(f"  Bijective: {is_bijective(fredkin)}\n")

    print("Toffoli truth table:")
    for inp, out in truth_table(toffoli):
        print(f"  {inp} -> {out}")
    print(f"  Bijective: {is_bijective(toffoli)}\n")

    print(f"Landauer limit per erased bit: {reversible_energy()*1e21:.2f} zJ")
