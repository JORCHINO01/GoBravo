import requests
from datetime import datetime, timedelta
import pandas as pd

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


def get_hourly_forecast(latitude: float, longitude: float):
    now = datetime.now()
    print(now)
    end = now + timedelta(hours=48) # Solicitamos 8 horas para considerar bien las proximas 24 horas (Open-Meteo devuelve desde las 12 am)
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "start": now.strftime("%Y-%m-%dT%H:%M"),
        "end": end.strftime("%Y-%m-%dT%H:%M"),
        "timezone": "auto"
    }
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame({
            "Hora": pd.to_datetime(data["hourly"]["time"]),
            "Temperatura": data["hourly"]["temperature_2m"]
        })

        # Filtrar próximas 24 horas desde el momento actual
        df = df[df["Hora"] >= datetime.now()]
        df = df.head(24)
        return df
    
    except requests.RequestException:
        return None