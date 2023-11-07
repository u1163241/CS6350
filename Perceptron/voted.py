import os


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
    for example in data:
        if example[-1] == str(0):
            example[-1] = -1
    return data


def product(weightList, line):
    total = 0
    for i in range(len(weightList)):
        total += weightList[i] * float(line[i])
    return total


def getPrediction(example, weightList, b):
    if product(weightList, example) + b > 0:
        return 1
    return -1


def updateWeightList(weightList, r, example):
    for i in range(len(weightList)):
        weight = float(weightList[i])
        yi = float(example[-1])
        xi = float(example[i])
        weightList[i] = weight + (r * yi * xi)
    return weightList


def getAveragePredictionError(testData, totalWeightList, bList, countList):
    count = 0
    for example in testData:
        actural = float(example[-1])
        pCount = 0
        nCount = 0
        prediction = 0
        for i in range(len(totalWeightList)):
            currentPrediction = getPrediction(example, totalWeightList[i], bList[i])
            if currentPrediction == -1:
                nCount += countList[i]
            else:
                pCount += countList[i]
        if pCount > nCount:
            prediction = 1
        else:
            prediction = -1
        if prediction != actural:
            count = count + 1
    return count / len(testData)


def main():
    data = motifyData(getDataFromPath("DataSets/train.csv"))
    testData = motifyData(getDataFromPath("DataSets/test.csv"))
    weightList = [0, 0, 0, 0]
    countList = [0]
    bList = [0]
    totalWeightList = [weightList.copy()]
    b = 0
    r = 0.1
    m = 0
    for i in range(10):
        for example in data:
            prediction = float(example[-1])
            if prediction * getPrediction(example, weightList, b) <= 0:
                weightList = updateWeightList(weightList, r, example)
                b = b + (r * float(example[-1]))
                m = m + 1
                countList.append(1)
                totalWeightList.append(weightList.copy())
                bList.append(b)
            else:
                countList[m] = countList[m] + 1
    for i in range(len(totalWeightList)):
        print("m = " + str(i))
        print("Weight vector is: " + str(totalWeightList[i]))
        print("Bias is: " + str(bList[i]))
        print("Count is: " + str(countList[i]))
    print(
        "Average prediction error on the test data: "
        + str(getAveragePredictionError(testData, totalWeightList, bList, countList))
    )
