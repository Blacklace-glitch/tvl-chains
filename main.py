import streamlit as st, pandas as pd

st.set_page_config(page_title="Données CSV", layout="wide")
st.title("📊 Aperçu de ton CSV")

CSV_URL = "https://docs.google.com/spreadsheets/d/1RLRjn6uya9zApbGMLBWmTPn2YL8T-_-FJTLiQD2GPwU/export?format=csv&gid=1167946643"

@st.cache_data
def load_data():
    return pd.read_csv(CSV_URL)

df = load_data()

st.subheader("Colonnes trouvées")
st.write(df.columns.tolist())

st.subheader("Contenu brut")
st.dataframe(df, use_container_width=True)
