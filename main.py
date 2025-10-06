import streamlit as st
import pandas as pd
import plotly.express as px

# --- Charger les données de la Google Sheet ---
@st.cache_data
def load_data():
    CSV_URL = "https://docs.google.com/spreadsheets/d/1RLRjn6uya9zApbGMLBWmTPn2YL8T-_-FJTLiQD2GPwU/export?format=csv&gid=1167946643"
    return pd.read_csv(CSV_URL)

df = load_data()

# --- Configuration de la page ---
st.set_page_config(page_title="TVL Chains Dashboard", layout="wide")
st.title("📊 TVL Chains Dashboard")
st.markdown("Visualisation des catégories de crypto avec volume 24h et évolution.")

# --- Filtrer par thème ---
if 'Thème' in df.columns:
    themes = df['Thème'].dropna().unique()
    selected_theme = st.multiselect("Filtrer par thème :", themes, default=themes)
    df_filtered = df[df['Thème'].isin(selected_theme)]
else:
    df_filtered = df

# --- Layout : tableau + graphique côte à côte ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Tableau des catégories")
    if 'Volume 24h' in df_filtered.columns:
        st.dataframe(df_filtered.style.background_gradient(subset=['Volume 24h'], cmap='Blues'))
    else:
        st.dataframe(df_filtered)

with col2:
    st.subheader("Graphique Volume 24h par catégorie")
    if 'Catégorie' in df_filtered.columns and 'Volume 24h' in df_filtered.columns:
        fig = px.bar(
            df_filtered, x='Catégorie', y='Volume 24h', color='Thème' if 'Thème' in df_filtered.columns else None,
            hover_data=[col for col in ['Nombre de monnaies','Ratio V/Nbr'] if col in df_filtered.columns],
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

# --- KPIs en haut ---
if 'Volume 24h' in df_filtered.columns:
    total_volume = df_filtered['Volume 24h'].sum()
    st.metric("Volume total 24h", f"{total_volume:,}")

if 'Catégorie' in df_filtered.columns:
    num_categories = df_filtered['Catégorie'].nunique()
    st.metric("Nombre de catégories affichées", num_categories)

