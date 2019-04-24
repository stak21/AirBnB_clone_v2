#!/usr/bin/python3
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
    return render_template('5_number_template.html', n=n)

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
