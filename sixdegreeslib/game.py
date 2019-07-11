from sixdegreeslib import search_tools

class Game:
    def __init__(self):
        # prompt user for two actors
        values = input("enter two actors: ")
        (actor_name1, actor_name2) = values.split(",")
        actor1 = search_tools.search_for_actor_by_name(actor_name1)[0]
        print(actor1)
        actor2 = search_tools.search_for_actor_by_name(actor_name2)[0]
        print(actor2)
        print(actor1.search_for(actor2))

