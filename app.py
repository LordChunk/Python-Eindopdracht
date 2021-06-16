from flask import Flask, render_template, request, session, redirect, url_for
import logging
from database import db, User
import secrets


app = Flask(__name__)
app.logger.setLevel(logging.INFO)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    dbuser = User.query.filter_by(username=username).first()
    print(dbuser)
    if dbuser is None:
        me = User(username=username)
        db.session.add(me)
        db.session.commit()
    return redirect('/game')


@app.route('/game')
def game():
    return render_template('game.html')


with app.app_context():
    db.create_all()
