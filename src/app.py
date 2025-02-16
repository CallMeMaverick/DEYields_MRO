import os
import streamlit as st
import pandas as pd
from translations import translations


st.set_page_config(page_title="German Bonds & ECB Policy", layout="wide")

language = st.sidebar.selectbox("🌐 Select Language / Виберіть мову", ["en", "uk"])
t = translations[language]

st.title(t["title"])
st.write(t["description"])

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "bond_yields_2000_2024.csv")

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH, dtype={"Date": str})

    if "show_full_data" not in st.session_state:
        st.session_state.show_full_data = False

    if st.button(t["toggle_dataset"]):
        st.session_state.show_full_data = not st.session_state.show_full_data

    if st.session_state.show_full_data:
        st.write(t["full_dataset"])
        st.dataframe(df)
    else:
        st.write(t["dataset_preview"])
        st.dataframe(df.head())

else:
    st.warning("No dataset found")

