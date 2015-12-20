###############################################
#Checks file from disk.########################
#Replace if correct one found.#################
#@Input: Topic, ListOfNews, CharacterSentences#
#@Output: void#################################
###############################################

import os.path
import NewsWrapper
from NewsSimilarityComputation import simCal
import re
import unicodedata
import json

#Try to open the document of certain topic.
#Returns true if file exists.
#Otherwise return false.
#@Input: topic:string, topic of news
#@Output: True/False
def checkTopicExistence(topic):
	try:
		f=open('/Users/weichengma/LabWork/NYU/RSS Updator/DocumentedNewsByTopic/'+topic,'r')
		return True
	except:
		return False

#Checks whether anything in the incoming list is an update to a documented news
#If so, update the file. Otherwise simply insert
#@Input: newsList:list(news), the incoming news; topic:string, the topic of the whole set
#@Output: file written on disk.
def checkUpdateFromDisk(obsoleteList,newsList, topic):
	threshold=0.9
	#If topic not existing, create new file
	#In JSON format
	if checkTopicExistence(topic)==False:
		newsMap={}
		for i in range(len(newsList)):
			news=newsList[i]
			newsElem={}
			newsElem['title']=news.getTitle()
			newsElem['content']=news.getContent()
			newsElem['charactervecs']=news.getCharVec()
			newsElem['topic']=topic
			newsElem['_obsolete']=obsoleteList[i]
			newsMap[i]=newsElem
		#Insert all news into new topic file, return
		with open('/Users/weichengma/LabWork/NYU/RSS Updator/DocumentedNewsByTopic/'+topic,'w') as fs:
			json.dump(newsMap,fs)
		fs.close()
		return
	#Otherwise if existed, read the data in, compare similarity and update
	with open('/Users/weichengma/LabWork/NYU/RSS Updator/DocumentedNewsByTopic/'+topic,'r') as fs:
		history=json.load(fs)
	for i in range(len(newsList)):
		news=newsList[i]
		#Check with all documented news
		maxSim=0.0
		maxSimPos=-1
		for oldNewsid in history:
			simTmp=history[oldNewsid]['charactervecs']
			if simTmp==None:
				continue
			simTmp=simTmp.split('#')
			simTmp=simCal(simTmp,news.getCharVec().split('#'))
			if maxSim<simTmp:
				maxSim=simTmp
				maxSimPos=oldNewsid
		#Replace the one with highest similarity and over threshold
		if maxSim>threshold:
			history[maxSimPos]['_obsolete'].append(history[maxSimPos])
			history[maxSimPos]['_obsolete'].extend(obsoleteList[i])
			history[maxSimPos]['title']=news.getTitle()
			history[maxSimPos]['content']=news.getContent()
			history[maxSimPos]['charactervecs']=news.getCharVec()
			history[maxSimPos]['topic']=topic
		#Otherwise add a new entry to history
		else:
			newsTmp={}
			newsTmp['_obsolete']=obsoleteList[i]
			newsTmp['title']=news.getTitle()
			newsTmp['content']=news.getContent()
			newsTmp['charactervecs']=news.getCharVec()
			newsTmp['topic']=topic
			history[max(history)+1]=newsTmp
	#Write out the file, overwrite
	with open('/Users/weichengma/LabWork/NYU/RSS Updator/DocumentedNewsByTopic/'+topic, 'w') as fs:
		json.dump(history,fs)
	fs.close()