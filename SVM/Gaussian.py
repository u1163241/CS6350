import os
from scipy.optimize import minimize
import numpy as np


def getDataFromPath(path: str):
    data = []
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), path), "r"
    ) as file:
        for line in file:
            terms = line.strip().split(",")
            data.append(terms)
    return data


def motifyData(data):
    for line in data:
        if line[-1] == str(0):
            line[-1] = -1
        else:
            line[-1] = 1
    return data


def getError(data, alpha, x, gamma):
    count = 0
    for example in data:
        expect = float(example[-1])
        k = K(np.array(example[0:-1], dtype=float).T, x, gamma)
        temp = np.sum(
            np.reshape(alpha, (-1, 1)) * np.array(example[-1:], dtype=float) * k
        )
        if temp > 0:
            actual = 1
        else:
            actual = -1
        if expect != actual:
            count += 1
    return count / len(data)


def K(x, z, gamma):
    return np.exp(-np.square(x - z) / gamma)


def obj(alpha, k, y):
    temp = np.reshape(alpha, (-1, 1)) * y
    dual = 0.5 * np.sum(temp @ temp.T @ k) - np.sum(alpha)
    return dual


def cons(alpha, y):
    return np.dot(alpha, y)[0]


def main():
    CList = [100 / 873, 500 / 873, 700 / 873]
    CPrint = ["100 / 873", "500 / 873", "700 / 873"]
    gammaList = [0.01, 0.1, 0.5, 1, 5, 100]
    data = motifyData(getDataFromPath("DataSets/bank-note/train.csv"))
    testData = motifyData(getDataFromPath("DataSets/bank-note/test.csv"))
    x = np.array([example[0:-1] for example in data], dtype=float)
    y = np.array([example[-1:] for example in data], dtype=float)
    num_example, num_feature = x.shape
    copy = []
    for c in range(len(CList)):
        C = CList[c]
        for gamma in gammaList:
            print("Processing...")
            bound = [(0, C)] * num_example
            alpha = np.zeros(num_example)
            k = K(x, x, gamma)
            res = minimize(
                lambda alpha: obj(alpha, k, y),
                alpha,
                method="SLSQP",
                constraints=({"type": "eq", "fun": lambda alpha: cons(alpha, y)}),
                bounds=bound,
            )
            if C == CList[1] and gamma <= 0.5:
                copy.append(res.x)
            print("C: " + CPrint[c])
            print("Gamma: " + str(gamma))
            print("Training Error: " + str(getError(data, res.x, x, gamma)))
            print("Test Error: " + str(getError(testData, res.x, x, gamma)))
    print("Overlapped support vectors between 0.01 and 0.1")
    print(len(np.intersect1d(copy[0], copy[1])))
    print("Overlapped support vectors between 0.1 and 0.5")
    print(len(np.intersect1d(copy[1], copy[2])))
