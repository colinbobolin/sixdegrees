# This class provides functions for updating the database
# with information gathered from IMDb.com

import requests
from sixdegrees import db
from flask import current_app
import os
import pandas as pd


# def update_filmography(nconst):
#     print(f"updating filmography for {nconst}")
#     movies = []
#     filmography = get_filmography_from_web(nconst)
#     for film_item in filmography:
#         add_movie_cast_entry(tconst=film_item.tconst,
#                              nconst=film_item.nconst)
#         title = db.query_db('SELECT title FROM Movies WHERE tconst=?', [film_item.tconst])[0]['title']
#         movies.append(title)
#     set_updated_date(nconst=nconst)
#     return movies


def add_movie_cast_entry(tconst, nconst):
    db.modify_db("INSERT OR IGNORE INTO Movie_Cast (tconst, nconst) VALUES (?,?)",
                 [tconst, nconst])


def set_updated_date(tconst=None, nconst=None):
    if tconst:
        db.modify_db("UPDATE Movies SET updated=DATE('now') WHERE tconst=?", [tconst])
    if nconst:
        db.modify_db("UPDATE Actors SET updated=DATE('now') WHERE nconst=?", [nconst])


def init_movies_and_actors():
    init_table_from_web('https://datasets.imdbws.com/name.basics.tsv.gz', 'Actors')
    init_table_from_web('https://datasets.imdbws.com/title.basics.tsv.gz', 'Movies')


def init_table_from_web(url, table):
    transfer_csv_to_db(csv_file=pull_csv(url), db_table_name=table)


def pull_csv(url):
    r = requests.get(url)
    path = os.path.join(current_app.instance_path, url.split('/')[-1])
    with open(path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=512):
            fd.write(chunk)
    print("Data file pulled")
    return path


def transfer_csv_to_db(csv_file, db_table_name):
    reader = pd.read_csv(csv_file, sep='\t', chunksize=1000)
    with db.get_db() as database:
        for chunk in reader:
            chunk.to_sql(db_table_name, con=database, if_exists='append', index=False)
    print("Data transferred to database")