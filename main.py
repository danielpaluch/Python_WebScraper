import requests
from bs4 import BeautifulSoup


# https://www.imdb.com/search/title/?title=avatar:+the+way+of+water


def validateTitle(str):
    return str.lower().replace(" ", "+")


class Scraper:
    rating = 0
    title = ""

    def __init__(self, title):
        self.title = title

    def imdb(self):
        self.title = validateTitle(self.title)
        URL = "https://www.imdb.com/search/title/?title=" + self.title
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="main")
        movies = results.find_all("div", class_="lister-item mode-advanced")
        if len(movies) > 0:
            rating = movies[0].find("div", class_="inline-block ratings-imdb-rating").attrs
            onlyRating = rating['data-value']
            votes = movies[0].find("p", class_="sort-num_votes-visible")
            onlyVotes = votes.find("span", {"name": "nv"})
            foundMovie = movies[0].find("a", href=True)
            print(onlyRating)
            print(onlyVotes.text)
            print("https://www.imdb.com" + foundMovie['href'])
        else:
            print("Nie znaleziono filmu.")


title = input("Wprowadź tytuł filmu: (po angielsku): ")

scrap = Scraper(title)

scrap.imdb()
