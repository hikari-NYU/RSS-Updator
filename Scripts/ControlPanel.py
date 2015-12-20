##################################################
#Gets RSS updates from API, ######################
#Checks duplication, #############################
#Checks cache hit, ###############################
#Then write to disk when reaching certain amount.#
##################################################

import feedparser
from goose import Goose
import NewsWrapper
import CheckUpdateFromDisk
import numpy
import gensim
import time
import re
import CacheAsQueue as cache

class ControlPanel:

	def __init__(self, source, timeInterval=1, cacheSize=100, threshold=0.9):
		self.NEWSPOOL=[]
		self.SOURCE=source
		self.TIMEINTERVAL=timeInterval
		self.THRESHOLD=threshold
		self.CACHE=cache.CacheAsQueue()
		self.MODEL=gensim.models.LdaModel.load('../TrainingData/news.lda')
		self.CORPUS=gensim.corpora.MalletCorpus('../TrainingData/training.mallet')
		self.ID2WORD=gensim.corpora.Dictionary()
		_=self.ID2WORD.merge_with(self.CORPUS.id2word)
		self.HASNUM=re.compile('[0-9]+[.]*[0-9]*')

	#Central command of the system
	#Loads RSS feeds every 300s after the last round
	def jobOn(self):
		g=Goose()
		newsList=[]
		while True:
			data=feedparser.parse(self.SOURCE)
			for post in data.entries:
				links=post['links']
				content=''
				for link in links:
					content=content+g.extract(url=link['href']).cleaned_text
				content=content.encode('utf8')
				#charaVec, topic from LDA
				query=content.split()
				query=self.ID2WORD.doc2bow(query)
				topic=list(sorted(self.MODEL[query], key=lambda x: x[1]))[-1][0]
				topic=self.MODEL.print_topic(topic)
				topic=topic.split()[0].split('*')[1]
				sentences=re.split('[.?!]+',content)
				charaVec=''
				for sentence in sentences:
					query=sentence.split()
					query=self.ID2WORD.doc2bow(query)
					sTopic=list(sorted(self.MODEL[query], key=lambda x: x[1]))[-1][0]
					sTopic=self.MODEL.print_topic(sTopic)
					sTopic=sTopic.split()[0].split('*')[1]
					hasNum=self.HASNUM.search(sentence)
					if sTopic==topic and hasNum!=None:
						charaVec=charaVec+sentence+'#'
				print charaVec
				news=NewsWrapper.NewsWrapper(post.title, content, charaVec, topic)
				#Cache-hit news updated by the cache class
				self.CACHE.add(news)
				#Write the news to disk
				if self.CACHE.size()>100:
					#When new news reach a certain number, write them to disk
					topics=self.CACHE.getTopics()
					for topic in topics:
						newsList=self.CACHE.getNews(topic)
						CheckUpdateFromDisk.checkUpdateFromDisk(newsList['_obsolete'],newsList['_new'],topic)
					self.CACHE.clear()
			#Sleep to wait for reading next feed
			time.sleep(300)