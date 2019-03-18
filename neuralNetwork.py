import numpy as np

# Weights and ouput of the function
epsilon = 0.12

hidden_layer_nodes = 500
time_to_train = 10

# Learning rate (alpha)
alpha = 0.1

# Sigmoid Function
def sigmoid(z):
  g = (1 / (1 + np.exp(-z)))
  return g

# Sigmoid Gradient
def sigmoid_derivative(z):
  g = sigmoid(z)
  g = g * (1-g)
  return g

def costFunction(results, Y, m):
  mul0 = ((Y) * np.log(results))
  mul1 = ((1 - Y) * np.log(1 - (results)))
  # Preforms the final cost function
  J = (1 / m[0]) * np.sum(np.sum(mul0 - mul1))
  return J

def feedForward(X, weights1, weights2):
    a1 = X.T
    z2 = np.dot(weights1, a1)
    a2 = sigmoid(z2).T
    a2 = np.insert(a2, 0, 1, axis=1).T
    z3 = np.dot(weights2, a2)
    output = sigmoid(z3).T
    return output, z2, a1, a2
    
def NN(time_to_train, X, y, weights1, weights2, yOutput):
    Y = np.zeros(5)
    Y[y] = 1

    m = np.shape(X)

    output = np.zeros(Y.shape)

    for i in range (time_to_train):
        output, z2, a1, a2 = feedForward(X, weights1, weights2)
        
        d3 = (output - Y)
        d2 = np.dot(d3,weights2) * (np.insert(sigmoid_derivative(z2).T, 0, 1, axis=1))
    
        d_weights1 = np.dot(a1,d2[:,1:]).T/m[0]
        d_weights2 = np.dot(a2,d3).T/m[0]
        
        weights1 -= d_weights1
        weights2 -= d_weights2

    return output, weights1, weights2
    
def predict(results, y):
  p = 0
  for i in range (np.shape(results)[0]):
    indexLocation = np.argwhere(results[i,:] == np.amax(results[i,:]))
    p = indexLocation[0]
  return p

def accuracy(outputFinal, y):
    accuracy = (np.double(predict(outputFinal, y) == y)).mean()*100
    return accuracy