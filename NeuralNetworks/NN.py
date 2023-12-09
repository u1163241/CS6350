import math


def sigmoid(s):
    return 1 / (1 + ((math.e) ** -s))


def lostSigmoid(s):
    return (1 - sigmoid(s)) * sigmoid(s)


def main():
    width = 3
    input = [1, 1, 1]
    label = 1

    # initialize neuron and lost
    Z1 = []
    Z2 = []
    # value before sigmoid
    vZ1 = []
    vZ2 = []
    lZ1 = []
    lZ2 = []
    for i in range(width):
        Z1.append(1)
        Z2.append(1)
        vZ1.append(1)
        vZ2.append(1)
        lZ1.append(1)
        lZ2.append(1)

    # initialize Weight and lost
    # W1 = [[1] * (width - 1)] * width
    # W2 = [[1] * (width - 1)] * width
    # W3 = [1]*width

    lW1 = [[1 for i in range(width - 1)] for j in range(len(input))]
    lW2 = [[1 for i in range(width - 1)] for j in range(width)]
    lW3 = [1 for i in range(width)]

    W1 = [[-1, 1], [-2, 2], [-3, 3]]
    W2 = [[-1, 1], [-2, 2], [-3, 3]]
    W3 = [-1, 2, -1.5]

    # forward pass get neuron
    for i in range(1, len(Z1)):
        temp = 0
        for j in range(len(input)):
            temp += input[j] * (W1[j][i - 1])
        vZ1[i] = temp
        Z1[i] = sigmoid(temp)
    for i in range(1, len(Z2)):
        temp = 0
        for j in range(len(W2)):
            temp += Z1[j] * (W2[j][i - 1])
        vZ2[i] = temp
        Z2[i] = sigmoid(temp)
    y = 0
    for i in range(width):
        y += Z2[i] * W3[i]

    # back propagation
    # layer 3 Weight
    dldy = y - label
    for i in range(len(lW3)):
        lW3[i] = dldy * Z2[i]

    # layer 2 Neural
    for i in range(1, len(lZ2)):
        lZ2[i] = dldy * W3[i]

    # layer 2 Weight
    for i in range(len(lZ2)):
        for j in range(1, len(lW2)):
            lW2[i][j - 1] = lZ2[j] * lostSigmoid(vZ2[j]) * Z1[i]

    # layer 1 Neural
    for i in range(1, len(lZ1)):
        temp = 0
        for j in range(1, len(W2)):
            temp += lZ2[j] * lostSigmoid(vZ2[j]) * W2[i][j - 1]
        lZ1[i] = temp

    # layer 1 Weight
    for i in range(len(input)):
        for j in range(1, len(lW1)):
            lW1[i][j - 1] = lZ1[j] * lostSigmoid(vZ1[j]) * input[i]

    print("Layer 3 partial derivatives over the weights")
    print(lW3)
    print("Layer 2 partial derivatives")
    print(lZ2)
    print("Layer 2 partial derivatives over the weights")
    print(lW2)
    print("Layer 1 partial derivatives")
    print(lZ1)
    print("Layer 1 partial derivatives over the weights")
    print(lW1)
