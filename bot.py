import os
import sys
import time
import datetime
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
	parser.add_argument('--forum', action='store', help='forum', choices=[i['forumAlias'] for i in Dcard.db])
	parser.add_argument('--threads_num', action='store', help='number of threads', type=int, default=4)
	parser.add_argument('--debug', action='store_true', help='show debug information', default=False)
	results = parser.parse_args()
	
	return {
		'forum': results.forum,
		'threads_num': results.threads_num,
		'debug': results.debug
	}

def main():
	# init
	Dcard.load_db()

	# var
	args = parse_argv()

	for i in Dcard.db:
		if args['forum'] and i['forumAlias'] != args['forum']:
			continue

		# init
		Dcard.init_forum(i)

		if not os.path.exists(PATH + i['forumAlias']):
			os.makedirs(PATH + i['forumAlias'])

		# threading
		Thread.run(args)

		# update
		i['latest'] = max([int(j) for j in os.listdir(PATH + i['forumAlias'])])
		i['updateAt'] = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
		Dcard.save_db()

if __name__ == '__main__':
	main()
