import streamlit as st
from src.weather_service import search_city
from src.favorites import init_favorites, add_favorite, get_favorites

def main():
    st.set_page_config(
        page_title="Weather App",
        page_icon="🌤️",
        layout="centered"
    )

    st.title("🌤️ Weather App")
    st.write("Busca una ciudad y agrégala a tus favoritos:")

    # Inicializar favoritos
    init_favorites()

    # Sidebar con favoritos
    st.sidebar.title("⭐ Favoritos")
    favorites = get_favorites()
    if favorites:
        for fav in favorites:
            st.sidebar.write(f"**{fav['name']}**, {fav.get('country', '')}")
    else:
        st.sidebar.info("Aún no tienes favoritos.")

    # Barra de búsqueda
    query = st.text_input("Escribe el nombre de la ciudad:")

    if query:
        with st.spinner("Buscando ciudades..."):
            results = search_city(query)
        if results:
            st.subheader("Resultados:")
            for city in results:
                city_info = {
                    "name": city["name"],
                    "country": city.get("country", ""),
                    "latitude": city.get("latitude"),
                    "longitude": city.get("longitude")
                }
                st.write(f"**{city_info['name']}**, {city_info['country']} "
                         f"({city_info['latitude']}, {city_info['longitude']})")
                key = f"{city_info['name']}_{city_info['latitude']}_{city_info['longitude']}"

                if st.button(f"Agregar a favoritos: {city_info['name']}", key=key):
                    added = add_favorite(city_info)
                    if added:
                        st.success(f"{city_info['name']} agregado a favoritos.")
                    else:
                        st.warning(f"{city_info['name']} ya está en favoritos.")
        else:
            st.warning("No se encontraron coincidencias.")

if __name__ == "__main__":
    main()
