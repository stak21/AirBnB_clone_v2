#!/usr/bin/python3
"""Routers and Controllers"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def tearDown(self):
    storage.close()


@app.route('/states')
def list_states_route():
    states = storage.all("State").values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>')
def list_state(id):
    """ Grab a state by its id and pass it to the html """
    states = storage.all("State").values()
    for state in states:
        if state.id == id:
            return render_template('9-states.html', state=state)
    """ No state pass in None to html """
    return render_template('9-states.html', state=None)


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
