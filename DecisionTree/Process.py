import os
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


def getData(KEY):
    if KEY == "CAR":
        return getDataFromPath("DataSets/car-4/train.csv"), getDataFromPath(
            "DataSets/car-4/test.csv"
        )
    if KEY == "TENNIS":
        return getDataFromPath("DataSets/train.csv"), getDataFromPath(
            "DataSets/test.csv"
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


def mostCommonLabel(Label):
    max = -1
    maxIndex = 0
    for i in range(len(Label)):  # return most commom label
        current = list(Label.values())[i]
        maxIndex, max = ((maxIndex, max), (i, current))[current > max]
    return {list(Label)[maxIndex]: max}


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
        current = round(purity(labels, attributes[attribute], KEY), 3)
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
    index = -1
    if len(node.branch) == 0:  # the prediction
        return current
    elif current in header:
        index = header.index(current)
        if node.contain(line[index]):
            return getPrediction(node.contain(line[index]), line, header)
        else:  # most common value
            max = float("-inf")
            returnLabel = ""
            label = list(node.label.values())[0]
            for currentLable, currentValue in label.items():
                if currentValue > max:
                    currentValue = max
                    returnLabel = currentLable
            return getPrediction(Node({returnLabel: currentValue}), line, header)
    else:
        return getPrediction(node.branch[0], line, header)
