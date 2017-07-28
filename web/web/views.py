import re

from django.shortcuts import render
from django.http import HttpResponse
from django.conf.urls.static import static

from pymongo import MongoClient 
from urllib.parse import urlparse

def home(request):
	if request.method == 'GET' and 'q' in request.GET:
		print(request.GET)
	else:
		pass

	return render(request, 'home.html', {
		'posts': query()
	})
	
def query():
	# var
	client = MongoClient('127.0.0.1', 27017)
	db = client.dcard

	# auth
	client.dcard.authenticate(
		'dcard', 
		'dcard',
		mechanism='SCRAM-SHA-1'
	)

	title = re.compile(r'#圖', re.I)

	results = db.posts.find({
		'$and': [
			{'title': {'$regex': title}},
			{'likeCount': { '$gt': 1000 }}
		]
	}).limit(50)

	#print(results[0])

	return results