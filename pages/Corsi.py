import streamlit as st
from utils.utils import *
import pymysql,cryptography
import pandas as pd

def create_query_tipo(tipo):
    query = ""
    for el in tipo:
        query += f"Tipo = '{el}' OR "
    return query

def create_query_where(cod_corsi):
    query = ""
    for el in cod_corsi:
        query += f"CodC = '{el}' OR "
    return query




def create_metrics():
    col1, col2 = st.columns(2)

    with col1:
        query = "SELECT COUNT(CodC) AS NCorsi FROM corsi;"
        result = execute_query(st.session_state["connection"], query)
        result_dict =[dict(zip(result.keys(), r)) for r in result]
        st.metric("Numero di corsi", result_dict[0]["NCorsi"])
    with col2:
        query = "SELECT COUNT(DISTINCT Tipo) AS NTipi FROM corsi;"
        result = execute_query(st.session_state["connection"], query)
        result_dict =[dict(zip(result.keys(), r)) for r in result]
        st.metric("Tipo di corsi", result_dict[0]["NTipi"])

def filtraggio_corsi():
    with st.expander("Filtri", expanded=True):
        col1, col2 = st.columns(2)

        tipologie = execute_query(st.session_state["connection"], "SELECT DISTINCT Tipo FROM corsi;")
        df_tipologie = pd.DataFrame(tipologie)
        tipo = col1.multiselect("Seleziona le tipologie di corso", df_tipologie)

        range_lv = execute_query(st.session_state["connection"], "SELECT MIN(Livello) AS MinLv, MAX(Livello) AS MaxLv FROM corsi;")
        range_lv_dict = [dict(zip(range_lv.keys(), r)) for r in range_lv]
        livelli = col2.slider("Seleziona il livello", range_lv_dict[0]["MinLv"], range_lv_dict[0]["MaxLv"], (range_lv_dict[0]["MinLv"], range_lv_dict[0]["MaxLv"]))

    query_tipo = create_query_tipo(tipo)[:len(create_query_tipo(tipo))-4] #rimuovo l'ultimo OR
    if query_tipo != "":
        query_tipo = f"AND ({query_tipo})" #aggiungo AND solo se la query_tipo non restituisce stringa vuota
    query = f"SELECT * FROM corsi WHERE Livello>={livelli[0]} AND Livello<={livelli[1]} {query_tipo};"
    result = execute_query(st.session_state["connection"], query)
    df = pd.DataFrame(result)
    st.dataframe(df, use_container_width=True)
    return df

def info_programma(df):
    cod_corsi = []
    for i in range(len(df)):
        if df["CodC"][i] not in cod_corsi:
            cod_corsi.append(df["CodC"][i])
    with st.expander("Programma", expanded=True):
        if len(cod_corsi) == 0:
            st.warning("Nessun corso trovato")
        else:
            query = f"SELECT CodC, Giorno, OraInizio, Durata, Sala, programma.CodFisc, Nome, Cognome, DataNascita, Email, Telefono FROM programma, istruttore WHERE {create_query_where(cod_corsi)[:len(create_query_where(cod_corsi))-4]} AND programma.CodFisc=istruttore.CodFisc;"
            df = pd.DataFrame(execute_query(st.session_state["connection"], query))
            st.dataframe(df, use_container_width=True)
        
    


if __name__=="__main__":
    if check_connection():
        create_metrics()
        df = filtraggio_corsi()
        info_programma(df)