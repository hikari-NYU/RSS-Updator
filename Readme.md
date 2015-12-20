###RSS News Updator
####Weicheng Ma


######Overview:
------
This project aims at managing a set of news coming from certain RSS source(s),
while replacing existing ones with new ones if they are about the same event,
namely, updating the old pieces of news.

######Storage of news separated into three parts:
------
	1. Category table: Traces the file on disk which contains all the stored
	news belonging to each category.
	2. Cache list: Contains recently hit news, given the observation that 
	rapidly changing event turn to get updated more often in a short period.
	3. Disk storage: Storing all the other news, one file per category.

######Training of LDA model and selection of categories:
------
	* Use existing news categories.
	* Get a bunch of news from each category and remove not so usual words.
	* Feed the word sets to LDA model.

######With incoming news:
------
	1. Check cache, if possible match, treat at once and replace.
	2. If not in cache, wait until reach 50 pieces.
	3. After reaching threshold, pause and treat them one by one with access
	of disk.
	4. Put the obsolete news into history tags.

######Update judgment:
------
	1. Select sentences of the same topic as the news with numbers.
	2. Compare overlap with those of all the news in the topic and select the 
	highest match.
	3. If above threshold, is update. Else, not.
	4. Can apply dependency parsing to avoid influence of descriptive words.

######External packages needed:
------
	1. Python LDA model
	2. NLTK package

######Directory structure:
------
	-Scripts
	> *** All script files, dependent files in same directory for convenience ***
	-TrainingData
	> *** News documents separated by topics ***
	-DocumentedNewsByTopic
	> *** News separated by topics. New file every some time and/or some pieces ***
	-CurrentShowCaseByTopic
	> *** Only newest versions from the documented ones. Separated by topics ***

######Use:
----
	1. Build up the formerly mentioned directories.
	2. Implement class ControlPanel with the parameters needed.
	3. Call the jobOn method of the instance.