# GoBravo: 🌤️ Weather App con Streamlit

Aplicación web desarrollada con **Python** y **Streamlit** para consultar el clima de cualquier ciudad del mundo. Permite guardar ciudades favoritas y visualizar el estado del tiempo actual, así como pronósticos por hora y por día.

La aplicación utiliza la API de Open-Meteo
 para consultar datos meteorológicos, debido a que no tiene restricciones de consultas y no es necesario generar una API_KEY

---

## **Funcionalidades**

1. **Búsqueda de ciudades**
   - Barra de búsqueda para consultar cualquier ciudad del mundo.
   - Muestra resultados que se aproximan al texto ingresado.
   - Posibilidad de agregar ciudades a favoritos.

2. **Favoritos**
   - Lista de ciudades favoritas en la barra lateral.
   - Botón para eliminar ciudades de favoritos.
   - Botón para seleccionar una ciudad favorita y mostrar su clima.

3. **Clima de la ciudad seleccionada**
   - Muestra la **temperatura actual**, **mínima** y **máxima** en grados Celsius.
   - Fecha en español (`jueves 28 de agosto 2025`).
   - Gráfico de **temperatura por hora** para las próximas 24 horas:
   - Gráfico de **temperatura diaria** para los próximos 7 días:

4. **Arquitectura**
La arquitectura del proyecto tiene como objetivo designar las funciones principales de consulta y favoritos en módulos para una mejor escalabilidad a futuro.
   - `main.py` → interfaz principal con Streamlit.
   - `src/weather_service.py` → consulta de datos de clima usando Open-Meteo y búsqueda de ciudades.
   - `src/favorites.py` → manejo de ciudades favoritas

---

## **Instalación**

1. **Clonar el repositorio:**

`git clone https://github.com/JORCHINO01/GoBravo.git`



2. **Crear un entorno virtual**

`python -m venv venv`
`source venv/bin/activate`  # Linux/macOS
`venv\Scripts\activate`     # Windows


3. **Instalar dependencias**

`pip install -r requirements.txt`

---

## **Uso**

Para ejecutar la aplicación:

`streamlit run main.py`

Abrirá la aplicación en el navegador predeterminado, con las funcionalidades antes descritas.

---

## **Consideraciones y pasos futuros**

- La arquitectura actual puede mejorarse para separar las funcionalidades de gráficos en módulos por separado.
- La aplicación está pensada para uso personal, pero para integración a otras aplicaciones/servicios es mejor considerar una API que responda con diferente formato
- Se puede trabajar en agregar pronósticos de lluvia, así como un comparativo por mes / año