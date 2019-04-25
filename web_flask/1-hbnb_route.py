#!/usr/bin/python3
"""Routers and Controllers"""
from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_route():
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb_route():
    return "HBNB"

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
