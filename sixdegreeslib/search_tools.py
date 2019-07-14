from bs4 import BeautifulSoup
import requests
import re
import json
from .movie import Movie
from .actor import Actor
from sixdegreeslib import movie
from sixdegreeslib import actor

ROOT_URL = "https://www.imdb.com/"
ACTOR_ID_SHAPE = re.compile("nm[0-9]{7}")
MOVIE_ID_SHAPE = re.compile("tt[0-9]{7}")
SEARCH_FOR = "search/"
NAME = "name/"
TITLE = "title/"
BY_NAME_STRING = "?name="
BY_ROLE = "?role="
BY_ROLES = "?roles="
COUNT_25 = "&count=25"
SORT_BY_BOX_OFFICE_DESC = "&sort=boxoffice_gross_us,desc"
html_dict = {}
actor_dict = {}
movie_dict = {}


def get_actor_search_results_by_name(name):
    print(f"Searching IMDB for: {name}.")
    actor_ids = get_unique_items(get_actor_ids_for_search_by_name(name))
    print(f"Found {len(actor_ids)} possible matches! Instantiating the first 5 actors for you.")
    return [get_actor_by_id(actor_id) for actor_id in actor_ids[:5]]


def get_top_movies_for_actor_id(actor_id):
    print(f"getting movies for actor id: {actor_id}\n{ROOT_URL + SEARCH_FOR + TITLE + BY_ROLE + actor_id}...")
    html_soup = get_html_soup(ROOT_URL + SEARCH_FOR + TITLE + BY_ROLE + actor_id + SORT_BY_BOX_OFFICE_DESC)
    page_content = get_page_content(html_soup)
    movie_ids = get_ids_from_html_soup_matching_shape(page_content, MOVIE_ID_SHAPE)
    valid_movie_ids = [movie_id for movie_id in movie_ids if is_valid_movie(movie_id)][:5]  # returns first 5 movies
    return [get_movie_by_id(movie_id) for movie_id in valid_movie_ids]


def get_movie_by_id(movie_id):
    if movie_id not in movie_dict.keys():
        movie_dict.update({movie_id: Movie(movie_id)})
        print(f"created a new movie: {movie_dict.get(movie_id)}")
    return movie_dict.get(movie_id)


def get_cast_list_for_movie_id(movie_id):
    html_soup = get_html_soup(ROOT_URL + TITLE + movie_id)
    cast_content = get_cast_content(html_soup)
    actor_ids = get_ids_from_html_soup_matching_shape(cast_content, ACTOR_ID_SHAPE)
    #valid_actor_ids = [actor_id for actor_id in actor_ids if is_valid_actor(actor_id)]
    print(f"Getting top 20 cast members for {get_movie_by_id(movie_id).name}")
    return [get_actor_by_id(actor_id) for actor_id in actor_ids[:20]]


def get_actor_by_id(actor_id):
    if actor_id not in actor_dict.keys():
        actor_dict.update({actor_id: Actor(actor_id)})
        print(f"created a new actor: {actor_dict.get(actor_id)}")
    else:
        print(f"found an existing actor: {actor_dict.get(actor_id)}")
    return actor_dict.get(actor_id)


def get_actor_ids_for_search_by_name(name):
    url = get_search_url(name)
    html_soup = get_html_soup(url)
    page_content = get_page_content(html_soup)
    return get_actor_ids_from_html_soup(page_content)


def get_page_content(html_soup):
    return html_soup.find(id="pagecontent")


def get_cast_content(html_soup):
    return html_soup.find(id="titleCast")


def get_unique_items(iterable):
    results = []
    for item in iterable:
        if item not in results:
            results.append(item)
    return results


def get_html_soup(url):
    if url not in html_dict.keys():
        html_dict.update({url: BeautifulSoup(requests.get(url).text, 'html.parser')})
        #print(html_dict.get(url))
    return html_dict.get(url)


def get_search_url(name):
    #print(ROOT_URL + SEARCH_FOR + NAME_ID + BY_NAME_STRING + name.replace(" ", "+"))
    return ROOT_URL + SEARCH_FOR + NAME + BY_NAME_STRING + name.replace(" ", "+")


def get_actor_url(actor_id):
    #print("getting actor url: " + ROOT_URL + NAME_ID + actor_id)
    return ROOT_URL + NAME + actor_id


def get_movie_url(movie_id):
    #print("getting movie url: " + ROOT_URL + TITLE_ID + movie_id)
    return ROOT_URL + TITLE + movie_id


def get_name_from_html_soup(html_soup):
    return get_json_value_from_html_soup_matching_json_key(html_soup, 'name')


def get_image_from_html_soup(html_soup):
    try:
        return get_json_value_from_html_soup_matching_json_key(html_soup, 'image')
    except KeyError:
        return None


def get_actor_ids_from_html_soup(html_soup):
    actor_ids = get_ids_from_html_soup_matching_shape(html_soup, ACTOR_ID_SHAPE)
    return [actor_id for actor_id in actor_ids]


def is_valid_movie(movie_id):
    return get_json_value_from_html_soup_matching_json_key(get_html_soup(get_movie_url(movie_id)), '@type') == "Movie"


def get_a_tags(html_soup):
    return html_soup.find_all('a')


def get_href_list_from_bs4_result_set(bs4_result_set):
    return get_unique_items([tag.get('href') for tag in bs4_result_set])


def append_element_to_list_if_not_duplicate(element, list):
    if element not in list:
        list.append(element)


# TODO this method probably needs some more abstraction
def get_ids_from_html_soup_matching_shape(html_soup, shape):
    results = []
    a_tag_bs4_result_set = get_a_tags(html_soup)
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


