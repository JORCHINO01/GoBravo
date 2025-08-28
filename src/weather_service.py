import requests

#URL de API en open-meteo; No se requiere API KEY
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Búsqueda de ciudades por nombre. 
# opem-meteo permite una búsqueda aproximada; no es indispensable escribir exactamente la ciudad, o completamente
def search_city(city_name: str, count: int = 5):
    params = {"name": city_name, "count": count, "language": "en", "format": "json"}
    try:
        response = requests.get(GEOCODE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("results", []):
            results.append({
                "name": item.get("name"),
                "state": item.get("admin1"),     
                "country": item.get("country"),
                "latitude": item.get("latitude"),
                "longitude": item.get("longitude")
            })
        return results
    except requests.RequestException:
        return []

#Obtiene el clima actual y pronóstico para una ciudad.
def get_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }
    try:
        response = requests.get(WEATHER_URL, params=params)
        response.raise_for_status()
        data = response.json()
        current_temp = data["current_weather"]["temperature"]
        today_max = data["daily"]["temperature_2m_max"][0]
        today_min = data["daily"]["temperature_2m_min"][0]
        return {
            "current": current_temp,
            "min": today_min,
            "max": today_max
        }
    except requests.RequestException:
        return None