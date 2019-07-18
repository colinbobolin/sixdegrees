from bs4 import BeautifulSoup
import requests
import re
from collections import deque
import time
from multiprocessing.dummy import Pool as ThreadPool


class Network:

    def __init__(self, start_id, target_id):
        self.start_id = start_id
        self.target_id = target_id
        print(f"new network created for {self.start_id} -> {self.target_id}")
        self.searched = []
        self.unsearched_actors = deque([self.start_id])
        self.unsearched_movies = deque()
        self.network = {start_id: None}
        self.found = False

    def search(self):
        while not self.found:
            print("target not found")
            self.load_more_movies()
            print("searching the next degree")
            self.load_more_actors()
            print(self.unsearched_actors)
        print(self.get_path())

    def load_more_actors(self):
        while self.unsearched_movies:
            movie = self.unsearched_movies.popleft()
            print(f"getting actors for {movie}")
            actors = self.get_actors(movie)
            # self.network.update({movie: actors}) moved this to the get_actors method
            if self.target_id in actors:
                self.found = True
                return
                #self.target_found()
            for actor in actors:
                if actor not in self.searched:
                    self.unsearched_actors.append(actor)
            self.searched.append(movie)

    def get_actors(self, movie):
        pool = ThreadPool(8)
        url = f"https://www.imdb.com/search/name/?roles={movie}&sort=starmeter,asc"
        # print(url)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        actor_aggregate = soup.find_all("div", {"class": "lister-item mode-detail"})
        actors = *pool.map(get_actor_id, actor_aggregate[:10]),
        self.network.update({movie: actors})
        pool.close()
        pool.join()
        return actors

    def load_more_movies(self):
        # print(f"loading more movies")
        while self.unsearched_actors:
            actor = self.unsearched_actors.popleft()
            print(f"getting movies for {actor}")
            movies = self.get_movies(actor)
            # self.network.update({actor: movies}) moved this to the get_movies method
            for movie in movies:
                if movie not in self.searched:
                    # print(f"adding {movie} to unsearched movies")
                    self.unsearched_movies.append(movie)
                else:
                    # print(f"{movie} already searched")
                    pass
            self.searched.append(actor)

    def get_movies(self, actor):
        pool = ThreadPool(8)
        #print(f"Searching for movie ids for actor id: {actor}")
        url = f"https://www.imdb.com/search/title/?role={actor}&sort=boxoffice_gross_us,desc"
        #print(url)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        movie_aggregate = soup.find_all("div", {"class": "lister-item mode-advanced"})
        movies = *pool.map(get_movie_id, movie_aggregate[:10]),
        self.network.update({actor: movies})
        pool.close()
        pool.join()
        return movies

    def target_found(self):
        print("TARGET FOUND")
        path = self.get_path()
        print(path)
        quit()

    def get_path(self):
        dq = deque()
        dq.append([self.start_id])
        while dq:
            path = dq.popleft()
            node = path[-1]
            if node == self.target_id:
                return path
            for adjacent in self.network.get(node, []):
                new_path = list(path)
                new_path.append(adjacent)
                dq.append(new_path)

    def print_network(self):
        for x in self.network:
            print(f"{x}: {self.network[x]}")


def get_actor_id(lister_item):
    if is_actor(lister_item):
        name_and_img = lister_item.find("a", {"href": re.compile("/name/nm[0-9]{7}")})
        return re.compile("nm[0-9]{7}").findall(name_and_img.get("href"))[0]


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




