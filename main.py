import requests
from bs4 import BeautifulSoup
#https://www.imdb.com/search/title/?title=avatar:+the+way+of+water


title = input("Wprowadź tytuł filmu: (po angielsku): ")
title = title.lower()
title = title.replace(" ", "+")

print(title)

URL = "https://www.imdb.com/search/title/?title=" + title
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="main")
movies = results.find_all("div", class_="lister-item mode-advanced")
rating = movies[0].find("div",class_="inline-block ratings-imdb-rating")
print(rating.text)