from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
from contextlib import closing
from peewee import *

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = '12345'
USERNAME = 'admin'
PASSWORD = 'admin'

application = app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# Model
db = SqliteDatabase(DATABASE)
class BaseModel(Model):
    class Meta:
            database = db
class Bookmark(BaseModel):
    title = TextField(null=False)
    url = TextField(unique=True, index=True)
    desc = TextField()
def create_tables():
    Bookmark.create_table()

# Routes
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return show_entries()
    else:
        return add_entry()

@app.route('/search', methods=['POST'])
def search():
    # q = request.form['q']
    a = Bookmark.select().where(
            (Bookmark.desc ** ("%"+ request.form['q'] + "%")) |
            (Bookmark.title ** ("%"+ request.form['q'] + "%")) |
            (Bookmark.url **  ("%"+ request.form['q'] + "%" ))
        )
    
    # return str(a.sql())

    flash("SQL: " + str(a.sql()))
    flash(str(a.count()) + " Results found for query: " + request.form['q'])
    return render_template('entries.html', entries=a)
    
@app.route('/delete')
def delete():
    del_query = Bookmark.delete()
    del_query.execute()
    flash("All bookmarks deleted")
    return show_entries()
def show_entries(err=""):
    # cur = g.db.execute('select title, text from entries order by id desc')
    # entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    entries = Bookmark.select()
    return render_template('entries.html', entries=entries, error=err)
def add_entry():
    if request.form['title'] == "" or request.form['url'] == "":
        error = "Title and URL are required"
        return show_entries(error)
    try:
        bookmark = Bookmark.get(url=request.form['url'])
        return show_entries("Bookmark already exists")
    except Bookmark.DoesNotExist:
        bookmark = Bookmark.create(
            title = request.form['title'],
            desc = request.form['desc'],
            url = request.form['url']
        )
        flash('Bookmark added')
        return render_template('entry.html', entry=bookmark)


if __name__ == "__main__":
	app.run()