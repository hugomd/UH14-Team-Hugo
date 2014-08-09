import os, string, random, time
import sqlite3
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta
from flask_wtf import Form
from wtforms import StringField, validators
from wtforms.validators import Email, InputRequired, ValidationError, Required, DataRequired

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup

# digital ocean
from dopy.manager import DoManager
do = DoManager('PyDSOzmle2zsvUO86yxqv', '9a48657f7a9c50261865af0bbb558f0e')

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

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def get_user_id(email, mc_user):
    """Convenience method to look up the id for a username."""
    rv = query_db('SELECT id FROM users WHERE email = ? OR mc_user = ?',
                  [email, mc_user], one=True)
    return rv[0] if rv else None

def countDroplets():
    count = 0;
    for i in do.all_active_droplets():
        count += 1

    return count

class SignupForm(Form):
    mc_user = StringField(u'Minecraft Username', validators=[validators.Required(message=u'Minecraft username required'), validators.Length(min = 4, max = 100, message=u'Minecraft username must be 4 characters or more.')])
    email = StringField(u'Email', validators=[validators.Required(message=u'Email required.'), validators.Email(message=u'That\'s not an email!')])

@app.route("/", methods=['GET', 'POST'])
def index():
    form = SignupForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit() == True:
            expires = int(time.time()) + 7200
            email = request.form['email']
            mc_user = request.form['mc_user']
            play_time = 120 # minutes
            server_ip = "127.0.0.1"
            key = ''.join(random.choice(string.ascii_uppercase) for i in range(20))

            db = get_db()
            if get_user_id(email, mc_user) is None:
                db.execute("INSERT INTO users (mc_user, email, server_hostname, server_ip, key, play_time, expires) VALUES (?, ?, ?, ?, ?, ?, ?)", [mc_user, email, mc_user, server_ip, key, play_time, expires])

                db.commit()

                # create minecraft server
                do.new_droplet(mc_user, 63, 5592844, 6, ssh_key_ids = None, virtio = False, private_networking = False, backups_enabled = False)

                for i in do.all_active_droplets():
                    if i['name'] == mc_user:
                        ip = i['ip_address']

                flash(Markup("Awesome! Your server is being setup <b>right</b> now! Here's your server's IP: " + str(ip) + " now go spam refresh!"))

            else:
                flash("Email or Minecraft username already in use.")

    return render_template('index.html', title="Craft! - simple, fast Minecraft servers", form=form)


@app.route("/register", methods=['GET', 'POST'])
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

@app.route("/api/<hostname>")
def api(hostname):
    db = get_db()

    user = query_db('SELECT * FROM users WHERE mc_user = ?',
                  [hostname], one=True)


    for i in do.all_active_droplets():
        i['ip_address']
    return render_template('API.html', title="API!", hostname = hostname, user = user)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
