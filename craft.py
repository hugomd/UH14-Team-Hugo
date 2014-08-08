import os
import sqlite3
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
from flask_wtf import Form
from wtforms import StringField, validators
from wtforms.validators import Email, InputRequired, ValidationError, Required, DataRequired

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

class SignupForm(Form):
    mc_user = StringField(u'Minecraft Username', validators=[validators.input_required()])
    email = StringField(u'Email', validators=[validators.input_required()])

@app.route("/", methods=['GET', 'POST'])
def index():
    form = SignupForm(request.form)
    if form.validate():
        print("TRUE")
    else:
        print("FALSE")

    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash("All fields are required!")
        else:
            flash("Success....?")

        return render_template('index.html', title="Craft! - Register YAY", form=form)

    return render_template('index.html', title="Craft! - simple, fast Minecraft servers", form=form)


@app.route("/regster", methods=['GET', 'POST'])
def register():


    error = None
    # if request.method == 'POST':
    #     expires = int(time.time()) + 7200
    #     email = request.form['email']
    #     mc_user = request.form['mc_user']
    #     play_time = 60 # minutes

    return render_template('index.html', title="Craft! - Register")

@app.route("/faq")
def faq():
    return render_template('index.html', title="Craft! - FAQ")

if __name__ == "__main__":
    app.run()
