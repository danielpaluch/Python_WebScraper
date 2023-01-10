import requests
from bs4 import BeautifulSoup


# https://www.imdb.com/search/title/?title=avatar:+the+way+of+water


def validateTitle(str):
    return str.lower().replace(" ", "+")


class Scraper:
    rating = ""
    votes = ""
    movieInfo = ""
    title = ""
    def __init__(self, title):
        self.title = title

    def showResults(self):
        print(self.rating + "/10 - " + self.votes)
        print(self.movieInfo)
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
            self.rating = str(onlyRating)
            self.movieInfo = "https://www.imdb.com" + foundMovie['href']
            self.votes = onlyVotes.text
            self.showResults()
        else:
            print("Nie znaleziono filmu.")
    def rottenTomatoes(self):
        self.title = validateTitle(self.title)
        URL = "https://www.rottentomatoes.com/search?search=" + self.title
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="search-results")
        if results is not None:
            movies = results.find_all("search-page-media-row")
            urlToMovie = movies[0].find("a", href=True) #WYSZUKANIE SCIEZKI DO FILMU

            URL = urlToMovie['href']
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="topSection")
            onlyRating = results.find("score-board").attrs
            self.rating = str(int(onlyRating['audiencescore'])/10)

            onlyVotes = results.find("a", class_="scoreboard__link scoreboard__link--audience").contents[0]

            votes = ""
            for char in onlyVotes:
                if (48 <= ord(char) <= 57) or char == ",":
                    votes = votes + char
                else:
                    break
            self.votes = votes
            self.movieInfo = urlToMovie['href']
            self.showResults()
        else:
            print("Nie znaleziono filmu.")

#KLIENT

title = input("Wprowadź tytuł filmu: (po angielsku): ")

scrap = Scraper(title)


scrap.imdb()
scrap.rottenTomatoes()

