from Process import *


def ID3(S, Attributes, Label, Depth, KEY):
    if len(Label.values()) < 2:  # if all example have same label
        return Node(Label)  # return a leaf with the label
    elif len(Attributes) < 1 or Depth == 0:  # if Attributes empty
        return Node(mostCommonLabel(Label))
    bestAttribute = bestToSplit(Label, Attributes, KEY)
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
        temp.append(ID3(subData, subAttributes, subLabels, Depth - 1, KEY))
    return root


# set up
version = "TENNIS"
data, testdata = getData(version)
header = getHeader(version)
data.insert(0, header)
attributes, labels = processData(data)
# for i in range(1, 7):
Root = ID3(data, attributes, labels, 5, "IG")
print(Root)
print(predictionError(Root, testdata, header))
