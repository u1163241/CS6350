from Process import *


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


# set up
version = "CAR"
data, testdata = getData(version)
traindata = data.copy()
header = getHeader(version)
data.insert(0, header)
attributes, labels = processData(data)
Root = ID3(data, attributes, labels, 4, "IG")
for i in range(1, 7):
    Root = ID3(data, attributes, labels, i, "IG")
    # print(Root)
    print(predictionError(Root, testdata, header))
