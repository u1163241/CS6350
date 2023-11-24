import os
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


def motifyData(data):
    for line in data:
        if line[-1] == str(0):
            line[-1] = 1
            line.append(-1)
        else:
            line[-1] = 1
            line.append(1)
    return data


def product(weightList, line):
    total = 0
    for i in range(len(weightList) - 1):
        total += weightList[i] * float(line[i])
    return total + weightList[-1]


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


def main():
    Question = input("Please enter a for 2(a) result or b for 2(b) result\n").upper()
    if Question != "A" and Question != "B":
        print("Wrong input")
        return
    CList = [100 / 873, 500 / 873, 700 / 873]
    CPrint = ["100 / 873", "500 / 873", "700 / 873"]
    data = motifyData(getDataFromPath("DataSets/bank-note/train.csv"))
    testData = motifyData(getDataFromPath("DataSets/bank-note/test.csv"))
    N = len(data) + 1
    for c in range(0, 3):
        C = CList[c]
        weightList = [0] * (len(data[0]) - 1)
        r_0 = 0.01
        a = 1
        for T in range(0, 100):
            random.shuffle(data)
            if Question == "A":
                r = r_0 / (1 + (r_0 * T) / a)
            else:
                r = r_0 / (1 + T)
            for example in data:
                if float(example[-1]) * product(weightList, example) <= 1:
                    for j in range(len(weightList)):
                        weightList[j] = (
                            weightList[j]
                            - r * weightList[j]
                            + r * C * N * float(example[-1]) * float(example[j])
                        )
                else:
                    for j in range(len(weightList)):
                        weightList[j] = (1 - r) * weightList[j]
        print("C: " + CPrint[c])
        print(weightList)
        print("Training Error: " + str(getError(data, weightList)))
        print("Test Error: " + str(getError(testData, weightList)))
