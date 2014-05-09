#!/usr/bin/python
# coding: utf-8

#A simple search data from Twitter API1.1
#Store and retrieve the collected info as json

#Configure the access type and get the OAuth settings
#https://dev.twitter.com/

import json
import nltk
import twitter

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

t = twitter.Twitter(auth=auth)

with open('tweets.txt', 'w') as outfile:
    data = json.dump(t.search.tweets(q='@fisl_oficial'), outfile, indent=4)

data = json.loads(open('tweets.txt').read())

tweets = []
for x in range(0, len(data['statuses'])): 
	tweets.append(data['statuses'][x]['text'])

words = []
for t in tweets:
	words += [w for w in t.split()]

print 'Numero de tweet: %d' %(len(tweets))
print 'Lista de Tweets:'
print '\n\n'.join(tweets)

#Frequency analyses and Lexical diversty
print 'Qunatidade de palavras: %d' %(len(words))      #words
print 'Quantidade de palavras unicas: %d' %(len(set(words))) #unique words
print 'Diversidade lexica: %f' %(1.0*len(set(words))/len(words))  #lexical diversity
print 'Media de palavras por tweet: %d' %(+1.0*sum([ len(t.split()) for t in tweets ])/len(tweets)) #avarange words/tweet

freq_dist = nltk.FreqDist(words)
print 'Palavras mais frequentes: '
print ', '.join(freq_dist.keys()[:50])   #50 most frequent words 
print 'Palavras menos frequentes: '
print ', '.join(freq_dist.keys()[-50:])  #50 less frequent words
