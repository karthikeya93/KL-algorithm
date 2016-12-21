import numpy as np

'''
This file contains all functions required to run KL Algorithm
'''

def createMatrix(nodes):

	connectivityMatrix = np.zeros((nodes,nodes),dtype=np.uint8)
	return connectivityMatrix

def storeValues(fileArray,connectivityMatrix):

	for line in fileArray:
		nodes = line.split()
		connectivityMatrix[int(nodes[0])-1][int(nodes[1])-1] += 1
		connectivityMatrix[int(nodes[1])-1][int(nodes[0])-1] += 1
	return connectivityMatrix

def createPartitions(numNodes):

	partitionA = np.array(range(0,(numNodes/2)),dtype=np.uint16)
	partitionB = np.array(range((numNodes/2),numNodes),dtype=np.uint16)
	return np.array([partitionA,partitionB],dtype=np.uint16)

def intWeight(numNodes,partitionA,partitionB,matrix):

	weight = np.zeros(numNodes,dtype = np.int8)
	for node in partitionA:
		weight[node] = np.sum(matrix[node][partitionA])
	for node in partitionB:
		weight[node] = np.sum(matrix[node][partitionB])
	return weight

def extWeight(numNodes,partitionA,partitionB,matrix):

	weight = np.zeros(numNodes,dtype = np.int8)
	for node in partitionA:
		weight[node] = np.sum(matrix[node][partitionB])
	for node in partitionB:
		weight[node] = np.sum(matrix[node][partitionA])
	return weight

def Dvalues(IntWt,ExtWt):

	D = np.array(ExtWt - IntWt,dtype = np.int16)
	return D

def updateD (A,B,darray,tempA,tempB,matrix):

	edgesA = np.nonzero(matrix[A])[0]
	edgesAA = np.intersect1d(edgesA,tempA)
	edgesAB = np.intersect1d(edgesA,tempB)
	for i in edgesAA:
		darray[i] = darray[i]+(2*matrix[A][i])
	for j in edgesAB:
		darray[j] = darray[j]-(2*matrix[A][j])
	
	edgesB = np.nonzero(matrix[B])[0]
	edgesBA = np.intersect1d(edgesB,tempA)
	edgesBB = np.intersect1d(edgesB,tempB)
	for k in edgesBB:
		darray[k] = darray[k]+(2*matrix[B][k])
	for l in edgesBA:
		darray[l] = darray[l]-(2*matrix[B][l])
	
	return darray

def calculateK(gainArray) :

	currentGain = 0
	previousGain = 0
	k = 0
	count = 0

	for value in gainArray:
		currentGain += value
		if currentGain > previousGain:
			previousGain = currentGain
			k = count
		count += 1
	if k == 0:
		k = False
	print 'Gain achieved in this pass is ' + str(previousGain)
	return k

def cutSetSize(partA,partB,matrix):

	total = 0
	for node in partA:
		total += int(np.sum(matrix[node][partB]))
	return total
