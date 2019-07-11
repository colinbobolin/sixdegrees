from sixdegreeslib import search_tools
# from .actor import Actor
movie_library = {}


class Movie:

    # TODO save the @genre json key and if it is TVSeries, it is not a valid movie
    def __init__(self, movie_id):
        self.movie_id = movie_id
        self.url = search_tools.get_movie_url(self.movie_id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_name_from_html_soup(self.html_soup)
        self.image = search_tools.get_image_from_html_soup(self.html_soup)
        self.cast_list = []
        movie_library.update({self.movie_id: self})

    def __repr__(self):
        return f"{self.movie_id}: {self.name}"

    def get_cast_list(self):
        self.cast_list = search_tools.get_cast_list_for_movie_id(self.movie_id)

    def search_for(self, actor, degree, path):
        self.get_cast_list()
        for next_actor in self.cast_list:
            print(f"{next_actor.name}, and...")
            next_actor.search_for(actor, degree=degree+1, path=path+f"{self.name}-")
        return path




