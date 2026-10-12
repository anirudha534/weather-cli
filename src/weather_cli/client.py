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
    first = results[0]
    return Location(
        name= first["name"],
        country= first["country"],
        latitude= first["latitude"],
        longitude= first["longitude"],
    )
    