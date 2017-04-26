import os
import argparse

# customized module
from module import Dcard
from module import Thread

# constant
PATH = os.path.dirname(os.path.abspath(__file__)) + '/data/'

def parse_argv():
	# init
	parser = argparse.ArgumentParser()

	# add argument
	parser.add_argument('--threads_num', action='store', help='number of threads', type=int, default=4)
	results = parser.parse_args()
	
	return {
		'threads_num': results.threads_num
	}

def main():
	# var
	args = parse_argv()

	# init
	Dcard.load_db()

	for i in Dcard.db:
		if i['forumAlias'] != 'nctu':
			continue

		# init
		Dcard.init_forum(i['forumAlias'])

		if not os.path.exists(PATH + i['forumAlias']):
			os.makedirs(PATH + i['forumAlias'])

		Thread.run(args)

if __name__ == '__main__':
	main()