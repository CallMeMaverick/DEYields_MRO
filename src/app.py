import os
import streamlit as st
import pandas as pd


st.set_page_config(page_title="German Bonds & ECB Policy", layout="wide")

st.title("Analyzing 10-Year German Bond Yields & ECB Policy")
st.write(
    "This app explores the relationship between the ECB’s Main Refinancing Operations Rate (MRO) "
    "and German 10-Year Government Bond Yields."
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "bond_yields_2000_2024.csv")

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH, dtype={"Date": str})

    if "show_full_data" not in st.session_state:
        st.session_state.show_full_data = False

    if st.button("🔁 Toggle dataset"):
        st.session_state.show_full_data = not st.session_state.show_full_data

    if st.session_state.show_full_data:
        st.write("### Full dataset")
        st.dataframe(df)
    else:
        st.write("### Dataset preview")
        st.dataframe(df.head())

else:
    st.warning("No dataset found")

