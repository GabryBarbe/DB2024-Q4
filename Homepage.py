import streamlit as st
from utils.utils import *
import pymysql,cryptography
import pandas as pd

def create_barchart():
    st.markdown("### Numero di lezioni per slot di tempo")
    query = "SELECT Giorno, OraInizio, Durata, COUNT(*) AS NLezioni FROM programma GROUP BY Giorno, OraInizio, Durata;"
    result = execute_query(st.session_state["connection"], query)
    df = pd.DataFrame(result)
    df["GiornoOra"] = df["Giorno"] + " " + df["OraInizio"] # Creo una nuova colonna concatenando Giorno e OraInizio per ottenere gli slot di tempo
    st.bar_chart(df, x="GiornoOra", y="NLezioni", use_container_width=True)

def create_areachart():
    st.markdown("### Numero di lezioni per giorno")
    query = "SELECT Giorno, COUNT(*) AS NLezioni FROM programma GROUP BY Giorno;"
    result = execute_query(st.session_state["connection"], query)
    df = pd.DataFrame(result)
    st.area_chart(df, x="Giorno", y="NLezioni", use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Quaderno 4 - Palestra",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    col1, col2 = st.columns(2)
    col1.markdown("# :red[Quaderno 4] - :blue[Basi di Dati]")
    col2.markdown("# Gabriele Barbero - 306989 ")
    st.write("")
    st.header(":red[Statistiche sulle lezioni]")

    if check_connection():
        create_barchart()
        create_areachart()
