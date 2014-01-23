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