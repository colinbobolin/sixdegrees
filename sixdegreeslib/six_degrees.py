from sixdegreeslib.network import Network
from sixdegreeslib import actor_search
import time

def main():
    start_actor = actor_search.get_actor_search_results_by_name("Cillian Murphy")[0]
    target_actor = actor_search.get_actor_search_results_by_name("Elijah Wood")[0]
    start_actor_id = start_actor[1]
    target_actor_id = target_actor[1]
    start_time = time.perf_counter()
    game = Network(start_actor_id, target_actor_id)
    game.search()
    end_time = time.perf_counter()
    time_taken = end_time - start_time
    print(f"Time Taken: {time_taken}")



if __name__=='__main__':
    main()
