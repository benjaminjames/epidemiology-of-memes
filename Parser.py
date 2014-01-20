import os
import json
from collections import Counter
from zipfile import BadZipFile, ZipFile

from unigram import Unigram, db


def tokenize(string):
	string = string.lower()
	for unigram in string.split():
		stripped = unigram.lstrip('>,(?*[\'(" ').rstrip(':;.,?!)"-] ')
		if stripped[-2:] != 's\'':
			stripped = stripped.rstrip("'")
		
		elipses = stripped.split('...')
		dash =  stripped.split('--')

		if len(elipses) > 1:
			tokenize(' '.join(elipses))
			continue
		if len(dash) > 1:
			tokenize(' '.join(dash))
			continue

		if stripped is not None:
			yield stripped
		continue
		
def get_comment_data_blobs(directory='data'):
	for zipped_file in os.walk(directory):
		for file_name in zipped_file[2]: #The file component of the tuple
			if file_name[-17:] != 'comments.json.zip':
				continue
			try:
				prepped_zip_file = ZipFile('data/' + file_name)
				print(file_name)
			except BadZipFile as e:
				continue

			for raw_file in prepped_zip_file.namelist():
				for line in prepped_zip_file.open(raw_file, 'r'):
					yield json.loads(line.decode())

db.create_all()
word_counts = {}
try:
	for blob in get_comment_data_blobs():
		body = blob['body']
		for unigram in tokenize(body):
			if unigram in word_counts:
				word_counts[unigram] += 1
			else:
				word_counts[unigram] = 1

except (Exception, KeyboardInterrupt) as e:
	print(e)

finally:
	final_count = open('count.txt', 'w')
	without_ones = open('without_ones.txt', 'w')

	unsorted_list = Counter(word_counts)
	raw_sorted = unsorted_list.most_common()
	for item in raw_sorted:
		current_item = '{} -> {}\n'.format(*item)
		final_count.write(current_item)
		if item[1] > 1:
			without_ones.write(current_item)

