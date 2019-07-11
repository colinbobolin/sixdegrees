from sixdegreeslib import search_tools
# from .movie import Movie
actor_library = {}


class Actor:

    def __init__(self, actor_id):
        self.actor_id = actor_id
        # print(f"An actor was created with id {self.actor_id}")
        self.url = search_tools.get_actor_url(self.actor_id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_name_from_html_soup(self.html_soup)
        self.image = search_tools.get_image_from_html_soup(self.html_soup)
        self.movies = []  # since this is a slow process, get the actor's movies only when calculating the network
        actor_library.update({self.actor_id: self})

    def __repr__(self):
        return f"{self.actor_id}: {self.name}, image: {self.image}\nURL: {self.url}"

    def get_top_25_movies(self):
        self.movies = search_tools.get_25_movies_for_actor_id(self.actor_id)

    # TODO let's just do one degree at a time...
    def search_for(self, actor, degree=1, path=""):
        if self.name == actor.name:
            return path.append(self)
        while degree < 6:
            self.get_top_25_movies()
            for movie in self.movies:
                print(f"{self.name} was in {movie.name} with...")
                movie.search_for(actor, degree, path=path + f"{self.name}-")
                print("no connection...")
        return "Wow! You managed to find 2 actors with more than six degrees of separation!"
