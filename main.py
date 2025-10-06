import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Crypto",
    page_icon="📊",
    layout="wide"
)

# CSS pour le fond sombre
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
    }
    .main-header {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Données d'exemple - remplacer par votre vraie source
    data = {
        'Catégorie': ['Bitcoin', 'Ethereum', 'DeFi', 'NFT', 'Gaming'],
        'Thème': ['Store of Value', 'Smart Contracts', 'Finance', 'Digital Art', 'Gaming'],
        'Volume 24h': [25489632.500000, 15432987.250000, 4896321.000000, 2158963.750000, 1896321.000000],
        'Évolution': [2.50, -1.20, 0.00, 5.80, -3.40],
        'Market Cap': [489632147852, 189632147852, 48963214785, 18963214785, 8963214785]
    }
    return pd.DataFrame(data)

def clean_numeric_columns(df):
    """Nettoie les colonnes numériques"""
    numeric_cols = ['Volume 24h', 'Évolution', 'Market Cap']
    
    for col in numeric_cols:
        if col in df.columns:
            # Supprime les zéros inutiles après la virgule
            df[col] = df[col].apply(lambda x: 
                int(x) if x == int(x) else round(x, 2)
            )
    return df

def main():
    st.markdown('<h1 class="main-header">📊 Dashboard Crypto - Analyse par Catégorie</h1>', 
                unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    df_clean = clean_numeric_columns(df)
    
    # Sidebar
    st.sidebar.header("Filtres")
    
    # Filtre par thème
    themes = df_clean['Thème'].unique()
    selected_themes = st.sidebar.multiselect(
        "Sélectionnez les thèmes:",
        options=themes,
        default=themes
    )
    
    # Application des filtres
    filtered_df = df_clean[df_clean['Thème'].isin(selected_themes)]
    
    # KPIs
    col1, col2 = st.columns(2)
    
    with col1:
        total_volume = filtered_df['Volume 24h'].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Volume 24h Total</h3>
            <h2>${total_volume:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        nb_categories = len(filtered_df)
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Catégories Affichées</h3>
            <h2>{nb_categories}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Dictionnaire de couleurs pour les thèmes
    color_map = {
        'Store of Value': '#FF6B6B',
        'Smart Contracts': '#4ECDC4',
        'Finance': '#45B7D1',
        'Digital Art': '#96CEB4',
        'Gaming': '#FFEAA7'
    }
    
    # Tableau interactif
    st.subheader("📋 Tableau des Données")
    
    # Fonction de style pour le tableau
    def style_dataframe(df):
        styled = df.style
        
        # Coloration par thème
        for theme, color in color_map.items():
            mask = df['Thème'] == theme
            styled = styled.map(
                lambda x: f'background-color: {color}; color: black' if x in [theme] else '',
                subset=pd.IndexSlice[mask, ['Thème']]
            )
        
        # Coloration de la colonne Évolution
        def color_evolution(val):
            if val > 0:
                return 'color: #00FF00; font-weight: bold'
            elif val < 0:
                return 'color: #FF0000; font-weight: bold'
            else:
                return 'color: #808080; font-weight: bold'
        
        styled = styled.map(color_evolution, subset=['Évolution'])
        
        # Style général pour fond blanc
        styled = styled.set_properties(**{
            'background-color': 'white',
            'color': 'black',
            'border-color': 'black'
        })
        
        return styled
    
    # Affichage du tableau stylisé
    st.dataframe(
        style_dataframe(filtered_df),
        use_container_width=True,
        height=400
    )
    
    # Graphique
    st.subheader("📈 Volume 24h par Catégorie")
    
    if not filtered_df.empty:
        fig = px.bar(
            filtered_df,
            x='Catégorie',
            y='Volume 24h',
            color='Thème',
            color_discrete_map=color_map,
            text='Volume 24h'
        )
        
        # Personnalisation du graphique
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )
        
        fig.update_layout(
            plot_bgcolor='#1E1E1E',
            paper_bgcolor='#1E1E1E',
            font_color='white',
            xaxis_title="Catégories",
            yaxis_title="Volume 24h (USD)",
            showlegend=True,
            height=500
        )
        
        fig.update_xaxes(
            gridcolor='#404040',
            zerolinecolor='#404040'
        )
        
        fig.update_yaxes(
            gridcolor='#404040',
            zerolinecolor='#404040'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Aucune donnée à afficher avec les filtres sélectionnés.")

if __name__ == "__main__":
    main()
