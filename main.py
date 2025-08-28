import streamlit as st
from src.weather_service import search_city

def main():
    st.set_page_config(
        page_title="Weather App",
        page_icon="🌤️",
        layout="centered"
    )

    st.title("🌤️ Weather App")
    st.write("¡Bienvenido a tu aplicación del clima!")
    st.write("Esta es la versión inicial. Pronto podrás consultar el clima de cualquier ciudad del mundo!")
    query = st.text_input("Escribe el nombre de la ciudad:")
    if query:
        with st.spinner("Buscando ciudades..."):
            results = search_city(query)
        if results:
            st.subheader("Resultados:")
            for city in results:
                st.write(f"**{city['name']}**, {city.get('country', '')} "
                         f"({city.get('latitude')}, {city.get('longitude')})")
        else:
            st.warning("No se encontraron coincidencias.")


if __name__ == "__main__":

    main()
