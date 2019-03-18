from neuralNetwork import *
import numpy as np



X =  np.array([(1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1), (1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1), (0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1)])
X = (X - np.amin(X))/(np.amax(X)-np.amin(X))
X = np.insert(X, 0, 1, axis=1)  
y = np.array([67, 1, 4])
yOutput = np.amax(y)
m = np.shape(X)
weights1 = np.random.rand(hidden_layer_nodes, m[1]) * (2 * epsilon) - epsilon
weights2 = np.random.rand(yOutput + 1, hidden_layer_nodes + 1) * (2 * epsilon) - epsilon

output, weights1, weights2 = NN(400, X, y, weights1, weights2, yOutput)

print(predict(output, y))
print(accuracy(output, y))