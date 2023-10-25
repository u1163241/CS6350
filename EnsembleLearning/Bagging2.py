import os
import statistics
from math import log2
import random
import math


class Node:
    def __init__(self, lable):
        self.label = lable
        self.branch = {}

    def __str__(self) -> str:
        printNode(self)
        return ""

    def contain(self, value):
        for node in self.branch:
            if list(node.label.keys())[0] == value:
                return node
        return False


def printNode(root: Node, level=0):
    print("\t" * level + str(root.label))
    for child in root.branch:
        printNode(child, level + 1)


def getDataFromPath(path: str):
    data = []
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), path), "r"
    ) as file:
        for line in file:
            terms = line.strip().split(",")
            data.append(terms)
    return data


def getHeader(KEY):
    if KEY == "CAR":
        return ["buying", "maint", "doors", "persons", "lug_boot", "safety", "label"]
    if KEY == "TENNIS":
        return ["Outlook", "Temperature", "Humidity", "Wind", "Play Tennis"]
    if KEY == "BANK":
        return [
            "age",
            "job",
            "marital",
            "education",
            "default",
            "balance",
            "housing",
            "loan",
            "contact",
            "day",
            "month",
            "duration",
            "campaign",
            "pdays",
            "previous",
            "outcome",
            "label",
        ]


def getData(KEY):
    if KEY == "CAR":
        return getDataFromPath("DataSets/car-4/train.csv"), getDataFromPath(
            "DataSets/car-4/test.csv"
        )
    if KEY == "TENNIS":
        return getDataFromPath("DataSets/train.csv"), getDataFromPath(
            "DataSets/test.csv"
        )
    if KEY == "BANK":
        return getDataFromPath("DataSets/bank-7/train.csv"), getDataFromPath(
            "DataSets/bank-7/test.csv"
        )


def processData(data):
    attributes = {}
    labels = {}
    for row in range(len(data)):
        for col in range(len(data[row])):
            cell = data[row][col]
            if row == 0:  # header, get each atrribute name
                if col != len(data[row]) - 1:
                    attributes.update({cell: {}})  # attribute names
            else:
                labelValue = data[row][len(data[row]) - 1]  # current label value
                if col == len(data[row]) - 1:  # update label
                    if labelValue in labels:
                        labels.update({labelValue: labels[labelValue] + 1})
                    else:
                        labels.update({labelValue: 1})
                else:  # update attribute
                    attribute = attributes[data[0][col]]
                    if (
                        cell in attribute and labelValue in attribute[cell]
                    ):  # update exist label value
                        attribute[cell].update(
                            {labelValue: attribute[cell][labelValue] + 1}
                        )
                    elif cell in attribute:  # add new label value
                        attribute[cell].update({labelValue: 1})
                    else:  # add new attribute value
                        attribute.update({cell: {labelValue: 1}})
    return attributes, labels


def calculation(labels, KEY):
    total = 0
    returnNumber = 0
    minority = float("inf")
    for count in labels.values():
        total += count
    for count in labels.values():
        if KEY == "IG":
            returnNumber -= (count / total) * log2(count / total)
        if KEY == "ME":
            minority = min(minority, count)
            returnNumber = minority / total
            if returnNumber == 1:
                returnNumber = 0
        if KEY == "GI":
            returnNumber += (count / total) ** 2
    if KEY == "GI":
        returnNumber = 1 - returnNumber
    return total, returnNumber


def purity(labels, attributes, KEY):
    total, totalCalculation = calculation(labels, KEY)
    sumPurity = 0
    for attribute in attributes:
        subTotal, subPurity = calculation(attributes[attribute], KEY)
        sumPurity += (subTotal / total) * subPurity
    return totalCalculation - sumPurity


def bestToSplit(labels, attributes, KEY):
    best = ""
    max = float("-inf")
    for attribute in attributes:
        current = purity(labels, attributes[attribute], KEY)
        best, max = ((best, max), (attribute, current))[current > max]
    return best


def getPrediction(node, line, header):
    current = list(node.label.keys())[0]
    currentLables = list(node.label.values())[0]
    index = -1
    if len(currentLables.keys()) == 1:  # the prediction
        return list(currentLables.keys())[0]
    elif current in header:
        index = header.index(current)
        if node.contain(line[index]):
            return getPrediction(node.contain(line[index]), line, header)
        else:  # most common value
            max = float("-inf")
            returnLabel = ""
            for currentLable, currentValue in currentLables.items():
                if currentValue > max:
                    max = currentValue
                    returnLabel = currentLable
            return returnLabel
    elif len(node.branch) < 1:
        max = float("-inf")
        returnLabel = ""
        for currentLable, currentValue in currentLables.items():
            if currentValue > max:
                max = currentValue
                returnLabel = currentLable
        return returnLabel
    else:
        return getPrediction(node.branch[0], line, header)


def processBank(bankData):
    processIndex = [0, 5, 9, 11, 12, 13, 14]
    numList = [[], [], [], [], [], [], []]
    medianList = [[], [], [], [], [], [], []]
    for line in bankData:
        for i in range(len(processIndex)):
            numList[i].append(float(line[processIndex[i]]))
    for i in range(len(numList)):
        medianList[i] = statistics.median(numList[i])
    for line in bankData:
        for i in range(len(processIndex)):
            if float(line[processIndex[i]]) >= medianList[i]:
                line[processIndex[i]] = "above"
            else:
                line[processIndex[i]] = "below"


def unknownProcess(data):
    majorityList = []
    count = []
    for line in data:
        current = line[15]
        if current != "unknown":
            if current not in majorityList:
                majorityList.append(current)
                count.append(1)
            else:
                count[majorityList.index(current)] += 1
    majority = majorityList[count.index(max(count))]
    for line in data:
        current = line[15]
        if current == "unknown":
            line[15] = majority


def predictionError(data, header, rootList):
    count = 0
    for line in data:
        prediction = getBaggingPrediction(rootList, line, header)
        actual = line[len(line) - 1]
        if prediction != actual:
            count += 1
    return count / len(data)


def treePredictionError(Node, data, header):
    count = 0
    for line in data:
        prediction = getPrediction(Node, line, header)
        actual = line[len(line) - 1]
        if prediction != actual:
            count += 1
    return count / len(data)


def getBaggingPrediction(rootList, line, header):
    totalVote = {}
    for i in range(len(rootList)):
        root = rootList[i]
        vote = getPrediction(root, line, header)
        if vote not in totalVote:
            totalVote[vote] = 0
        totalVote[vote] += 1
    max = float("-inf")
    returnVote = ""
    for vote, number in totalVote.items():
        if number > max:
            returnVote = vote
            max = number
    return returnVote


def listAverage(l):
    return sum(l) / len(l)


def getVariance(predictionList, average, count):
    total = 0
    for prediction in predictionList:
        total += (prediction - average) ** 2
    return math.sqrt(total / count)


def ID3(S, Attributes, Label, Depth, KEY):
    bestAttribute = bestToSplit(Label, Attributes, KEY)
    childList = []  # branch
    root = Node({bestAttribute: Label})  # current root node
    root.branch = childList
    for attribute in Attributes[bestAttribute]:  # split each attribute value
        subData = []
        for row in range(len(S)):
            line = S[row].copy()
            if row == 0:  # header
                line.remove(bestAttribute)
                subData.append(line)
            else:  # subdata
                index = list(Attributes.keys()).index(bestAttribute)
                if line[index] == attribute:
                    del line[index]
                    subData.append(line)
        subAttributes, subLabels = processData(subData)  # process new data
        child = Node({attribute: subLabels})
        childList.append(child)  # connect each child node to current
        if len(subLabels.values()) > 1 and (Depth - 1) != 0:
            temp = []  # continue branch on child node
            child.branch = temp
            temp.append(ID3(subData, subAttributes, subLabels, Depth - 1, KEY))
    return root


def main():
    # set up
    version = "BANK"
    data, testdata = getData(version)
    processBank(data)
    processBank(testdata)
    header = getHeader(version)
    data.insert(0, header)

    treeList = []
    baggedList = []

    print("Processing...")
    for T in range(0, 100):
        rootList = []
        for j in range(500):
            sample = []
            dataCopy = data.copy()
            sample.insert(0, header)
            for j in range(1000):
                pick = random.randint(1, len(dataCopy) - 2)
                sample.append(dataCopy[pick])
                dataCopy.remove(dataCopy[pick])
            attributes, labels = processData(sample)
            Root = ID3(sample, attributes, labels, 16, "IG")
            rootList.append(Root)
        baggedList.append(rootList)
        treeList.append(rootList[0])

    treeBiasList = []
    baggedBiasList = []
    treeVarianceList = []
    baggedVarianceList = []
    for line in dataCopy:
        treePredictionList = []
        baggedPredictionList = []
        for tree in treeList:
            if getPrediction(tree, line, header) == "yes":
                treePredictionList.append(1)
            else:
                treePredictionList.append(0)
        for bagged in baggedList:
            if getBaggingPrediction(bagged, line, header) == "yes":
                baggedPredictionList.append(1)
            else:
                baggedPredictionList.append(0)
        temp = 0
        if line[-1] == "yes":
            temp = 1
        treeBiasList.append((listAverage(treePredictionList) - temp) ** 2)
        treeVarianceList.append(
            getVariance(treePredictionList, listAverage(treePredictionList), 10)
        )
        baggedBiasList.append((listAverage(baggedPredictionList) - temp) ** 2)
        baggedVarianceList.append(
            getVariance(baggedPredictionList, listAverage(baggedPredictionList), 10)
        )
    print("Single trees average bias term: " + str(listAverage(treeBiasList)))
    print("Single trees average variance term: " + str(listAverage(treeVarianceList)))
    print(
        "Single trees average general squared error: "
        + str(listAverage(treeBiasList) + listAverage(treeVarianceList))
    )
    print("Bagged predictors average bias term: " + str(listAverage(baggedBiasList)))
    print(
        "Bagged predictors average variance term: "
        + str(listAverage(baggedVarianceList))
    )
    print(
        "Bagged predictors average general squared error: "
        + str(listAverage(baggedBiasList) + listAverage(baggedVarianceList))
    )
