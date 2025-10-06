import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Crypto Categories Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS pour fond sombre
st.markdown("""
    <style>
    .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stMetric {
        background-color: #2D2D2D;
        padding: 15px;
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# Mapping des couleurs par thème
color_map = {
    "Portefeuille de Trump": "#FFCCCB",
    "Infrastructure": "#ADD8E6",
    "Gouvernance": "#90EE90",
    "Tokens Adossés": "#FFD700",
    "Launchpad": "#FFA07A",
    "Tokens": "#DDA0DD",
    "Jeux et Métavers": "#87CEEB",
    "Thèmes Culturels": "#FFB6C1",
    "Finance Décentralisée": "#98FB98",
    "L1": "#F0E68C",
    "Stablecoins": "#E6E6FA",
    "POW": "#C0C0C0",
    "MadeinUSA": "#FF6347",
    "MadeinChina": "#FF4500",
    "POS": "#A9A9A9",
    "Meme": "#FF69B4",
    "Régulation": "#B0C4DE",
    "Interopérabilité": "#7B68EE",
    "Intelligence Artificielle": "#20B2AA",
    "NFT et Collectibles": "#BA55D3",
    "Écosystème Binance": "#FFDAB9",
    "DEX": "#F08080",
    "RWA": "#8FBC8F",
    "L2": "#D2B48C",
    "CEX": "#CD5C5C",
    "Social": "#FFA500",
    "Agregatransac": "#6A5ACD",
    "OptimismeetCO": "#48D1CC",
    "Analytique": "#5F9EA0",
    "Confidentialité": "#4682B4",
    "Identité": "#87CEFA",
    "Dérivés": "#BDB76B",
    "Utilitaires": "#EEE8AA",
    "Blockchain": "#6495ED",
    "Modular": "#8A2BE2",
    "IoT": "#00CED1",
    "Sidechain": "#00BFFF",
    "Sécurité": "#FF8C00",
    "Marketing": "#FF1493",
    "Immobilier": "#FFE4B5",
    "Énergie": "#32CD32",
    "Murad": "#FF6347",
}

@st.cache_data(ttl=600)
def load_data():
    CSV_URL = "https://docs.google.com/spreadsheets/d/1RLRjn6uya9zApbGMLBWmTPn2YL8T-_-FJTLiQD2GPwU/export?format=csv&gid=1167946643"
    df = pd.read_csv(CSV_URL)
    
    # Nettoyage des colonnes numériques
    for col in ['Volume 24h', 'Nombre de monnaies', 'Ratio V/Nbr', 'Classement']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# Chargement des données
df = load_data()

# Titre
st.title("📊 Dashboard Catégories Crypto")

# Sidebar - Filtres
st.sidebar.header("Filtres")

# Filtre par thème
themes_disponibles = sorted(df['Thème'].dropna().unique().tolist())
themes_selectionnes = st.sidebar.multiselect(
    "Sélectionner des thèmes",
    options=themes_disponibles,
    default=themes_disponibles[:5] if len(themes_disponibles) > 5 else themes_disponibles
)

# Filtre par classement
min_classement = st.sidebar.slider(
    "Classement maximum à afficher",
    min_value=1,
    max_value=int(df['Classement'].max()) if 'Classement' in df.columns else 100,
    value=50
)

# Application des filtres
if themes_selectionnes:
    df_filtered = df[df['Thème'].isin(themes_selectionnes)]
else:
    df_filtered = df.copy()

df_filtered = df_filtered[df_filtered['Classement'] <= min_classement]

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    total_volume = df_filtered['Volume 24h'].sum()
    st.metric("Volume 24h Total", f"${total_volume:,.0f}")
with col2:
    nb_categories = len(df_filtered)
    st.metric("Catégories affichées", nb_categories)
with col3:
    nb_themes = df_filtered['Thème'].nunique()
    st.metric("Thèmes uniques", nb_themes)

# Tableau interactif
st.subheader("📋 Tableau des catégories")

# Préparer le dataframe pour l'affichage
df_display = df_filtered.copy()

# Fonction pour colorer les cellules Évolution
def color_evolution(val):
    if pd.isna(val):
        return 'background-color: #e0e0e0'
    if val > 0:
        return 'background-color: #b6ffb6'
    elif val < 0:
        return 'background-color: #ffb6b6'
    else:
        return 'background-color: #e0e0e0'

# Fonction pour colorer par thème
def color_theme(row):
    theme = row['Thème']
    color = color_map.get(theme, '#FFFFFF')
    return [f'background-color: {color}' if col == 'Thème' else '' for col in row.index]

# Afficher le tableau avec style
styled_df = df_display.style.apply(color_theme, axis=1)
if 'Évolution' in df_display.columns:
    styled_df = styled_df.applymap(color_evolution, subset=['Évolution'])

st.dataframe(
    styled_df,
    use_container_width=True,
    height=500
)

# Graphiques
st.subheader("📈 Visualisations")

tab1, tab2, tab3 = st.tabs(["Volume par Catégorie", "Distribution par Thème", "Évolution"])

with tab1:
    # Top 20 par volume
    top_20 = df_filtered.nlargest(20, 'Volume 24h')
    fig1 = px.bar(
        top_20,
        x='Catégorie',
        y='Volume 24h',
        color='Thème',
        color_discrete_map=color_map,
        title="Top 20 Catégories par Volume 24h"
    )
    fig1.update_layout(
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
        font_color='#FFFFFF',
        xaxis_title="Catégorie",
        yaxis_title="Volume 24h ($)",
        showlegend=True
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    # Distribution par thème
    theme_counts = df_filtered['Thème'].value_counts()
    fig2 = px.pie(
        values=theme_counts.values,
        names=theme_counts.index,
        title="Distribution des Catégories par Thème",
        color=theme_counts.index,
        color_discrete_map=color_map
    )
    fig2.update_layout(
        plot_bgcolor='#1E1E1E',
        paper_bgcolor='#1E1E1E',
        font_color='#FFFFFF'
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    # Évolution (positif vs négatif)
    if 'Évolution' in df_filtered.columns:
        df_evo = df_filtered.dropna(subset=['Évolution'])
        df_evo = df_evo[df_evo['Évolution'] != 'Nouveau']
        
        positif = len(df_evo[df_evo['Évolution'] > 0])
        negatif = len(df_evo[df_evo['Évolution'] < 0])
        stable = len(df_evo[df_evo['Évolution'] == 0])
        
        fig3 = px.bar(
            x=['Progression', 'Régression', 'Stable'],
            y=[positif, negatif, stable],
            title="Répartition des Évolutions",
            color=['Progression', 'Régression', 'Stable'],
            color_discrete_map={'Progression': '#b6ffb6', 'Régression': '#ffb6b6', 'Stable': '#e0e0e0'}
        )
        fig3.update_layout(
            plot_bgcolor='#1E1E1E',
            paper_bgcolor='#1E1E1E',
            font_color='#FFFFFF',
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("🔄 Données actualisées automatiquement depuis Google Sheets | Mise à jour toutes les 10 minutes")
