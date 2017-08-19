import datetime

from flask_login import UserMixin
from peewee import *

db = SqliteDatabase('journal.db')


class Entry(UserMixin, Model):
    title = CharField(max_length=255, unique=True)
    date = CharField(default=datetime.datetime.now().strftime('%Y-%m-%d'))
    time = CharField(max_length=50)
    learned = TextField()
    resources = TextField()

    class Meta:
        database = db
        order_by = ("-date", )

    @classmethod
    def create_entry(cls, title, date, time, learned, resources):
        cls.create(
            title=title,
            date=date,
            time=time,
            learned=learned,
            resources=resources
        )


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    db.close()
