from collections import deque
from flask import g
from sixdegrees import db


def get_network():
    if 'network' not in g:
        g.network = {}
    return g.network


class Network:
    def __init__(self, start, end):
        """start and target are nconst for each actor"""
        self.start = start
        self.end = end
        #print(f"new network created for {self.start} -> {self.end}")
        self.searched = []
        self.unsearched_actors = deque([self.start])
        self.unsearched_movies = deque()
        self.network = get_network()
        self.network.update({self.start: None})
        #print("Thinking hard about this one... please wait.")
        self.found = False
        while not self.found:
            self.load_more_movies()
            self.load_more_actors()
        path_const = self.get_path()
        #print([db.get_name(elem) for elem in path_const])
        self.path = [db.get_name(elem) for elem in path_const]

    def load_more_actors(self):
        #print("loading more actors.")
        while self.unsearched_movies:
            tconst = self.unsearched_movies.popleft()
           #print(f"loading actors for {tconst}")
            actors = db.get_actors(tconst)
            get_network().update({tconst: actors})
            if self.end in actors:
                self.found = True
                return
            for actor in actors:
                if actor not in self.searched:
                    self.unsearched_actors.append(actor)
            self.searched.append(tconst)

    def load_more_movies(self):
        # print(f"loading more movies")
        while self.unsearched_actors:
            nconst = self.unsearched_actors.popleft()
            movies = db.get_movies(nconst)
            self.network.update({nconst: movies})
            for tconst in movies:
                if tconst not in self.searched:
                    self.unsearched_movies.append(tconst)
                else:
                    pass
            self.searched.append(nconst)

    def get_path(self):
        dq = deque()
        dq.append([self.start])
        while dq:
            path = dq.popleft()
            node = path[-1]
            if node == self.end:
                return path
            for adjacent in self.network.get(node, []):
                new_path = list(path)
                new_path.append(adjacent)
                dq.append(new_path)









