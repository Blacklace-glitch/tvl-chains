import streamlit as st
import pandas as pd

# Charger les données de la Google Sheet
@st.cache_data
def load_data():
    CSV_URL = "https://docs.google.com/spreadsheets/d/1RLRjn6uya9zApbGMLBWmTPn2YL8T-_-FJTLiQD2GPwU/export?format=csv&gid=1167946643"
    return pd.read_csv(CSV_URL)

df = load_data()

# Affichage dans Streamlit
st.title("📊 TVL Chains Dashboard")
st.dataframe(df)

