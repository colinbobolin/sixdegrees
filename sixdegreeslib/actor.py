class Actor:
    def __init__(self, _id):
        self._id = _id
        self._name = None

    def __repr__(self):
        return self.id

    @property
    def id(self):
        return self._id

    @property
    def actor_page_url(self):
        print("getter of actor_page_url called")
        return f"https://www.imdb.com/name/{self.id}"

    @property
    def movie_search_url(self):
        return f"https://www.imdb.com/search/title/?role={self.id}&sort=boxoffice_gross_us,desc"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        print("setter of name called")
        self._name = value

