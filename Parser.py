import os
import json
from collections import Counter
from zipfile import BadZipFile, ZipFile

def tokenize(string):
	string = string.lower()
	for unigram in string.split():
		stripped = unigram.lstrip(',(?*[\'("').rstrip(':;.,?!)"-]')
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
		

word_counts = {}
try:
	for zipped_file in os.walk('data'):
		for file_name in zipped_file[2]: #The file component of the tuple
			try:
				prepped_zip_file = ZipFile('data/' + file_name)
				print(file_name)
			except BadZipFile as e:
				continue

			for raw_file in prepped_zip_file.namelist():
				for line in prepped_zip_file.open(raw_file, 'r'):
					decoded_json = json.loads(line.decode())
					try:
						body = decoded_json['body']
						for unigram in tokenize(body):
							if unigram in word_counts:
								word_counts[unigram] += 1
							else:
								word_counts[unigram] = 1

					except KeyError:
						continue
except (Exception, KeyboardInterrupt) as e:
	print(e)
finally:
	final_count = open('count.txt', 'w')
	unsorted_list = Counter(word_counts)
	sorted_list = []
	raw_sorted = unsorted_list.most_common()
	for item in raw_sorted:
		sorted_list.append('{} -> {}'.format(*item))
	final_count.write('\n'.join(sorted_list))
	
	shorter = []
	without_ones = open('without_ones.txt', 'w')
	for item in raw_sorted:
		if item[1] > 1:
			shorter.append('{} -> {}'.format(*item))
	without_ones.write('\n'.join(shorter))

