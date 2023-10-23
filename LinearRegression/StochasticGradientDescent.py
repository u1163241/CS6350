import os
import math
import random


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


def getNewWeight(weightList, line, r, b):
    newList = [0] * (len(weightList))
    for i in range(len(weightList)):
        wTxi = b + product(weightList, line)
        error = float(line[-1]) - wTxi
        input = float(line[i])
        newList[i] = weightList[i] + (r * error * input)
    return newList


def getNewB(line, weightList, r, b):
    total = 0
    wTxi = b + product(weightList, line)
    error = float(line[-1]) - wTxi
    return b + (r * error)


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
r = 0.001
b = 0
norm = 1
i = 1
while norm > tolerance:
    line = random.choice(data)
    newWeight = getNewWeight(weightList, line, r, b)
    norm = getNorm(weightList, newWeight)
    weightList = newWeight
    b = getNewB(line, weightList, r, b)
    cost = getCost(data, weightList, b)
    print(str(i) + ": " + str(cost))
    r = 0.5 * r
    i = i + 1
    # print(newWeight)

print("Learned b: " + str(b))
print("Learned weight vector: " + str(weightList))
print("Learning rate r chosen: 0.001")
print("Cost function value of the test data: " + str(getCost(testData, weightList, b)))
