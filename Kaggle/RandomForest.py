import os
import statistics
from math import log2
import random
import numpy as np


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


def getData():
    return getDataFromPath("Data/train_final.csv"), getDataFromPath(
        "Data/test_final.csv"
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


def predictionError(data, header, rootList):
    count = 0
    for line in data:
        prediction = getBaggingPrediction(rootList, line, header)
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


def RandTreeLearn(S, Attributes, Label, Depth, KEY, featureSize):
    bestAttribute = ""
    if len(Attributes) > featureSize:
        randomAttributes = {}
        randomLable = {}
        AttributesCopy = Attributes.copy()
        for i in range(featureSize):
            pick = random.randint(0, len(AttributesCopy) - 1)
            newRandom = AttributesCopy[list(AttributesCopy.keys())[pick]]
            randomAttributes[list(AttributesCopy.keys())[pick]] = newRandom
            del AttributesCopy[list(AttributesCopy.keys())[pick]]
        for attribute in randomAttributes.values():
            for label in attribute.values():
                for key, value in label.items():
                    if key not in randomLable:
                        randomLable[key] = 0
                    randomLable[key] += value
        bestAttribute = bestToSplit(randomLable, randomAttributes, KEY)
    else:
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
        if len(subLabels.values()) > 1 and (Depth - 1) != 0 and len(subAttributes) > 0:
            temp = []  # continue branch on child node
            child.branch = temp
            temp.append(
                RandTreeLearn(
                    subData, subAttributes, subLabels, Depth - 1, KEY, featureSize
                )
            )
    return root


# set up
data, testdata = getData()
for line in data:
    del line[13]
    del line[12]
    del line[11]
    del line[10]
    del line[4]
    del line[2]
    del line[0]
print(data[0])
for line in testdata:
    del line[14]
    del line[13]
    del line[12]
    del line[11]
    del line[5]
    del line[3]
    del line[1]
    del line[0]
print(testdata[0])
header = data[0]

list1 = []
list0 = []
# balance data
for line in data:
    if line[-1] == str(1):
        list1.append(line)
    else:
        list0.append(line)
for line in list1:
    data.append(line)
    data.append(line)

rootList = []
for T in range(50):
    sample = []
    sample.insert(0, header)
    for i in range(len(data)):
        pick = random.randint(1, len(data) - 2)
        sample.append(data[pick])
    attributes, labels = processData(sample)
    Root = RandTreeLearn(sample, attributes, labels, 3, "IG", 3)
    rootList.append(Root)

    error = predictionError(data[1:], header, rootList)
    print(str(T + 1) + " Training Error: " + str(error))

# ouput csv file
predictionList = []
for i in range(len(testdata)):
    if i == 0:
        predictionList.append(["ID", "Prediction"])
        continue
    line = testdata[i]
    prediction = getBaggingPrediction(rootList, line, header)
    predictionList.append([i, prediction])
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Prediction.csv")
np.savetxt(path, predictionList, delimiter=", ", fmt="% s")
