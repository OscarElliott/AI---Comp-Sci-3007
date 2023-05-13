#import relevant libraries
import sys
import numpy as np
import pandas as pd
from node1 import Node


# function for distance
def distance(point1, point2):
    return np.sqrt(np.sum((np.array(point1) - np.array(point2))**2))

# function for building the Kd-tree
def BuildKdTree(points, depth=0):
    P_points = len(points) # amount of rows
    if P_points == 0:
        return None
    elif P_points == 1:
        # get no of cols
        M_dimension = len(points[0])
        # only one point left so val = current dimension of only point
        return Node(points[0], depth % M_dimension, points[0][depth % M_dimension])
    # get no of cols
    M_dimension = len(points[0])-1 # fixing indexing?
    # get current dimension
    axis = (depth) % M_dimension
    # sort points based on axis value so we can find median
    sorted_points = sorted(points, key=lambda point: point[axis])
    median_index = P_points // 2
    median_value = sorted_points[median_index][axis]
    median_point = sorted_points[median_index]

    # create nodes for left and right subtrees
    left = BuildKdTree(sorted_points[:median_index], depth + 1)
    right = BuildKdTree(sorted_points[median_index+1:], depth + 1)
    # create node for current point
    return Node(median_point, axis, median_value, left, right)
    

# lowerbound distance function
def distance_lb(query_point, point, axis):
    distance = abs(point[axis]-query_point[axis])
    return distance

# function for searching the Kd-tree
def nn_search(node, point, closest=None):
    if node is None:
        return closest
    # check if current distance is smaller then closest distance
    if closest is None or distance(point, node.point[:11,]) < distance(point, closest[:11,]):
        closest = node.point

    if point[node.axis] <= node.median_val:
        next_node = node.left
        opposite_node = node.right
    else:
        next_node = node.right
        opposite_node = node.left

    closest = nn_search(next_node, point, closest)

    if opposite_node is not None and (closest is None or distance_lb(point, opposite_node.point[:11,], node.axis) < distance(point, closest[:11,])):
        closest = nn_search(opposite_node, point, closest)

    return closest
    


if __name__ == '__main__':
    train = sys.argv[1]
    testfile = sys.argv[2]
    min_dimension = int(sys.argv[3])

    #import datasets
    train_df = pd.read_csv(train, delimiter='\s+')
    test_df = pd.read_csv(testfile, delimiter='\s+')

    # get the list of attributes from the test data frame
    test_attributes = test_df.columns.tolist()
    #print(test_attributes[:11]) # prints the first five attributes in the list

    # extract training points and build kd_tree from the chosen dimension
    training_points = train_df.values[:, :]
    Kd_tree = BuildKdTree(training_points, min_dimension)

    # predict quality ratings of wine for each test point
    predicted_ratings = []
    for i in range(len(test_df)):
        query_point = np.array(test_df.values[i, :])
        nearest_neighbor = nn_search(Kd_tree, query_point)
        predicted_ratings.append(int((nearest_neighbor[-1])))
    


    # print the predicted quality ratings vertically
    print('\n'.join(str(j) for j in predicted_ratings))