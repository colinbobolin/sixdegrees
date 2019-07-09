from sixdegreeslib import search_tools
from sixdegreeslib.actor import Actor


class SixDegrees:

    def main():

        possible_actors = []
        while len(possible_actors) == 0:
            search1 = input("Enter the first actor: ")
            possible_actors = search_tools.search_for_actor_by_name(search1)
        for actor_id in possible_actors:
            search_result = Actor(actor_id)
            print(f"{search_result}")
        actor1 = Actor(input("enter the id of the actor you want"))

        movies1 = actor1.movies
        for movie in movies1:
            print(movie.name)

    if __name__=='__main__':
        main()
