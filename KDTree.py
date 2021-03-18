import numpy as np
import matplotlib.pyplot as plt
from time import time


def createKDTree(dataSet, depth):
    n = np.shape(dataSet)[0]
    treeNode = {}
    if n == 0:
        return None
    else:
        n, m = np.shape(dataSet)
        split_axis = depth % m
        depth += 1
        treeNode['split'] = split_axis
        dataSet = sorted(dataSet, key=lambda a: a[split_axis])
        num = n // 2
        treeNode['median'] = dataSet[num]
        treeNode['left'] = createKDTree(dataSet[:num], depth)
        treeNode['right'] = createKDTree(dataSet[num + 1:], depth)
        return treeNode


def searchTree(tree, data):
    k = len(data)
    if tree is None:
        return [0] * k, float('inf')
    split_axis = tree['split']
    median_point = tree['median']
    if data[split_axis] <= median_point[split_axis]:
        nearestPoint, nearestDistance = searchTree(tree['left'], data)
    else:
        nearestPoint, nearestDistance = searchTree(tree['right'], data)
    nowDistance = np.linalg.norm(data - median_point)  # the distance between data to current point
    if 0 < nowDistance < nearestDistance:
        nearestDistance = nowDistance
        nearestPoint = median_point.copy()
    splitDistance = abs(data[split_axis] - median_point[split_axis])  # the distance between hyperplane
    if splitDistance > nearestDistance > 0:
        return nearestPoint, nearestDistance
    else:
        if data[split_axis] <= median_point[split_axis]:
            nextTree = tree['right']
        else:
            nextTree = tree['left']
        nearPoint, nearDistance = searchTree(nextTree, data)
        if nearestDistance > nearDistance > 0:
            nearestDistance = nearDistance
            nearestPoint = nearPoint.copy()
        return nearestPoint, nearestDistance
