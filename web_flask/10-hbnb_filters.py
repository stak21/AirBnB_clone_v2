#!/usr/bin/python3
"""Routers and Controllers"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def tearDown(self):
    storage.close()


@app.route('/hbnb_filters')
def index_route():
    """ display the index route """
    states = storage.all("State").values()
    amenity = storage.all("Amenity").values()
    print(amenity)
    return render_template('6-index.html', states=states, amenities=amenity)


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
