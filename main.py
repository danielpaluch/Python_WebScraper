import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, Text


def validateTitle(str):
    return str.lower().replace(" ", "+")


class Scraper:
    rating = ""
    votes = ""
    movieInfo = ""
    title = ""
    messages = []

    def __init__(self, title):
        self.title = title

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
                self.saveResults(self.rating, self.votes, self.movieInfo)
            else:
                message = "Nie znaleziono filmu."
                self.errorMessage(message)
                print(message)
        except:
            message = "Wykryto błąd."
            self.errorMessage(message)
            print(message)

    def rottenTomatoes(self):
        try:
            self.title = validateTitle(self.title)
            URL = "https://www.rottentomatoes.com/search?search=" + self.title
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="search-results")
            if results is not None:
                movies = results.find_all("search-page-media-row")
                numberOfMovie = 0
                for i in range(0, 5) or len(movies):
                    movieTitle = movies[i].find("img").attrs
                    movie = validateTitle(movieTitle['alt'])
                    print(movie, self.title)
                    if movie == self.title:
                        numberOfMovie = i
                        break # petla sluzy do znajdowania poprawnego filmu, rotten toamtoes sortuje od najpopularniejszego
                urlToMovie = movies[numberOfMovie].find("a", href=True)  # WYSZUKANIE SCIEZKI DO FILMU

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
                self.saveResults(self.rating, self.votes, self.movieInfo)
            else:
                message = "Nie znaleziono filmu."
                self.errorMessage(message)
                print(message)
        except:
            message = "Wykryto błąd."
            self.errorMessage(message)
            print(message)

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
            self.saveResults(self.rating, self.votes, self.movieInfo)
        except:
            message = "Wykryto błąd."
            self.errorMessage(message)
            print(message)

    def scrapCommand(self):
        self.imdb()
        self.rottenTomatoes()
        self.filmweb()

    def saveResults(self, rating, votes, movieInfo):
        self.messages.append(["Ocena: " + rating + "/10", "Ilość ocen: " + votes.replace(",", ""), movieInfo])
        print("Ocena: " + rating + "/10", "Ilość ocen: " + votes, movieInfo)

    def errorMessage(self, message):
        self.messages.append([message])


# KLIENT
def scrapButton():
    print(entryTitle.get(), "halo")
    scrap = Scraper(entryTitle.get())
    scrap.scrapCommand()
    titleFrame.destroy()
    imdbFrame.destroy()
    rottenTomatoesFrame.destroy()
    filmwebFrame.destroy()

    newImdbFrame = tk.Frame(sitesFrame)
    tk.Label(newImdbFrame, text="IMDB", font=("Helvetica", 20, "bold")).pack(padx=50, pady=20)
    for message in scrap.messages[0]:
        tk.Label(newImdbFrame, text=message, font=("Helvetica", 13,)).pack(padx=50, pady=20)
    newImdbFrame.pack(side="left", fill='both', expand=True)

    newRottenTomatoesFrame = tk.Frame(sitesFrame)
    tk.Label(newRottenTomatoesFrame, text="Rotten Tomatoes", font=("Helvetica", 20, "bold")).pack(padx=50, pady=20)
    if scrap.messages:
        for message in scrap.messages[1]:
            tk.Label(newRottenTomatoesFrame, text=message, font=("Helvetica", 13)).pack(padx=50, pady=20)
    newRottenTomatoesFrame.pack(side="left", fill='both', expand=True)

    newFilmwebFrame = tk.Frame(sitesFrame)
    tk.Label(newFilmwebFrame, text="Filmweb", font=("Helvetica", 20, "bold")).pack(padx=50, pady=20)
    if scrap.messages:
        for message in scrap.messages[2]:
            tk.Label(newFilmwebFrame, text=message, font=("Helvetica", 13)).pack(padx=50, pady=20)
    newFilmwebFrame.pack(side="left", fill='both', expand=True)


root = tk.Tk()

titleFrame = tk.Frame(root, bg="white")
tk.Label(titleFrame, text="Wprowadź tytuł filmu: ", font=("Helvetica", 18)).pack(side='left')
entryTitle = tk.Entry(titleFrame, width=30, font=("Helvetica", 15))
entryTitle.pack(side="right")
titleFrame.pack()

sitesFrame = tk.Frame(root, height=700)

imdbFrame = tk.Frame(sitesFrame)

tk.Label(imdbFrame, text="IMDB", font=("Helvetica", 20, "bold")).pack(padx=50, pady=20)
tk.Label(imdbFrame, text="Ocena: N/A", font=("Helvetica", 13,)).pack(pady=20)
tk.Label(imdbFrame, text="Ilość ocen: N/A", font=("Helvetica", 13,)).pack(pady=20)
tk.Label(imdbFrame, text="Link do filmu: N/A", font=("Helvetica", 13,)).pack(pady=20)

imdbFrame.pack(side="left", fill='both', expand=True)

rottenTomatoesFrame = tk.Frame(sitesFrame)
tk.Label(rottenTomatoesFrame, text="Rotten Tomatoes", font=("Helvetica", 20, "bold")).pack(padx=50, pady=20)
tk.Label(rottenTomatoesFrame, text="Ocena: N/A", font=("Helvetica", 13,)).pack(pady=20)
tk.Label(rottenTomatoesFrame, text="Ilość ocen: N/A", font=("Helvetica", 13,)).pack(pady=20)
tk.Label(rottenTomatoesFrame, text="Link do filmu: N/A", font=("Helvetica", 13,)).pack(pady=20)
rottenTomatoesFrame.pack(side="left", fill='both', expand=True)

filmwebFrame = tk.Frame(sitesFrame)
tk.Label(filmwebFrame, text="Filmweb", font=("Helvetica", 20, "bold")).pack(padx=50, pady=20)
tk.Label(filmwebFrame, text="Ocena: N/A", font=("Helvetica", 13,)).pack(pady=20)
tk.Label(filmwebFrame, text="Ilość ocen: N/A", font=("Helvetica", 13,)).pack(pady=20)
tk.Label(filmwebFrame, text="Link do filmu: N/A", font=("Helvetica", 13,)).pack(pady=20)
filmwebFrame.pack(side="left", fill='both', expand=True)

sitesFrame.pack(fill='both', expand=True)

startScraping = tk.Button(root, text="Pobierz oceny!", padx=10,
                          pady=5, fg="white", bg="#263D42", command=scrapButton)
startScraping.pack()

saveInFile = tk.Button(root, text="Zapisz do pliku", padx=10,
                       pady=5, fg="white", bg="#263D42")
saveInFile.pack()

root.mainloop()
