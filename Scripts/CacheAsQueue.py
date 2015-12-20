####################################################
# This program is for caching newly came news. #####
# Once detected as an update to an existing piece, #
# Move the original to obsolete. ###################
####################################################

from NewsSimilarityComputation import simCal
import CheckUpdateFromDisk

class CacheAsQueue:
	NewsMap={}
	def __init__(self,size=100):
		self.threshold=0.7

	#Adds news to storage.
	#If detected as update, update in memory.
	#@Input: news:NewsWrapper
	def add(self,news):
		topic=news.getTopic()
		try:
			newsList=self.NewsMap[topic]['_new']
			maxSim=0.0
			maxId=-1
			#Traverse existing news for similarity
			for i in range(len(newsList)):
				oldNews=newsList[i]
				sim=simCal(news.getCharVec(),oldNews.getCharVec())
				if sim>maxSim:
					maxSim=sim
					maxId=i
			if maxSim>self.threshold:
				#The new piece is an update
				#Move the most similar one to its obsolete list
				#Put new piece in position.
				self.NewsMap[topic]['_obsolete'][maxId].append(NewsMap[topic]['_new'][maxId])
				self.NewsMap[topic]['_new'][maxId]=news
		except:
			#If current topic not exists, create one and add the news to it.
			self.NewsMap[topic]={'_obsolete':[[]],'_new':[news]}

	#Returns currently existing topics in cache
	#@Output: list(string):topics
	def getTopics(self):
		return [val for val in self.NewsMap]

	#Returns all news under certain topic
	#@Input: topic:string:Topic
	#@Output: dict:news and obsolete versions
	def getNews(self,topic):
		return self.NewsMap[topic]

	#Returns current number of original news
	#@Output: size:integer:number of original news
	def size(self):
		size=0
		for topic in self.NewsMap:
			size+=len(self.NewsMap[topic]['_new'])
		return size

	#Removes all entries in cache
	def clear(self):
		self.NewsMap={}