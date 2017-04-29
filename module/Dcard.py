import os
import json
import requests
import datetime

# customized module
from . import Thread

# constant
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# global
db = []

class Object:
	def __init__(self, var):
		self.content = None
		self.comments = None
		for key in var.keys():
			setattr(self, key, var[key])

def get_content(id):
	try:
		_request = requests.get('https://www.dcard.tw/_api/posts/%s' % id)
		_response = json.loads(_request.text)
		return _response
	except Exception as e:
		print('[%10s] %s' % ('api', str(e)))
		return None

def get_comments(id):
	try:
		_request = requests.get('https://www.dcard.tw/_api/posts/%s/comments' % id)
		_response = json.loads(_request.text)
		return _response
	except Exception as e:
		print('[%10s] %s' % ('api', str(e)))
		return None

def get_posts(alias, payload):
	try:
		_request = requests.get('https://www.dcard.tw/_api/forums/' + alias + '/posts', params=payload)
		_response = json.loads(_request.text)
		return _response
	except Exception as e:
		print('[%10s] %s' % ('api', str(e)))
		return None

def init_forum(var):
	print('[%10s] %s' % (var['forumAlias'], 'init'))

	# var
	_index = var['latest']
	_max = max([i['id'] for i in get_posts(var['forumAlias'], {'popular': 'false'})])

	print(_index, _max)

	while _index < _max:
		posts = [Object(i) for i in get_posts(var['forumAlias'], {
			'popular': 'false',
			'after': _index
		})]

		# add to queue
		list(map(Thread.q.put, posts))

		if len(posts) < 30:
			break

		# update
		_index = max([i.id for i in posts])


def get_forums():
	# var
	forums = []

	try:
		_request = requests.get('https://www.dcard.tw/_api/forums/')
		_response = json.loads(_request.text)

		for i in _response:
			forums.append({
				'forumAlias': i['alias'],
				'forumName': i['name'],
			})

		return forums
	except Exception as e:
		print('[%10s] %s' % ('forums', str(e)))
		exit()

def save_db():
	try:
		with open(PATH + '/db.json', 'w+') as file:
			json.dump(db, file)
	except Exception as e:
		print('[%10s] %s' % ('db', str(e)))

def load_db():
	# var
	global db

	try:
		print('[%10s] %s' % ('init', 'db'))
		with open(PATH + '/db.json', 'r') as file:
			db = json.load(file)
	except:
		print('[%10s] %s' % ('init', 'creating db'))
		
		for i in get_forums():
			db.append({
				'forumName': i['forumName'],
				'forumAlias': i['forumAlias'],
				'latest': 1,
				'updateAt': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
			})

	save_db()