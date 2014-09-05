# -*- coding: UTF-8 -*-

import networkx as nx
from twython import Twython
import pickle
import time

twitter = Twython('nope', 'nope', 'nope', 'nope')

def followers_list(screenname):
	followers = list()
	followerslist = twitter.get_followers_list(screen_name=screenname, count=200)
	for f in followerslist['users']:
		followers.append(f['screen_name'])
	while followerslist['next_cursor_str'] != '0' and not len(followers) >= 1000:
		time.sleep(65)
		followers_list = twitter.get_followers_list(screen_name=screenname, count=200, cursor=followerslist['next_cursor_str'])
		for f in followers_list['users']:
			followers.append(f['screen_name'])
	return followers
	

def friends_list(screenname):
	friends = list()
	friendslist = twitter.get_friends_list(screen_name=screenname, count=200)
	for f in friendslist['users']:
		friends.append(f['screen_name'])
	while friendslist['next_cursor_str'] != '0' and not len(friends) >= 10000:
		time.sleep(65)
		friendslist = twitter.get_friends_list(screen_name=screenname, count=200, cursor=friendslist['next_cursor_str'])
		for f in friendslist['users']:
			friends.append(f['screen_name'])
	return friends


def createTopicGraph(data, topic):
	logfile = open('graphlog.txt', 'wb')
	g = nx.Graph()
	logfile.write('Creating initial set of nodes...\n')
	for i, tweet in data[topic].iteritems():
		g.add_node(tweet['user']['screen_name'])
		logfile.write('Added node ' + tweet['user']['screen_name'] + '\n')
	seeds = g.nodes()
	for n in seeds:
		time.sleep(65)
		followers = followers_list(n)
		friends = friends_list(n)
		logfile.write('Adding the followers of ' + str(n) + '\n')
		for follower in followers:
			g.add_node(follower)
			logfile.write('Added node ' + str(follower) + '\n')
			g.add_edge(u=follower, v=n)
			logfile.write('Added a connection between ' + str(follower) + ' and ' + str(n) + '\n')
		logfile.write('Adding the friends of ' + str(n) + '\n')
		for friend in friends:
			g.add_node(friend)
			logfile.write('Added node ' + str(friend) + '\n')
			g.add_edge(u=n, v=friend)
			logfile.write('Added a connection between ' + str(n) + ' and ' + str(friend) + '\n')
	logfile.write('YAY, COMPLETED GRAPH!!!!\n')
	return g

tweetdata = pickle.load(open('copiedtweets.dat', 'rb'))
#print friends_list('michaelgrube')
g = createTopicGraph(tweetdata, 'ISIS')
pickle.dump(g, open('completegraph.dat', 'wb'))
