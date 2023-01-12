import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, Text
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
        try:
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
        except:
            print("Wykryto błąd.")

    def rottenTomatoes(self):
        try:
            self.title = validateTitle(self.title)
            URL = "https://www.rottentomatoes.com/search?search=" + self.title
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="search-results")
            if results is not None:
                movies = results.find_all("search-page-media-row")
                urlToMovie = movies[0].find("a", href=True)  # WYSZUKANIE SCIEZKI DO FILMU

                URL = urlToMovie['href']
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                results = soup.find(id="topSection")
                onlyRating = results.find("score-board").attrs
                self.rating = str(int(onlyRating['audiencescore']) / 10)

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
        except:
            print("Wykryto błąd.")

    def filmweb(self):
        try:
            self.title = validateTitle(self.title)
            URL = "https://www.filmweb.pl/search?q=" + self.title
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("ul", class_="resultsList hits")
            urlToMovie = results.find("a", class_="preview__link").attrs
            URL = "https://www.filmweb.pl" + urlToMovie['href']  # STATYCZNA STRONA FILMU

            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("div", class_="filmRating filmRating--hasPanel").attrs
            self.rating = str(round(float(results['data-rate']), 1))
            self.votes = str(results['data-count'])
            self.movieInfo = URL
            self.showResults()
        except:
            print("Wykryto błąd.")


# KLIENT

#title = input("Wprowadź tytuł filmu: (po angielsku): ")

#scrap = Scraper(title)

#scrap.imdb()
#scrap.rottenTomatoes()
#scrap.filmweb()

root = tk.Tk()

canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

startScraping = tk.Button(root, text="Pobierz oceny!", padx=10,
                          pady=5, fg="white", bg="#263D42")
startScraping.pack()

saveInFile = tk.Button(root, text="Zapisz do pliku", padx=10,
                          pady=5, fg="white", bg="#263D42")
saveInFile.pack()

root.mainloop()