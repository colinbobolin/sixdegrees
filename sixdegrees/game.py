from sixdegrees.db import get_db, query_db
from sixdegrees.network import Network
from sixdegrees.db_update import update_filmography
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/play', methods=('GET', 'POST'))
def play():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_nconst = query_db(f"SELECT nconst from Actors where name=?", [start])[0]['nconst']
        end_nconst = query_db(f"SELECT nconst from Actors where name=?", [end])[0]['nconst']
        network = Network(start_nconst, end_nconst)
        path = network.get_path()
        print(f"path is: {path}")
        return render_template('game/play.html', network=network)

    return render_template('game/play.html')


@bp.route('/update', methods=('GET', 'POST'))
def update():
    if request.method == 'POST':
        # TODO store that actor's movies in the database.
        actor = request.form['actor']
        nconst = query_db(f"SELECT nconst from Actors where name=?", [actor])[0]['nconst']
        movies = update_filmography(nconst)
        return render_template('game/update.html', movies=movies)

    return render_template('game/update.html')