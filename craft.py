import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

# CONFIG!
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'craft.db'),
    DEBUG=True,
    SECRET_KEY='26a1$27832721df59dbc4@acf4a301093c'
))

# connection
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# get db
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# close after req
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Create the .db file from schema, thanks to the Flask tutorial
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
