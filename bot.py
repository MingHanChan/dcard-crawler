import requests
import json
import os
import time
import sys
import threading
import queue

url_API_FORUMS = 'https://www.dcard.tw/_api/forums/'
url_API_FILTER = '/posts?popular=false'
url_API_POSTS = 'https://www.dcard.tw/_api/posts/'

# argv
debug = '--debug' in sys.argv

# globle var
q = queue.Queue()

def next():
	while q.qsize() > 0:
		job = q.get()
		job.run()

class Crawler:
	def __init__(self, id):
		self.id = id
		self.path = str(os.path.abspath(os.path.join(__file__, os.pardir)))

	def request_post(self, post_id):
		try:
			__request = requests.get(url_API_POSTS + str(post_id))
			__response = json.loads(__request.text)
		except:
			if debug:
				print('Error: ' + str(post_id) + ' request_post')
			return
		return __response

	def request_comment(self, post_id):
		try:
			__request = requests.get(url_API_POSTS + str(post_id) + '/comments')
			__response = json.loads(__request.text)
		except:
			if debug:
				print('Error: ' + str(post_id) + ' request_comment')
			return
		return __response

	def save_file(self, var):
		try:
			path = self.path + '/data/' + var['posts']['forumAlias'] + '/'

			# create folder
			if not os.path.exists(path):
				os.makedirs(path)

			file_name = str(var['posts']['id']) + '.json'
			f = open(path + file_name, 'w', encoding='UTF-8')
			f.write(json.dumps(var))
			f.close()
		except:
			if debug:
				print('Error: ' + str(var['posts']['id']) + ' save_file')
			return

	def run(self):
		temp = {
			"posts": self.request_post(self.id),
			"comments": self.request_comment(self.id)
		}
		self.save_file(temp)
		if debug:
			print(self.id)

class Dcard:
	def __init__(self):
		# var
		self.path = str(os.path.abspath(os.path.join(__file__, os.pardir)))

		# para
		try:
			print('Loading paraments...')
			with open(self.path + '/paraments.json', 'r') as file:
				self.para = json.load(file)
		except:
			print('Creating paraments...')
			# var
			self.para = []
			
			# request forums list
			try:
				print('Requesting forum list...')
				__request = requests.get(url_API_FORUMS)
				__response = json.loads(__request.text)
			except:
				print('Error: requests.get() failed')

			# init
			for x in __response:
				temp = {
					"alias": x['alias'],
					"updatedAt": "null",
					"max": 0,
					"min": 0
				}
				self.para.append(temp)

	def request_post_list(self, var, index):
		try:
			__request = requests.get(url_API_FORUMS + var['alias'] + url_API_FILTER + '&before=' + str(index))
			__response = json.loads(__request.text)
			return __response
		except:
			if debug:
				print('Error: ' + var['alias'] + ' request before ' + str(index))
			return

	def update_para(self):
		with open(self.path + '/paraments.json', 'w') as file:
			json.dump(self.para, file)

	def run_forum(self, var):
		# request lastest post id
		try:
			__request = requests.get(url_API_FORUMS + var['alias'] + url_API_FILTER)
			__response = json.loads(__request.text)
			index = __response[0]['id']
		except:
			if debug:
				print('Error: ' + var['alias'] + ' list')
			return

		while index > var['max']:
			# init
			post_list = self.request_post_list(var, index)

			try:
				if len(post_list) == 0:
					# first
					if var['min'] == 0:
						var['min'] = index
					break
			except:
				continue

			# init
			for i in post_list:
				try:
					# update max
					index = i['id']

					# done
					if i['id'] <= var['max']:
						break

					q.put(Crawler(i['id']))
				except:
					print('Error: init')

			# create threads 
			t1 = threading.Thread(target=next, name='T1')
			t2 = threading.Thread(target=next, name='T2')
			t3 = threading.Thread(target=next, name='T3')
			t4 = threading.Thread(target=next, name='T4')

			t1.start()
			t2.start()
			t3.start()
			t4.start()

			while t1.is_alive() or t2.is_alive() or t3.is_alive() or t4.is_alive():
				time.sleep(1)

		# update para
		temp = self.para.index(var)
		if self.para[temp]['max'] < __response[0]['id']:
			self.para[temp]['max'] = __response[0]['id']
		self.update_para()

	def run_all(self):
		for x in self.para:
			# console
			print('ForumAlias: ' + x['alias'])
			print('Percentage: ' + str(self.para.index(x) + 1) + '/' + str(len(self.para)))
			self.run_forum(x)

while 1:
	dcard = Dcard()
	dcard.run_all()
	time.sleep(600)