from sixdegrees import app
from sixdegrees.network import Network
from flask import render_template, request, redirect
from sixdegrees import db


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        start_nconst = db.query_db(f"SELECT nconst from Actors where name=?", [start])[0]['nconst']
        end_nconst = db.query_db(f"SELECT nconst from Actors where name=?", [end])[0]['nconst']
        return redirect(f'/finding/{start_nconst}/to/{end_nconst}')

    return render_template('game.html')


@app.route('/finding/<start>/to/<end>', methods=('GET', 'POST'))
def finding(start, end):
    print(start, end)
    Network(start, end)
    return render_template('thinking.html')
