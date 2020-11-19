import qiskit
import numpy as np
from gates import Rz, Ry
from qiskit.quantum_info.operators import Operator

class MinimumQClassifier():

    def __init__(self):
        q = qiskit.QuantumRegister(4)
        c = qiskit.ClassicalRegister(2)
        self.circuito = qiskit.QuantumCircuit(q,c)
        # A
        self.circuito.h(q[0])
        self.circuito.h(q[1])
        
        # B
        gRy = qiskit.circuit.library.RYGate(4.304).control(num_ctrl_qubits=1)
        self.circuito.append(gRy, [q[0],q[1]])
        self.circuito.x(q[0])

        # C
        gToffoli = qiskit.circuit.library.XGate().control(num_ctrl_qubits=2)
        self.circuito.append(gToffoli, [q[0],q[1],q[2]])
        self.circuito.x(q[1])

        # D
        gRy = qiskit.circuit.library.RYGate(1.325).control(num_ctrl_qubits=2)
        self.circuito.append(gRy, [q[0],q[1],q[2]])

        # E
        self.circuito.swap(q[2],q[3])
        self.circuito.cnot(1,2)

        # Classifying
        self.circuito.h(0)
        self.circuito.measure(q[0],c[1])
        self.circuito.measure(q[2],c[0])
