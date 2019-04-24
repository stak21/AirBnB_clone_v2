#!/usr/bin/python3
from flask import Flask
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
if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
