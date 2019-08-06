from sixdegrees.db import query_db, update_filmography
from sixdegrees.network import Network
from flask import (
    Blueprint, render_template, request
)
from sixdegrees import network as net

bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/play', methods=('GET', 'POST'))
def play():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_nconst = query_db(f"SELECT nconst from Actors where primaryName=?", [start])[0]['nconst']
        end_nconst = query_db(f"SELECT nconst from Actors where primaryName=?", [end])[0]['nconst']
        #network = Network(start_nconst, end_nconst)
        #path = network.calc_path()
        network = net.get_path(start_nconst, end_nconst)
        return render_template('game/play.html', network=network)

    return render_template('game/play.html')


@bp.route('/update', methods=('GET', 'POST'))
def update():
    if request.method == 'POST':
        actor = request.form['actor']
        nconst = query_db(f"SELECT nconst from Actors where primaryName=?", [actor])[0]['nconst']
        movies = update_filmography(nconst)
        return render_template('game/update.html', movies=movies)

    return render_template('game/update.html')