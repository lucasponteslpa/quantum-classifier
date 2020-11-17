import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets
from sklearn.decomposition import PCA
import numpy as np

class ProcessData():

    def __init__(self, name='iris'):
        self.data_name = name
        self.iris = datasets.load_iris()
        self.X = self.iris.data[:, :2]  # we only take the first two features.
        self.Y = self.iris.target

        self.mean = np.array([np.mean(self.X[:,i]) for i in range(self.X.shape[1])])
        self.var = np.array([np.var(self.X[:,i]) for i in range(self.X.shape[1])])
        center = (self.X - np.reshape(self.mean,(1,2)))/np.reshape(self.var,(1,2))
        a = np.array([np.linalg.norm(center[i,:]) for i in range(self.X.shape[0])])
        a = np.array([a,a])
        self.norm = center/np.reshape(a,(a.shape[1],a.shape[0]))
        #self.norm = self.X/np.reshape(a,(a.shape[1],a.shape[0]))

    def show_data(self):
        x_min, x_max = self.norm[:, 0].min() - .5, self.norm[:, 0].max() + .5
        y_min, y_max = self.norm[:, 1].min() - .5, self.norm[:, 1].max() + .5

        plt.figure(2, figsize=(8, 6))
        plt.clf()

        # Plot the training points
        plt.scatter(self.norm[:, 0], self.norm[:, 1], c=self.Y)
        plt.xlabel('Sepal length')
        plt.ylabel('Sepal width')

        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        plt.xticks(())
        plt.yticks(())

        # To getter a better understanding of interaction of the dimensions
        # plot the first three PCA dimensions
        fig = plt.figure(1, figsize=(8, 6))
        ax = Axes3D(fig, elev=-150, azim=110)
        X_reduced = PCA(n_components=3).fit_transform(self.iris.data)
        ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=self.Y, s=40)
        ax.set_title("First three PCA directions")
        ax.set_xlabel("1st eigenvector")
        ax.w_xaxis.set_ticklabels([])
        ax.set_ylabel("2nd eigenvector")
        ax.w_yaxis.set_ticklabels([])
        ax.set_zlabel("3rd eigenvector")
        ax.w_zaxis.set_ticklabels([])

        plt.show()