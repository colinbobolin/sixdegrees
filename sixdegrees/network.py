from collections import deque
from flask import g
from sixdegrees import db


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









