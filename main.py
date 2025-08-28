import streamlit as st

def main():
    st.set_page_config(
        page_title="Weather App",
        page_icon="🌤️",
        layout="centered"
    )

    st.title("🌤️ Weather App")
    st.write("¡Bienvenido a tu aplicación del clima!")
    st.write("Esta es la versión inicial. Pronto podrás consultar el clima de cualquier ciudad del mundo!")

if __name__ == "__main__":
    main()
