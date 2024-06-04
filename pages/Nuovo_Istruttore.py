import streamlit as st
from utils.utils import *
import pymysql,cryptography
import datetime

def check_campi_nulli(campi):
    for (key, value) in campi.items():
        if (value == ''):
            return True
    return False

def insert_tupla(campi):
    if not check_campi_nulli(campi) :
        attributi = ", ".join(campi.keys())
        valori = ", ".join([f"'{val}'" if val != 'NULL' else val for val in campi.values()])
        query = f"INSERT INTO Istruttore ({attributi}) VALUES ({valori});"
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
    with st.form("Nuovo Istruttore"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cf = st.text_input("Codice Fiscale: ", placeholder="Inserisci il codice fiscale")
            data_nascita = st.date_input("Data di nascita: ", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        with col2:
            nome = st.text_input("Nome: ", placeholder="Inserisci il nome")
            email = st.text_input("Email: ", placeholder="Inserisci l'email")
        with col3:
            cognome = st.text_input("Cognome: ", placeholder="Inserisci il cognome")
            telefono = st.text_input("Telefono: ", placeholder="Inserisci il telefono con prefisso")

        if telefono== '':
            telefono = 'NULL'
        campi = {
            "CodFisc": cf, 
            "Nome": nome, 
            "Cognome": cognome, 
            "DataNascita": str(data_nascita), 
            "Email": email, 
            "Telefono": telefono
        }

        submitted = st.form_submit_button("Inserisci", type="primary")

    if submitted:
        if insert_tupla(campi) is False:
            st.error("Inserire tutti i campi obbligatori")

    

if __name__=="__main__":
    if check_connection():
        st.header(":red[Inserimento di un nuovo istruttore]")
        create_form()