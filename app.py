import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("Scraper Persée (sommaire de numéro)")

url = st.text_input("URL du numéro Persée")

headers = {"User-Agent": "Mozilla/5.0"}

if st.button("Scraper"):

    if not url.startswith("http"):
        st.error("Entre une URL valide.")
        st.stop()

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    titres = []
    auteurs = []
    pages = []

    # titres
    for t in soup.select(".title"):
        titres.append(t.text.strip())

    # auteurs
    for a in soup.select(".authors"):
        auteurs.append(a.text.strip())

    # pages
    for p in soup.select(".pages"):
        pages.append(p.text.strip())

    n = min(len(titres), len(auteurs), len(pages))

    data = []

    for i in range(n):
        data.append({
            "titre": titres[i],
            "auteurs": auteurs[i],
            "pages": pages[i]
        })

    df = pd.DataFrame(data)

    if len(df) == 0:
        st.warning("Aucun résultat détecté.")
    else:
        st.success(f"{len(df)} articles trouvés")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Télécharger CSV",
            csv,
            "persee_sommaire.csv",
            "text/csv"
        )
