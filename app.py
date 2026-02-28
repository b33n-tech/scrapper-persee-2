import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE = "https://www.persee.fr"

st.title("Scraper Persée")

issue_url = st.text_input("Colle l'URL du numéro Persée")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"
}

if st.button("Scraper"):

    if issue_url == "":
        st.warning("Merci d'entrer une URL Persée.")
    else:

        r = requests.get(issue_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        articles = []
        urls_seen = set()

        for link in soup.select("a[href*='/doc/']"):

            article_url = BASE + link.get("href")

            if article_url in urls_seen:
                continue

            urls_seen.add(article_url)

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

                st.write("✔", titre)

                time.sleep(1)

            except:
                pass

        df = pd.DataFrame(articles)

        st.success(f"{len(df)} articles trouvés")

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Télécharger CSV",
            csv,
            "persee_articles.csv",
            "text/csv"
        )
