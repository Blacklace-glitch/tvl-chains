import streamlit as st
import pandas as pd
import plotly.express as px

# --- Couleurs par thème ---
color_map = {
    "Portefeuille de Trump": "#FFCCCB",
    "MadeinUSA": "#FF6347",
    "L1": "#F0E68C",
    "Thèmes Culturels": "#FFB6C1",
    "Stablecoins": "#E6E6FA",
    "Finance Décentralisée": "#98FB98",
    "Infrastructure": "#ADD8E6",
    "Tokens Adossés": "#FFD700",
    "Meme": "#FF69B4",
    "CEX": "#CD5C5C",
    "POW": "#C0C0C0",
    "Écosystème Binance": "#FFDAB9",
    "Interopérabilité": "#7B68EE",
    "Jeux et Métavers": "#87CEEB",
    "Tokens": "#DDA0DD",
    "Gouvernance": "#90EE90",
    "Intelligence Artificielle": "#20B2AA",
    "IoT": "#00CED1",
    "POS": "#A9A9A9",
    "RWA": "#8FBC8F",
    "L2": "#D2B48C",
    "Santé": "#00FF00",
    "OptimismeetCO": "#48D1CC",
    "Portefeuille YZi": "#FFE4E1",
    "DEX": "#F08080",
    "MadeinChina": "#FF4500",
    "Dérivés": "#BDB76B",
    "Confidentialité": "#4682B4",
    "Divertissement": "#FF00FF",
    "Identité": "#87CEFA",
    "Marketing": "#FF1493",
    "Utilitaires": "#EEE8AA",
    "Sidechain": "#00BFFF",
    "Agregatransac": "#6A5ACD",
    "NFT et Collectibles": "#BA55D3",
    "Régulation": "#B0C4DE",
    "Paiements": "#FF8C00",
    "Analytique": "#5F9EA0",
    "Commerce": "#FF7F50",
    "Blockchain": "#6495ED",
    "Launchpad": "#FFA07A",
    "Écosystème Virtuals": "#DDA0DD",
    "Énergie": "#32CD32",
    "Murad": "#FF6347",
    "Éducation": "#1E90FF",
    "Social": "#FFA500",
    "Science Décentralisée": "#7FFF00",
    "Finance Traditionnelle": "#8B4513",
    "Politique": "#800080",
    "Modular": "#8A2BE2",
    "Sécurité": "#FF8C00",
    "Immobilier": "#FFE4B5",
    "Recrutement": "#808000",
    "Juridique": "#000080",
    "Propriété Intellectuelle": "#B0E0E6",
    "Assurance": "#FFD700",
    "Charité": "#FF69B4",
    "Thèmes Sociaux": "#FFA07A"
}

# --- Config Streamlit ---
st.set_page_config(page_title="TVL Chains Dashboard", layout="wide")

# --- Fond sombre mais tableaux lisibles ---
st.markdown(
    """
    <style>
    /* Fond général sombre */
    .main {background-color: #1E1E1E; color: #FFFFFF;}
    .stMarkdown p {color: #FFFFFF;}
    /* Laisser les tableaux lisibles */
    .stDataFrame div{background-color: inherit !important;}
    </style>
    """, unsafe_allow_html=True
)

st.title("📊 TVL Chains Dashboard")
st.markdown("Visualisation des catégories de crypto avec fond sombre et couleurs par thème.")

# --- Charger les données ---
@st.cache_data
def load_data():
    CSV_URL = "https://docs.google.com/spreadsheets/d/1RLRjn6uya9zApbGMLBWmTPn2YL8T-_-FJTLiQD2GPwU/export?format=csv&gid=1167946643"
    return pd.read_csv(CSV_URL)

df = load_data()

# --- Filtrer par thème ---
themes = df['Thème'].dropna().unique()
selected_theme = st.multiselect("Filtrer par thème :", themes, default=themes)

# CORRECTION : Si aucun thème sélectionné, afficher tout
if len(selected_theme) == 0:
    df_filtered = df
else:
    df_filtered = df[df['Thème'].isin(selected_theme)]

# --- KPIs ---
col_kpi1, col_kpi2 = st.columns(2)
with col_kpi1:
    total_volume = df_filtered['Volume 24h'].sum()
    st.metric("Volume total 24h", f"{total_volume:,}")
with col_kpi2:
    num_categories = len(df_filtered)
    st.metric("Nombre de catégories affichées", num_categories)

# --- Préparer les données pour le style ---
df_filtered_display = df_filtered.copy()

# Colonnes numériques sans décimales
for col in ['Volume 24h', 'Nombre de monnaies', 'Ratio V/Nbr']:
    if col in df_filtered_display.columns:
        df_filtered_display[col] = df_filtered_display[col].fillna(0).astype(int)

# Fonction de coloration par thème
def color_theme(val):
    return f"background-color: {color_map.get(val, '#333333')}; color: white;"

# Fonction de coloration pour la colonne évolution
def color_evolution(val):
    try:
        val = float(val)
        if val > 0:
            return 'background-color: #00FF00; color: black;'   # vert
        elif val < 0:
            return 'background-color: #FF0000; color: white;'   # rouge
        else:
            return 'background-color: #D3D3D3; color: black;'   # gris
    except:
        return ''  # si vide ou non numérique

# --- Layout : tableau + graphique ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Tableau des catégories")
    st.dataframe(
        df_filtered_display.style
        .applymap(color_theme, subset=['Thème'])
        .applymap(color_evolution, subset=['Évolution'])
    )

with col2:
    st.subheader("Graphique Volume 24h par catégorie")
    fig = px.bar(
        df_filtered, x='Catégorie', y='Volume 24h',
        color='Thème', color_discrete_map=color_map,
        hover_data=['Nombre de monnaies', 'Ratio V/Nbr'],
        height=600
    )
    fig.update_layout(
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
        font_color='white',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)
