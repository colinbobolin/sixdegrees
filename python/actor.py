from bs4 import BeautifulSoup
import requests
import json
import re

class Actor:
    address = ""
    name = ""
    movies_acted_in = []

    def __init__(self, address):
        self.address = address
        self.parse_actor_info()
        self.movies_acted_in = self.get_addresses_for_movies_acted_in()
        print(self.get_actor_soup())
        pass

    def get_actor_soup(self):
        return BeautifulSoup(requests.get(self.address).text, 'html.parser')

#TODO fix this. it is finding a links where an href doesn't exist
# <b><a href="/title/tt4919268/">Bad Boys 4</a></b>
    def get_addresses_for_movies_acted_in(self):
        soup = self.get_actor_soup()
        for link in soup.find_all('a'):
            print(link.get('href'))
            if re.compile("/title/[a-z]{2}[0-9]{7}/$").search(link.get('href')):
                pass
        # print(soup.prettify)

        return ["Aladdin"]

    def get_actor_name(self):
        return self.name

    def parse_actor_info(self):
        soup = self.get_actor_soup()
        data = json.loads(soup.find('script', type="application/ld+json").text)
        self.name = data['name']

