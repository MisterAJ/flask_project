from time import strptime

from flask import Flask, render_template, redirect, url_for, flash, \
    request, g
from flask_login import LoginManager

from models import journal
from forms import forms

import json

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'nstoheunoadeigc4ybihct.bp8i7euhibethuibcgroep!'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    """Connect to DB before each request"""
    g.db = journal.db
    g.db.get_conn()


@app.after_request
def after_request(response):
    """Close DB connection after each request"""
    g.db.close()
    return response


@app.route('/')
@app.route('/entries/')
def index():
    entries = journal.Entry.select()
    return render_template('index.html', entries=entries)


@app.route('/entries/<entry_id>')
def detail(entry_id):
    single_entry = journal.Entry.select().where(journal.Entry.id == entry_id)
    return render_template('detail.html', entry=single_entry[0])


@app.route('/entries/edit/<entry_id>', methods=['POST', 'GET'])
def edit(entry_id):
    single_entry = journal.Entry.select().where(journal.Entry.id == entry_id)
    single_entry = single_entry[0]
    form = forms.EntryForm(obj=single_entry)
    if form.validate_on_submit():
        form.populate_obj(single_entry)
        single_entry.title = form.title.data
        single_entry.date = form.date.data
        single_entry.time = form.time.data
        single_entry.learned = form.learned.data
        single_entry.resources = form.resources.data

        single_entry.save()
        flash('Updated!')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)


@app.route('/entries/delete/<entry_id>', methods=('GET', 'POST'))
def delete(entry_id):
    single_entry = journal.Entry.select().where(journal.Entry.id == entry_id)
    single_entry[0].delete_instance()
    return redirect(url_for('index'))


@app.route('/entry')
@app.route('/new', methods=['POST', 'GET'])
def save_new():
    form = forms.EntryForm()
    if form.validate_on_submit():
        flash('Entry Added!', "success")
        journal.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            learned=form.learned.data,
            resources=form.resources.data
        )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


if __name__ == '__main__':
    journal.initialize()

    app.run(debug=DEBUG, port=PORT)
