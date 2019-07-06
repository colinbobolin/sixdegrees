#testing push to master

from bs4 import BeautifulSoup
import requests
import re

BASE_WEB_ADDRESS = "https://www.imdb.com/"


def find_connection__between_actors(actor1, actor2):
    pass


# TODO get regular expression to return the first link that has no trailing ?ref
def search_for_actor(actor):
    html = get_html_for_actor_search(get_search_url(actor))
    html.find_all(text=re.compile('name/nm[0-9]{7}'))
    for link in html.find_all('a'):
        if "/name/nm" in link.get('href'):
            print(BASE_WEB_ADDRESS + link.get('href'))
            # return BASE_WEB_ADDRESS + link
    pass


# advanced search URL for an actor.
# https://www.imdb.com/search/name/?name=Will+Smith
def get_search_url(actor):
    return BASE_WEB_ADDRESS + "search/name/?name=" + actor.replace(" ", "+")


def get_html_for_actor_search(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')


def main():
    # url = get_search_url("Will Smith")
    # html = get_html_for_actor_search(url)
    search_for_actor("Will Smith")


main()
