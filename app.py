from flask import Flask
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route('/')
def hello_world():
    return 'Hello World!'
