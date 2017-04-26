import os
import json
import requests

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
