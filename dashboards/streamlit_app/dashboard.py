import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import ast
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Saúde por Bairro - Fortaleza")

# --- Função para carregar o GeoDataFrame dos bairros ---
@st.cache_data
def load_bairros_geodf(path):
    df = pd.read_csv(path, sep=';')

    # Converte texto -> lista -> shapely.geometry.Polygon
    df['coords'] = df['POLYGON'].apply(ast.literal_eval)
    df['geometry'] = df['coords'].apply(lambda x: Polygon(x))

    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    return gdf

# --- Função para carregar séries temporais ---
@st.cache_data
def load_series_temporais(path):
    df = pd.read_csv(path, sep=';', index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    return df

# --- Carregamento dos dados ---
gdf_bairros = load_bairros_geodf("../../datasets/IBGE_BAIRRO.csv")
df_casos = load_series_temporais("../../datasets/SERIES_CASOS_BAIRRO.csv")
df_obitos = load_series_temporais("../../datasets/SERIES_OBITOS_BAIRRO.csv")

# --- Seletor de bairro e data ---
bairro_selecionado = st.selectbox("Selecione um bairro:", sorted(gdf_bairros['NM_BAIRRO'].unique()))
data_selecionada = st.date_input("Selecione uma data:", df_casos.index.max())

# --- Métricas principais ---
col1, col2 = st.columns(2)
data_selecionada = pd.to_datetime(data_selecionada, errors='coerce') 
casos_dia = df_casos.loc[data_selecionada, bairro_selecionado] if bairro_selecionado in df_casos.columns else 0
obitos_dia = df_obitos.loc[data_selecionada, bairro_selecionado] if bairro_selecionado in df_obitos.columns else 0
col1.metric("Casos no dia", int(casos_dia))
col2.metric("Óbitos no dia", int(obitos_dia))

# --- Mapa interativo dos bairros ---
st.subheader("🗺️ Mapa dos Bairros de Fortaleza")

mapa = folium.Map(location=[-3.75, -38.54], zoom_start=11, tiles='cartodbpositron')

for _, row in gdf_bairros.iterrows():
    nome = row['NM_BAIRRO']
    popup_text = f"""
    <b>Bairro:</b> {nome}<br>
    <b>População:</b> {row.get('POP', 'N/A')}<br>
    <b>Área (km²):</b> {row.get('ARE', 'N/A')}<br>
    <b>Incidência:</b> {row.get('INC', 'N/A')}
    """
    folium.GeoJson(
        row['geometry'],
        name=nome,
        tooltip=nome,
        popup=folium.Popup(popup_text, max_width=300),
        style_function=lambda x: {'color': 'blue', 'fillOpacity': 0.1}
    ).add_to(mapa)

folium_static(mapa, width=1000, height=600)

# --- Gráficos temporais por bairro ---
st.subheader(f"📈 Séries Temporais por Bairro: {bairro_selecionado}")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Casos")
    st.line_chart(df_casos[bairro_selecionado])

with col2:
    st.subheader("Óbitos")
    st.line_chart(df_obitos[bairro_selecionado])
