from dataclasses import dataclass

import httpx

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


@dataclass
class Location:
    name: str
    country: str
    latitude: float
    longitude: float


def geocode(city: str, client: httpx.Client) -> Location | None:
    """Return the best match for a city name, or None if nothing is found."""
    response = client.get(GEOCODE_URL, params = {"name": city, "count": 1})
    response.raise_for_status()
    data = response.json()
    results = data.get("results")
    if not results:
        return None
    first= results[0]
    return Location(
        name= first["name"],
        country= first["country"],
        latitude= first["latitude"],
        longitude= first["longitude"],
    )


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


@dataclass
class Weather:
    temperature_c: float
    wind_kmh: float


def get_weather(location: Location, client: httpx.Client) -> Weather:
    """Return the current weather for a location."""
    response= client.get(WEATHER_URL, params= {"latitude": location.latitude, "longitude": location.longitude, "current": "temperature_2m,wind_speed_10m",})
    response.raise_for_status()
    data= response.json()
    current = data["current"]
    return Weather(
        temperature_c= current["temperature_2m"],
        wind_kmh= current["wind_speed_10m"],
    )

import time


def get_json(client: httpx.Client, url: str, params: dict[str, str | float]) -> dict:
    """GET a URL and return the parsed JSON, retrying on temporary failures."""
    attempts = 3
    for attempt in range(1, attempts + 1):
    
        try:
            response= client.get(url, params= params)
            response.raise_for_status()
            return response.json()
    
        except httpx.TransportError:
            if attempt == attempts:
                raise

        except httpx.HTTPStatusError as e:
            if e.response.status_code < 500 or attempt == attempts:
                raise

        time.sleep(2 ** (attempt - 1))

    raise RuntimeError("unreachable")