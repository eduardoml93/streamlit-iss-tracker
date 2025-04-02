import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import time
from datetime import datetime
import pytz  # Para conversão de fuso horário

st.title("🛰️🌍 Posição Atual da ISS 🚀🧑‍🚀")

# Criando um espaço para atualizar os dados
map_placeholder = st.empty()

while True:
    try:
        # Obtendo a posição atual da ISS via API
        response = requests.get("http://api.open-notify.org/iss-now.json")
        data = response.json()

        # Extraindo latitude, longitude e timestamp
        latitude = float(data["iss_position"]["latitude"])
        longitude = float(data["iss_position"]["longitude"])
        timestamp = data["timestamp"]

        # Convertendo para horário UTC
        utc_time = datetime.utcfromtimestamp(timestamp)

        # Convertendo para horário de Brasília (UTC-3)
        brasilia_tz = pytz.timezone("America/Sao_Paulo")
        brasilia_time = utc_time.replace(tzinfo=pytz.utc).astimezone(brasilia_tz)
        time_formatted_brasilia = brasilia_time.strftime('%Y-%m-%d %H:%M:%S BRT')

        # Criando a string de informações
        info_popup = f"""
        <b>🚀 Estação Espacial Internacional</b><br>
        🌍 <b>Latitude:</b> {latitude}<br>
        🌎 <b>Longitude:</b> {longitude}<br>
        ⏳ <b>Horário (Brasília):</b> {time_formatted_brasilia}<br>
        🔗 <a href='https://www.google.com/maps/search/?api=1&query={latitude},{longitude}' target='_blank'>Ver no Google Maps</a>
        """

        # Criando o mapa centrado na posição da ISS
        mapa = folium.Map(location=[latitude, longitude], zoom_start=4)
        
        # Adicionando um marcador para a ISS com informações
        folium.Marker(
            [latitude, longitude],
            popup=folium.Popup(info_popup, max_width=300),
            tooltip="Clique para mais informações",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(mapa)

        # Renderizando o mapa no Streamlit
        with map_placeholder.container():
            folium_static(mapa, width=700, height=700)

        # Aguardando antes de atualizar novamente
        time.sleep(10)

    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        break
