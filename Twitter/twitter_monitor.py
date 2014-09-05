# -*- coding: UTF-8 -*-

from twython import Twython
from apiclient.discovery import build
import pickle
from pymongo import MongoClient

mongoclient = MongoClient('localhost', 27017)

twitter = Twython('nope', 'nope', 'nope', 'nope')

db = mongoclient['tweets']
posts = db.posts

#Basically the approach here is to insert every tweet into mongo and ignore duplicates.

def fetchTweets(searchtermsfile):
	searchterms = open(searchtermsfile, 'rb')
	for s in searchterms:
		results = twitter.search(q=s.strip(), count=200)
		print len(results['statuses'])
		print 'Fetching tweets for search term: ' + s
		for r in results['statuses']:
			print 'Inserting tweet ' + str(r['id'])
			doc = [{"_id": str(r['id']) + '_' +  s.strip(),  "tweet_data" : r }]
			posts.insert(doc)

fetchTweets('searchterms.txt')

