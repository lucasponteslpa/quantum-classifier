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

def run_classifier(params):
    dataexp = ProcessData()
    #dataexp.show_data()
    if(params["circuit"]=="minimun"):
        mini = MinimumQClassifier()
        print(mini.circuito)
        print_res(mini.circuito)
    #set_trace()
    else:
        # qclass = QClassifier(dataexp.norm[42:58,:],dataexp.Y[42:58], dataexp.norm[54,:])
        qclass = QClassifier(np.append(dataexp.norm[0:32,:],dataexp.norm[55:87,:]).reshape(64,2),np.append(dataexp.Y[0:32],dataexp.Y[55:87]), dataexp.norm[32,:])
        # qclass = QClassifier(np.array([[0.0,1.0],[0.789,0.615]]), np.array([0,1]), np.array([-0.549,0.836]))
        qclass.preparation()
        #print(qclass.circuito)
        #print_state(qclass.circuito)
        print_res(qclass.circuito)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Preprocess')
    parser.add_argument('--circuit', type=str, help='Define what circuit will be used')
    parser.add_argument('--num_exemples', type=str, help='Number of training exemples')
    parser.add_argument('--test_index', type=str, help='Index of test data')

    params = vars(parser.parse_args())

    print('PARAMS:')
    print(params)
    run_classifier(params)
