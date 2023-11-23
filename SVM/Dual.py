import os
from scipy.optimize import minimize
import numpy as np


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
    for line in data:
        if line[-1] == str(0):
            line[-1] = -1
        else:
            line[-1] = 1
    return data
