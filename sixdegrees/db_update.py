# This class provides functions for updating the database
# with information gathered from IMDb.com

import requests
from sixdegrees import db
from bs4 import BeautifulSoup
import re
from collections import namedtuple
import datetime


def update_cast_if_not_updated(tconst):
    query_result = db.query_db('SELECT updated FROM Movies WHERE tconst=?', [tconst])
    for row in query_result:
        #print(f"{tconst}: {row['updated']}")
        if not row['updated']:
            update_cast_list(tconst)


def update_filmography_if_not_updated(nconst):
    query_result = db.query_db('SELECT updated FROM Actors WHERE nconst=?', [nconst])
    for row in query_result:
        #print(f"{row['updated']}")
        if not row['updated']:
            update_filmography(nconst)


def update_cast_list(tconst):
    print(f"updating cast list for {tconst}")
    cast_list = get_cast_list_from_web(tconst)
    for cast_item in cast_list:
        add_cast_member(tconst=cast_item.tconst,
                        nconst=cast_item.nconst)
    set_updated_date(tconst=tconst)


def update_filmography(nconst):
    print(f"updating filmography for {nconst}")
    movies = []
    filmography = get_filmography_from_web(nconst)
    for film_item in filmography:
        add_cast_member(tconst=film_item.tconst,
                        nconst=film_item.nconst)
        title = db.query_db('SELECT title FROM Movies WHERE tconst=?', [film_item.tconst])[0]['title']
        movies.append(title)
    set_updated_date(nconst=nconst)
    return movies


def add_cast_member(tconst, nconst):
    db.modify_db("INSERT OR IGNORE INTO Movie_Cast (tconst, nconst) VALUES (?,?)",
                 [tconst, nconst])


def set_updated_date(tconst=None, nconst=None):
    if tconst:
        db.modify_db("UPDATE Movies SET updated=DATE('now') WHERE tconst=?", [tconst])
    if nconst:
        db.modify_db("UPDATE Actors SET updated=DATE('now') WHERE nconst=?", [nconst])


def get_cast_list_from_web(tconst):
    """Returns a list of namedtuple('CastItem', 'tconst nconst')"""
    cast_list = []
    CastItem = namedtuple('CastItem', 'tconst nconst')
    url = f"https://www.imdb.com/search/name/?roles={tconst}&sort=starmeter,asc"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    lister_items = soup.find_all("div", {"class": "lister-item mode-detail"})
    for item in lister_items[:10]:
        nconst = parse_nconst(item)
        category = parse_category(item)
        if category in ('Actor', 'Actress'):
            cast_list.append(CastItem(tconst=tconst,
                                      nconst=nconst))
    return cast_list


def get_filmography_from_web(nconst):
    """Returns a list of namedtuple('CastItem', 'tconst nconst')"""
    filmography = []
    CastItem = namedtuple('CastItem', 'tconst nconst')
    url = f"https://www.imdb.com/search/title/?roles={nconst}&sort=boxoffice_gross_us,desc"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    lister_items = soup.find_all("div", {"class": "lister-item mode-advanced"})
    for item in lister_items:
        tconst = parse_tconst(item)
        filmography.append(CastItem(tconst=tconst,
                                    nconst=nconst))
    return filmography


def parse_nconst(lister_item):
    name_and_img = lister_item.find("a", {"href": re.compile("/name/nm[0-9]{7}")})
    return re.compile("nm[0-9]{7}").findall(name_and_img.get("href"))[0]


def parse_category(lister_item):
    try:
        role_type = lister_item.find("p", {"class": "text-muted text-small"}).contents[0].strip()
    except AttributeError:
        role_type = None
    return role_type


def parse_actor_name(lister_item):
    return lister_item.find("img").get("alt")


def parse_actor_image(lister_item):
    return lister_item.find("img").get("src")


def parse_tconst(lister_item):
    image_detail = lister_item.find("a", {"href": re.compile("/title/tt[0-9]{7}")})
    return re.compile("tt[0-9]{7}").findall(image_detail.get("href"))[0]


def parse_movie_name(lister_item):
    return lister_item.find("img").get("alt")


def parse_movie_image(lister_item):
    return lister_item.find("img").get("src")