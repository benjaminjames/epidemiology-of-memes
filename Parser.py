import os
import re
import json
from collections import Counter
from zipfile import BadZipFile, ZipFile

def tokenizer(string):
	string = string.lower()
	for unigram in string.split():
		re.findall('[ ]', unigram)
		

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
	with open('count.txt', 'w') as final_count:
		unsorted_list = Counter(word_counts)
		sorted_list = []
		for item in unsorted_list.most_common():
			sorted_list.append('{} -> {}'.format(*item))
		final_count.write('\n'.join(sorted_list))

