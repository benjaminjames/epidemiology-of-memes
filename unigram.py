from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy import DateTime, Table, Column, ForeignKey, Integer, String, create_engine


engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

Base.metadata.create_all(engine)

association_table = Table('ngrams', Base.metadata,
    Column('unigram_id', String, ForeignKey('comment.id')),
    Column('comment_id', String, ForeignKey('unigram.id')))


class Unigram(Base):
    __tablename__ = 'unigram'

    id = Column(String, primary_key=True)
    times_occurred = Column(Integer)
    occurs_in = relationship('Comment', secondary=association_table,
                             backref('unigrams', lazy='no-load'))

    def __init__(self, id, times_occurred, occurs_in):
        self.id = id
        self.times_occurred = times_occurred
        self.occurs_in = occurs_in

    def __repr__(self):
        return '{} -> {}'.format(self.id, self.times_occurred)

    def __lt__(self, other):
        if self.times_occurred < other.times_occurred:
            return True
        elif self.times_occurred == other.times_occurred:
            return self.id < other.id
        else:
            return False


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(String, primary_key=True, unique=True)
    creation_time = Column(DateTime)

    def __init__(self, id, creation_time):
        self.id = id
        self.creation_time = creation_time

    def __repr__(self):
        return '{} created at {}'.format(self.id, self.creation_time)

    def __lt__(self, other):
        if self.creation_time < other.creation_time:
            return True
        return False
