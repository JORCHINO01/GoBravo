import streamlit as st

#Inicializa la lista de favoritos en session_state si no existe. La lista actualmente no se guarda al cerrar la app
def init_favorites():
    if "favorites" not in st.session_state:
        st.session_state["favorites"] = []

 #Agrega una ciudad a favoritos si no está ya incluida.
 #Devuelve True si se agregó, False si ya existía.
def add_favorite(city: dict):
    favorites = st.session_state["favorites"]
    if any(fav["name"] == city["name"] and 
           fav["latitude"] == city["latitude"] and 
           fav["longitude"] == city["longitude"] for fav in favorites):
        return False
    favorites.append(city)
    return True

def get_favorites():
    return st.session_state.get("favorites", [])

def remove_favorite(city: dict):
    if city in st.session_state["favorites"]:
        st.session_state["favorites"].remove(city)
