import sqlite3
from flask import g, current_app
from flask.cli import with_appcontext
import click
from sixdegrees.definitions import ROOT_DIR
#from sixdegrees import app
from contextlib import closing
from pathlib import Path
import requests
import pandas as pd
from datetime import date
from sixdegrees import db_update

DATABASE = Path(ROOT_DIR + '/database')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def connect_db():
    return sqlite3.connect(DATABASE)


# @app.before_request
# def before_request():
#     g.db = connect_db()


# @app.teardown_request
# def teardown_request(exception):
#     if hasattr(g, 'db'):
#         g.db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_request(close_db)
    app.cli.add_command(init_db_command)


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def modify_db(query, args=()):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    g.db.commit()
    return rv


# TODO it might be cool to have this archive each datafile according to their update dates,
#  see which values are different, then update the table accordingly.
def pull_data_files():
    db_urls = ['https://datasets.imdbws.com/title.principals.tsv.gz',
               'https://datasets.imdbws.com/name.basics.tsv.gz',
               'https://datasets.imdbws.com/title.basics.tsv.gz']
    today_code = date.today().strftime('%Y%m%d')
    for url, r in [(url, requests.get(url)) for url in db_urls]:
        path = Path(ROOT_DIR + "/sixdegrees/datafiles/" + today_code + url.split('/')[-1])
        with open(path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk)
    print("Done")


def transfer_csv_to_db(csv_file, db_table_name):
    #path = Path(ROOT_DIR + "/sixdegrees/datafiles/20190729title.basics.tsv.gz")
    reader = pd.read_csv(csv_file.name, sep='\t', chunksize=1000)
    with connect_db() as db:
        for chunk in reader:
            chunk.to_sql(db_table_name, con=db, if_exists='append', index=False)
    print("Done")


def get_movies(nconst):
    #db_update.update_filmography_if_not_updated(nconst)
    results = query_db('SELECT tconst FROM Movie_Cast WHERE nconst=?;', [nconst])[:10]
    movies = [tconst for tconst in [movie_row['tconst'] for movie_row in results]]
    return movies


def get_actors(tconst):
    #db_update.update_cast_if_not_updated(tconst)
    results = query_db('SELECT nconst FROM Movie_Cast WHERE tconst=?;', [tconst])[:10]
    actors = [nconst for nconst in [actor['nconst'] for actor in results]]
    return actors


def get_name(const):
    if const[0] == 'n':
        query = query_db('SELECT name FROM Actors WHERE nconst=?', [const])
        return query[0]['name']
    if const[0] == 't':
        query = query_db('SELECT title FROM Movies WHERE tconst=?', [const])
        return query[0]['title']