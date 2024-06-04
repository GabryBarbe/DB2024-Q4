import streamlit as st
from utils.utils import *
import pymysql,cryptography
import time, datetime
import pandas as pd

def filtra_istruttori():
    with st.expander("Filtri istruttori: ", expanded=True):
        col1, col2 = st.columns(2)
        cognome = col1.text_input("Cognome: ")
        range_date = col2.date_input("Data di nascita: ", (datetime.date(1900,1,1), datetime.date(2000,1,1)))
        
    query_cognome = ''
    if cognome!='':
        query_cognome = f" AND Cognome='{cognome}'"
    query = f"SELECT * FROM istruttore WHERE DataNascita>='{range_date[0]}' AND DataNascita<='{range_date[1]}' {query_cognome};"
    result = execute_query(st.session_state["connection"], query)

    df = pd.DataFrame(result)

    if df.empty:
        st.warning("Nessun risultato")
    else:
        for index, row in df.iterrows():
            col1, col2 = st.columns(2)
            col1.subheader(f"👤:red[Risultato {index+1}]")
            col2.text(f"Codice Fiscale: {row['CodFisc']}")
            col2.text(f"Nome: {row['Nome']}")
            col2.text(f"Cognome: {row['Cognome']}")
            col2.text(f"Data di Nascita: {row['DataNascita']}")
            col2.text(f"Email: {row['Email']}")
            col2.text(f"Telefono {row['Telefono']}")
            st.text("")
            


if __name__=="__main__":
    if check_connection():
        filtra_istruttori()