from sixdegreeslib import search_tools


class Movie:

    # TODO save the @genre json key and if it is TVSeries, it is not a valid movie
    def __init__(self, movie_id):
        self.movie_id = movie_id
        self.url = search_tools.get_movie_url(self.movie_id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_name_from_html_soup(self.html_soup)
        self.image = search_tools.get_image_from_html_soup(self.html_soup)
        self.cast_list = []

    def __repr__(self):
        return f"{self.movie_id}: {self.name}"

    def get_cast_list(self):
        self.cast_list = search_tools.get_cast_list_for_movie_id(self.movie_id)
