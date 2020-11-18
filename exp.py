import qiskit
from minimum import MinimumQClassifier
from dataset import ProcessData

mini = MinimumQClassifier()

print(mini.circuito)
backend = qiskit.Aer.get_backend('statevector_simulator')
#job = qiskit.execute(mini.circuito, backend)
#result = job.result()
results = qiskit.execute(mini.circuito, backend=backend, shots=1024).result()
answer = results.get_counts()
#print(result.get_statevector())
print(answer)

#dataexp = ProcessData()

#dataexp.show_data()