from bs4 import BeautifulSoup
import requests
import re
import json
from .movie import Movie

ROOT_URL = "https://www.imdb.com/"
ACTOR_ID_SHAPE = re.compile("nm[0-9]{7}/?$")
MOVIE_ID_SHAPE = re.compile("tt[0-9]{7}/?$")
SEARCH_FOR = "search/"
NAME_ID = "name/"
TITLE_ID = "title/"
BY_NAME_STRING = "?name="
BY_ROLE = "?role="
BY_ROLES = "?roles="
COUNT_25 = "&count=25"


def search_for_actor_by_name(name):
    url = get_search_url(name)
    html_soup = get_html_soup(url)
    # print(html_soup)
    return get_actor_ids_from_html_soup(html_soup)


def get_html_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def get_search_url(name):
    print(ROOT_URL + SEARCH_FOR + NAME_ID + BY_NAME_STRING + name.replace(" ", "+"))
    return ROOT_URL + SEARCH_FOR + NAME_ID + BY_NAME_STRING + name.replace(" ", "+")


def get_actor_url(actor_id):
    print(ROOT_URL + NAME_ID + actor_id)
    return ROOT_URL + NAME_ID + actor_id


def get_movie_url(movie_id):
    print(ROOT_URL + TITLE_ID + movie_id)
    return ROOT_URL + TITLE_ID + movie_id


def get_name_from_html_soup(html_soup):
    return get_json_value_from_html_soup_matching_json_key(html_soup, 'name')


def get_image_from_html_soup(html_soup):
    try:
        return get_json_value_from_html_soup_matching_json_key(html_soup, 'image')
    except KeyError:
        return None


def get_actor_ids_from_html_soup(html_soup):
    return get_href_from_html_soup_matching_shape(html_soup, ACTOR_ID_SHAPE)


def get_movie_urls_from_html_soup(html_soup):
    return get_href_from_html_soup_matching_shape(html_soup, MOVIE_ID_SHAPE)


def get_25_movies_for_actor_id(actor_id):
    # print(f"getting movies for actor id: {actor_id}\n{ROOT_URL + SEARCH_FOR + TITLE_ID + BY_ROLE + actor_id}")
    html_soup = get_html_soup(ROOT_URL + SEARCH_FOR + TITLE_ID + BY_ROLE + actor_id + COUNT_25)
    movie_ids = get_href_from_html_soup_matching_shape(html_soup, MOVIE_ID_SHAPE)
    return instantiate_movies_from_ids(movie_ids)


def instantiate_movies_from_ids(movie_ids):
    movies = []
    for movie_id in movie_ids:
        # print(movie_id)
        append_element_to_list_if_not_duplicate(Movie(movie_id), movies)
    return movies


def get_cast_list_for_movie_id(movie_id):
    html_soup = get_html_soup(ROOT_URL + SEARCH_FOR + NAME_ID + BY_ROLE + movie_id)
    return get_href_from_html_soup_matching_shape(html_soup, ACTOR_ID_SHAPE)


def get_a_tags_from_html_soup(html_soup):
    return html_soup.find_all('a')


def get_href_list_from_bs4_result_set(bs4_result_set):
    href_list = []
    for a_tag in bs4_result_set:
        append_element_to_list_if_not_duplicate(a_tag.get('href'), href_list)
    return href_list


def append_element_to_list_if_not_duplicate(element, list):
    if element not in list:
        list.append(element)


def element_matches_shape(element, shape):
    return shape.search(element)


def get_href_from_html_soup_matching_shape(html_soup, shape):
    results = []
    a_tag_list = get_a_tags_from_html_soup(html_soup)
    href_list = get_href_list_from_bs4_result_set(a_tag_list)
    for href in href_list:
        if shape.search(href):
            print(href)
            append_element_to_list_if_not_duplicate(href, results)
    return results


def get_json_value_from_html_soup_matching_json_key(html_soup, json_key):
    html_of_json_data = html_soup.find('script', type="application/ld+json").text
    json_data = json.loads(html_of_json_data)
    return json_data[json_key]


