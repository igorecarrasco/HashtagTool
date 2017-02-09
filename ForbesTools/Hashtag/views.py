from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os
from os.path import join,dirname
from dotenv import load_dotenv,find_dotenv
import urllib2
import oauth2
import json
import datetime
from pprint import pprint

# Create your views here.

dotenv_path = join(dirname(__file__),'..','.env')
load_dotenv(dotenv_path)
csecret = os.getenv('csecret')
ckey = os.getenv('ckey')
ctoken = os.getenv('token')
tokensecret = os.getenv('tokensecret')

def oauth_req(url,key,secret,http_method="GET",post_body="", http_headers=None):
	consumer = oauth2.Consumer(key=ckey,secret=csecret)
	token = oauth2.Token(key=ctoken,secret=tokensecret)
	client = oauth2.Client(consumer,token)
	resp,content = client.request(url,method=http_method,body=post_body,headers=http_headers )
	return content

def index(request):
	template = loader.get_template('Hashtag/index.html')
	return HttpResponse(template.render(request))

def twitter(request):
	hashtag = request.GET.get('hashtag','')
	datestart = request.GET.get('datestart','').split(' ')
	dateend = request.GET.get('dateend','').split(' ')
	since=datestart[0]
	until=dateend[0]
	datetime.datetime
	twitterlist = oauth_req('https://api.twitter.com/1.1/search/tweets.json?q=%23'+hashtag+'%20since%3A'+since+'%20until%3A'+until+'&count=100','', '') 
	data = json.loads(twitterlist)
	statuslist=[]
	statuslist.append(data['statuses'])
	try:
		postcount = len(data['statuses'])
	except KeyError:
		HttpResponse("Number of API requests exceeded. Try again in 15 minutes")
	i=99
	while postcount == 100:
		nextresults = data['search_metadata']['next_results']
		twitterlist = oauth_req('https://api.twitter.com/1.1/search/tweets.json'+nextresults,'', '')
		data = json.loads(twitterlist)
		statuslist.extend(data['statuses'])
		postcount = len(data['statuses'])
		i=i+100
	# each one
	# if created_at
	# print datetime.datetime.strptime("statuslist[0]['created_at']","%a %b %d %H:M:S +0000 %Y")
	with open('data.txt', 'w') as outfile:
		json.dump(statuslist, outfile)
    	print "SUSSA"
	statuses = {'statuslist':statuslist}
	template = loader.get_template('Hashtag/index.html')
	return HttpResponse(template.render(statuses, request))