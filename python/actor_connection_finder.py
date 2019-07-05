from bs4 import BeautifulSoup
import requests

BASE_WEB_ADDRESS = "https://www.imdb.com/"

def findConnectionBetweenActors(actor1, actor2):
    return ""

def searchForActor(actor):
    print(getHTMLForActorSearch(getSearchURL(actor)))
    return getHTMLForActorSearch(getSearchURL(actor))

# advanced search URL for an actor.
# https://www.imdb.com/search/name/?name=Will+Smith
def getSearchURL(actor):
    print(BASE_WEB_ADDRESS + "search/name/?name=" + actor.replace(" ", "+"))
    return BASE_WEB_ADDRESS + "search/name/?name=" + actor.replace(" ", "+")

#TODO clean this up.
def getHTMLForActorSearch(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    print(soup.prettify)
    return soup

def main():
    url = getSearchURL("Will Smith")
    html = getHTMLForActorSearch(url)

main()
