# Python3 program to implement traveling salesman
# problem using naive approach.
from sys import maxsize
from itertools import permutations

V = n

# store all vertex apart from source vertex
vertex = []
for i in range(V):
	if i != s:
		vertex.append(i)

min_path = maxsize
next_permutation=permutations(vertex)
for i in next_permutation:
	current_pathweight = 0
	k = s
	for j in i:
		current_pathweight += graph[k][j]
		k = j
	current_pathweight += graph[k][s]
	min_path = min(min_path, current_pathweight)