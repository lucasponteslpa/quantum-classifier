import qiskit
import numpy as np

class QClassifier(object):

    def __init__(self, dataset, features, test):
        
        # Load the data and your parameters
        self.dataset_size = dataset.shape[0]
        self.num_features = dataset.shape[1]
        self.log2M = int(np.log2(self.dataset_size))
        self.log2N = int(np.log2(self.num_features))
        self.dataset = dataset
        self.target = features
        self.test = test

        # Create the respective registers for each component of
        # the implemented classifier
        self.ancilla = qiskit.QuantumRegister(1)
        self.ket_m = qiskit.QuantumRegister(self.log2M)
        self.ket_phi = qiskit.QuantumRegister(self.log2N)
        self.ket_y = qiskit.QuantumRegister(1)
        self.c_anc = qiskit.ClassicalRegister(1)
        self.c_class = qiskit.ClassicalRegister(1)
        self.circuito = qiskit.QuantumCircuit(self.ancilla,self.ket_m,self.ket_phi,self.ket_y,self.c_anc,self.c_class)


    def preparation(self):

        # Stage A: put the qubits of ancilla and ket_m register in superposition
        self.circuito.h(self.ancilla)
        for i in range(int(np.log2(self.dataset_size))):
            self.circuito.h(self.ket_m[i])
        
        # Stage B: Preparation of the test state, with controlled in ancilla = 0
        q_test = self.init(self.test, label="x~", ctrl_str='0')
        qb = np.array([self.ancilla])
        
        if(self.log2N > 1):
            for i in range(self.log2M):
                qb = np.append(qb,self.ket_phi[i])
        else:
            qb = np.append(qb,self.ket_phi)

        self.circuito.append(q_test,list(qb))
        
        # Stage C: Preparation of the exemples states, with controlled in ancilla = 1
        for i in range(self.dataset_size):
            q_m = self.init(self.dataset[i,:],label='x_'+str(i), ctrl_str=self.ctrl_bin(i,self.log2M)+'1')
            qb = np.array([self.ancilla])
            for j in range(self.log2M):
                qb = np.append(qb,self.ket_m[j])

            if(self.log2N > 1):
                for j in range(self.log2M):
                    qb = np.append(qb,[self.ket_phi[j]])
            else:
                qb = np.append(qb,self.ket_phi)
            self.circuito.append(q_m,list(qb))

        # Stage D: Tangle the class states with the index ket_m
        for i in range(self.dataset_size):
            if self.target[i] == 1:
                target_gate = qiskit.circuit.library.XGate().control(num_ctrl_qubits=self.log2M, ctrl_state=self.ctrl_bin(i,self.log2M))
                qb = np.array([])
                for j in range(self.log2M):
                    qb = np.append(qb,self.ket_m[j])

                qb = np.append(qb,self.ket_y)
                self.circuito.append(target_gate,list(qb))
        

        self.circuito.h(self.ancilla)
        self.circuito.measure(self.ancilla,self.c_anc)
        self.circuito.measure(self.ket_y,self.c_class)


    def init(self, vetor, label="qV", ctrl_str=None):

        circuito = qiskit.QuantumCircuit(int(np.log2(len(vetor))))

        norms = lambda v: np.sqrt(np.absolute(v[0::2])**2 + np.absolute(v[1::2])**2)
        select_alpha = lambda v,p,i: 2*np.arcsin(v[2*i + 1]/p) if v[2*i]>0 else 2*np.pi - 2*np.arcsin(v[2*i + 1]/p) 

        alphas = []
        parents = norms(vetor)
        alphas = np.append(alphas, np.array([ select_alpha(vetor,parents,i) for i in range(vetor.shape[0]//2)]))[::-1]
        # alphas = np.append(alphas, np.array(2*np.arcsin(vetor[1::2]/parents)))[::-1]

        for _ in range(int(np.log2(len(vetor)))-1):
            new_parents = norms(parents)
            alphas = np.append(alphas, np.array(2*np.arcsin(parents[1::2]/new_parents))[::-1])
            parents = new_parents

        level = 1
        gate_op = qiskit.circuit.library.RYGate(alphas[-1])
        circuito.append(gate_op, [int(np.log2(len(vetor)))-1])
        qlines = range(int(np.log2(len(vetor))))[::-1]
        ctrl_state = 0

        for i in range(len(vetor)-2):
            gate_op = qiskit.circuit.library.RYGate(alphas[len(alphas)-2-i]).control(num_ctrl_qubits=level,ctrl_state=self.ctrl_bin(ctrl_state,level))
            circuito.append(gate_op, qlines[0:level+1])

            if ctrl_state == (2**level - 1):
                ctrl_state = 0
                level += 1
            else:
                ctrl_state +=1
        qvetor = circuito.to_gate(label=label).control(num_ctrl_qubits=len(ctrl_str),ctrl_state=ctrl_str)
        qvetor.name = label

        return qvetor


    def ctrl_bin(self, state, level):

        state_bin = ''
        i = state
        while i//2 != 0:
            if(i>3):
                state_bin = state_bin + str(i%2)
                i = i//2
            else:
                state_bin = state_bin + str(i%2) + str(i//2)
                i = i//2
        
        #if level > len(state_bin):
        i = level - len(state_bin) - 1

        if state//2 == 0 and level > len(state_bin):
             state_bin = str(state%2)

        for _ in range(level-len(state_bin)):
            state_bin = state_bin + '0'
    
        return state_bin

