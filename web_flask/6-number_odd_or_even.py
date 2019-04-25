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


@app.route('/c/<text>')
def c_route(text):
    return "C {:s}".format(text).replace("_", " ")


@app.route('/python/', defaults={'text': "is cool"})
@app.route('/python/<text>')
def python_route(text):
    return "Python {:s}".format(text).replace("_", " ")


@app.route('/number/<int:n>')
def number_route(n):
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>')
def number_template_route(n):
    return render_template('5-number_template.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def number_odd_even(n):
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
