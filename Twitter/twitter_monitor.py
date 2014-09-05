# -*- coding: UTF-8 -*-

from twython import Twython
from apiclient.discovery import build
import pickle
from pymongo import MongoClient

mongoclient = MongoClient('localhost', 27017)

twitter = Twython('nope', 'nope', 'nope', 'nope')

collection = mongoclient

def updateResults(datafile):
	allresults = pickle.load(open(datafile, 'wb'))
	for s in allresults.keys():
		results = twitter.search(q=s.strip(), count=200)
		print 'Fetching tweets for search term: ' + s
		for r in results['statuses']:
			allresults[s][r['id']] = r
	pickle.dump(allresults, open(datafile, 'wb'))


def generateResults(searchtermsfile):
	resultsdict = dict()
	searchterms = open(searchtermsfile, 'rb')
	for s in searchterms:
		resultsdict[s.strip()] = dict()
		results = twitter.search(q=s.strip(), count=200)
		print 'Fetching tweets for search term: ' + s
		for r in results['statuses']:
			resultsdict[s.strip()][r['id']] = r
	return resultsdict
