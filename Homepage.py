import streamlit as st
from utils.utils import *
import pymysql,cryptography

if __name__ == "__main__":
    st.set_page_config(
        page_title="Quaderno 4 - Palestra",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("# :red[Quaderno 4] - :blue[Basi di Dati]")
    st.markdown("#### Gabriele Barbero - 306989 ")