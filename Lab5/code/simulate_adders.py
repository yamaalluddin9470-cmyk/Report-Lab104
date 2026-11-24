"""Simulator experiments for Lab 5: Half Adder, Full Adder, and 2-bit RCA."""
import csv
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(parents=True, exist_ok=True)
SIM = AerSimulator()
SHOTS = 1024


def run(qc):
    return SIM.run(qc, shots=SHOTS).result().get_counts()


def half_adder(a, b):
    qc = QuantumCircuit(4, 4)
    if a: qc.x(0)
    if b: qc.x(1)
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.ccx(0, 1, 3)
    for q in range(4): qc.measure(q, q)
    return run(qc)


def full_adder(a, b, cin):
    qc = QuantumCircuit(5, 2)
    if a: qc.x(0)
    if b: qc.x(1)
    if cin: qc.x(2)
    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.cx(2, 3)
    qc.ccx(0, 1, 4)
    qc.ccx(0, 2, 4)
    qc.ccx(1, 2, 4)
    qc.measure(3, 0)  # Sum
    qc.measure(4, 1)  # Carry-out
    return run(qc)


def ripple_2bit(a, b):
    # q0=A0, q1=A1, q2=B0, q3=B1, q4=Sum0, q5=Sum1,
    # q6=carry between bits, q7=final carry.
    qc = QuantumCircuit(8, 3)
    if a & 1: qc.x(0)
    if (a >> 1) & 1: qc.x(1)
    if b & 1: qc.x(2)
    if (b >> 1) & 1: qc.x(3)
    qc.cx(0, 4)
    qc.cx(2, 4)
    qc.ccx(0, 2, 6)
    qc.cx(1, 5)
    qc.cx(3, 5)
    qc.cx(6, 5)
    qc.ccx(1, 3, 7)
    qc.ccx(1, 6, 7)
    qc.ccx(3, 6, 7)
    qc.measure(4, 0)  # Sum0
    qc.measure(5, 1)  # Sum1
    qc.measure(7, 2)  # final carry
    return run(qc)


def write_rows(path, rows, headers):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)


half_rows = []
for a, b in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    counts = half_adder(a, b)
    state, count = max(counts.items(), key=lambda item: item[1])
    half_rows.append({"a": a, "b": b, "expected_state": ["0000", "0110", "0101", "1011"][(a << 1) | b], "state": state, "count": count, "probability_percent": round(100 * count / SHOTS, 3)})
write_rows(OUT / "half_adder_simulation.csv", half_rows, half_rows[0].keys())

full_rows = []
for a in (0, 1):
    for b in (0, 1):
        for cin in (0, 1):
            counts = full_adder(a, b, cin)
            state, count = max(counts.items(), key=lambda item: item[1])
            carry = 1 if (a*b + a*cin + b*cin) else 0
            expected = f"{carry}{(a ^ b ^ cin)}"
            full_rows.append({"a": a, "b": b, "cin": cin, "expected_cout_sum": expected, "state_cout_sum": state, "count": count, "probability_percent": round(100 * count / SHOTS, 3)})
write_rows(OUT / "full_adder_simulation.csv", full_rows, full_rows[0].keys())

rca_rows = []
for a, b in [(1, 3), (2, 3)]:
    counts = ripple_2bit(a, b)
    state, count = max(counts.items(), key=lambda item: item[1])
    expected = f"{(a + b) >> 2}{(a + b) & 3:02b}"
    rca_rows.append({"A": f"{a:02b}", "B": f"{b:02b}", "expected_carry_sum1_sum0": expected, "state_carry_sum1_sum0": state, "count": count, "probability_percent": round(100 * count / SHOTS, 3)})
write_rows(OUT / "ripple_carry_2bit_simulation.csv", rca_rows, rca_rows[0].keys())

print("Simulation complete")
print("Half Adder:", half_rows)
print("Full Adder:", full_rows)
print("2-bit RCA:", rca_rows)
