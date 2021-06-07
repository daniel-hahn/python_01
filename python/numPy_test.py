'''
testing array and vector functionalities with numPy

learned from https://devopscube.com/
'''

import numpy as np

# create array from list and multiply arrays
list1 = [4, 5, 2, 4, 1]
list2 = [3, 9, 6, 7, 4]

arr1 = np.array(list1)
arr2 = np.array(list2)

print(arr1*arr2)

# dimensions and shape of array
array = np.array([
    [1, 2, 3, 5, 6],
    [2, 1, 5, 6, 7]
])

print("dimensions of array: ", array.ndim)
print("structure of array: ", array.shape)

# array from tuple
tuple = (1, 2, 3, 5, 6)
array_2 = np.array(tuple)
print(array_2)

# create zeros array
array = np.zeros((3, 7))
print(array)

# indexing arrays
list = [1, 2, 3, 5, 6]
array = np.array(list)
print(array)

newArray = array[
    np.array([2, 1, 1, 4])
]
print(newArray)

# slicing and indexing of array
array = np.array([
    [4, 4, 7, 6],
    [6, 1, 4, 7],
    [5, 3, 4, 6],
    [1, 1, 3, 5]
])
print(array)

# print first three rows and first columns
print("\n", array[0:3, 0:1])

# print all rows and last column
print("\n", array[:, 3:4])

# string operations
string = "hello world"
print(np.char.upper(string))
print(np.char.split(string, sep=' '))

string1 = "aa"
string2 = "bb"
print(np.char.equal(string1, string2))

# maths functions
x = np.pi
print(np.sin(x))

arr = [.44454, .3456, 1.3]
roundingValues = np.round_(arr, decimals=3)
print(roundingValues)

#natural log
arr = [3, 2, 50]
logArray = np.log(arr)
print(logArray)

#exponential
expArray = np.exp(arr)
print(expArray)

# scalar product
vector_a = 1 + 4j
vector_b = 2 + 8j

vectorProduct = np.dot(vector_a, vector_b)
print("scalar product of vectors: ", vectorProduct)