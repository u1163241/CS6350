import os
from math import log2


class Node:
    def __init__(self, lable):
        self.label = lable
        self.branch = {}


def printNode(root: Node, level=0):
    print("\t" * level + root.label)
    for child in root.branch:
        printNode(child, level + 1)


def getData(path: str):
    data = []
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), path), "r"
    ) as file:
        for line in file:
            terms = line.strip().split(",")
            data.append(terms)
    return data


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


def mostCommonLabelIndex(Label):
    max = -1
    maxIndex = 0
    for i in range(len(Label)):  # return most commom label
        current = list(Label.values())[i]
        maxIndex, max = ((maxIndex, max), (i, current))[current > max]
    return maxIndex


def Entropy(labels, KEY):
    total = 0
    returnNumber = 0
    min = float("inf")
    for count in labels.values():
        total += count
    for count in labels.values():
        if KEY == "IG":
            returnNumber -= (count / total) * log2(count / total)
        if KEY == "ME":
            returnNumber += (count / total) * (count / total)
    return total, returnNumber


def IG(labels, attributes, KEY):
    total, totalEntropy = Entropy(labels, KEY)
    sumEntropy = 0
    for attribute in attributes:
        subTotal, subEntropy = Entropy(attributes[attribute], KEY)
        sumEntropy += (subTotal / total) * subEntropy
    return totalEntropy - sumEntropy


def bestToSplit(labels, attributes, KEY):
    best = ""
    max = 0
    for attribute in attributes:
        current = IG(labels, attributes[attribute], KEY)
        best, max = ((best, max), (attribute, current))[current >= max]
    return best
