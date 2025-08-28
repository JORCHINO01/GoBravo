import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def search_city(city_name: str, count: int = 5):
    """Busca ciudades por nombre usando Open-Meteo."""
    params = {"name": city_name, "count": count, "language": "en", "format": "json"}
    try:
        response = requests.get(GEOCODE_URL, params=params)
        response.raise_for_status
        return response.json().get("results", [])
    except requests.RequestException:
        return []

def get_weather(latitude: float, longitude: float):
    """Obtiene el clima actual y pronóstico para una ciudad."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }
    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None
