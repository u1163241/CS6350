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


def product(weightList, line):
    total = 0
    for i in range(len(weightList)):
        total += weightList[i] * float(line[i])
    return total


def getError(data, weightList):
    count = 0
    for example in data:
        expect = float(example[-1])
        temp = product(weightList, example)
        if temp > 0:
            actual = 1
        else:
            actual = -1
        if expect != actual:
            count += 1
    return count / len(data)


def obj(alpha, x, y):
    temp = np.reshape(alpha, (-1, 1)) * y * x
    dual = 0.5 * np.sum(temp @ temp.T) - np.sum(alpha)
    return dual


def cons(alpha, y):
    return np.dot(alpha, y)[0]


def main():
    CList = [100 / 873, 500 / 873, 700 / 873]
    CPrint = ["100 / 873", "500 / 873", "700 / 873"]
    data = motifyData(getDataFromPath("DataSets/bank-note/train.csv"))
    testData = motifyData(getDataFromPath("DataSets/bank-note/test.csv"))
    x = np.array([example[0:-1] for example in data], dtype=float)
    y = np.array([example[-1:] for example in data], dtype=float)
    num_example, num_feature = x.shape

    for c in range(len(CList)):
        print("Processing...")
        C = CList[c]
        bound = [(0, C)] * num_example
        alpha = np.zeros(num_example)
        res = minimize(
            lambda alpha: obj(alpha, x, y),
            alpha,
            method="SLSQP",
            constraints=({"type": "eq", "fun": lambda alpha: cons(alpha, y)}),
            bounds=bound,
        )
        w = np.sum(np.reshape(res.x, (-1, 1)) * y * x, axis=0)
        b = np.mean(y - np.dot(x, w.T))
        weightList = w.tolist()
        weightList.append(b)
        print("C: " + CPrint[c])
        print(weightList)
        print("Training Error: " + str(getError(data, weightList)))
        print("Test Error: " + str(getError(testData, weightList)))
