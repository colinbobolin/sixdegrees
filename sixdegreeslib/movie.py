from sixdegreeslib import search_tools
# from .actor import Actor
movie_library = {}


class Movie:

    def __init__(self, movie_id):
        self.movie_id = movie_id
        self.url = search_tools.get_movie_url(self.movie_id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_name_from_html_soup(self.html_soup)
        self.image = search_tools.get_image_from_html_soup(self.html_soup)
        self.cast_list = []
        self.genre = self.get_movie_genre()
        movie_library.update({self.movie_id: self})

    def __repr__(self):
        return f"{self.movie_id}: {self.name} genre:{self.genre} URL:{self.url}"

    def get_cast_list(self):
        self.cast_list = search_tools.get_cast_list_for_movie_id(self.movie_id)
        return self.cast_list

    def get_movie_genre(self):
        return search_tools.get_json_value_from_html_soup_matching_json_key(self.html_soup, 'genre')

    def get_movie_type(self):
        return search_tools.get_json_value_from_html_soup_matching_json_key(self.html_soup, '@type')
