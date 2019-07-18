from bs4 import BeautifulSoup
import requests
import re


def get_actor_search_results_by_name(name):
    print(f"Searching IMDB for: {name}.")
    return get_actor_ids_for_search_by_name(name)


def get_actor_ids_for_search_by_name(name):
    url = "https://www.imdb.com/search/name/?name=" + name.replace(" ", "+")
    print(url)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    return parse_search_results(soup)


def parse_search_results(soup):
    results = []
    actor_aggregate = soup.find_all("div", {"class": "lister-item mode-detail"})
    for actor_details in actor_aggregate:
        name_and_img = actor_details.find("a", {"href": re.compile("/name/nm[0-9]{7}")})
        img_src = name_and_img.find("img").get("src")
        name = name_and_img.find("img").get("alt")
        id_ = re.compile("nm[0-9]{7}").findall(name_and_img.get("href"))[0]
        results.append((name, id_, img_src))
    return results
