"""Fixture for Flask validation rules."""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "OK"