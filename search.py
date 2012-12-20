#!/usr/bin/python

import urllib
import json as simplejson
import re
import sys
#import nltk
#from nltk import FreqDist, WordPunctTokenizer


def searchTweets(query):
	# search is a string in json format returned by twitter search API
	search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
	# dict is a dictionary created by parsing the search string
	# all tweets are in dict["result"], which is a list of dictionaries
	dict = simplejson.loads(search.read())
	#for result in dict["results"]:
	#    print "*",result["text"],"\n"
	return dict["results"]

def getBuzz(tweetList):
	regSplit = '[\s!@#\$%\^&*\(\).\?\"\"\'\':;/]+'
	# nltk's stopset (static because requires installation)
	stopset = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'];
	# Get all words in the tweetlist
	wordsCleaned = []
	for tweet in tweetList:
		words = re.split(regSplit, tweet["text"])
		#print tweet["text"].encode('utf-8'), words
		wordsCleaned += [word.lower() for word in words if word.lower() not in stopset and len(word) > 2 ]

	# Calc frequency distribution of each word	
	distrib = dict()
	for word in wordsCleaned:
		if word not in distrib:
			distrib[word] = 0		
		else:
			count = distrib[word]
			count += 1
			distrib[word] = count
	
	#print distrib

	# Using distrib, get the tweet with the highest 'score'
	maxScore = 0
	buzz = tweetList[0]
	for tweet in tweetList:
		score = 0
		words = re.split(regSplit, tweet["text"])
		wordsCleaned += [word.lower() for word in words if word.lower() not in stopset and len(word) > 2 ]
		for word in wordsCleaned:
			score += distrib[word]
		if score > maxScore:
			maxScore = score
			buzz = tweet
	
	return buzz
				
	
		

if __name__ == '__main__':
    searchTweets(sys.argv[1])
