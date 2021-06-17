from flask import Flask, render_template, request, session, redirect
import logging
from database import db
import secrets
from src.Mastermind import Mastermind

# These imports ensure the database is created properly
from models.Color import Color
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
    db_user = User.query.filter_by(username=username).first()

    if db_user is None:
        db_user = User(username=username)
        db.session.add(db_user)
        db.session.commit()

    session['user_id'] = db_user.id
    return redirect('/game')


@app.route('/game')
def game_list():
    # ToDO: fix logout login bug with stats
    games = Game.query.filter_by(user_id=session['user_id']).all()
    user = User.query.filter_by(id=session['user_id']).first()
    games_played = Game.query.filter_by(id=session['user_id']).count()

    if games_played == 0:
        average_turns = 0
    else:
        average_turns = sum(game.turns for game in games) / games_played

    return render_template('game-list.html', games=games, user=user, games_played=games_played, average_turns=average_turns)


@app.route('/game/create', methods=['GET', 'POST'])
def create_game():
    if request.method == 'GET':
        return render_template('create-game.html')
    else:
        new_game = Game(
            user_id=session['user_id'],
            turns=0,
            cheat_mode=False,
            duplicate_color=bool(request.form.get('duplicate_color') or ''),
            number_of_colors=int(request.form['number_of_colors']),
            number_of_positions=int(request.form['number_of_positions']),
        )

        new_mastermind = Mastermind(new_game)
        new_game.code = new_mastermind.make_code()

        db.session.add(new_game)
        db.session.commit()

        return redirect('/game/' + str(new_game.id))


@app.route('/game/<game_id>', methods=['GET', 'POST'])
def game(game_id):
    game = Game.query.filter_by(id=game_id).first()
    mastermind = Mastermind(game)
    if request.method == 'GET':
        pins = Pin.query.filter_by(game_id=game_id).all()
        used_colors = list(Color)[0:game.number_of_colors]
        results = mastermind.get_all_results()
        # TODO: Add logic for winning
        for result in results:
            if mastermind.did_player_win(result):
                game.won = True
                break

        db.session.commit()
        return render_template('game.html', game=game, pins=pins, Color=used_colors, code=game.code, results=results)
    else:
        color_array = []
        for value in request.form.values():
            if value == 'None':
                color_array.append(None)
            else:
                color_array.append(Color[value])

        mastermind = Mastermind(game)
        # TODO save pins to db
        mastermind.add_new_pin_row(color_array)

        return redirect('/game/' + str(game.id))


with app.app_context():
    db.create_all()
    PinColor.seed()

if __name__ == "__main__":
    app.run(debug=True)
