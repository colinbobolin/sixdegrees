from bs4 import BeautifulSoup
import requests
import re
from collections import deque
from multiprocessing.dummy import Pool as ThreadPool
from .actor import Actor
from .movie import Movie


class Network:

    def __init__(self, start_id, target_id):
        self.start = Actor(start_id)
        self.target = Actor(target_id)
        print(f"new network created for {self.start.name} -> {self.target.name}")
        self.searched = []
        self.unsearched_actors = deque([self.start])
        self.unsearched_movies = deque()
        self.network = {self.start: None}
        self.found = False

    def search(self):
        print("Thinking hard about this one... please wait.")
        while not self.found:
            #print("target not found")
            self.load_more_movies()
            #print("searching the next degree")
            self.load_more_actors()
            #print(self.unsearched_actors)
        print(self.get_path())

    def load_more_actors(self):
        while self.unsearched_movies:
            movie = self.unsearched_movies.popleft()
            #print(f"getting actors for {movie}")
            actors = self.get_actors(movie)
            if self.target.id in [actor.id for actor in actors]:
                self.found = True
                return
            for actor in actors:
                if actor not in self.searched:
                    self.unsearched_actors.append(actor)
            self.searched.append(movie)

    def get_actors(self, movie):
        url = f"https://www.imdb.com/search/name/?roles={movie.id}&sort=starmeter,asc"
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        actor_aggregate = soup.find_all("div", {"class": "lister-item mode-detail"})
        actors = [Actor(get_actor_id(actor)) for actor in actor_aggregate[:10]]
        self.network.update({movie: actors})
        return actors

    def load_more_movies(self):
        # print(f"loading more movies")
        while self.unsearched_actors:
            actor = self.unsearched_actors.popleft()
            #print(f"getting movies for {actor}")
            movies = self.get_movies(actor)
            for movie in movies:
                if movie not in self.searched:
                    # print(f"adding {movie} to unsearched movies")
                    self.unsearched_movies.append(movie)
                else:
                    # print(f"{movie} already searched")
                    pass
            self.searched.append(actor)

    def get_movies(self, actor):
        #print(f"Searching for movie ids for actor id: {actor}")
        url = f"https://www.imdb.com/search/title/?role={actor.id}&sort=boxoffice_gross_us,desc"
        #print(url)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        movie_aggregate = soup.find_all("div", {"class": "lister-item mode-advanced"})
        movies = [Movie(get_movie_id(movie)) for movie in movie_aggregate[:10]]
        self.network.update({actor: movies})
        return movies

    def get_path(self):
        dq = deque()
        dq.append([self.start])
        while dq:
            path = dq.popleft()
            node = path[-1]
            if node.id == self.target.id:
                return path
            for adjacent in self.network.get(node, []):
                new_path = list(path)
                new_path.append(adjacent)
                dq.append(new_path)

    def print_network(self):
        for x in self.network:
            print(f"{x}: {self.network[x]}")


def parse_actor_info(lister_item):
    id_ = get_actor_id(lister_item)
    actor = Actor(id_)
    actor.name = parse_actor_name(lister_item)
    actor.image = parse_actor_image(lister_item)


def get_actor_id(lister_item):
    if is_actor(lister_item):
        name_and_img = lister_item.find("a", {"href": re.compile("/name/nm[0-9]{7}")})
        return re.compile("nm[0-9]{7}").findall(name_and_img.get("href"))[0]


# TODO
def parse_actor_name(lister_item):
    pass


# TODO
def parse_actor_image(lister_item):
    pass


def is_actor(lister_item):
    try:
        role_type = lister_item.find("p", {"class": "text-muted text-small"}).contents[0].strip()
        return role_type == "Actor" or role_type == "Actress"
    except AttributeError:
        return False


def get_movie_id(lister_item):
    if is_movie(lister_item):
        image_detail = lister_item.find("a", {"href": re.compile("/title/tt[0-9]{7}")})
        return re.compile("tt[0-9]{7}").findall(image_detail.get("href"))[0]


# TODO complete this check. Not super important, but may be relevant in corner cases
def is_movie(lister_item):
    return True




