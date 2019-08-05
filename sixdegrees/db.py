import sqlite3
from flask import g, current_app
from flask.cli import with_appcontext
import click
import pandas as pd
from sixdegrees.web_scraper import get_filmography_from_web


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

    init_movies_and_actors()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_request(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_top_actors_movies)


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def modify_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    db.commit()
    return rv


def get_movies(nconst):
    results = query_db('SELECT tconst FROM Movie_Cast WHERE nconst=?;', [nconst])
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


def add_movie_cast_entry(tconst, nconst):
    modify_db("INSERT OR IGNORE INTO Movie_Cast (tconst, nconst) VALUES (?,?)",
                 [tconst, nconst])


def set_updated_date(tconst=None, nconst=None):
    if tconst:
        modify_db("UPDATE Movies SET updated=DATE('now') WHERE tconst=?", [tconst])
    if nconst:
        modify_db("UPDATE Actors SET updated=DATE('now') WHERE nconst=?", [nconst])


def init_movies_and_actors():
    mappings = [('https://datasets.imdbws.com/name.basics.tsv.gz', 'Actors'),
                ('https://datasets.imdbws.com/title.basics.tsv.gz', 'Movies')]
    for url, table_name in mappings:
        reader = pd.read_csv(url, sep='\t', header=0, chunksize=1000)
        with get_db() as database:
            for chunk in reader:
                chunk.to_sql(table_name, con=database, if_exists='append', index=False)


def get_top_nconsts():
    df = pd.read_csv('https://www.imdb.com/list/ls058011111/export?ref_=nmls_otexp', encoding='ISO-8859-1')
    top_nconst = df['Const'].values
    return top_nconst


@click.command('init-top-actors-movies')
@with_appcontext
def init_top_actors_movies():
    nconsts = get_top_nconsts()
    for nconst in nconsts:
        update_filmography(nconst)
        modify_db("UPDATE Actors SET updated=DATE('now') WHERE nconst=?", [nconst])


def update_filmography(nconst):
    filmography = get_filmography_from_web(nconst)
    for cast_item in filmography:
        add_movie_cast_entry(tconst=cast_item.tconst, nconst=cast_item.nconst)
    return filmography
