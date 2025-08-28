import streamlit as st
from src.weather_service import search_city, get_weather, get_hourly_forecast
from src.favorites import init_favorites, add_favorite, get_favorites, remove_favorite
from datetime import datetime
import locale
import altair as alt
import pandas as pd


try:
    locale.setlocale(locale.LC_TIME, "es_MX.UTF-8")  # Linux/macOS
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, "Spanish_Mexico.1252")  # Windows
    except locale.Error:
        # fallback: no cambia idioma
        pass

def handle_add(city_info):
    added = add_favorite(city_info)
    st.session_state["last_action"] = "added" if added else "exists"

def main():
    st.set_page_config(
        page_title="Weather App",
        page_icon="🌤️",
        layout="centered"
    )

    st.title("🌤️ Weather App")

    # Inicializar favoritos
    init_favorites()
    if "selected_city" not in st.session_state:
        st.session_state["selected_city"] = None

    # Sidebar con favoritos
    st.sidebar.title("⭐ Favoritos")
    favorites = get_favorites()
    if favorites:
        for fav in favorites:
            st.sidebar.write(f"**{fav['name']}, {fav.get('state','')}, {fav.get('country','')}**")
            col1, col2 = st.sidebar.columns([2,1])
            
            # Botón para mostrar clima (guarda la ciudad seleccionada en session_state)
            key_weather = f"weather_{fav['name']}_{fav['latitude']}_{fav['longitude']}"
            if col1.button("Mostrar clima", key=key_weather):
                st.session_state["selected_city"] = fav

            # Botón para eliminar
            key_remove = f"remove_{fav['name']}_{fav['latitude']}_{fav['longitude']}"
            if col2.button("Eliminar", key=key_remove):
                remove_favorite(fav)
                # Si la ciudad eliminada era la seleccionada, limpiar selección
                if st.session_state.get("selected_city") == fav:
                    st.session_state["selected_city"] = None
                st.rerun()
    else:
        st.sidebar.info("Aún no tienes favoritos.")
    query = None
    # Barra de búsqueda
    if st.session_state.get("selected_city") is None:
        query = st.text_input("Busca una ciudad y agrégala a tus favoritos:")

    if query:
        with st.spinner("Buscando ciudades..."):
            results = search_city(query)
        if results:
            st.subheader("Resultados:")
            for city in results:
                city_info = {
                    "name": city["name"],
                    "state": city.get("state",""),
                    "country": city.get("country", ""),
                    "latitude": city.get("latitude"),
                    "longitude": city.get("longitude")
                }
                st.write(f"**{city_info['name']}**, {city_info.get('state','')}, {city_info['country']} "
                         f"({city_info['latitude']}, {city_info['longitude']})")
                search_key = f"{city_info['name']}_{city_info['latitude']}_{city_info['longitude']}"
 
                if st.button(f"⭐ Agregar a favoritos", key=search_key):
                    added = add_favorite(city_info)
                    if added:
                        st.success(f"{city_info['name']} agregado a favoritos.")
                        del st.session_state[search_key]
                        st.rerun()
                    else:
                        st.warning(f"{city_info['name']} ya está en favoritos.")
        else:
            st.warning("No se encontraron coincidencias.")

    selected_city = st.session_state.get("selected_city")
    if selected_city:
        st.subheader(f"🌡️ Clima de {selected_city['name']}, {selected_city.get('state','')}, {selected_city.get('country','')}")
        weather = get_weather(selected_city["latitude"], selected_city["longitude"])
        if weather:
            today = datetime.now()
            day_str = today.strftime("%A, %d %B %Y")  # Ej: 'Thursday, 28 August 2025'
            st.write(f"**{day_str.capitalize()}**")
            st.write(f"**Temperatura actual:** {weather['current']} °C")
            st.write(f"**Mínima:** {weather['min']} °C")
            st.write(f"**Máxima:** {weather['max']} °C")
            df = get_hourly_forecast(selected_city["latitude"], selected_city["longitude"])
            if df is not None and not df.empty:
                print(df["Hora"])
                df["Hora"] = pd.to_datetime(df["Hora"])
                df["Fecha"] = df["Hora"].dt.strftime("%A %d de %B").str.capitalize()
                df["Hora_str"] = df["Hora"].dt.strftime("%I:%M %p")

                chart = alt.Chart(df).mark_line(point={'size': 60}).encode(
                    x=alt.X("Hora:T", title="Hora"),
                    y=alt.Y("Temperatura:Q", title="Temperatura (°C)"),
                    tooltip=[alt.Tooltip("Fecha:N", title="Fecha"),
                             alt.Tooltip("Hora_str:N", title="Hora"), 
                            alt.Tooltip("Temperatura:Q", title="Temperatura (°C)")]
                ).properties(title="Pronóstico para las próximas 24 horas")
                st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No se pudo obtener el clima.")
        if st.button("🔄 Realizar nueva búsqueda"):
            st.session_state["selected_city"] = None
            st.rerun()
if __name__ == "__main__":
    main()
