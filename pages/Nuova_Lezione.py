import streamlit as st
from utils.utils import *
import pymysql,cryptography
import pandas as pd
import datetime

def extract_cf_instructors():
    query = "SELECT CodFisc FROM Istruttore;"
    res = execute_query(st.session_state["connection"], query)
    cf_istruttori = [cf[0] for cf in res]
    return cf_istruttori

def extract_courses():    
    query = "SELECT CodC FROM Corsi;"
    res = execute_query(st.session_state["connection"], query)
    info_corsi = [codc[0] for codc in res]
    return info_corsi

def check_campi_nulli(campi):
    for (key, value) in campi.items():
        if (value == ''):
            st.error("Inserire tutti i campi obbligatori")
            return True
    return False

def check_duplicate(campi):
    query = f"SELECT * FROM Programma WHERE CodC = '{campi['CodC']}' AND Giorno = '{campi['Giorno']}';"
    res = [i[0] for i in execute_query(st.session_state["connection"], query)]
    if len(res) > 0:
        st.error("Lezione già presente in programma")
        return True
    return False

def insert_tupla(campi):
    if not check_campi_nulli(campi) and not check_duplicate(campi):
        attributi = ", ".join(campi.keys())
        valori = ", ".join([f"'{val}'" for val in campi.values()])
        query = f"INSERT INTO programma ({attributi}) VALUES ({valori});"
        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
            st.success("Istruttore inserito correttamente")
        except Exception as e:
            st.error("Errore: " + str(e))
            return False
        return True
    else:
        return False


def create_form():
    array_cf_istruttori = extract_cf_instructors()
    array_codc = extract_courses()

    df_istruttori = pd.DataFrame(array_cf_istruttori)
    df_corsi = pd.DataFrame(array_codc)

    with st.form("Inserisci lezione"):
        col1, col2, col3 = st.columns(3)
        with col1:
            istruttore = st.selectbox("Istruttore: ", df_istruttori)
            codc = st.selectbox("Corso: ", df_corsi)
        with col2:
            giorno = st.selectbox("Giorno: ", ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"])
            sala = st.text_input("Sala: ", placeholder="Inserisci la sala")
        with col3:
            ora_inizio = st.slider("Ora inizio:", min_value=datetime.time(0, 0), max_value=datetime.time(23, 0), format="HH:mm:ss", step=datetime.timedelta(seconds=1800))
            durata = st.slider("Durata: ", min_value=0, max_value=60, step=1)

        campi = {
            "CodFisc": istruttore,
            "CodC": codc,
            "Giorno": giorno,
            "Sala": sala,
            "OraInizio": ora_inizio,
            "Durata": durata
        }

        submitted = st.form_submit_button("Inserisci", type="primary")

    if submitted:
        insert_tupla(campi)


if __name__=="__main__":
    if check_connection():
        st.header(":red[Inserimento di una nuova lezione in programma]")
        create_form()