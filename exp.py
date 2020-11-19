import qiskit
from minimum import MinimumQClassifier
from dataset import ProcessData
from general_preparation import QClassifier
from qiskit.visualization import plot_histogram

dataexp = ProcessData()
#print(dataexp.Y)
#dataexp.show_data()

# mini = MinimumQClassifier()
# print(mini.circuito)
qclass = QClassifier(dataexp.X[40:56,:],dataexp.Y[40:56], dataexp.X[8,:])
qclass.preparation()
qclass.circuito.draw(output='latex_source')
# print(qclass.circuito)
# backend = qiskit.Aer.get_backend('statevector_simulator')
# job = qiskit.execute(mini.circuito, backend)
# result = job.result()
# print(result.get_statevector())

# backend = qiskit.Aer.get_backend('qasm_simulator')
# results = qiskit.execute(mini.circuito, backend=backend, shots=1024).result()
# answer = results.get_counts()
backend = qiskit.Aer.get_backend('qasm_simulator')
results = qiskit.execute(qclass.circuito, backend=backend, shots=1024).result()
answer = results.get_counts()

print(answer)
#plot_histogram(answer)