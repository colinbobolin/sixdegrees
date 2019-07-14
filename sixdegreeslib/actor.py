from sixdegreeslib import search_tools
from .network import Network

class Actor:

    def __init__(self, actor_id, path_string=None):
        self.actor_id = actor_id
        self.url = search_tools.get_actor_url(self.actor_id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_name_from_html_soup(self.html_soup)
        self.image = search_tools.get_image_from_html_soup(self.html_soup)
        self.path_string = path_string

    def __repr__(self):
        return f"{self.actor_id}: {self.name}, image: {self.image} URL: {self.url}"

    def get_top_movies(self):
        return search_tools.get_top_movies_for_actor_id(self.actor_id)

    def get_network(self):
        #network = []
        #for movie_obj in self.get_top_movies():
        #    for actor_obj in movie_obj.get_cast_list():
        #        network.append((movie_obj.name, actor_obj.name))
        #for tup in network:
        #    print(tup)
        #return network
        network = {}
        for movie_obj in self.get_top_movies():
            actors = [actor_obj.name for actor_obj in movie_obj.get_cast_list()]
            network.update({movie_obj: actors})
        for key in network:
            print(key)
        return network


