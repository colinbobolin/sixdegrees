from bs4 import BeautifulSoup
import requests
import json
import re

from sixdegreeslib import search_tools


class Actor:
    actor_id = ""
    url = ""
    name = ""
    movies_acted_in = []

    def __init__(self, actor_id):
        self.actor_id = actor_id
        self.url = search_tools.get_actor_url(actor_id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_actor_name(self.html_soup)
        self.image = search_tools.get_actor_image(self.html_soup)
        self.movies_acted_in = search_tools.get_movies_for_actor_id(self.actor_id)

    def get_actor_name(self):
        return self.name
