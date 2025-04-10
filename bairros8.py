import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.features import GeoJsonTooltip, GeoJson

st.title("🗺️ Mapa de Bairros - Salvador")

# Lista de bairros a serem destacados
bairros_destacados = [
    "Mata Escura", "Cajazeiras VIII", "Cajazeiras XI", "Curuzu", "Liberdade", "Ribeira", 
    "Pituba", "Graça", "IAPI", "Pau Miúdo", "Barra", "Lobato", "Plataforma", "Periperi", 
    "Coutos", "São Tomé de Paripe", "Nazaré", "Imbuí", "Stella Maris", "Bomfim", 
    "Rio Vermelho", "Santo Antonio Além do Carmo", "Itapoan", "Mont Serrat", "Ondina"
]

file_path = "prototipo_3/Bairros_salvador.geojson"

@st.cache_data
def load_geojson(file_path):
    return gpd.read_file(file_path)

if file_path:
    gdf = load_geojson(file_path)

    # Criar mapa base
    m = folium.Map(location=[-12.9714, -38.5014], zoom_start=12, tiles="OpenStreetMap")

    # Função de estilo para os polígonos
    def estilo_poligono(feature):
        nome_bairro = feature["properties"].get("NomeBairro", "")
        if nome_bairro in bairros_destacados:
            return {"fillColor": "yellow", "color": "black", "weight": 2, "fillOpacity": 0.7}
        return {"fillColor": "transparent", "color": "#FF0000", "weight": 1, "fillOpacity": 0.3}

    # Destaque ao passar o mouse
    def highlight_function(feature):
        return {"fillColor": "blue", "color": "black", "weight": 3, "fillOpacity": 0.9}

    # Adiciona os bairros no mapa
    geojson = GeoJson(
        gdf,
        style_function=estilo_poligono,
        highlight_function=highlight_function,
        tooltip=GeoJsonTooltip(fields=["NomeBairro"], aliases=["Bairro:"]),
        name="Bairros"
    )
    geojson.add_to(m)

    # Mostra o mapa e captura o clique
    st_data = st_folium(m, width=800, height=600, key="mapa_bairros")

    # Verifica se o usuário clicou em algum bairro
    if st_data and st_data.get("last_active_drawing"):
        properties = st_data["last_active_drawing"]["properties"]
        bairro_clicado = properties.get("NomeBairro")

        if bairro_clicado:
            st.success(f"🏙️ Você clicou no bairro: **{bairro_clicado}**")
    
# HTML do botão
button_html = """
    <style>
        .redirect-button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            text-align: center;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            cursor: pointer;
        }
    </style>
    <a href="https://c6gaxlo56lonsnztdktfrm.streamlit.app/" target="_blank">
        <button class="redirect-button">Ir para o site</button>
    </a>
"""

st.markdown(button_html, unsafe_allow_html=True)
