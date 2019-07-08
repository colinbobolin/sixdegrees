from sixdegreeslib import search_tools

class Actor:

    def __init__(self, actor_id):
        self.actor_id = actor_id
        self.url = search_tools.get_actor_url(actor_id)
        self.html_soup = search_tools.get_html_soup(self.url)
        self.name = search_tools.get_name_from_html(self.html_soup)
        self.image = search_tools.get_image_from_html(self.html_soup)
        self.movies_acted_in = search_tools.get_movies_for_actor_id(self.actor_id)
