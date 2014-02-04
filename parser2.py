from multiprocessing.dummy import Pool as ThreadPool
from zipfile import ZipFile, BadZipFile
import json
import os

pool = ThreadPool()

def get_comment_files(directory='data'):
    for zipped_file in os.walk(directory):
        for file_name in zipped_file[2]:
            if file_name[-17:] != 'comments.json.zip':
                continue
            try:
                prepped_zip_file = ZipFile('data/' + file_name)
                form = '\n{0}\n{1}\n{0}'
                print(form.format('-'*75, file_name))
            except BadZipFile as e:
                continue

            for raw_file in prepped_zip_file.namelist():
                yield prepped_zip_file.open(raw_file, 'r')

def get_blobs(zip_file):
    form = '\n{0}\n{1}\n{0}\n'
    line_sep = '-' * 50
    for line in zip_file:
        blob = json.loads(line.decode())
        comment = build_comment(blob)

        print(form.format(line_sep, ', '.join(comment)))
        yield blob['body']

def get_unigrams(body):
    for unigram in tokenize(body):
        yield(unigram)

def iterate_through(files):
    for zip_file in files:
        for blobs in get_blobs(zip_file):
            pool.map(print, get_unigrams(blobs))

def build_comment(blob):
    comment_id = blob['_id']
    comment_created = blob['updated_on']['$date']
    return comment_id, str(comment_created)

def tokenize(string):
    string = string.lower()
    for unigram in string.split():
        stripped = unigram.lstrip('>,(?*[\'(" ').rstrip(':;.,?!)\"-] ')
        if stripped[-2:] != 's\'':
            stripped = stripped.rstrip("'")

        elipses = stripped.split('...')
        dash = stripped.split('--')

        if len(elipses) > 1:
            tokenize(' '.join(elipses))
            continue
        if len(dash) > 1:
            tokenize(' '.join(dash))
            continue

        if stripped is not None:
            yield stripped

iterate_through(get_comment_files())