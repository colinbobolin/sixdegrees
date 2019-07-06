from bs4 import BeautifulSoup
import requests
import re

BASE_WEB_ADDRESS = "https://www.imdb.com/"


def find_connection__between_actors(actor1, actor2):
    pass


def get_possible_actor_addresses_by_name(actor):
    html = get_html_for_actor_search(get_search_url(actor))
    possible_actor_addresses = []
    for link in html.find_all('a'):
        if re.compile("/name/nm[0-9]{7}$").search(link.get('href')):
            possible_actor_addresses.append(BASE_WEB_ADDRESS + link.get('href'))
    return possible_actor_addresses


# advanced search URL for an actor.
# https://www.imdb.com/search/name/?name=Will+Smith
def get_search_url(actor):
    return BASE_WEB_ADDRESS + "search/name/?name=" + actor.replace(" ", "+")


def get_html_for_actor_search(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def main():
    # url = get_search_url("Will Smith")
    # html = get_html_for_actor_search(url)
    possible_actor_addresses = get_possible_actor_addresses_by_name("Will Smith")
    #for actor in possible_actor_addresses: print(actor)
    # print(search_for_actor("Will Smith") + "{.__name__}")


main()
