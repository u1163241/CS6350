from Process import *

attributes = {}
labels = {}
data = getData("DataSets/car-4/train.csv")
header = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "label"]
data.insert(0, header)
attributes, labels = processData(data)


def ID3(S, Attributes, Label, Depth):
    if len(Label.values()) < 2:  # if all example have same label
        return Node(list(Label)[0])  # return a leaf with the label
    elif len(Attributes) < 1 or Depth == 0:  # if Attributes empty
        return Node(
            list(Label)[mostCommonLabelIndex(Label)]
        )  # return most commom label
    bestAttribute = bestToSplit(
        Label, Attributes, "IG"
    )  # depend on different implementation
    root = Node(Attributes[bestAttribute])  # current root node
    childList = []  # branch
    root.label = bestAttribute  # current label
    root.branch = childList
    for attribute in Attributes[bestAttribute]:  # split each attribute value
        subData = []
        for row in range(len(S)):
            line = S[row].copy()
            if row == 0:  # header
                line.remove(bestAttribute)
                subData.append(line)
            else:  # subdata
                if attribute in line:
                    line.remove(attribute)
                    subData.append(line)
        subAttributes, subLabels = processData(subData)  # process new data
        child = Node(attribute)
        childList.append(child)  # connect each child node to current
        temp = []  # continue branch on child node
        child.branch = temp
        temp.append(ID3(subData, subAttributes, subLabels, Depth - 1))
    return root


Root = ID3(data, attributes, labels, 2)
printNode(Root)
