from sixdegreeslib import search_tools
from sixdegreeslib.actor import Actor
from sixdegreeslib.game import Game


class SixDegrees:

    def main():
        while(True):
            Game()
        #possible_actors = []
        #while len(possible_actors) == 0:
        #    possible_actors = search_tools.search_for_actor_by_name(input("Enter a name: "))
        #for actor in possible_actors:
        #    print(actor)
        #actor1 = possible_actors[0]

        #actor1.get_top_25_movies()
        #movies1 = actor1.movies
        #actors2 = [Actor(actor_id) for actor_id in (movie.get_cast_list() for movie in movies1)]
        #for movie in movies1:
            #print(movie.name)

    if __name__=='__main__':
        main()
