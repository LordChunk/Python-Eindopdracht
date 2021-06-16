from flask import Flask, render_template, request, session, redirect
import logging
from database import db
import secrets

# These imports ensure the database is created properly
from models.User import User
from models.Game import Game
from models.Pin import Pin
from models.PinColor import PinColor


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
    db_user = User.query.filter_by(username=username).first()
    if db_user is None:
        me = User(username=username)
        db.session.add(me)
        db.session.commit()
    return redirect('/game')


@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/game/create')
def create_game():
    return render_template('create-game.html')


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
