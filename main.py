import streamlit as st, pandas as pd, plotly.express as px

st.set_page_config(page_title="TVL Chains", layout="wide")
st.title("💰 Chaînes : TVL & Volume 24h")

CSV_URL = "https://docs.google.com/spreadsheets/d/1RLRjn6uya9zApbGMLBWmTPn2YL8T-_-FJTLiQD2GPwU/export?format=csv&gid=1167946643"

@st.cache_data
def load_data():
    return pd.read_csv(CSV_URL)

df = load_data()

chaines = st.sidebar.multiselect("Choisis une ou plusieurs chaînes", df["Chaîne"].unique(), default=df["Chaîne"].unique())
df_filtre = df[df["Chaîne"].isin(chaines)]

st.dataframe(df_filtre, use_container_width=True)

fig_tvl = px.bar(df_filtre, x="Chaîne", y="TVL", title="TVL par chaîne")
st.plotly_chart(fig_tvl, use_container_width=True)

fig_vol = px.bar(df_filtre, x="Chaîne", y="Volume 24h", title="Volume 24h par chaîne")
st.plotly_chart(fig_vol, use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("TVL Total", f"{df_filtre['TVL'].sum():,.0f}")
with col2:
    st.metric("Volume Total", f"{df_filtre['Volume 24h'].sum():,.0f}")
with col3:
    st.metric("Nb chaînes", len(df_filtre))
