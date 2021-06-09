from flask import Flask
import logging

from database import db

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


with app.app_context():
    db.create_all()
