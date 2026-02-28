import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE = "https://www.persee.fr"

issue_url = "COLLE_ICI_URL_NUMERO"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"
}

# récupérer la page du numéro
r = requests.get(issue_url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

articles = []

# récupérer tous les liens d'articles
for link in soup.select("a[href*='/doc/']"):

    article_url = BASE + link.get("href")

    # éviter les doublons
    if article_url in [a["url"] for a in articles]:
        continue

    print("Scraping:", article_url)

    try:
        r = requests.get(article_url, headers=headers)
        s = BeautifulSoup(r.text, "html.parser")

        # titre
        titre = s.select_one("h1")
        titre = titre.text.strip() if titre else ""

        # auteurs
        auteurs = [a.text.strip() for a in s.select(".authors a")]
        auteurs = "; ".join(auteurs)

        # pages
        pages = ""
        for li in s.select("li"):
            if "p." in li.text.lower():
                pages = li.text.strip()

        articles.append({
            "titre": titre,
            "auteurs": auteurs,
            "pages": pages,
            "url": article_url
        })

        time.sleep(1)

    except:
        pass

df = pd.DataFrame(articles)

df.to_excel("persee_articles.xlsx", index=False)

print("Terminé : persee_articles.xlsx")
