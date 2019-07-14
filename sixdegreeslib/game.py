from sixdegreeslib import search_tools


class Game:
    def __init__(self):
        # prompt user for two actors
        #values = input("enter two actors: ")
        #(actor_name1, actor_name2) = values.split(",")
        #actor1 = search_tools.get_actor_search_results_by_name(actor_name1)[0]
        actor1 = search_tools.get_actor_search_results_by_name("Leonardo DiCaprio")[0]
        print(actor1)
        #actor2 = search_tools.get_actor_search_results_by_name(actor_name2)[0]
        actor2 = search_tools.get_actor_search_results_by_name("Kate Winslet")[0]
        print(actor2)
        actor1.get_network()
        #for associate in actor1.get_direct_associates():
        #    print(associate)
        #play(actor1, actor2)
        #while not actor1.network.__contains__(actor2):
        #    actor1.network.get_next_degree()


def play(start_actor, end_actor):
    degree = get_next_degree([start_actor])
    degree_num = 1
    print("printing degree %d", degree_num)
    for element in degree:
        print(element)
    while not actor_in_degree(end_actor, degree):
        degree = get_next_degree(degree)
        degree_num += 1
    print(f"FOUND ACTOR IN {degree_num} DEGREES")


def actor_in_degree(end_actor, actor_list):
    return end_actor in actor_list


def get_next_degree(degree):
    next_degree = []
    for actor_obj in degree:
        movies = actor_obj.get_top_movies()
        for movie_obj in movies:
            next_degree.append(cast_member for cast_member in movie_obj.get_cast_list())
    #movies = [movie_obj for movie_obj in [actor_obj.get_top_movies() for actor_obj in degree]]
    #return [actor_obj for actor_obj in [movie_obj.get_cast_list() for movie_obj in movies]]
    return next_degree

