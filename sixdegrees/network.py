from collections import deque
from flask import g
from sixdegrees import db


# def get_network():
#     if 'network' not in g:
#         g.network = {}
#     return g.network
#
#
# class Network:
#     def __init__(self, start, end):
#         """start and target are nconst for each actor"""
#         self.start = start
#         self.end = end
#         self.searched = []
#         self.unsearched_actors = deque([self.start])
#         self.unsearched_movies = deque()
#         self.network = get_network()
#         self.network.update({self.start: None})
#         self.found = False
#         while not self.found:
#             self.load_more_movies()
#             self.load_more_actors()
#         path_const = self.calc_path()
#         self.path = [db.get_name(elem) for elem in path_const]
#
#     def load_more_actors(self):
#         while self.unsearched_movies:
#             tconst = self.unsearched_movies.popleft()
#             actors = db.get_actors(tconst)
#             get_network().update({tconst: actors})
#             if self.end in actors:
#                 self.found = True
#                 return
#             for actor in actors:
#                 if actor not in self.searched:
#                     self.unsearched_actors.append(actor)
#             self.searched.append(tconst)
#
#     def load_more_movies(self):
#         while self.unsearched_actors:
#             nconst = self.unsearched_actors.popleft()
#             movies = db.get_movies(nconst)
#             self.network.update({nconst: movies})
#             for tconst in movies:
#                 if tconst not in self.searched:
#                     self.unsearched_movies.append(tconst)
#                 else:
#                     pass
#             self.searched.append(nconst)
#
#     def calc_path(self):
#         dq = deque()
#         dq.append([self.start])
#         while dq:
#             path = dq.popleft()
#             node = path[-1]
#             if node == self.end:
#                 return path
#             for adjacent in self.network.get(node, []):
#                 new_path = list(path)
#                 new_path.append(adjacent)
#                 dq.append(new_path)


def get_path(nconst1, nconst2):
    dq = deque()
    dq.append([nconst1])
    while dq:
        path = dq.popleft()
        node = path[-1]
        if node == nconst2:
            return path
        for adjacent in db.get_connected_actors(node):
            new_path = list(path)
            new_path.append(adjacent)
            dq.append(new_path)


def get_path_representation(nconst_list):
    print(nconst_list)
    path = []
    for index, elem in enumerate(nconst_list):
        try:
            cur = elem
            next = nconst_list[index+1]
            path.append(
                f"{db.get_name(cur)} was in "
                f"{db.get_name(db.get_direct_relationship(cur, next)[0])} "
                f"with {db.get_name(next)}"
            )
        except IndexError:
            pass
    return path









