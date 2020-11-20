import qiskit
from minimum import MinimumQClassifier
from dataset import ProcessData
from general_preparation import QClassifier
from qiskit.visualization import plot_histogram
from pdb import set_trace
import numpy as np

def print_state(cq):
    backend = qiskit.Aer.get_backend('statevector_simulator')
    job = qiskit.execute(cq, backend)
    result = job.result()
    print(result.get_statevector())

def print_res(cq):
    backend = qiskit.Aer.get_backend('qasm_simulator')
    results = qiskit.execute(cq, backend=backend, shots=1024).result()
    answer = results.get_counts()
    print(answer)


dataexp = ProcessData()
#dataexp.show_data()

# mini = MinimumQClassifier()
# print(mini.circuito)
# print_state(mini.circuito)
# set_trace()
# qclass = QClassifier(dataexp.X[42:58,:],dataexp.Y[42:58], dataexp.X[54,:])
# qclass = QClassifier(np.array([dataexp.norm[32,:],dataexp.norm[84,:]]),np.array([dataexp.Y[32],dataexp.Y[84]]), dataexp.norm[28,:])
qclass = QClassifier(np.array([[0.0,1.0],[0.789,0.615]]), np.array([0,1]), np.array([-0.549,0.836]))
qclass.preparation()
print(qclass.circuito)
#print_state(qclass.circuito)
print_res(qclass.circuito)
