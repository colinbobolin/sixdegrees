from collections import namedtuple
from bs4 import BeautifulSoup
import requests
import re


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
    try:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        lister_items = soup.find_all("div", {"class": "lister-item mode-advanced"})
        for item in lister_items:
            tconst = parse_tconst(item)
            filmography.append(CastItem(tconst=tconst,
                                        nconst=nconst))
    except ConnectionError:
        print(f'Connection error when retrieving {nconst}\'s movies. Continuing')
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