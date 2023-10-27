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
while True:
    version = input(
        "Which Dataset you want? Bank or Car? Enter exit to quit.\n"
    ).upper()
    if version == "EXIT":
        exit(0)
    if version != "BANK" and version != "CAR":
        print("Wrong input, try again.\n")
        continue
    data, testdata = getData(version)
    depth = 6
    if version == "BANK":
        depth = 16
        processBank(data)
        processBank(testdata)
        unknown = input("Replace Unknown? Yes or No\n").upper()
        if unknown != "YES" and unknown != "NO":
            print("Wrong input, try again.\n")
            continue
        if unknown == "YES":
            unknownProcess(data)
            unknownProcess(testdata)
    traindata = data.copy()
    header = getHeader(version)
    data.insert(0, header)
    attributes, labels = processData(data)
    split = input(
        "How to pick best attribute to split? Enter IG for informtaion gain, ME for majority error and GI for gini index.\n"
    ).upper()
    if split != "IG" and split != "ME" and split != "GI":
        print("Wrong input, try again.\n")
        continue
    print("Training Errors:")
    for i in range(1, int(depth) + 1):
        Root = ID3(data, attributes, labels, i, split)
        print(Root)
        print(str(i) + ": " + str(predictionError(Root, traindata, header)))
    print("Test Errors:")
    for i in range(1, int(depth) + 1):
        Root = ID3(data, attributes, labels, i, split)
        # print(Root)
        print(str(i) + ": " + str(predictionError(Root, testdata, header)))
