from sixdegrees import app
from sixdegrees.network import Network
from flask import render_template, request, redirect
from sixdegrees import db
from sixdegrees import db_update


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_nconst = db.query_db(f"SELECT nconst from Actors where name=?", [start])[0]['nconst']
        end_nconst = db.query_db(f"SELECT nconst from Actors where name=?", [end])[0]['nconst']
        network = Network(start_nconst, end_nconst)
        path = network.get_path()
        print(f"path is: {path}")
        return render_template('game.html', network=network)

    return render_template('game.html')


@app.route('/update', methods=('GET', 'POST'))
def update():
    if request.method == 'POST':
        # TODO store that actor's movies in the database.
        actor = request.form['actor']
        nconst = db.query_db(f"SELECT nconst from Actors where name=?", [actor])[0]['nconst']
        movies = db_update.update_filmography(nconst)
        return render_template('update.html', movies=movies)

    return render_template('update.html')
