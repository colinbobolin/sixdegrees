from bs4 import BeautifulSoup
import requests
import re
import json

ROOT_URL = "https://www.imdb.com/"
ACTOR_URL_SHAPE = re.compile("/name/nm[0-9]{7}/$")
MOVIE_URL_SHAPE = re.compile("/title/tt[0-9]{7}/$")
SEARCH_FOR = "search/"
NAME_ID = "name/"
BY_NAME_STRING = "?name="
MOVIES_BY_ACTOR_ID= "title/?role="
SUFFIX_FIRST_100 = "&count=100"


def search_for_actor_by_name(name):
    url = get_search_url(name)
    html_soup = get_html_soup(url)
    return get_actor_ids_from_html_soup(html_soup)


def get_html_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def get_search_url(name):
    return ROOT_URL + SEARCH_FOR + NAME_ID + BY_NAME_STRING + name.replace(" ", "+")


def get_movie_urls_from_html_soup(html_soup):
    return search_html_soup_for_href_shape(html_soup, MOVIE_URL_SHAPE)


# TODO the naming isn't clear here
def get_actor_ids_from_html_soup(html_soup):
    return search_html_soup_for_href_shape(html_soup, ACTOR_URL_SHAPE)


def get_movies_for_actor_id(actor_id):
    html_soup = get_html_soup(ROOT_URL + SEARCH_FOR + MOVIES_BY_ACTOR_ID + actor_id)
    return search_html_soup_for_href_shape(html_soup, MOVIE_URL_SHAPE)


def search_html_soup_for_href_shape(html_soup, shape):
    results = []
    for link in html_soup.find_all('a'):
        if shape.search(link.get('href')):
            #if link.get('href') is not None:
            results.append(ROOT_URL + link.get('href'))
    return results


def search_html_soup_for_json_key(html_soup, json_key):
    html_of_json_data = html_soup.find('script', type="application/ld+json").text
    json_data = json.loads(html_of_json_data)
    return json_data[json_key]


def get_actor_name(html_soup):
    return search_html_soup_for_json_key(html_soup, 'name')


def get_actor_url(actor_id):
    return ROOT_URL + NAME_ID + actor_id


def get_actor_image(html_soup):
    return search_html_soup_for_json_key(html_soup, 'image')
