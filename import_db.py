import glob
import json

from pymongo import MongoClient

def main():
	# var
	client = MongoClient('127.0.0.1', 27017)
	db = client.dcard

	# auth
	client.dcard.authenticate(
		'dcard', 
		'dcard',
		mechanism='SCRAM-SHA-1'
	)

	for filename in glob.iglob('/home/cjyeh/Github/dcard-crawler/data/**/*.json', recursive=True):
		with open(filename, 'r') as file:
			try:
				post = json.load(file)
				print(db.posts.insert_one(post))
			except Exception as e:
				print(str(e))
				print(filename)
				return
	return

if __name__ == '__main__':
	main()