# Quantum Classifier
A non-official implementation of the paper "Implementing a distance-based classifier with a quantum interference circuit"(arXiv:1703.10793).

To run the experiment:
    
    python exp.py [-h] [--circuit CIRCUIT] [--num_example NUM_EXAMPLES] [--show_data SHOW_DATA] [--draw DRAW]

To specify if the circuit will be the general implementation of the distance based classifier

    python exp.py --circuit general

To specify the number of the samples for classification(the option are 2, 4, 8, 16 and 64)

    python exp.py --circuit general --num_examples 4

To show the plot of the data distribution normalized

    python exp.py --circuit general --num_examples 4 --show_data True

To write a file with a tex description of the circuit

    python exp.py --circuit general --draw True

If the circuito was not specified with 'general' string, will run the circuit proposed in the article.

In the file exp.ipynb are the experiment presented in relatorio.pdf

## Team
Lucas Pontes de Albuquerque

Lucas Augusto Mota de Alcantara

Miguel Luiz Pessoa da Cruz Silva
