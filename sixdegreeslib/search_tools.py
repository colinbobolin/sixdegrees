from bs4 import BeautifulSoup
import requests
import re
import json
from .movie import Movie
from .actor import Actor

ROOT_URL = "https://www.imdb.com/"
ACTOR_ID_SHAPE = re.compile("nm[0-9]{7}")
MOVIE_ID_SHAPE = re.compile("tt[0-9]{7}")
SEARCH_FOR = "search/"
NAME_ID = "name/"
TITLE_ID = "title/"
BY_NAME_STRING = "?name="
BY_ROLE = "?role="
BY_ROLES = "?roles="
COUNT_25 = "&count=25"


def search_for_actor_by_name(name):
    actor_ids = get_actor_ids_for_search_by_name(name)
    actor_ids = get_unique_items(actor_ids)
    return instantiate_actors_from_ids(actor_ids)


def get_actor_ids_for_search_by_name(name):
    url = get_search_url(name)
    html_soup = get_html_soup(url)
    actor_ids = get_actor_ids_from_html_soup(html_soup)
    #print(actor_ids)
    return actor_ids


def get_unique_items(iterable):
    results = []
    for item in iterable:
        if item not in results:
            results.append(item)
    return results


def get_html_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def get_search_url(name):
    #print(ROOT_URL + SEARCH_FOR + NAME_ID + BY_NAME_STRING + name.replace(" ", "+"))
    return ROOT_URL + SEARCH_FOR + NAME_ID + BY_NAME_STRING + name.replace(" ", "+")


def get_actor_url(actor_id):
    #print("getting actor url: " + ROOT_URL + NAME_ID + actor_id)
    return ROOT_URL + NAME_ID + actor_id


def get_movie_url(movie_id):
    #print("getting movie url: " + ROOT_URL + TITLE_ID + movie_id)
    return ROOT_URL + TITLE_ID + movie_id


def get_name_from_html_soup(html_soup):
    return get_json_value_from_html_soup_matching_json_key(html_soup, 'name')


def get_image_from_html_soup(html_soup):
    try:
        return get_json_value_from_html_soup_matching_json_key(html_soup, 'image')
    except KeyError:
        return None


def get_actor_ids_from_html_soup(html_soup):
    return get_ids_from_html_soup_matching_shape(html_soup, ACTOR_ID_SHAPE)


def get_movie_ids_from_html_soup(html_soup):
    return get_ids_from_html_soup_matching_shape(html_soup, MOVIE_ID_SHAPE)


def get_25_movies_for_actor_id(actor_id):
    #print(f"getting movies for actor id: {actor_id}\n{ROOT_URL + SEARCH_FOR + TITLE_ID + BY_ROLE + actor_id}")
    html_soup = get_html_soup(ROOT_URL + SEARCH_FOR + TITLE_ID + BY_ROLE + actor_id + COUNT_25)
    movie_ids = get_ids_from_html_soup_matching_shape(html_soup, MOVIE_ID_SHAPE)
    return instantiate_movies_from_ids(movie_ids)


def instantiate_movies_from_ids(movie_ids):
    return get_unique_items([Movie(movie_id) for movie_id in movie_ids])


def instantiate_actors_from_ids(actor_ids):
    return get_unique_items([Actor(actor_id) for actor_id in actor_ids])


def get_cast_list_for_movie_id(movie_id):
    html_soup = get_html_soup(ROOT_URL + SEARCH_FOR + NAME_ID + BY_ROLE + movie_id)
    actor_ids = get_ids_from_html_soup_matching_shape(html_soup, ACTOR_ID_SHAPE)
    return instantiate_actors_from_ids(actor_ids)


def get_a_tags(html_soup):
    return html_soup.find_all('a')


def get_href_list_from_bs4_result_set(bs4_result_set):
    return get_unique_items([a_tag.get('href') for a_tag in bs4_result_set])


def append_element_to_list_if_not_duplicate(element, list):
    if element not in list:
        list.append(element)


def get_ids_from_html_soup_matching_shape(html_soup, shape):
    results = []
    page_content = html_soup.find(id="pagecontent")
    a_tag_bs4_result_set = get_a_tags(page_content)
    href_list = get_href_list_from_bs4_result_set(a_tag_bs4_result_set)
    for href in href_list:
        if shape.search(href):
            #print("found an href in the html" + href)
            #print(f"appending {shape.findall(href)} to the results list")
            results.extend(shape.findall(href))
    return get_unique_items(results)


def get_json_value_from_html_soup_matching_json_key(html_soup, json_key):
    html_of_json_data = html_soup.find('script', type="application/ld+json").text
    #print(html_soup.find('script', type="application/ld+json").text)
    json_data = json.loads(html_of_json_data)
    return json_data[json_key]


