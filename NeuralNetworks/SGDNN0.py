import os
import math
import decimal
import random
from numpy import random


def getDataFromPath(path: str):
    data = []
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), path), "r"
    ) as file:
        for line in file:
            terms = line.strip().split(",")
            data.append(terms)
    return data


def getError(data, W1, W2, W3, width):
    count = 0
    for line in data:
        y = getPrediction(line, width, W1, W2, W3)
        if y > 0.5:
            y = 1
        else:
            y = 0
        actual = int(line[-1])
        if y != actual:
            count += 1
    return count / len(data)


def getPrediction(line, width, W1, W2, W3):
    input = line[:-1]
    Z1 = []
    Z2 = []
    for i in range(width):
        Z1.append(1)
        Z2.append(1)
    # forward pass get neuron
    for i in range(1, width):
        temp = 0
        for j in range(len(input)):
            temp += float(input[j]) * (W1[j][i - 1])
        Z1[i] = sigmoid(temp)
    for i in range(1, width):
        temp = 0
        for j in range(len(W2)):
            temp += Z1[j] * (W2[j][i - 1])
        Z2[i] = sigmoid(temp)
    y = 0
    for i in range(width):
        y += Z2[i] * W3[i]
    return y


def updateW(W, lW, r):
    for i in range(len(W)):
        for j in range(len(W[i])):
            W[i][j] -= r * lW[i][j]
    return W


def sigmoid(s):
    if s < -100:
        return 1
    return 1 / (1 + ((math.e) ** -s))


def lostSigmoid(s):
    return (1 - sigmoid(s)) * sigmoid(s)


def NN(line, W1, W2, W3, width):
    input = line[:-1]
    label = line[-1]

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

    lW1 = [[1 for i in range(width - 1)] for j in range(len(input))]
    lW2 = [[1 for i in range(width - 1)] for j in range(width)]
    lW3 = [1 for i in range(width)]

    # forward pass get neuron
    for i in range(1, len(Z1)):
        temp = 0
        for j in range(len(input)):
            temp += float(input[j]) * (W1[j][i - 1])
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
    dldy = float(y) - float(label)
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
            lW1[i][j - 1] = lZ1[j] * lostSigmoid(vZ1[j]) * float(input[i])
    return lW1, lW2, lW3


def main():
    data = getDataFromPath("DataSets/bank-note/train.csv")
    testData = getDataFromPath("DataSets/bank-note/test.csv")
    widthList = [5, 10, 25, 50, 100]
    for width in widthList:
        # initialize Weight and lost
        W1 = [[0 for i in range(width - 1)] for j in range(len(data[0]) - 1)]
        W2 = [[0 for i in range(width - 1)] for j in range(width)]
        W3 = [0 for i in range(width)]

        for T in range(10):
            r = 0.1
            random.shuffle(data)
            for line in data:
                lW1, lW2, lW3 = NN(line, W1, W2, W3, width)
                W1 = updateW(W1, lW1, r)
                W2 = updateW(W2, lW2, r)
                for i in range(len(W3)):
                    W3[i] -= r * lW3[i]
                r = r / (1 + r * T)
        print("Width: " + str(width))
        print("Training Error: " + str(getError(data, W1, W2, W3, width)))
        print("Test Error: " + str(getError(testData, W1, W2, W3, width)))
