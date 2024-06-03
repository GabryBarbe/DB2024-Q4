import streamlit as st
from sqlalchemy import create_engine,text

def connect_db(dialect, username, password, host, dbname):
    try:
        engine = create_engine(f'{dialect}://{username}:{password}@{host}/{dbname}') 
        conn = engine.connect() #connessione
        return conn
    except:
        return False


def execute_query(conn, query):
    return conn.execute(text(query))

def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    if st.sidebar.button("Connetti il DB"):
        connection = connect_db("mysql+pymysql", "root", "root", "localhost", "palestra")

        if connection is not False:
            st.session_state["connection"] = connection
        else:
            st.sidebar.error("Errore di connessione", icon="🔴")

    if st.session_state["connection"]:
        st.sidebar.success("Connesso al DB", icon="🟢")
        return True

    
