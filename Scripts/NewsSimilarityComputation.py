#####################################################
#Returns the similarity of a given pair of tweets####
#@Input: Two vectors of characteristic sentences#####
#@Output: Similarity of the two vectors##############
#Criteria: Count of similar sentence pairs###########
#Criteria2: Sum of similarities of similar sentences#
#over threshold######################################
#####################################################

#Public interface for similarity calculation.
#@Input: charvecs1:list(string):paragraph1; charvecs2:list(string):paragraph2
#@Output: similarity of two sentences in range [0.0,1.0]
def simCal(charvecs1, charvecs2):
	Len1=len(charvecs1)
	Len2=len(charvecs2)
	#Go through each possibility
	SimilarityMatrix=[[None]*Len1]*Len2
	for i in range(Len1):
		sent1=charvecs1[i]
		for j in range(Len2):
			sent2=charvecs2[j]
			SimilarityMatrix[i][j]=sentSimCal(sent1,sent2)
	SimVec=[]
	while(len(SimVec)<min(Len1,Len2)):
		maxSim=0
		maxRow=0
		maxColumn=0
		#Find local maximum and store
		for i in range(Len2):
			for j in range(Len1):
				if maxSim<SimilarityMatrix[i][j]:
					maxSim=SimilarityMatrix[i][j]
					maxRow=i
					maxColumn=j
		SimVec.append(maxSim)
		#Remove all elements in the same column or row as local maximum 
		#To make one sentence assigned to at most one sentence
		for i in range(Len2):
			SimilarityMatrix[i][maxColumn]=0
		for j in range(Len2):
			SimilarityMatrix[maxRow][j]=0
	threshold=0.7
	#Remove pairs not so similar to each other
	for i in range(len(SimVec)):
		if SimVec[i]<threshold:
			SimVec[i]=0
	simSents=0
	for i in range(len(SimVec)):
		if SimVec[i]!=0:
			simSents=simSents+1
	#Even if same similarity, the more similar sentences the higher the score.
	return (simSents*1.0/len(SimVec))*sum(SimVec)

#Calculation of sentence similarity by word count using sliding windows of size 3.
#@Input: sent1:string:sentence1; sent2:string:sentence2
#@Output: sentSim:double:sentence similarity in range [0.0,1.0]
def sentSimCal(sent1,sent2):
	'''Bag of words, check for same words only.
	May later apply similar word comparison.
	Should choose from Word2Vec or Wordnet.'''
	sentSim=0
	#len(sent1)-2 windows of size 3
	for i in range(len(sent1)-2):
		tripleSim=0
		#len(sent2)-2 windows of size 3
		for j in range(len(sent2)-2):
			simTmp=0
			for k in range(3):
				if sent1[i+k]==sent2[j] or sent1[i+k]==sent2[j+1] or sent1[i+k]==sent2[j+2]:
					simTmp=simTmp+1
			if tripleSim<simTmp:
				tripleSim=simTmp
		#Each element calculated 3 times in total roughly
		sentSim=sentSim+tripleSim*1.0/3.0
	return sentSim