import numpy as np
import KLfunctions as KL
'''
This file contains KL Algorithm function definition
'''

def algorithm (matrix,nodes,partA,partB,darray):
	tempA = partA #Temporary copy to mainpulate partition
	tempB = partB
	
	queueA = np.array([],dtype=np.uint16) #Queue in which nodes must be swapped
	queueB = np.array([],dtype=np.uint16)
	gainArray = np.array([],dtype=np.int16) #Gain queue
	
	K = True
	passCount = 1
	while(K):
		print '---------------------------------------------'
		print 'Pass ' + str(passCount)
		while(len(tempA) != 0):
			DA = darray[tempA]
			DB = darray[tempB]
			DAmaxInd = np.argmax(DA)
			DBmaxInd = np.argmax(DB)
			DAmax = DA[DAmaxInd]
			DBmax = DB[DBmaxInd]
			d = DAmax + DBmax
			Amax = tempA[DAmaxInd]
			Bmax = tempB[DBmaxInd]
			queueA = np.array(np.append(queueA,[Amax]),dtype=np.uint16)
			queueB = np.array(np.append(queueB,[Bmax]),dtype=np.uint16)
			gain = d - 2*matrix[Amax][Bmax]
			gainArray = np.array(np.append(gainArray,gain),dtype=np.int8)
			darray = KL.updateD(Amax,Bmax,darray,tempA,tempB,matrix) #Update D values
			tempA = np.delete(tempA,[DAmaxInd])
			tempB = np.delete(tempB,[DBmaxInd])
		
		K = KL.calculateK(gainArray)
		if K == False: #If condition is true, that means no more optimization possible
			print '0 Nodes swapped in this pass'
			print '---------------------------------------------'
			print '\n'
			break
			
		print str(K) + ' Nodes swapped in this pass'
		partA = np.setdiff1d(partA,queueA[0:K+1]) #Remove nodes of queueA from A
		partB = np.setdiff1d(partB,queueB[0:K+1])
		partA = np.append(partA,queueB[0:K+1]) #Add nodes of queueB to remaining A
		partB = np.append(partB,queueA[0:K+1])
	
		intWt = KL.intWeight(nodes,partA,partB,matrix)
		extWt = KL.extWeight(nodes,partA,partB,matrix)
		darray = KL.Dvalues(intWt,extWt)
		
		tempA = partA
		tempB = partB
		
		queueA = np.array([],dtype=np.uint16)
		queueB = np.array([],dtype=np.uint16)
		gainArray = np.array([],dtype=np.int16)
		passCount += 1
	
	cutsetsize = KL.cutSetSize(partA,partB,matrix)
	return (cutsetsize,partA,partB)

