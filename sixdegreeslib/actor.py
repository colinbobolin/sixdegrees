from sixdegreeslib import search_tools


class Actor:

    def __init__(self, actor_id, degree: int = None):
        self.actor_id = actor_id
        print(f"An actor was created with id {self.actor_id}")
        self.url = search_tools.get_actor_url(self.actor_id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_name_from_html_soup(self.html_soup)
        self.image = search_tools.get_image_from_html_soup(self.html_soup)
        self.movies = []  # since this is a slow process, get the actor's movies only when calculating the network
        self.degree = degree

    def __repr__(self):
        return f"{self.actor_id}: {self.name}, image={self.image}"

    def get_top_25_movies(self):
        self.movies = search_tools.get_25_movies_for_actor_id(self.actor_id)
