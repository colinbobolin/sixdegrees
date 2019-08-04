import sqlite3
from flask import g, current_app
from flask.cli import with_appcontext
import click
from sixdegrees import db_update
from pathlib import Path
import requests
import pandas as pd
from datetime import date


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


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    db_update.init_movies_and_actors()


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


def get_movies(nconst):
    results = query_db('SELECT tconst FROM Movie_Cast WHERE nconst=?;', [nconst])[:10]
    movies = [tconst for tconst in [movie_row['tconst'] for movie_row in results]]
    return movies


def get_actors(tconst):
    results = query_db('SELECT nconst FROM Movie_Cast WHERE tconst=?;', [tconst])[:10]
    actors = [nconst for nconst in [actor['nconst'] for actor in results]]
    return actors


def get_name(const):
    if const[0] == 'n':
        query = query_db('SELECT primaryName FROM Actors WHERE nconst=?', [const])
        return query[0]['primaryName']
    if const[0] == 't':
        query = query_db('SELECT primaryTitle FROM Movies WHERE tconst=?', [const])
        return query[0]['primaryTitle']
