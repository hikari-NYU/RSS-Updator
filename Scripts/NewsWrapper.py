#####################################################
# Class for storing information of a piece of news. #
# Provides interfaces to get the information. #######
#####################################################

class NewsWrapper:
	title=None
	content=None
	charactervecs=[]
	topic=None
	def __init__(self, title, content, charactervecs, topic):
		self.title=title
		self.content=content
		self.charactervecs=charactervecs
		self.topic=topic

	#Returns the title of the news
	#@Output: title:string:title
	def getTitle(self):
		return self.title

	#Returns the content of the news
	#@Output: content:string:content
	def getContent(self):
		return self.content

	#Returns the character words of the news
	#Output: charactervecs:list(string):character words
	def getCharVec(self):
		return self.charactervecs

	#Returns the topic of the news
	#Output: topic:string:topic
	def getTopic(self):
		return self.topic