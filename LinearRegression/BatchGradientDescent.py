import os
import math


def getDataFromPath(path: str):
    data = []
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), path), "r"
    ) as file:
        for line in file:
            terms = line.strip().split(",")
            data.append(terms)
    return data


def product(weightList, line):
    total = 0
    for i in range(len(weightList)):
        total += weightList[i] * float(line[i])
    return total


def getGradientList(data, weightList, b):
    newList = [0] * (len(weightList))
    for i in range(len(data)):
        line = data[i]
        wTxi = b + product(weightList, line)
        error = float(line[-1]) - wTxi
        for j in range(len(line) - 1):
            input = float(data[i][j])
            newList[j] -= error * input
    return newList


def getNewWeight(weightList, gradientList, r):
    newList = [0] * (len(weightList))
    for i in range(len(weightList)):
        newList[i] = weightList[i] - (r * gradientList[i])
    return newList


def getNewB(data, weightList, r, b):
    total = 0
    for line in data:
        wTxi = b + product(weightList, line)
        error = float(line[-1]) - wTxi
        total -= error
    return b - (r * total)


def getNorm(weightList, newList):
    difference = [0] * (len(weightList))
    norm = 0
    for i in range(len(weightList)):
        difference[i] = weightList[i] - newList[i]
    for current in range(len(difference)):
        norm += difference[current] ** 2
    return math.sqrt(norm)


def getCost(data, weightList, b):
    cost = 0
    for line in data:
        wTxi = b + product(weightList, line)
        error = float(line[-1]) - wTxi
        cost += 0.5 * (error**2)
    return cost


data = getDataFromPath("DataSets/concrete/train.csv")
testData = getDataFromPath("DataSets/concrete/test.csv")
tolerance = 0.000001
weightList = [0] * (len(data[0]) - 1)
r = 0.02
b = 0
norm = 1
i = 1
while norm > tolerance:
    gradientList = getGradientList(data, weightList, b)
    newWeight = getNewWeight(weightList, gradientList, r)
    norm = getNorm(weightList, newWeight)
    weightList = newWeight
    b = getNewB(data, weightList, r, b)
    cost = getCost(data, weightList, b)
    print(str(i) + ": " + str(cost))
    r = 0.5 * r
    i = i + 1
    # print(newWeight)

print("Learned b: " + str(b))
print("Learned weight vector: " + str(weightList))
print("Learning rate r chosen: 0.02")
print("Cost function value of the test data: " + str(getCost(testData, weightList, b)))
