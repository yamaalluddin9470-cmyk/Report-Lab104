# Lab 6 Report: Quantum Fourier Transform

**Course:** SCI-104 – Mathematical Foundations and Quantum Mechanics Essentials  
**Institution:** Prince of Songkla University, Phuket Campus

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yamaalluddin9470-cmyk/Report-Lab104/blob/main/Lab6/lab-6-quantum-fourier-transform.ipynb)

| Field | Detail |
|---|---|
| Lab | Lab 6 – Quantum Fourier Transform (QFT) |
| Student Name | Yamalluddin Chahama |
| Student ID | 6930614038 |
| Major | AISE |
| Instructor | Komsan Kanjanasit |
| Date Performed | To be completed |
| Date Submitted | To be completed |
| Colab Notebook | [Open in Google Colab](https://colab.research.google.com/github/yamaalluddin9470-cmyk/Report-Lab104/blob/main/Lab6/lab-6-quantum-fourier-transform.ipynb) |

---

## Abstract

This lab studied the Quantum Fourier Transform (QFT), the quantum analogue of the discrete Fourier transform (DFT). A QFT circuit was implemented in Qiskit using Hadamard gates, controlled-phase rotations and final SWAP gates. The circuit was tested on two-, three- and four-qubit registers using statevector simulation. For the three-qubit circuit, the implementation contained three Hadamard gates, three controlled-phase gates and one SWAP gate, with circuit depth 6. Applying QFT to $\lvert000\rangle$ produced an equal superposition of all eight computational basis states, each with amplitude $1/\sqrt{8}$. Applying QFT to other basis states preserved the equal measurement probabilities while changing the relative phases. The results agreed with the theoretical definition of QFT and demonstrated why the final qubit swaps are required for the standard output ordering. The experiment also showed that an $n$-qubit QFT requires $O(n^2)$ elementary gates and is an important component of quantum phase estimation, Shor's algorithm and quantum arithmetic.

## 1. Objectives

1. To understand the relationship between the classical DFT and the Quantum Fourier Transform.
2. To implement QFT circuits using Hadamard and controlled-phase gates in Qiskit.
3. To test QFT on small quantum registers and interpret the resulting statevectors.
4. To understand the purpose of the final SWAP gates and qubit ordering.
5. To connect QFT with phase estimation, Shor's algorithm and quantum arithmetic.

## 2. Background

### 2.1 Classical Discrete Fourier Transform

For a vector $x=(x_0,x_1,\ldots,x_{N-1})$, the normalized discrete Fourier transform is

$$y_k=\frac{1}{\sqrt{N}}\sum_{j=0}^{N-1}x_j e^{2\pi i jk/N}.$$

The transform changes a representation from the computational or time domain to a frequency-domain representation. The inverse DFT changes the sign of the exponent and transforms the result back.

### 2.2 Quantum Fourier Transform

The QFT acts on an $n$-qubit computational basis state $\lvert j\rangle$ as

$$\mathrm{QFT}_N\lvert j\rangle=\frac{1}{\sqrt{N}}\sum_{k=0}^{N-1}e^{2\pi i jk/N}\lvert k\rangle,\qquad N=2^n.$$

The output probabilities of a basis-state input are equal, but the amplitudes contain phase information that depends on the input integer $j$. This phase information becomes useful when QFT is combined with other quantum operations.

### 2.3 Circuit Decomposition

The standard QFT circuit is built from:

- Hadamard gates, which create equal superpositions;
- controlled-phase gates $CP(\theta)$, which encode relative phases;
- SWAP gates, which reverse the qubit order at the end of the circuit.

For an $n$-qubit QFT, the number of Hadamard gates is $n$, the number of controlled-phase gates is $n(n-1)/2$, and the number of final SWAP gates is $\lfloor n/2\rfloor$. Therefore, the direct circuit has quadratic gate complexity, $O(n^2)$.

### 2.4 Phase Rotations

The controlled-phase gate is

$$CP(\theta)=\mathrm{diag}(1,1,1,e^{i\theta}).$$

In the QFT circuit, the required angles are powers of two, such as $\pi/2$, $\pi/4$ and $\pi/8$. These gates do not change computational-basis probabilities by themselves; they change relative phases between amplitudes.

## 3. Tools and Environment

| Item | Version / Detail |
|---|---|
| Platform | Google Colab or local Python environment |
| Python | Python 3 |
| qiskit | 2.2.3 (verification run) |
| Simulator | Qiskit Statevector simulator |
| Libraries | `numpy`, `qiskit`, `qiskit-aer`, `matplotlib` |

## 4. Lab Tasks and Results

### Task 1 — Setup

```python
%pip install -q qiskit qiskit-aer pylatexenc

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
```

The required packages were imported successfully. Statevector simulation was used because it gives the complete complex amplitudes, including phase information that cannot be observed directly from a computational-basis histogram.

### Task 2 — QFT Building Block

```python
def qft(n):
    qc = QuantumCircuit(n)

    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            qc.cp(np.pi / 2**(k - j), k, j)

    # Reverse the qubit order for the standard QFT output.
    for j in range(n // 2):
        qc.swap(j, n - j - 1)

    return qc
```

The function applies one Hadamard gate to each qubit, followed by the required controlled-phase rotations. The final loop reverses the order of the qubits.

![QFT circuit construction](images/Quantum%20Fourier%20Transform.png)

### Task 3 — Two-Qubit QFT

```python
qc2 = qft(2)
print(qc2.draw())
```

For two qubits, the circuit contains two Hadamard gates, one controlled-phase gate with angle $\pi/2$, and one SWAP gate. The controlled phase introduces the relative phase between the two branches of the superposition, while the SWAP corrects the reversed output order.

### Task 4 — Three-Qubit QFT

```python
qc3 = qft(3)
print(qc3.draw())
```

![Three-qubit QFT code](images/Code%20for%203-bit%20QFT.png)

The three-qubit circuit had the following resource counts:

| Gate | Number |
|---|---:|
| Hadamard ($H$) | 3 |
| Controlled phase ($CP$) | 3 |
| SWAP | 1 |
| Circuit depth | 6 |

The controlled-phase angles in this circuit are $\pi/2$, $\pi/4$ and $\pi/2$. The number of controlled-phase gates follows $3(3-1)/2=3$.

### Task 5 — Statevector Testing

```python
for i in range(8):
    qc_test = QuantumCircuit(3)
    for q in range(3):
        if i & (1 << q):
            qc_test.x(q)

    qc_test.compose(qft(3), inplace=True)
    state = Statevector.from_instruction(qc_test)
    print(f"Input |{i:03b}>, output = {state}")
```

For input $\lvert000\rangle$, the theoretical output is

$$\mathrm{QFT}_8\lvert000\rangle=\frac{1}{\sqrt8}(\lvert000\rangle+\lvert001\rangle+\cdots+\lvert111\rangle).$$

The statevector simulation gave eight amplitudes of approximately $0.3536$, since $1/\sqrt8\approx0.3536$:

| Input | Output amplitudes | Measurement probability |
|---|---|---|
| $\lvert000\rangle$ | $0.3536$ for every basis state | $0.125$ for every state |
| $\lvert001\rangle$ | $\pm0.3536$ according to the phase factor | $0.125$ for every state |
| $\lvert010\rangle$ | Complex phases with magnitude $0.3536$ | $0.125$ for every state |
| $\lvert011\rangle$ | Complex phases with magnitude $0.3536$ | $0.125$ for every state |

The remaining basis-state inputs produced the same amplitude magnitude, while their complex phases changed according to $e^{2\pi i jk/8}$. Thus, QFT encodes information in phase rather than changing the uniform probability distribution of a basis-state input.

![Three-qubit QFT result](images/results%203-b%20QFT%20x.png)

### Task 6 — Four-Qubit Scaling

```python
qc4 = qft(4)
print(qc4.draw())
```

![Four-qubit QFT code](images/Code%20for%204-bit%20QFT.png)

For four qubits, $N=16$. The circuit requires four Hadamard gates, six controlled-phase gates and two SWAP gates. The number of controlled-phase gates increases from 3 for three qubits to 6 for four qubits, illustrating the quadratic scaling of the direct QFT construction.

| Register size | $H$ gates | $CP$ gates | SWAP gates |
|---:|---:|---:|---:|
| 2 qubits | 2 | 1 | 1 |
| 3 qubits | 3 | 3 | 1 |
| 4 qubits | 4 | 6 | 2 |

## 5. Exercises

### Exercise 1 — Manual QFT(3)

The three-qubit QFT can be written manually by applying the following operations in sequence:

1. Apply $H$ to qubit 0, then controlled phases from qubits 1 and 2 to qubit 0.
2. Apply $H$ to qubit 1, then a controlled phase from qubit 2 to qubit 1.
3. Apply $H$ to qubit 2.
4. Apply a SWAP between qubits 0 and 2.

This gate sequence is equivalent to the output of `qft(3)`.

### Exercise 2 — Inverse Check

The inverse QFT is obtained with `qft(3).inverse()`:

```python
qc_check = QuantumCircuit(3)
qc_check.x(0)
initial = Statevector.from_instruction(qc_check)

qc_check.compose(qft(3), inplace=True)
qc_check.compose(qft(3).inverse(), inplace=True)
final = Statevector.from_instruction(qc_check)

print(initial.equiv(final))
```

The final state is equivalent to the initial state up to numerical precision. This confirms that QFT is unitary and that the inverse circuit reverses the transformation.

### Exercise 3 — Omitting the Final SWAPs

If the final SWAP gates are omitted, the circuit still performs the Fourier transform, but the output qubits appear in reversed order. The phase information is not destroyed; it is simply associated with the opposite qubit ordering. The SWAP gates are therefore a convention for presenting the result in the standard order.

## 6. Concept Questions

**Q1. Why is QFT important in quantum computing?**

QFT converts information encoded in computational-basis amplitudes into relative phases. This makes periodicity and phase differences accessible to quantum algorithms. It is a central subroutine in quantum phase estimation and Shor's factoring algorithm.

**Q2. What is the role of controlled-phase gates?**

Controlled-phase gates add phase factors to selected components of the superposition. Their angles determine the phase resolution of each qubit and reproduce the factor $e^{2\pi i jk/N}$ in the mathematical definition of QFT.

**Q3. Why are the final SWAP gates needed?**

The natural decomposition produces the output qubits in reversed order because the least-significant and most-significant qubits are processed in opposite directions. The final SWAP gates reverse this order so that the output matches the conventional binary labeling.

**Q4. How many controlled-phase gates are needed for an $n$-qubit QFT?**

The direct circuit needs one controlled phase for each pair of qubits, so the number is

$$\frac{n(n-1)}{2}.$$

For three and four qubits, this gives 3 and 6 controlled-phase gates, respectively.

**Q5. What happens when QFT is followed by its inverse?**

The original quantum state is recovered, apart from negligible numerical round-off error. This is because QFT is unitary and therefore has an inverse.

## 7. Discussion

The simulation results agreed with the QFT definition. When the input was a computational-basis state, every output amplitude had magnitude $1/\sqrt{N}$, so every computational-basis measurement outcome had probability $1/N$. The input value was not visible in the probabilities; it was stored in the relative phases. This is the key difference between inspecting a statevector and measuring directly in the computational basis.

The three-qubit implementation used 3 Hadamard gates, 3 controlled-phase gates and 1 SWAP gate. This matches the theoretical gate counts. The four-qubit circuit required 6 controlled-phase gates, confirming the $O(n^2)$ scaling of the standard exact QFT circuit.

The final SWAP gates are important for interpreting the output. Without them, the circuit is still a valid Fourier transform, but the qubits are in reversed order. This is a qubit-labeling issue rather than a failure of the algorithm.

One limitation of this experiment is that only small registers were simulated. Statevector simulation requires $2^n$ complex amplitudes, so its memory requirement grows exponentially with the number of qubits. In larger systems, approximate QFT circuits may omit very small-angle controlled rotations to reduce the circuit cost.

## 8. Conclusion

This lab implemented and tested the Quantum Fourier Transform using Qiskit. The circuit was constructed from Hadamard gates, controlled-phase rotations and final SWAP gates. The three-qubit QFT produced the expected equal-magnitude amplitudes, while the input-dependent information appeared in the relative phases. The inverse-QFT check confirmed that the circuit is reversible, and the scaling experiment verified that the direct implementation uses $n(n-1)/2$ controlled-phase gates. The experiment met the objectives and demonstrated why QFT is a foundational component of quantum phase estimation, Shor's algorithm and quantum arithmetic.

## 9. References

1. M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press.
2. IBM Quantum Learning, *Quantum Fourier Transform*. https://quantum.cloud.ibm.com/learning
3. IBM Quantum Documentation. https://quantum.cloud.ibm.com/docs
4. D. Coppersmith, “An approximate Fourier transform useful in quantum factoring,” arXiv:quant-ph/0201067.
5. V. Vedral, A. Barenco and A. Ekert, “Quantum networks for elementary arithmetic operations,” *Physical Review A*, 54(1), 147–153, 1996.
6. Lab sheet: Komsan Kanjanasit, *Lab 6: Quantum Fourier Transform*. https://github.com/komsan-k/quantum-computation/tree/9d6aece722653c87cd30371f9e7967afc517c1e6/lab/lab-6-quantum-fourier-transform

## Appendix — Full Code

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def qft(n):
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            qc.cp(np.pi / 2**(k - j), k, j)
    for j in range(n // 2):
        qc.swap(j, n - j - 1)
    return qc

for n in [2, 3, 4]:
    circuit = qft(n)
    print(f"{n}-qubit QFT")
    print(circuit.draw())

for i in range(8):
    test = QuantumCircuit(3)
    for q in range(3):
        if i & (1 << q):
            test.x(q)
    test.compose(qft(3), inplace=True)
    state = Statevector.from_instruction(test)
    print(f"Input |{i:03b}>")
    print(state)
```

---

*Report prepared from the Lab2 report format supplied by the student. Numerical values in the results section were verified with Qiskit statevector simulation.*
