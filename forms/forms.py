import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, \
    Length, EqualTo

from models import journal

Entry = journal.Entry


def title_exists(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError("Title already exists")


class EntryForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired()
        ])
    date = StringField(
        'Date',
        default=datetime.datetime.now().strftime('%Y-%d-%m'),
        validators=[
            DataRequired()
        ])
    time = StringField(
        'Time Spent',
        validators=[
            DataRequired()
        ])
    learned = StringField(
        'What You Learned',
        validators=[
            DataRequired()
        ])
    resources = StringField(
        'Resources To Remember',
        validators=[
            DataRequired()
        ])
