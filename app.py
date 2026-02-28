import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE = "https://www.persee.fr"

st.title("Scraper Persée – Sommaire d'un numéro")

issue_url = st.text_input("URL du numéro Persée")

headers = {
    "User-Agent": "Mozilla/5.0"
}

if st.button("Scraper"):

    if not issue_url.startswith("http"):
        st.error("Entre une URL valide (https://...)")
        st.stop()

    r = requests.get(issue_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    seen = set()

    # récupérer les liens d’articles
    links = soup.find_all("a", href=True)

    for link in links:

        href = link["href"]

        if "/doc/" in href:

            article_url = BASE + href

            if article_url in seen:
                continue

            seen.add(article_url)

            try:

                r = requests.get(article_url, headers=headers)
                s = BeautifulSoup(r.text, "html.parser")

                # titre
                titre = s.find("h1")
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

                st.write("✔", titre)

                time.sleep(1)

            except:
                pass

    if len(articles) == 0:
        st.warning("Aucun article détecté. Vérifie l'URL du numéro.")

    df = pd.DataFrame(articles)

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Télécharger CSV",
        csv,
        "persee_articles.csv",
        "text/csv"
    )
