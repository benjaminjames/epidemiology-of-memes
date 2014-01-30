import os
import json
from copy import deepcopy
from collections import deque
from datetime import datetime
from zipfile import BadZipFile, ZipFile

from bookmark import Bookmark
from unigram import Unigram, Comment, db

class Parser:


    def __init__(self):
        try:
            stopped_at = open('.bookmark')
            stopping_place = eval(stopped_at.readline())
            self.current_position = Bookmark(*stopping_place)
        except FileNotFoundError:
            self.current_position = Bookmark()

        self.word_counts = {}
        self.place_saved = Bookmark()
        db.create_all()

    def save_place(self):
        with open('.bookmark', 'w') as stopped_at:
            stopped_at.write('{}'.format(self.place_saved))

    def get_comment_data_blobs(self, directory='data'):
        for zipped_file in os.walk(directory):
            for file_name in zipped_file[2]:
                if file_name[-17:] != 'comments.json.zip' \
                    or not self.current_position.right_file(file_name):
                    print('Skipped parsing {}'.format(file_name))
                    continue
                try:
                    prepped_zip_file = ZipFile('data/' + file_name)
                    print(file_name)
                except BadZipFile as e:
                    continue

                for raw_file in prepped_zip_file.namelist():
                    for line in prepped_zip_file.open(raw_file, 'r'):
                        yield json.loads(line.decode()), file_name

    def run(self):
        try:
            for blob, current_file in self.get_comment_data_blobs():
                comment = build_comment(blob)
                if not self.current_position.back_where_we_need_to_be(current_file, comment.id):
                    continue

                db.session.add(comment)

                if len(self.word_counts) > 100000:
                    self.dump_into_db(db)

                for unigram in tokenize(blob['body']):
                    if unigram in self.word_counts:
                        self.word_counts[unigram]['count'] += 1
                    else:
                        self.word_counts[unigram] = {}
                        self.word_counts[unigram]['count'] = 1

                    if not self.word_counts[unigram].get('occurences'):
                        self.word_counts[unigram]['occurences'] = deque()

                    self.word_counts[unigram]['occurences'].append(comment)
                self.current_position.commit = True

        except (KeyboardInterrupt) as e:
            print(e)
            self.dump_into_db(db)

        finally:
            final_count = sorted(Unigram.query.all(), reverse=True)
            for unigram in final_count:
                print('{}'.format(unigram))

    def dump_into_db(self, db):
        start = datetime.now()
        length = len(self.word_counts)
        alert = '\nMoving from memory into database. ({})'
        db.session.commit()

        print(alert.format(length))

        for current in Unigram.query.filter(Unigram.id in self.word_counts).all():
            current.times_occurred += self.word_counts[current.id]['count']
            current.occurs_in.extend( self.word_counts[current.id]['occurences'])
            del(self.word_counts[current.id])

        for ngram in self.word_counts:
            current = Unigram(ngram, self.word_counts[ngram]['count'],
                                  self.word_counts[ngram]['occurences'])
            db.session.add(current)

        db.session.commit()
        print('Leaving dump after {}.'.format(datetime.now()-start))
        self.place_saved = deepcopy(self.current_position)
        self.save_place()


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
        continue


def build_comment(blob):
    comment_id = blob['_id']
    comment_created = blob['updated_on']['$date']
    comment_created = datetime.fromtimestamp(comment_created / 1000)
    return Comment(comment_id, comment_created)

if __name__ == '__main__':
    Parser().run()