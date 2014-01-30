from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Unigram(db.Model):
    id = db.Column(db.String(60), primary_key=True)
    times_occurred = db.Column(db.Integer)
    #occurs_in = db.Column(db.Integer)

    def __init__(self, id, times_occurred):
        self.id = id
        self.times_occurred = times_occurred
        #self.occurs_in = occurs_in

    def __repr__(self):
        return '{} -> {}'.format(self.id, self.times_occurred)

    def __lt__(self, other):
        if self.times_occurred < other.times_occurred:
            return True
        elif self.times_occurred == other.times_occurred:
            return self.id < other.id
        else:
            return False


class Comment(db.Model):
    id = db.Column(db.String, primary_key=True, unique=True)
    creation_time = db.Column(db.DateTime)

    def __init__(self, id, creation_time):
        self.id = id
        self.creation_time = creation_time

    def __repr__(self):
        return '{} created at {}'.format(self.id, self.creation_time)

    def __lt__(self, other):
        if self.creation_time < other.creation_time:
            return True
        return False
