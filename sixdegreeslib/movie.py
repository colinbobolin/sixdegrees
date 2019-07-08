from sixdegreeslib import search_tools

class Movie:

    def __init__(self, id):
        self.id = id
        self.url = search_tools.get_movie_url(self.id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_name_from_html(self.html_soup)
        self.image = search_tools.get_image_from_html(self.html_soup)
        self.cast_list = search_tools.get_cast_list_for_movie_id(self.id)