import os
import statistics
from math import log2


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
        return getDataFromPath("DataSets/bank-4/train.csv"), getDataFromPath(
            "DataSets/bank-4/test.csv"
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


def predictionError(Node, data, header):
    count = 0
    for line in data:
        prediction = getPrediction(Node, line, header)
        actual = line[len(line) - 1]
        if prediction != actual:
            count += 1
    return count / len(data)


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
