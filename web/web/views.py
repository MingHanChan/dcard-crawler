import re

from django.shortcuts import render
from django.http import HttpResponse

from pymongo import MongoClient 

def home(request):
	# var
	client = MongoClient('127.0.0.1', 27017)
	db = client.dcard

	# auth
	client.dcard.authenticate(
		'dcard', 
		'dcard',
		mechanism='SCRAM-SHA-1'
	)

	target = re.compile(r'#', re.I)

	results = db.posts.find({'title' : {'$regex': target}}).limit(20)

	return render(request, 'home.html', {
		'posts': results
	})